---
title: "Determination of the Overall Heat Transfer Coefficient in a Double-Pipe Exchanger"
subtitle: "CHE 3XX Unit Operations Laboratory — Experiment 4"
author:
  - name: "A. Student"
    id: "12345678"
    role: "Lead author, data analysis"
  - name: "B. Partner"
    id: "87654321"
    role: "Experimental operation, calibration"
group: "Bench 3, Group C"
course: "CHE 3XX Unit Operations Laboratory"
instructor: "Dr. C. Instructor"
demonstrator: "D. Demonstrator"
date_performed: 2026-03-12
date_submitted: 2026-03-19
apparatus_id: "HX-02 (double-pipe, counter-current)"
word_count: 2480
bibliography: references.bib
csl: ieee.csl
---

<!--
HOW TO USE THIS TEMPLATE
========================
Replace every bracketed placeholder and delete these comment blocks before
submitting. Each section carries a target length and a note on what markers
actually look for -- delete those notes too.

Render to PDF:
    pandoc lab_report_template.md -o report.pdf --citeproc --number-sections
    quarto render lab_report_template.md --to pdf     # if you prefer Quarto

The YAML front matter above feeds the title page. Check your course's required
fields -- some want a student number on every page, some forbid names entirely
for anonymous marking.

CHECK YOUR COURSE HANDBOOK. It overrides this template on structure, length,
referencing style, and whether raw data goes in an appendix or a spreadsheet.
-->

# Abstract

<!-- 150-250 words. Write this LAST. -->

One sentence of context. One sentence stating the objective. Two or three sentences on
method, including the range of conditions covered. Then the results **with numbers and
uncertainties** — this is the part markers check, and a vague abstract loses marks no matter
how good the report is. Finish with one sentence of conclusion.

> *Example of the level of specificity expected:* "The overall heat transfer coefficient was
> measured for a counter-current double-pipe exchanger over Reynolds numbers from 4 200 to
> 21 000. U increased from 480 ± 40 to 1 310 ± 90 W m⁻² K⁻¹ across this range. Values agreed
> with the Dittus–Boelter prediction within 12% above Re = 10 000 but exceeded it by up to
> 31% in the transition region, consistent with the correlation's stated validity limit."

**Keywords:** heat transfer, double-pipe exchanger, Dittus–Boelter, forced convection

---

# 1. Introduction

<!-- ~400-600 words. -->

## 1.1 Background and motivation

Why this measurement matters industrially. Keep it to a paragraph — the marker knows what a
heat exchanger is, and padding here costs you space you'll want in the discussion.

## 1.2 Theory

State the governing relations, define every symbol, and number the equations so you can refer
back to them.

The heat duty from the energy balance on either fluid:

$$ \dot{Q} = \dot{m} c_p \Delta T \tag{1} $$

The rate equation defining the overall coefficient:

$$ \dot{Q} = U A \, \Delta T_{\text{lm}} \tag{2} $$

with the log-mean temperature difference for counter-current flow:

$$ \Delta T_{\text{lm}} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)} \tag{3} $$

The resistances in series, which is what lets you separate the film coefficients from the wall:

$$ \frac{1}{U A} = \frac{1}{h_i A_i} + \frac{\ln(r_o/r_i)}{2 \pi k L} + \frac{1}{h_o A_o} + R_{f} \tag{4} $$

The correlation being tested [@dittus1930]:

$$ Nu = 0.023 \, Re^{0.8} Pr^{n}, \qquad n = 0.4 \text{ (heating)}, \; 0.3 \text{ (cooling)} \tag{5} $$

**State the validity range of every correlation you use.** Equation (5) holds for
Re > 10 000, 0.6 < Pr < 160, and L/D > 10. If your data extends outside that, say so here and
return to it in the discussion — knowing where a correlation stops applying is most of what
this experiment teaches.

## 1.3 Objectives

Numbered, specific, and testable:

1. Measure U over the range Re = 4 000 to 20 000 at three flow ratios.
2. Compare measured Nusselt numbers against Equation (5) and quantify the deviation.
3. Estimate the fouling resistance by comparison with the clean-condition prediction.

---

# 2. Materials and Methods

<!-- ~400-600 words. Enough for a competent peer to repeat it. Past tense, passive or
     active as your course prefers -- be consistent. -->

## 2.1 Apparatus

Describe the rig with a labelled schematic. Include: geometry (lengths, diameters, wall
material and thickness), instrument locations, and how flow was controlled.

```
        Hot water in                          Hot water out
         (TI-101)                              (TI-102)
             |                                     |
             v                                     |
    =========================================================
    ||  <<<<<<<<<<< inner tube, hot fluid <<<<<<<<<<<<<<   ||
    ||  >>>>>>>>>>> annulus, cold fluid  >>>>>>>>>>>>>>>   ||
    =========================================================
             ^                                     |
             |                                     v
        Cold water in                        Cold water out
         (TI-103)                              (TI-104)
        FI-201                                 FI-202
```

