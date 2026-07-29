---
experiment_id: "EXP-2026-0142"
title: "Effect of impeller speed on kLa in a 2 L stirred bioreactor"
project: "OXY-TRANSFER — oxygen transfer scale-down"
work_package: "WP2 — bench characterisation"
author: "A. Researcher"
orcid: "0000-0000-0000-0000"
witness: "[Name — required for IP-relevant or GxP work]"
date_started: 2026-05-04
date_completed: 2026-05-04
status: "complete"        # planned | in-progress | complete | abandoned
supersedes: null          # e.g. EXP-2026-0118 if this repeats an earlier attempt
related:
  - "EXP-2026-0118"       # first attempt, aborted on probe failure
  - "SOP-BR-004"          # dynamic gassing-out method
tags: [kLa, mass-transfer, bioreactor, scale-down, dynamic-gassing-out]
risk_assessment: "RA-2026-031"
data_location: "s3://lab-data/oxy-transfer/EXP-2026-0142/"
notebook_page: "LB-07 pp. 44-49"
---

<!--
ELECTRONIC LAB NOTEBOOK ENTRY
=============================
One entry per experiment. Written BEFORE the work (hypothesis, plan), DURING
(observations, deviations), and immediately AFTER (results, conclusions).

The rule that makes a notebook worth keeping: record what happened, not what
was supposed to happen. A deviation you wrote down is data. A deviation you
didn't is an unexplained result six months from now.

Entries are append-only. Corrections go in the Amendments section at the
bottom with a date and a reason -- never edit an entry in place after it is
signed. In a regulated environment (GLP/GMP/21 CFR Part 11), this template is
a starting structure only; your validated ELN system's requirements govern.
-->

# EXP-2026-0142 — Effect of impeller speed on kLa in a 2 L stirred bioreactor

---

## 1. Objective and hypothesis

### Question

How does the volumetric oxygen mass transfer coefficient, $k_La$, vary with impeller speed in
the 2 L bench bioreactor, and does the exponent match the Van 't Riet correlation form used to
plan the 200 L scale-up?

### Hypothesis

$k_La$ will scale with volumetric power input as $k_La \propto (P/V)^{\alpha} v_s^{\beta}$ with
$\alpha \approx 0.4$–$0.7$, consistent with published values for coalescing aqueous systems. If
the fitted $\alpha$ falls outside that range, the constant-$P/V$ scale-up basis chosen in the WP1
report needs revisiting before the 200 L run is booked.

### Why this experiment, now

The 200 L campaign is scheduled for June and its aeration strategy assumes an $\alpha$ of 0.5
taken from literature rather than measured on this geometry. Measuring it costs one day; being
wrong costs a 200 L batch.

### Success criteria

Defined **before** the run, so the outcome cannot be reinterpreted afterwards:

- At least 5 speeds spanning 200–800 rpm, in triplicate
- Each $k_La$ fit with $R^2 > 0.98$ on the first-order response
- Triplicate relative standard deviation below 10%
- Fitted $\alpha$ reported with a 95% confidence interval

---

## 2. Materials

| Item | Supplier | Cat. / Lot | Purity / Grade | Notes |
| --- | --- | --- | --- | --- |
| Deionised water | In-house | Loop A | 18.2 MΩ·cm | Used as the coalescing reference medium |
| Sodium sulfite | Merck | 239321 / L-4471 | ≥98% | Only for the sulfite cross-check, Section 5.3 |
| Cobalt(II) chloride | Merck | 232696 / L-1120 | ≥98% | Catalyst for sulfite method, 10⁻⁷ M |
| Nitrogen, oxygen-free | BOC | N5.0 | 99.999% | For deoxygenation |
| Compressed air | House supply | — | Filtered, 0.2 µm | Inlet filter changed 2026-04-30 |
| Antifoam 204 | Sigma | A6426 | — | **Not used** — see deviation D-2 |

### Equipment

| Equipment | ID | Calibration | Settings |
| --- | --- | --- | --- |
| Bioreactor, 2 L jacketed | BR-02 | — | 1.5 L working volume |
| Impeller | — | — | 2 × Rushton, D = 45 mm, C/T = 0.33 |
| DO probe, polarographic | DO-11 | 2026-05-04 08:15, 2-point | τ_probe = 6.2 s (measured, Section 5.2) |
| Mass flow controller | MFC-03 | 2026-02-11 | 0.5–5 L/min air |
| Overhead drive | — | 2025-12-02 | 0–1200 rpm, ±5 rpm |
| Temperature control | TIC-02 | 2026-01-20 | 30.0 ± 0.1 °C |

**Probe response time matters.** If $\tau_{probe}$ is not small compared with $1/k_La$, the
measurement is of the probe, not the reactor. At 800 rpm the expected $1/k_La \approx 12$ s
against a 6.2 s probe — too close to ignore, so the first-order probe correction is applied in
Section 6 and the raw and corrected values are both reported.

