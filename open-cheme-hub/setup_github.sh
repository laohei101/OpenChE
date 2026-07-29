#!/usr/bin/env bash
# =============================================================================
# setup_github.sh — publish the Open ChemE Hub to GitHub
#
# Creates (or reuses) a GitHub organisation, then for each repository directory
# here: creates the repo, initialises git, commits, and pushes.
#
# The script is IDEMPOTENT. Run it twice and the second run reports what
# already exists and pushes only what changed. That matters because the first
# run of anything like this usually fails partway through on a permission you
# didn't know you needed.
#
# -----------------------------------------------------------------------------
# QUICK START
# -----------------------------------------------------------------------------
#   1. Install the GitHub CLI:  https://cli.github.com
#   2. Authenticate:            gh auth login
#      (or export GITHUB_TOKEN with scopes: repo, admin:org, workflow)
#   3. Dry run first:           ./setup_github.sh --dry-run --org my-org
#   4. For real:                ./setup_github.sh --org my-org
#
# -----------------------------------------------------------------------------
# READ THIS BEFORE THE FIRST RUN
# -----------------------------------------------------------------------------
# * ORGANISATIONS CANNOT BE CREATED VIA THE API. GitHub's REST API has no
#   endpoint for creating a free organisation, and `gh` has no command for it.
#   Only Enterprise Cloud accounts can do it programmatically. This script
#   detects whether the org exists and, if not, prints the ~30-second manual
#   step and offers to fall back to your personal account.
#
# * THE ORG NAME `open-cheme-hub` IS ALMOST CERTAINLY TAKEN, or will be by the
#   time you read this. Pass --org with your own name. Every cross-reference in
#   the committed files points at `open-cheme-hub`; --rewrite-urls updates them
#   to your org before committing.
#
# * PLACEHOLDER CONTACT ADDRESSES. `yu.dai@mail.utoronto.ca` and
#   `yu.dai@mail.utoronto.ca` appear in CODE_OF_CONDUCT.md and SECURITY.md
#   and do not exist. Replace them with addresses you actually monitor — a code
#   of conduct with an unreachable reporting address is worse than none.
#
# * PUSHING IS PUBLIC BY DEFAULT. Use --private if you want to review first.
#
# Author  : Open ChemE Hub contributors
# Licence : MIT
# =============================================================================

set -euo pipefail

# --- Defaults ----------------------------------------------------------------
ORG="OpenChemE"
VISIBILITY="public"
DRY_RUN=false
REWRITE_URLS=false
SKIP_ORG_CHECK=false
DEFAULT_BRANCH="main"
COMMIT_MESSAGE="Initial commit: Open ChemE Hub"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Repository directories, in the order they should be created. The `.github`
# repo goes first so the community health files are in place before anyone can
# open an issue on the others.
REPOS=(
  ".github"
  "awesome-chemical-engineering"
  "awesome-chemoinformatics"
  "awesome-bioengineering"
  "awesome-medical-engineering"
  "awesome-general-engineering"
  "templates"
  "workflows"
  "hub-website"
)

