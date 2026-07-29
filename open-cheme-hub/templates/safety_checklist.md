---
title: "Process Safety Review Checklist"
node: "[Node ID and description, e.g. N-03: Reactor R-101 feed section]"
drawing_refs: ["P&ID-1042 Rev C", "PFD-0031 Rev B", "Cause & Effect Matrix CE-07"]
review_type: "HAZOP"   # HAZOP | What-If | Checklist | LOPA | Pre-startup (PSSR) | MOC
review_date: 2026-04-14
facilitator: "[Name, qualification]"
scribe: "[Name]"
team:
  - "[Process engineer]"
  - "[Operations representative — must have run this unit]"
  - "[Instrument/control engineer]"
  - "[Mechanical engineer]"
  - "[Safety/HSE representative]"
revision: "0"
status: "DRAFT"        # DRAFT | IN REVIEW | CLOSED-OUT
---

# Process Safety Review Checklist

> ## Read this before using the checklist
>
> **This is a prompt list, not a safety case.** It helps a competent team remember to ask
> questions. It does not make anyone competent, it does not cover your specific hazards, and a
> completed copy is not evidence that a process is safe.
>
> A real process hazard analysis requires a **multidisciplinary team** including someone who
> has actually operated the unit, a **trained facilitator**, current drawings verified against
> the plant as built, and a **documented, tracked close-out** of every action. Where a
> jurisdiction mandates a methodology (OSHA 29 CFR 1910.119 PSM, EU Seveso III, COMAH), that
> mandate governs, not this file.
>
> **Never** use this to sign off a design, satisfy a regulator, or replace a formal HAZOP.
> Use it to prepare for one, to structure a small-scale or laboratory review, and as a
> teaching aid.

---

## How to use it

1. **Break the system into nodes** — sections with a common design intent (a line between two
   vessels, a reactor, a pump set). Review one node at a time.
2. **State the design intent explicitly** before you start deviating from it. "Transfer feed
   from T-101 to R-101 at 3–5 m³/h, 20–30 °C, 4 barg." Most missed hazards trace back to a
   vague intent.
3. **Apply guide words systematically** (Section 2). Do not skip a combination because it
   "obviously can't happen" — say why it can't, and record that.
4. **For each credible deviation**, record cause, consequence, existing safeguards, and
   whether risk is tolerable. Assign an action with a **named owner and a date** if not.
5. **Close out every action.** An open action from a review three years ago is a finding in
   its own right.

Record findings in the worksheet at Section 8.

---

## 1. Preparation — before the review meeting

- [ ] Node boundaries defined and marked up on the P&IDs
- [ ] **P&IDs verified against the plant as built** (not as designed — walk the line)
- [ ] PFD, heat and material balance, and stream table available and current
- [ ] Equipment datasheets, relief device sizing calculations, and vendor manuals available
- [ ] Safety Data Sheets for **every** material present, including intermediates, utilities,
      cleaning agents, and anything formed by credible mis-operation
- [ ] Chemical compatibility / reactivity matrix reviewed (see Section 3)
- [ ] Previous PHA reports, and their **outstanding actions**, available
- [ ] Incident history for this unit and for similar units elsewhere in the company
- [ ] Cause-and-effect matrix and interlock schedule available
- [ ] Alarm rationalisation records available
- [ ] Team assembled, including at least one person who has operated the unit
- [ ] Facilitator is independent of the design team
- [ ] Time allowed is realistic — a rushed review is worse than none, because it produces a
      document that says the hazards were considered

---

## 2. Guide-word matrix (HAZOP core)

Apply each guide word to each parameter within the node. Tick when considered; record the
outcome in the worksheet, including "not credible because…".

| Parameter | NO / NONE | MORE | LESS | REVERSE | AS WELL AS | PART OF | OTHER THAN |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Flow** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| **Pressure** | ☐ | ☐ | ☐ | ☐ | — | — | ☐ |
| **Temperature** | — | ☐ | ☐ | — | — | — | ☐ |
| **Level** | ☐ | ☐ | ☐ | — | — | — | — |
| **Composition** | ☐ | ☐ | ☐ | — | ☐ | ☐ | ☐ |
| **Reaction** | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| **Phase** | — | — | — | — | ☐ | ☐ | ☐ |
| **Mixing / agitation** | ☐ | ☐ | ☐ | ☐ | — | — | ☐ |
| **Time / sequence** | ☐ | ☐ | ☐ | ☐ | — | ☐ | ☐ |
| **Utilities** (steam, CW, air, N₂, power) | ☐ | ☐ | ☐ | — | — | ☐ | ☐ |