---

## 3. Method

Per **SOP-BR-004** (dynamic gassing-out), with the deviations recorded in Section 4.

1. Charge 1.5 L DI water; equilibrate at 30.0 °C, impeller at the test speed.
2. Sparge N₂ at 2 L/min until DO < 5% saturation; confirm stable for 60 s.
3. Stop N₂, switch to air at 1.0 L/min (v_s = 3.6 × 10⁻³ m/s), start logging at 1 Hz.
4. Log until DO > 95% saturation.
5. Repeat in triplicate; randomise speed order to avoid confounding drift with speed.
6. Between speeds, allow 5 min re-equilibration.

Speeds: 200, 300, 400, 500, 600, 800 rpm. Randomised order:
`500, 200, 800, 400, 300, 600` (seed recorded in the analysis script).

### Analysis

$k_La$ from the first-order response of the un-corrected probe signal:

$$ \ln\left(\frac{C^* - C_0}{C^* - C}\right) = k_La \cdot t $$

Probe dynamics corrected by the standard first-order model. Analysis script:
`analysis/fit_kla.py`, commit `a3f9c21`.

---

## 4. Execution log

Written as it happened. Timestamps are local (CEST).

| Time | Entry |
| --- | --- |
| 08:15 | Probe two-point calibration: 0% in N₂-sparged water, 100% in air-saturated water at 30 °C. Slope within spec. |
| 08:40 | Reactor charged, 1.502 L by balance (target 1.5 L). |
| 09:05 | First run at 500 rpm. DO floor reached 3.1% after 4 min N₂ sparge. |
| 09:12 | Run 1 complete, 500 rpm. Response looks clean, no foaming. |
| 09:35 | **D-1**: MFC-03 reading drifted from 1.00 to 1.07 L/min during run 3. Paused, reseated the connector, re-zeroed. Runs 1–3 at 500 rpm flagged; repeated at 11:40. |
| 10:20 | 200 rpm runs. Visible surface vortex, poor bulk mixing at this speed — noted for interpretation, the well-mixed assumption is weakest here. |
| 11:05 | 800 rpm runs. **D-2**: significant foaming at 800 rpm. Antifoam **not** added, because it would change the coalescence behaviour and therefore kLa itself — which is the quantity being measured. Instead reduced working volume to 1.40 L for 800 rpm only, and recorded the change. |
| 11:40 | Repeated 500 rpm triplicate after MFC fix. |
| 13:10 | All conditions complete. Probe re-checked against air saturation: 99.2%, drift acceptable. |
| 13:30 | Data exported, checksums recorded. |

### Deviations from plan

| ID | Deviation | Reason | Impact | Action |
| --- | --- | --- | --- | --- |
| D-1 | Air flow drifted +7% during three runs | Loose MFC connector | Those runs excluded | Repeated after repair; MFC on the weekly check list |
| D-2 | Working volume 1.40 L at 800 rpm instead of 1.50 L | Foaming; antifoam would confound the measurement | v_s and P/V both change slightly; corrected in the analysis and flagged in the fit | Reported separately in Table 6.1 and included in the fit with the corrected P/V |

---

## 5. Observations

### 5.1 Qualitative

- Below 300 rpm the sparged bubbles rose in a distinct plume rather than dispersing — the
  impeller is not flooding-limited but is clearly not fully dispersing at these speeds. The
  well-mixed assumption behind the analysis is weakest here, and the 200 rpm point should
  carry less weight in the fit.
- Bubble size visibly decreased above 500 rpm, consistent with the increase in $k_La$.
- Foaming above ~700 rpm was persistent, not transient.

### 5.2 Probe response time

Measured by step transfer from N₂-saturated to air-saturated water: **τ_probe = 6.2 ± 0.4 s**
(n = 3). Used in the correction in Section 6.

### 5.3 Cross-check (not performed)

The sulfite oxidation cross-check was **not** run. Reagents were prepared but the day ran out.
Noted as a gap: the dynamic method alone can over-read if probe dynamics are mis-corrected, and
an independent method would have settled that. **Follow-up: EXP-2026-0151.**

---

## 6. Results

### 6.1 Measured kLa

| Speed (rpm) | P/V (W/m³) | n | kLa raw (h⁻¹) | kLa corrected (h⁻¹) | RSD (%) | R² |
| --- | --- | --- | --- | --- | --- | --- |
| 200 | 41 | 3 | 18.2 | 18.4 | 6.1 | 0.995 |
| 300 | 139 | 3 | 31.7 | 32.4 | 4.4 | 0.997 |
| 400 | 330 | 3 | 48.9 | 50.6 | 5.2 | 0.998 |
| 500 | 645 | 3 | 68.3 | 71.8 | 3.8 | 0.999 |
| 600 | 1114 | 3 | 89.1 | 95.2 | 7.3 | 0.998 |
| 800 | 2640 | 3 | 121.4 | 134.7 | 9.1 | 0.996 |