# --- Colours, disabled when not a terminal or when NO_COLOR is set -----------
if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[0;33m'
  BLUE=$'\033[0;34m'; BOLD=$'\033[1m'; DIM=$'\033[2m'; RESET=$'\033[0m'
else
  RED=""; GREEN=""; YELLOW=""; BLUE=""; BOLD=""; DIM=""; RESET=""
fi

info()    { printf '%s\n' "${BLUE}==>${RESET} $*"; }
success() { printf '%s\n' "${GREEN} ok ${RESET} $*"; }
warn()    { printf '%s\n' "${YELLOW}warn${RESET} $*" >&2; }
error()   { printf '%s\n' "${RED}fail${RESET} $*" >&2; }
skip()    { printf '%s\n' "${DIM}skip${RESET} $*"; }
step()    { printf '\n%s\n' "${BOLD}$*${RESET}"; }

die() { error "$*"; exit 1; }

# In dry-run mode, print the command instead of running it.
run() {
  if $DRY_RUN; then
    printf '%s\n' "${DIM}     would run: $*${RESET}"
  else
    "$@"
  fi
}

# -----------------------------------------------------------------------------
# Usage
# -----------------------------------------------------------------------------
usage() {
  cat <<'HELPTEXT'
setup_github.sh — publish the Open ChemE Hub to GitHub

USAGE
    ./setup_github.sh [options]

OPTIONS
    --org NAME          GitHub organisation or user to publish under.
                        Default: OpenChemE

    --user              Publish under your personal account instead of an organisation.
                        Equivalent to --org <your-username> --skip-org-check

    --private           Create repositories private. Default: public.

    --dry-run           Print what would happen without creating or pushing anything.
                        Run this first.

    --rewrite-urls      Rewrite github.com/OpenChemE -> github.com/<your-org>
                        throughout the files before committing. Do this unless you
                        are genuinely publishing as open-cheme-hub, or every
                        cross-link in your copy will point at someone else's org.

    --skip-org-check    Assume the org/user exists and skip the check. Useful when
                        the token has repo scope but not read:org.

    --branch NAME       Default branch name. Default: main

    --message TEXT      Commit message. Default: "Initial commit: Open ChemE Hub"

    -h, --help          This message.

AUTHENTICATION
    Either:
        gh auth login                       (interactive, recommended)
    or:
        export GITHUB_TOKEN=ghp_xxxxx       (scopes: repo, admin:org, workflow)

    The `workflow` scope is required: several repositories contain files under
    .github/workflows/, and GitHub rejects a push containing those without it.
    The failure message when it is missing does not mention the scope, which is
    why it is called out here.

EXAMPLES
    ./setup_github.sh --dry-run --org my-cheme-hub --rewrite-urls
    ./setup_github.sh --org my-cheme-hub --rewrite-urls
    ./setup_github.sh --user --private
HELPTEXT
}

# -----------------------------------------------------------------------------
# Argument parsing
# -----------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --org)            ORG="${2:?--org needs a value}"; shift 2 ;;
    --user)           ORG="__USE_CURRENT_USER__"; SKIP_ORG_CHECK=true; shift ;;
    --private)        VISIBILITY="private"; shift ;;
    --dry-run|-n)     DRY_RUN=true; shift ;;
    --rewrite-urls)   REWRITE_URLS=true; shift ;;
    --skip-org-check) SKIP_ORG_CHECK=true; shift ;;
    --branch)         DEFAULT_BRANCH="${2:?--branch needs a value}"; shift 2 ;;
    --message|-m)     COMMIT_MESSAGE="${2:?--message needs a value}"; shift 2 ;;
    -h|--help)        usage; exit 0 ;;
    *)                error "Unknown option: $1"; echo; usage; exit 2 ;;
  esac
done

# =============================================================================
# 1. Preflight
# =============================================================================
step "1. Checking prerequisites"

command -v git >/dev/null 2>&1 || die "git is not installed."
success "git $(git --version | awk '{print $3}')"

if ! command -v gh >/dev/null 2>&1; then
  error "The GitHub CLI (gh) is not installed."
  cat >&2 <<'EOF'

  Install it:
    macOS         brew install gh
    Debian/Ubuntu sudo apt install gh
    Fedora        sudo dnf install gh
    Windows       winget install --id GitHub.cli
    Other         https://cli.github.com

EOF
  exit 1
fi
success "gh $(gh --version | head -1 | awk '{print $3}')"

# --- Authentication ----------------------------------------------------------
# gh prefers GITHUB_TOKEN when it is set, which is what makes this work
# unattended in CI as well as interactively.
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  success "Using GITHUB_TOKEN from the environment"
elif gh auth status >/dev/null 2>&1; then
  success "Using an existing gh login"
else
  error "Not authenticated to GitHub."
  cat >&2 <<'EOF'

  Do one of:

    gh auth login                       # interactive, recommended

    export GITHUB_TOKEN=ghp_xxxxxxxx    # a personal access token with scopes:
                                        #   repo         create and push repositories
                                        #   admin:org    create repos inside an org
                                        #   workflow     push files under .github/workflows/

  Create a token at: https://github.com/settings/tokens

EOF
  exit 1
fi

CURRENT_USER="$(gh api user --jq .login 2>/dev/null || true)"
[[ -n "$CURRENT_USER" ]] || die "Could not read the authenticated user. Is the token valid?"
success "Authenticated as ${BOLD}${CURRENT_USER}${RESET}"