### 2.1 Prompts that catch what the matrix misses

- [ ] **Loss of all utilities simultaneously** — a site power dip takes cooling water,
      instrument air, and agitation together. What is the safe state, and does it get there
      without operator action?
- [ ] **Instrument air failure** — does every control valve fail to its *safe* position, and
      is "safe" the same during startup, normal operation, and shutdown? (It often is not.)
- [ ] **Loss of cooling on an exothermic reaction** — time to onset of runaway from normal
      operating conditions. If nobody in the room can state this number, the review stops here.
- [ ] **Two-phase relief** — is the relief device sized for the actual relieving case,
      including possible two-phase flow (DIERS methodology)?
- [ ] **Thermal expansion of trapped liquid** between two closed valves
- [ ] **Reverse flow** on pump trip — is the non-return valve the only protection?
- [ ] **Overfilling** — what happens when the tank is full and the filling continues?
- [ ] **Wrong material delivered or connected** — can it be? Different couplings?
- [ ] **Human error under time pressure** — the night shift, one operator, an alarm flood
- [ ] **Start-up and shut-down** — most incidents happen in transient states, and most PHAs
      are conducted against the steady state
- [ ] **Maintenance and line breaking** — isolation, purge, drain, blind list
- [ ] **External events** — flood, extreme cold, high wind, vehicle impact, loss of site power

---

## 3. Chemical hazards

Complete for every material present.

| Material | Phase | Inventory | Flash point | AIT | LEL–UEL | Exposure limit | Key hazard |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