Probe correction raises $k_La$ by 1% at 200 rpm and 11% at 800 rpm — which is why it was worth
measuring $\tau_{probe}$ rather than assuming it negligible.

### 6.2 Correlation fit

Fitting $k_La = C (P/V)^{\alpha} v_s^{\beta}$ at constant $v_s$:

**α = 0.48 (95% CI 0.44–0.52), C = 2.9, R² = 0.997**

### 6.3 Figures

![kLa versus volumetric power input, log-log. Error bars are the standard deviation of
triplicates. Slope gives α = 0.48.](figures/kla_vs_PV.png)

![Representative dissolved oxygen response at 500 rpm with the first-order fit and residuals.
Residuals are unstructured, supporting the first-order assumption.](figures/do_response_500rpm.png)

---

## 7. Interpretation

**The hypothesis is supported.** α = 0.48 sits inside the predicted 0.4–0.7 band and is close
to the 0.5 assumed in the WP1 scale-up basis. The constant-P/V basis for the 200 L run does not
need revisiting on this evidence.

**What this does not establish.** The measurement is in water, a coalescing system. Fermentation
broth with cells, salts, and antifoam is non-coalescing and typically shows a *higher* α and a
different absolute $k_La$. Applying α = 0.48 to the actual broth is an extrapolation across a
physical regime change, not an interpolation. Before the 200 L run I would want the same
measurement in spent medium.

**Weakest point.** The absent sulfite cross-check (Section 5.3). The probe correction at 800 rpm
is an 11% adjustment based on a single measured τ, and an independent method would have
confirmed it. The 800 rpm point also carries the volume deviation D-2.

**Unexpected observation.** Foaming set in more sharply than expected between 600 and 700 rpm.
If the 200 L vessel foams proportionally, headspace and antifoam strategy need attention — this
was not in scope but is worth flagging to the project.

---

## 8. Conclusions and next steps

1. $k_La$ scales as $(P/V)^{0.48}$ over 41–2640 W/m³ in water at 1.5 L, 30 °C, v_s = 3.6 mm/s.
2. The scale-up basis in WP1 is consistent with the measured behaviour and stands.
3. Probe dynamics are **not** negligible above 500 rpm; correction is required.

### Actions

| # | Action | Owner | Due |
| --- | --- | --- | --- |
| 1 | Repeat in spent medium to capture non-coalescing behaviour (EXP-2026-0151) | A. Researcher | 2026-05-18 |
| 2 | Sulfite cross-check at 500 rpm as an independent validation | A. Researcher | 2026-05-18 |
| 3 | Flag foaming onset to the 200 L campaign team | A. Researcher | 2026-05-08 |
| 4 | Add MFC-03 to the weekly instrument check list | Lab manager | 2026-05-11 |

---

## 9. Data and code

| Item | Location | Checksum / commit |
| --- | --- | --- |
| Raw DO logs (18 runs, CSV) | `s3://lab-data/oxy-transfer/EXP-2026-0142/raw/` | `sha256:8f3a...c21d` |
| Instrument metadata | `.../raw/metadata.json` | — |
| Analysis script | `github.com/[org]/oxy-transfer/analysis/fit_kla.py` | `a3f9c21` |
| Environment | `.../environment.yaml` | conda, pinned |
| Figures | `.../figures/` | regenerable from raw + script |

**Reproducibility statement.** Figures and fitted parameters regenerate from the raw logs by
running `snakemake --cores 4` in the analysis repository at the commit above.

---

## 10. Signatures

| Role | Name | Date | Signature |
| --- | --- | --- | --- |
| Performed by | A. Researcher | 2026-05-04 | |
| Reviewed by | | | |
| Witnessed by | | | |

---

## 11. Amendments

*Append only. Never edit an entry above after signature — record the correction here with the
date and the reason.*

| Date | Section | Amendment | Reason | By |
| --- | --- | --- | --- | --- |
| 2026-05-06 | 6.1 | 600 rpm RSD corrected from 4.3% to 7.3% | Transcription error; the analysis output was correct, the table was not | A. Researcher |

---

<!--
CHECKLIST BEFORE MARKING AN ENTRY COMPLETE

  [ ] Hypothesis and success criteria were written before the work, not after
  [ ] Every material has a lot number
  [ ] Every instrument has a calibration date
  [ ] Deviations recorded, including the ones that make you look careless
  [ ] Negative and null results recorded -- they are results
  [ ] Raw data archived with a checksum, in a location that outlives your laptop
  [ ] Analysis code committed, and the commit hash is in Section 9
  [ ] Interpretation distinguishes what was shown from what was assumed
  [ ] Next steps have owners and dates
  [ ] Someone else could repeat this from the entry alone

Template maintained at github.com/open-cheme-hub/templates. MIT licence.
-->