if [[ "$ORG" == "__USE_CURRENT_USER__" ]]; then
  ORG="$CURRENT_USER"
  info "Publishing under your personal account: $ORG"
fi

# --- Warn about the placeholder org name -------------------------------------
if [[ "$ORG" == "OpenChemE" ]]; then
  info "Using the default org name 'OpenChemE'. Pass --org if you own a different one."
fi

# --- Warn about the token scope people forget --------------------------------
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  TOKEN_SCOPES="$(gh api -i user 2>/dev/null | grep -i '^x-oauth-scopes:' | cut -d: -f2- | tr -d ' \r' || true)"
  if [[ -n "$TOKEN_SCOPES" && "$TOKEN_SCOPES" != *"workflow"* ]]; then
    warn "Your token does not appear to have the 'workflow' scope."
    warn "Pushes containing .github/workflows/ files will be rejected, and the"
    warn "error GitHub returns does not say why. Scopes seen: $TOKEN_SCOPES"
  fi
fi

# =============================================================================
# 2. Organisation
# =============================================================================
step "2. Checking the destination"

ORG_IS_USER=false

if $SKIP_ORG_CHECK; then
  skip "Org check skipped (--skip-org-check)"
  [[ "$ORG" == "$CURRENT_USER" ]] && ORG_IS_USER=true
elif [[ "$ORG" == "$CURRENT_USER" ]]; then
  success "Publishing under your personal account: $ORG"
  ORG_IS_USER=true
elif gh api "orgs/${ORG}" >/dev/null 2>&1; then
  success "Organisation ${BOLD}${ORG}${RESET} exists and is reachable"
else
  # This is the manual step. It is manual because GitHub's API genuinely has no
  # endpoint for creating a free organisation -- not because the script is
  # cutting a corner.
  error "Organisation '${ORG}' does not exist, or your token cannot see it."
  cat >&2 <<EOF

  GitHub's REST API has no endpoint for creating a free organisation, and the
  gh CLI has no command for it. Only Enterprise Cloud accounts can create orgs
  programmatically. This is a GitHub limitation, not a gap in this script.

  Create it by hand -- it takes about thirty seconds:

      1. Open  https://github.com/organizations/plan
      2. Choose the Free plan
      3. Name it: ${ORG}
      4. Skip the invite step
      5. Re-run this script

  Or publish under your own account instead:

      ./setup_github.sh --user${DRY_RUN:+ --dry-run}

  If the org DOES exist and your token simply cannot see it (a fine-grained
  token without read:org, for example), re-run with --skip-org-check.

EOF
  exit 1
fi

# =============================================================================
# 3. Plan
# =============================================================================
step "3. Plan"

cat <<EOF
  Destination     ${BOLD}${ORG}${RESET}$( $ORG_IS_USER && echo " (personal account)" || echo " (organisation)")
  Visibility      ${VISIBILITY}
  Default branch  ${DEFAULT_BRANCH}
  Rewrite URLs    $( $REWRITE_URLS && echo "yes -> github.com/${ORG}" || echo "no (links point at OpenChemE)" )
  Mode            $( $DRY_RUN && echo "${YELLOW}DRY RUN — nothing will be created${RESET}" || echo "${GREEN}LIVE${RESET}" )

  Repositories to create or update:
EOF

MISSING_DIRS=()
for repo in "${REPOS[@]}"; do
  if [[ -d "${SCRIPT_DIR}/${repo}" ]]; then
    file_count=$(find "${SCRIPT_DIR}/${repo}" -type f -not -path '*/.git/*' | wc -l | tr -d ' ')
    printf '    %-32s %s file(s)\n' "$repo" "$file_count"
  else
    printf '    %-32s %s\n' "$repo" "${RED}MISSING${RESET}"
    MISSING_DIRS+=("$repo")
  fi
done
echo