| Component | Specification |
| --- | --- |
| Inner tube | Copper, 15.0 mm OD × 13.4 mm ID, k = 401 W m⁻¹ K⁻¹ |
| Outer tube | Copper, 28.0 mm OD × 25.6 mm ID |
| Effective length | 1.500 m |
| Configuration | Counter-current |

## 2.2 Instrumentation and uncertainty

**Fill this table honestly — it drives your entire error analysis, and a report with no
uncertainty is a report with no result.**

| Instrument | Tag | Range | Resolution | Stated accuracy | Calibrated |
| --- | --- | --- | --- | --- | --- |
| Type-K thermocouple | TI-101…104 | 0–150 °C | 0.1 °C | ±1.1 °C or 0.4% | 2026-01-15 |
| Rotameter, hot side | FI-201 | 0.5–5.0 L min⁻¹ | 0.1 L min⁻¹ | ±2% FSD | 2025-11-03 |
| Rotameter, cold side | FI-202 | 0.5–8.0 L min⁻¹ | 0.2 L min⁻¹ | ±2% FSD | 2025-11-03 |

## 2.3 Procedure

Numbered steps, past tense. Include the things that determine whether the data is any good:

1. The rig was purged of air and circulation established at maximum flow for 10 min.
2. Hot-side inlet temperature was set to 60 °C and allowed to stabilise.
3. Flows were set to the first condition in Table 2.
4. **Steady state was confirmed** as all four temperatures varying by less than 0.2 °C over
   5 min before recording. *Say how you judged steady state — "when it looked steady" is not
   a method, and a report that omits this invites the question of whether it ever was.*
5. Five readings were recorded at 1 min intervals and averaged.
6. Steps 3–5 were repeated for each condition in randomised order to avoid confounding any
   drift with the flow sequence.

## 2.4 Data reduction

State exactly how raw readings became results, in the order the calculation runs. Reference
your code if you used any:

1. Volumetric flows converted to mass flows using density at the mean bulk temperature
   (correlation from [@perry2018], or CoolProp — say which).
2. Duty computed from Equation (1) for **both** streams; the two agreed within X%, and the
   mean was used. *Report this agreement — a large mismatch means an unaccounted heat loss,
   and hiding it is worse than having it.*
3. ΔT_lm from Equation (3), U from Equation (2).
4. Uncertainty propagated by the root-sum-square method (Section 3.3).

---

# 3. Results

<!-- ~500-700 words. Results ONLY. Interpretation goes in Section 4. This separation is
     marked, and mixing them is the most common structural error. -->

## 3.1 Raw and reduced data

Summary table in the body; full raw data in Appendix A.

| Run | ṁ_hot (kg s⁻¹) | ṁ_cold (kg s⁻¹) | T_h,in (°C) | T_h,out (°C) | T_c,in (°C) | T_c,out (°C) | Q̇_hot (W) | Q̇_cold (W) | Δ (%) | ΔT_lm (K) | U (W m⁻² K⁻¹) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0170 | 0.0250 | 59.8 | 51.2 | 18.4 | 24.3 | 612 | 617 | 0.8 | 33.7 | 481 ± 38 |
| 2 | 0.0250 | 0.0250 | 60.1 | 53.6 | 18.5 | 25.4 | 680 | 722 | 6.2 | 34.5 | 553 ± 41 |
| 3 | … | … | … | … | … | … | … | … | … | … | … |

**Significant figures.** Report to the precision your uncertainty justifies and no further.
`U = 481.2947 W/m²K` alongside `± 38` announces that you have not thought about it.

## 3.2 Figures

Every figure needs: axis labels with units, a caption below that stands alone, error bars,
and a legend if there's more than one series. Refer to each in the text.