- [ ] SDS current (within 3 years) and available at point of use
- [ ] **Incompatibility matrix completed** — every pair that can credibly meet, including in a
      drain, a vent header, or a spill bund. Check against
      [CAMEO Chemicals](https://cameochemicals.noaa.gov)
- [ ] Thermal stability data reviewed (DSC/ARC) for anything that can be heated above normal
      operating temperature
- [ ] Runaway reaction potential assessed: onset temperature, adiabatic temperature rise,
      time to maximum rate
- [ ] Decomposition products identified, including under fire conditions
- [ ] Dust explosion potential assessed for any solid handling (Kst, MIE, MEC)
- [ ] Static accumulation potential for low-conductivity liquids
- [ ] Peroxide-forming chemicals identified, dated, and on a test schedule
- [ ] Materials of construction compatible with **all** process fluids, including at upset
      conditions and with cleaning agents
- [ ] Water reactivity checked — including firewater contact
- [ ] Corrosion and erosion mechanisms identified, with inspection scope to match

---

## 4. Protective systems

### 4.1 Pressure relief

- [ ] Every vessel and blockable section has overpressure protection
- [ ] Relief sizing basis documented for **each** credible scenario: blocked outlet, fire
      case, control valve failure open, thermal expansion, tube rupture, runaway reaction
- [ ] Governing case identified and the device sized for it
- [ ] Two-phase relief evaluated where a reacting or foaming system can relieve
- [ ] Inlet pressure drop below 3% of set pressure; outlet backpressure within device limits
- [ ] Relief discharge routed to a **safe location** — scrubber, flare, or safe elevation, and
      not onto an access platform, an air intake, or another unit
- [ ] Isolation valves under relief devices are car-sealed open and on the operator round
- [ ] Rupture disc / PRV combinations have a monitored interspace

### 4.2 Instrumented protection

- [ ] Safety instrumented functions identified and separated from the basic control system
- [ ] SIL determination performed where required, with the method recorded
- [ ] **The BPCS is not credited as an independent layer of protection against a hazard it can
      itself cause** — a control loop and its own high alarm on the same transmitter are one
      layer, not two
- [ ] Proof-test intervals defined, scheduled, and actually being performed
- [ ] Bypass and override management procedure in place, with time limits and authorisation
- [ ] Alarm rationalisation done: every safety-critical alarm has a defined operator response,
      enough time to perform it, and a consequence if not performed

### 4.3 Other layers

- [ ] Fire and gas detection coverage adequate for the credible release scenarios
- [ ] Emergency shutdown accessible from a safe location — not only inside the hazard zone
- [ ] Containment: bunding, drainage, and firewater retention capacity
- [ ] Explosion protection: venting, suppression, or containment for dust and gas hazards
- [ ] Ventilation adequate and its failure detected
- [ ] Emergency response plan reflects the **current** inventory and layout

---

## 5. Human factors and operations

- [ ] Written operating procedures exist, are current, and match what operators actually do
      (ask them — the gap is the finding)
- [ ] Safe operating limits documented with consequences of deviation
- [ ] Start-up, normal shutdown, and emergency shutdown procedures written and practised
- [ ] Training records current for everyone who operates the unit
- [ ] Shift handover process defined for the hazards in this node
- [ ] Critical manual actions have realistic time available under upset conditions
- [ ] Labelling on equipment matches the P&ID and the procedures
- [ ] Access and egress adequate, including with a fire at the likely release point
- [ ] Lone working and out-of-hours operation considered
- [ ] Permit to work covers hot work, confined space, line breaking, and excavation

---

## 6. Management systems

- [ ] Management of change process applied to **all** changes, including "like-for-like"
      replacements that are not (different seal material, different vendor, different alloy)
- [ ] Pre-startup safety review scheduled before introducing hazardous materials
- [ ] Mechanical integrity programme covers this equipment, with inspection intervals based on
      the degradation mechanisms identified in Section 3
- [ ] Contractor management for work in this area
- [ ] Incident reporting and investigation process functioning — near misses are being reported
- [ ] Emergency drills conducted and lessons acted upon
- [ ] **Actions from previous reviews closed out** and verified as effective

---

## 7. Laboratory and pilot-scale supplement

For bench and pilot work, where a formal HAZOP is often disproportionate but the hazard is real.

- [ ] Risk assessment written, reviewed, and signed **before** work starts
- [ ] Scale is the minimum that answers the question
- [ ] Reaction thermochemistry known — heat of reaction, adiabatic temperature rise, gas
      evolution. If it is unknown, that is the first experiment, at the smallest scale
- [ ] Quench or emergency cooling available and tested
- [ ] Pressure relief on any closed vessel, including glassware under pressure
- [ ] Work behind a blast shield or in a fume hood as appropriate
- [ ] Correct PPE selected for the actual chemical (glove material checked against a
      permeation chart, not assumed)
- [ ] Waste route defined and compatible before the reaction is run
- [ ] Someone else knows what you are doing, when you expect to finish, and what to do if you
      do not — **no unattended hazardous reactions, no out-of-hours lone working**
- [ ] Spill kit appropriate to the materials, present and unexpired
- [ ] Emergency contacts and eyewash/shower locations known without looking them up
- [ ] Scale-up factors considered before increasing quantity — surface-to-volume ratio falls
      as scale rises, so heat removal gets *worse*, and a reaction that was controllable at
      100 mL may not be at 10 L

---

## 8. Findings worksheet

| # | Guide word / deviation | Cause | Consequence | Existing safeguards | S | L | Risk | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- | :-: | :-: | :-: | --- | --- | --- | --- |
| 1 | | | | | | | | | | | |
| 2 | | | | | | | | | | | |
| 3 | | | | | | | | | | | |

**S** = severity, **L** = likelihood, per your site's risk matrix. Record which matrix and
which revision — comparing scores across different matrices is meaningless.

### Action ranking

Prefer higher-order controls. An action that adds a procedure where an inherently safer design
was available is a weak action, and reviewers should say so:

1. **Eliminate** the hazard — don't use the material, don't store the inventory
2. **Substitute** something less hazardous
3. **Engineering controls** — inherently safer design, containment, relief, interlocks
4. **Administrative controls** — procedures, training, alarms
5. **PPE** — the last line, never the only line

---

## 9. Sign-off

| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Facilitator | | | |
| Process engineer | | | |
| Operations representative | | | |
| HSE representative | | | |
| Area authority / approver | | | |

**Next scheduled review:** ____________  (typically 5 years, or on significant change)

---

## References and further reading

- [OSHA 29 CFR 1910.119 — Process Safety Management](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119)
- [CCPS — Center for Chemical Process Safety](https://www.aiche.org/ccps) — guidelines on HAZOP, LOPA, and inherently safer design
- [IEC 61882 — Hazard and operability studies application guide](https://webstore.iec.ch/publication/61973)
- [IEC 61511 — Functional safety, process sector](https://webstore.iec.ch/publication/5527)
- [CSB investigation reports](https://www.csb.gov/investigations/) — read these; every one is a review that missed something
- [HSE (UK) COMAH guidance](https://www.hse.gov.uk/comah/) — free and detailed
- [CAMEO Chemicals reactivity checker](https://cameochemicals.noaa.gov)

---

*Template maintained at [open-cheme-hub/templates](https://github.com/open-cheme-hub/templates).
Provided as-is under MIT licence, with no warranty of fitness for any purpose. Adapt it to your
site's procedures; where they differ, your site's procedures win.*