if (( ${#MISSING_DIRS[@]} > 0 )); then
  die "Missing directories: ${MISSING_DIRS[*]}. Run this script from inside open-cheme-hub/."
fi

if ! $REWRITE_URLS && [[ "$ORG" != "OpenChemE" ]]; then
  warn "You are publishing to '${ORG}' but URLs still point at 'OpenChemE'."
  warn "Every cross-reference in your copy will link to someone else's organisation."
  warn "Re-run with --rewrite-urls unless that is what you want."
  echo
fi

if ! $DRY_RUN; then
  read -r -p "  Proceed? [y/N] " reply
  [[ "$reply" =~ ^[Yy]$ ]] || { info "Aborted. Nothing was changed."; exit 0; }
fi

# =============================================================================
# 4. Rewrite URLs
# =============================================================================
if $REWRITE_URLS && [[ "$ORG" != "OpenChemE" ]]; then
  step "4. Rewriting URLs to ${ORG}"

  if $DRY_RUN; then
    hits=$(grep -rl 'OpenChemE' "${SCRIPT_DIR}" \
             --include='*.md' --include='*.yml' --include='*.yaml' \
             --include='*.html' --include='*.json' --include='*.py' \
             --include='*.js' --include='*.sh' --include='*.dwxml' \
             2>/dev/null | wc -l | tr -d ' ')
    info "Would rewrite occurrences in ${hits} file(s)"
  else
    # -print0/-0 so paths with spaces survive. LC_ALL=C keeps sed predictable
    # across locales.
    find "${SCRIPT_DIR}" -type f \
      \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' -o -name '*.html' \
         -o -name '*.json' -o -name '*.py' -o -name '*.js' -o -name '*.sh' \
         -o -name '*.dwxml' -o -name 'Dockerfile' -o -name 'Snakefile' \) \
      -not -path '*/.git/*' -print0 \
    | LC_ALL=C xargs -0 sed -i.bak \
        -e "s|github\.com/OpenChemE|github.com/${ORG}|g" \
        -e "s|orgs/OpenChemE|orgs/${ORG}|g" \
        -e "s|ghcr\.io/opencheme|ghcr.io/$(echo "${ORG}" | tr "[:upper:]" "[:lower:]")|g" \
        -e "s|opencheme\.github\.io|$(echo "${ORG}" | tr "[:upper:]" "[:lower:]").github.io|g"

    find "${SCRIPT_DIR}" -name '*.bak' -not -path '*/.git/*' -delete
    success "URLs rewritten to ${ORG}"
    warn "Contact addresses (conduct@, security@) were NOT rewritten — set those by hand."
  fi
fi

# =============================================================================
# 5. Create and push each repository
# =============================================================================
step "5. Creating and pushing repositories"

CREATED=(); UPDATED=(); FAILED=()

# One-line description per repo, used when creating it.
describe_repo() {
  case "$1" in
    .github)                        echo "Community health files and organisation profile for Open ChemE Hub" ;;
    awesome-chemical-engineering)   echo "Curated open-source tools, data, and courses for chemical process engineering" ;;
    awesome-chemoinformatics)       echo "Curated open tools for cheminformatics and computational chemistry" ;;
    awesome-bioengineering)         echo "Curated open resources for bioprocess engineering and synthetic biology" ;;
    awesome-medical-engineering)    echo "Curated open resources for medical devices, biomechanics, and health informatics" ;;
    awesome-general-engineering)    echo "Curated cross-cutting engineering tools: CAD/CAE, control, embedded, documentation" ;;
    templates)                      echo "Ready-to-use templates for chemical engineering calculations, reports, and lab records" ;;
    workflows)                      echo "Reproducible Snakemake pipelines, GitHub Actions, and a pinned Docker environment" ;;
    hub-website)                    echo "Static site and search for the Open ChemE Hub" ;;
    *)                              echo "Part of the Open ChemE Hub" ;;
  esac
}

repo_topics() {
  case "$1" in
    .github)                        echo "chemical-engineering,open-science,community" ;;
    awesome-chemical-engineering)   echo "awesome,awesome-list,chemical-engineering,process-simulation,thermodynamics" ;;
    awesome-chemoinformatics)       echo "awesome,awesome-list,cheminformatics,computational-chemistry,rdkit" ;;
    awesome-bioengineering)         echo "awesome,awesome-list,bioengineering,synthetic-biology,metabolic-modeling" ;;
    awesome-medical-engineering)    echo "awesome,awesome-list,biomedical-engineering,medical-imaging,medical-devices" ;;
    awesome-general-engineering)    echo "awesome,awesome-list,engineering,cad,control-systems" ;;
    templates)                      echo "chemical-engineering,templates,jupyter-notebook,education" ;;
    workflows)                      echo "snakemake,reproducibility,docker,github-actions,cheminformatics" ;;
    hub-website)                    echo "jekyll,github-pages,chemical-engineering" ;;
    *)                              echo "chemical-engineering" ;;
  esac
}

for repo in "${REPOS[@]}"; do
  repo_path="${SCRIPT_DIR}/${repo}"
  full_name="${ORG}/${repo}"

  printf '\n  %s%s%s\n' "$BOLD" "$full_name" "$RESET"

  # --- Does the repo already exist? -----------------------------------------
  repo_exists=false
  if gh repo view "$full_name" >/dev/null 2>&1; then
    repo_exists=true
    skip "  repository already exists — will push to it"
  fi

  # --- Create it if not ------------------------------------------------------
  if ! $repo_exists; then
    if $DRY_RUN; then
      printf '%s\n' "${DIM}     would create ${full_name} (${VISIBILITY})${RESET}"
    else
      if gh repo create "$full_name" \
            --"$VISIBILITY" \
            --description "$(describe_repo "$repo")" \
            >/dev/null 2>&1; then
        success "  created (${VISIBILITY})"
        CREATED+=("$repo")
      else
        error "  could not create ${full_name}"
        error "  Common causes: name already taken by someone else; token lacks"
        error "  'repo' or 'admin:org' scope; org policy forbids member repo creation."
        FAILED+=("$repo")
        continue
      fi
    fi
  fi

  # --- Initialise git locally, if needed --------------------------------------
  if [[ ! -d "${repo_path}/.git" ]]; then
    run git -C "$repo_path" init -q -b "$DEFAULT_BRANCH"
    $DRY_RUN || success "  git initialised on ${DEFAULT_BRANCH}"
  else
    skip "  already a git repository"
    # Make sure we are on the intended branch without clobbering existing work.
    if ! $DRY_RUN; then
      current="$(git -C "$repo_path" branch --show-current 2>/dev/null || echo "")"
      if [[ -n "$current" && "$current" != "$DEFAULT_BRANCH" ]]; then
        warn "  on branch '${current}', not '${DEFAULT_BRANCH}' — leaving it alone"
      fi
    fi
  fi

  # --- Stage and commit -------------------------------------------------------
  if $DRY_RUN; then
    file_count=$(find "$repo_path" -type f -not -path '*/.git/*' | wc -l | tr -d ' ')
    printf '%s\n' "${DIM}     would commit ${file_count} file(s)${RESET}"
  else
    git -C "$repo_path" add -A
    if git -C "$repo_path" diff --cached --quiet 2>/dev/null; then
      skip "  nothing to commit — already up to date"
    else
      # --no-verify: a contributor's global pre-commit hooks shouldn't be able
      # to fail a bulk publish of files they have not seen.
      git -C "$repo_path" -c user.name="${GIT_AUTHOR_NAME:-$CURRENT_USER}" \
          -c user.email="${GIT_AUTHOR_EMAIL:-${CURRENT_USER}@users.noreply.github.com}" \
          commit -q --no-verify -m "$COMMIT_MESSAGE"
      success "  committed"
    fi
  fi

  # --- Remote -----------------------------------------------------------------
  remote_url="https://github.com/${full_name}.git"
  if ! $DRY_RUN; then
    if git -C "$repo_path" remote get-url origin >/dev/null 2>&1; then
      git -C "$repo_path" remote set-url origin "$remote_url"
    else
      git -C "$repo_path" remote add origin "$remote_url"
    fi
  fi

  # --- Push, with backoff for transient network failures ---------------------
  if $DRY_RUN; then
    printf '%s\n' "${DIM}     would push to ${remote_url}${RESET}"
    continue
  fi

  branch="$(git -C "$repo_path" branch --show-current)"
  pushed=false
  delay=2
  for attempt in 1 2 3 4 5; do
    if git -C "$repo_path" push -u origin "$branch" >/dev/null 2>&1; then
      success "  pushed to ${branch}"
      pushed=true
      $repo_exists && UPDATED+=("$repo")
      break
    fi
    if (( attempt < 5 )); then
      warn "  push failed (attempt ${attempt}/5), retrying in ${delay}s"
      sleep "$delay"
      delay=$(( delay * 2 ))
    fi
  done

  if ! $pushed; then
    error "  push failed after 5 attempts"
    error "  If the repository contains .github/workflows/, the most likely cause is a"
    error "  token without the 'workflow' scope. GitHub's error does not say so."
    FAILED+=("$repo")
    continue
  fi

  # --- Topics and settings (best effort — never fail the run on these) -------
  topics="$(repo_topics "$repo")"
  gh api -X PUT "repos/${full_name}/topics" \
     -H "Accept: application/vnd.github.mercy-preview+json" \
     -f "names[]=$(echo "$topics" | cut -d, -f1)" >/dev/null 2>&1 || true
  # Set the remaining topics in one call.
  topic_args=()
  IFS=',' read -ra topic_list <<< "$topics"
  for t in "${topic_list[@]}"; do topic_args+=(-f "names[]=${t}"); done
  gh api -X PUT "repos/${full_name}/topics" \
     -H "Accept: application/vnd.github.mercy-preview+json" \
     "${topic_args[@]}" >/dev/null 2>&1 \
     && success "  topics set" || warn "  could not set topics (harmless)"

  # Discussions are where the contributing guide sends people, so turn them on
  # for the .github repo. Org-level discussions still have to be enabled by hand
  # in the org settings.
  if [[ "$repo" == ".github" ]]; then
    gh api -X PATCH "repos/${full_name}" -F has_discussions=true >/dev/null 2>&1 \
      && success "  discussions enabled" || true
  fi

  # GitHub Pages for the website, served from /docs on the default branch.
  if [[ "$repo" == "hub-website" ]]; then
    if gh api -X POST "repos/${full_name}/pages" \
         -f "source[branch]=${branch}" -f "source[path]=/docs" >/dev/null 2>&1; then
      success "  GitHub Pages enabled from /docs"
    else
      warn "  could not enable Pages automatically"
      warn "  Do it by hand: Settings -> Pages -> branch ${branch}, folder /docs"
    fi
  fi
done

# =============================================================================
# 6. Summary
# =============================================================================
step "6. Summary"

if $DRY_RUN; then
  cat <<EOF
  ${YELLOW}Dry run — nothing was created, committed, or pushed.${RESET}

  When the plan above looks right, run it again without --dry-run.
EOF
  exit 0
fi

(( ${#CREATED[@]} > 0 )) && { printf '  %sCreated%s (%d):\n' "$GREEN" "$RESET" "${#CREATED[@]}"; printf '    %s\n' "${CREATED[@]}"; }
(( ${#UPDATED[@]} > 0 )) && { printf '  %sUpdated%s (%d):\n' "$BLUE" "$RESET" "${#UPDATED[@]}"; printf '    %s\n' "${UPDATED[@]}"; }
(( ${#FAILED[@]}  > 0 )) && { printf '  %sFailed%s (%d):\n'  "$RED" "$RESET" "${#FAILED[@]}";  printf '    %s\n' "${FAILED[@]}"; }

cat <<EOF

  Organisation:  https://github.com/${ORG}
  Website:       https://${ORG}.github.io/hub-website/  (or your Pages URL)

  ${BOLD}Manual steps the API cannot do for you${RESET}

    1. ${BOLD}Enable organisation Discussions.${RESET}
       Org Settings -> Discussions -> enable, sourced from the .github repository.
       Create the categories the issue templates link to: Q&A, Ideas, Show and Tell.
       Those links 404 until you do.

    2. ${BOLD}Confirm the contact address.${RESET}
       yu.dai@mail.utoronto.ca and yu.dai@mail.utoronto.ca appear in
       CODE_OF_CONDUCT.md and SECURITY.md and do not exist. A code of conduct
       with an unreachable reporting address is worse than not having one.

    3. ${BOLD}Check the Pages deployment.${RESET}
       hub-website -> Settings -> Pages. If the site 404s on its stylesheet,
       \`baseurl\` in docs/_config.yml does not match where it is served from.

    4. ${BOLD}Set branch protection${RESET} on anything you expect contributions to:
       require a pull request, require the link-check status, disallow force push.

    5. ${BOLD}Review the content as your own.${RESET} The lists are a starting point,
       not a finished reference. Verify the entries in your own field before you
       point colleagues at them — a curated list is only worth what its curator
       has actually checked.

EOF

if (( ${#FAILED[@]} > 0 )); then
  error "Some repositories failed. Fix the cause and re-run — the script is idempotent."
  exit 1
fi

success "Done."