![Overall heat transfer coefficient as a function of hot-side Reynolds number. Error bars show
combined standard uncertainty (k = 1). The dashed line is the Dittus–Boelter prediction,
Equation (5); the shaded region marks Re < 10 000, below the correlation's stated validity
limit.](figures/U_vs_Re.png){#fig:u-vs-re width=85%}

## 3.3 Uncertainty analysis

**Do not skip this section.** Show the propagation for one representative run in full, then
tabulate the rest.

For $U = \dot{Q}/(A \, \Delta T_{\text{lm}})$ with independent inputs:

$$ \frac{u_U}{U} = \sqrt{ \left(\frac{u_{\dot{Q}}}{\dot{Q}}\right)^2 + \left(\frac{u_A}{A}\right)^2 + \left(\frac{u_{\Delta T_{\text{lm}}}}{\Delta T_{\text{lm}}}\right)^2 } \tag{6} $$

| Source | Value | Contribution to u_U/U |
| --- | --- | --- |
| Mass flow (±2% FSD) | ±0.0010 kg s⁻¹ | 4.1% |
| Temperature difference (±1.1 °C each) | ±1.56 K | 6.3% |
| Area (±0.5 mm on diameter) | ±0.0002 m² | 0.4% |
| **Combined (RSS)** | | **7.6%** |

**Identify the dominant term and say so.** Here the temperature measurement dominates,
because ΔT_lm is a small difference of two larger numbers — which is exactly why this
experiment is sensitive to thermocouple calibration and why improving the flow meter would
have been a waste of effort.

---

# 4. Discussion

<!-- ~600-900 words. This is where the marks are. A report with perfect data and a thin
     discussion scores below one with imperfect data that is properly interrogated. -->

## 4.1 Comparison with theory

Quantify the agreement, don't assert it. "The results agree well with theory" is worth
nothing; "measured Nu exceeded the Dittus–Boelter prediction by 8–12% above Re = 10 000,
within the correlation's own quoted ±15% scatter" is worth the marks.

## 4.2 Sources of deviation

For each proposed explanation, give the **direction and magnitude** it would push the result,
and say whether that matches what you observed. An explanation that would move the data the
wrong way is evidence against itself — noticing that is what distinguishes a good discussion.

- **Entrance effects.** L/D = 112 here, so developing-flow enhancement should be negligible.
- **Fouling.** Would decrease U. The measured values sit *above* prediction, so fouling does
  not explain the deviation and is likely small on this rig.
- **Heat loss to ambient.** Would make Q̇_hot exceed Q̇_cold. Runs 2 and 5 show this at 6% and
  9%; the lagging was visibly damaged near the hot inlet.
- **Property evaluation temperature.** Using bulk mean rather than film temperature changes
  the predicted Nu by about 4% at these conditions — worth stating, not enough to explain 12%.

## 4.3 Limitations

What this experiment cannot tell you, stated plainly. Single apparatus, one fluid pair, no
independent measurement of the individual film coefficients, and no repeat on a different rig.

## 4.4 Recommendations

Specific and actionable. "Improve accuracy" is not a recommendation; "replace the type-K
thermocouples with calibrated RTDs, which would reduce the dominant uncertainty contribution
from 6.3% to about 1%" is.

---

# 5. Conclusions

<!-- Numbered, one per objective, each with a number in it. No new information. -->

1. U rose from 481 ± 38 to 1 310 ± 90 W m⁻² K⁻¹ over Re = 4 200 to 21 000, following the
   expected Re^0.8 dependence with a fitted exponent of 0.78 ± 0.04.
2. Agreement with Dittus–Boelter was within 12% above Re = 10 000 and degraded to 31% in the
   transition region, consistent with the correlation's stated validity limit.
3. The energy balance closed within 6% on average, with the residual attributable to
   identified heat loss through damaged insulation near the hot inlet.

---

# Nomenclature

| Symbol | Description | Units |
| --- | --- | --- |
| $A$ | Heat transfer area | m² |
| $c_p$ | Specific heat capacity | J kg⁻¹ K⁻¹ |
| $h$ | Convective heat transfer coefficient | W m⁻² K⁻¹ |
| $k$ | Thermal conductivity | W m⁻¹ K⁻¹ |
| $\dot{m}$ | Mass flow rate | kg s⁻¹ |
| $Nu$ | Nusselt number, $hD/k$ | – |
| $Pr$ | Prandtl number, $c_p\mu/k$ | – |
| $\dot{Q}$ | Heat duty | W |
| $Re$ | Reynolds number, $\rho v D/\mu$ | – |
| $U$ | Overall heat transfer coefficient | W m⁻² K⁻¹ |
| $\Delta T_{\text{lm}}$ | Log-mean temperature difference | K |
| $\mu$ | Dynamic viscosity | Pa s |
| $\rho$ | Density | kg m⁻³ |

*Subscripts:* i inner, o outer, h hot, c cold, f fouling, lm log-mean.

---

# References

<!-- Use your course's required style. With pandoc --citeproc, cite as [@key] and keep the
     entries in references.bib. Cite the ORIGINAL source for a correlation, not the textbook
     that reprinted it -- and if you only read the textbook, cite it as such. -->

---

# Appendix A — Raw data

Complete, unprocessed readings with timestamps. Include the runs you rejected and say why you
rejected them; silently deleting inconvenient data is the one thing here that is actually
misconduct rather than a lost mark.

# Appendix B — Sample calculation

One complete worked calculation from raw reading to final U, with units carried at every step.

# Appendix C — Analysis code

```python
# Include your script, or link the repository and give the commit hash so the
# exact version that produced these numbers can be recovered.
# See: https://github.com/OpenChemE/templates
```

# Appendix D — Risk assessment

Attach the signed assessment. Note any deviation from the planned procedure and what was done
about it.
