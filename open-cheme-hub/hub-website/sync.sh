#!/usr/bin/env bash
# Copy the canonical site (repo root /public, what Vercel serves) into docs/,
# which is what GitHub Pages serves if this directory is published as its own
# repository. Root is canonical; this directory is a mirror.
#
#     ./sync.sh
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/public"
DST="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/docs"

[[ -d "$SRC" ]] || { echo "No site at $SRC" >&2; exit 1; }

rm -rf "${DST:?}"/assets "${DST}"/*.html
cp -r "$SRC"/. "$DST"/
touch "$DST/.nojekyll"
echo "Synced $SRC -> $DST"
