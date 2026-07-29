# Awesome Chemical Engineering [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Open-source software, data, and learning resources for chemical process engineering — simulation,
> thermodynamics, unit operations, control, and safety.

Chemical engineering software has historically meant five-figure licences and a USB dongle. That's
changed: there is now a credible open stack for flowsheeting, physical properties, kinetics,
optimisation, and control. This list is what's actually worth your time, with a sentence on each so
you can tell them apart without installing six of them.

Every entry is free to use. Where a tool has a commercial edition, the entry is tagged
`commercial-free-tier` and the description says what the free version can do.

**Contributions welcome** — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Contents

- [Process Simulation](#process-simulation)
- [Thermodynamics & Physical Properties](#thermodynamics--physical-properties)
- [Reaction Engineering & Kinetics](#reaction-engineering--kinetics)
- [Unit Operations & Equipment Design](#unit-operations--equipment-design)
- [Optimisation & Numerical Solvers](#optimisation--numerical-solvers)
- [Process Control & Safety](#process-control--safety)
- [Computational Fluid Dynamics](#computational-fluid-dynamics)
- [Data & Benchmarks](#data--benchmarks)
- [Learning Resources](#learning-resources)
- [Community & Conferences](#community--conferences)
- [Related Lists](#related-lists)

---

## Process Simulation

Steady-state and dynamic flowsheeting. If you're replacing Aspen Plus or HYSYS for teaching or
early-stage work, start with DWSIM.

- [DWSIM](https://dwsim.org) — Full CAPE-OPEN compliant steady-state and dynamic flowsheet simulator with a graphical editor, ~1500 compounds, and rigorous distillation. The closest open equivalent to a commercial process simulator. `c#` `gui` `cross-platform`
- [COCO Simulator](https://www.cocosimulator.org) — Free CAPE-OPEN flowsheeting environment bundling the COFE flowsheet editor, TEA thermodynamics server, and COUSCOUS unit operations. Windows only, free as in beer. `windows` `gui` `cape-open`
- [ChemSep](https://www.chemsep.org) — Rigorous rate-based and equilibrium-stage column simulator; the LITE edition is free and handles up to 40 stages and 10 components. Bundled with COCO. `gui` `distillation` `commercial-free-tier`
- [IDAES-PSE](https://github.com/IDAES/idaes-pse) — US-DOE process systems engineering framework built on Pyomo, with equation-oriented flowsheets, property packages, and simultaneous design-and-control optimisation. Steep learning curve, unmatched capability. `python` `equation-oriented`
- [OpenModelica](https://openmodelica.org) — Equation-based modelling environment for the Modelica language; with the ThermoPower and Modelica Fluid libraries it handles dynamic process models well. `modelica` `gui` `dynamic`
- [WaterTAP](https://github.com/watertap-org/watertap) — IDAES-based library for water treatment flowsheets: RO, ion exchange, crystallisation, with costing. `python` `water-treatment`
- [pyflowsheet](https://github.com/qtdevs/pyflowsheet) — Generates publication-quality PFD and BFD drawings programmatically from Python, so flowsheet diagrams live in version control. `python` `drawing`

## Thermodynamics & Physical Properties

Where most simulation errors actually come from. Get the property package right before you argue
about the solver.

- [Cantera](https://cantera.org) — Object-oriented toolkit for chemical kinetics, thermodynamics, and transport, with reactor networks, flame solvers, and equilibrium calculations. The reference tool for reacting systems. `python` `c++` `matlab` `fortran`
- [CoolProp](http://www.coolprop.org) — Thermophysical properties for ~122 fluids and humid air using Helmholtz-energy equations of state, plus incompressible fluids and brines. Bindings for almost every language. `c++` `python` `excel` `matlab`
- [thermo](https://github.com/CalebBell/thermo) — Pure-Python chemical engineering thermodynamics: VLE/LLE flashes, cubic and SAFT-type EOS, activity coefficient models, and property estimation for ~20 000 compounds. `python`
- [chemicals](https://github.com/CalebBell/chemicals) — Companion database of pure-component constants, correlations, and critical properties with careful literature sourcing. `python` `dataset`
- [fluids](https://github.com/CalebBell/fluids) — Fluid dynamics correlations for pressure drop, friction factors, control valve sizing, flow meters, and two-phase flow. `python`
- [ht](https://github.com/CalebBell/ht) — Heat transfer correlations: conduction, convection, boiling, condensation, radiation, and exchanger effectiveness–NTU. `python`
- [Clapeyron.jl](https://github.com/ClapeyronThermo/Clapeyron.jl) — Julia framework for equations of state covering cubics, SAFT variants, activity models, and electrolytes, with automatic differentiation throughout. Fast and unusually well documented. `julia`
- [REFPROP alternatives via `teqp`](https://github.com/usnistgov/teqp) — NIST's templated EOS library giving exact derivatives via automatic differentiation; the open successor to hand-coded property derivatives. `c++` `python`
- [PHREEQC](https://www.usgs.gov/software/phreeqc-version-3) — USGS geochemical speciation and reaction-path modelling; the standard for aqueous equilibria, scaling, and mineral saturation. `c++` `gui`
- [pyromat](https://github.com/chmarti1/PYroMat) — Compact ideal-gas and multiphase property library aimed at thermodynamics coursework, with a clean unit system. `python` `educational`

## Reaction Engineering & Kinetics

- [Cantera reactor networks](https://cantera.org/stable/userguide/reactors.html) — Batch, CSTR, PFR-as-a-chain, and plug flow with surface chemistry; the workhorse for anything with a mechanism file. `python` `c++`
- [ASALI](https://github.com/srebughini/ASALI) — GUI and library for catalytic reactor modelling (batch, CSTR, 1D heterogeneous PFR) built on Cantera, aimed at people who don't want to write the ODEs. `c++` `python` `gui`
- [Reaction Mechanism Generator (RMG)](https://rmg.mit.edu) — Automatically constructs detailed kinetic mechanisms from thermochemistry and rate rules, with a database of estimated parameters. `python` `mechanism-generation`
- [pMuTT](https://github.com/VlachosGroup/pMuTT) — Python multiscale thermochemistry toolbox: converts DFT output into thermodynamic and kinetic parameters usable by Cantera or Chemkin. `python`
- [Catalyst.jl](https://github.com/SciML/Catalyst.jl) — Domain-specific language for reaction networks in Julia that compiles to ODE, SDE, or jump-process models. `julia`
- [OpenSMOKE++ (free academic)](https://www.opensmokepp.polimi.it) — Detailed-kinetics solver suite for 0D/1D reacting flows and flames, widely used for combustion mechanisms. `c++` `commercial-free-tier`

## Unit Operations & Equipment Design

- [ChemSep](https://www.chemsep.org) — Column design and rating with tray hydraulics and packed-bed pressure drop; also usable as a standalone from the free COCO bundle. `gui` `distillation`
- [HTRI alternatives — `ht` exchanger sizing](https://github.com/CalebBell/ht) — Shell-and-tube and plate exchanger sizing routines including Bell–Delaware shell-side calculations. `python`
- [pdsim](https://github.com/ibell/pdsim) — Positive-displacement compressor and expander simulation (scroll, reciprocating), from the CoolProp author. `python` `compressors`
- [OpenFOAM `reactingFoam` tutorials](https://www.openfoam.com/documentation/tutorial-guide) — Reference cases for reacting flow in packed and fluidised beds when lumped models stop being credible. `c++` `cfd`
- [Ergun and packed-bed calculators in `fluids`](https://fluids.readthedocs.io) — Voidage correlations, packed and fluidised bed pressure drop, minimum fluidisation velocity. `python`

## Optimisation & Numerical Solvers

- [Pyomo](https://www.pyomo.org) — Algebraic modelling language in Python for LP, MILP, NLP, MINLP, and DAE-constrained problems; the base layer under IDAES. `python`
- [CasADi](https://web.casadi.org) — Symbolic framework for nonlinear optimisation and algorithmic differentiation, with excellent support for optimal control and moving-horizon estimation. `python` `matlab` `c++`
- [Ipopt](https://github.com/coin-or/Ipopt) — Interior-point solver for large-scale nonlinear programs; the default NLP solver behind most open process optimisation. `c++` `solver`
- [GEKKO](https://gekko.readthedocs.io) — Python package for dynamic optimisation, parameter estimation, and nonlinear MPC with a very gentle on-ramp. `python`
- [HiGHS](https://highs.dev) — High-performance open LP/MIP solver, now the default in SciPy and fast enough for real scheduling problems. `c++` `solver`
- [SUNDIALS](https://computing.llnl.gov/projects/sundials) — CVODE, IDA, and KINSOL: the stiff ODE/DAE integrators nearly every process simulator eventually calls. `c` `solver`

## Process Control & Safety

- [python-control](https://python-control.readthedocs.io) — Classical and state-space control: transfer functions, root locus, Bode, LQR, and system identification helpers. `python`
- [do-mpc](https://www.do-mpc.com) — Model predictive control and moving-horizon estimation on CasADi, with robust multi-stage MPC for uncertain process models. `python` `mpc`
- [SIPPY](https://github.com/CPCLAB-UNIPI/SIPPY) — System identification for process models: ARX, ARMAX, subspace methods, output-error, from step or PRBS data. `python` `system-id`
- [TCLab](https://apmonitor.com/heat.htm) — $35 Arduino temperature-control kit with an open Python API; the standard hardware-in-the-loop platform for teaching PID and MPC. `hardware` `python` `course`
- [ALOHA](https://www.epa.gov/cameo/aloha-software) — EPA/NOAA atmospheric dispersion model for accidental chemical releases, with toxic, flammable, and overpressure footprints. Free, widely used by emergency planners. `gui` `windows` `macos`
- [CAMEO Chemicals](https://cameochemicals.noaa.gov) — Reactivity matrix and response information for ~6000 hazardous materials; check binary incompatibilities before you mix anything. `database` `web`
- [OSHA PSM standard 29 CFR 1910.119](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119) — The process safety management rule itself; read the source rather than a summary of it. `standard` `regulatory`
- [Layer of Protection Analysis worksheets (CCPS concept)](https://www.aiche.org/ccps) — CCPS guidance and free resources on LOPA, bow-tie analysis, and incident investigation. `methodology`

## Computational Fluid Dynamics

- [OpenFOAM](https://www.openfoam.com) — General-purpose finite-volume CFD with solvers for multiphase, reacting, and turbulent flow; the default open CFD platform in process industries. `c++` `linux`
- [SU2](https://su2code.github.io) — Open suite for PDE-constrained simulation and adjoint-based shape optimisation, strong for compressible flow and turbomachinery. `c++` `python`
- [Basilisk](http://basilisk.fr) — Adaptive-mesh solver especially good at interfacial flows — droplets, films, bubbles, coalescence. `c` `multiphase`
- [FEniCSx](https://fenicsproject.org) — Finite-element framework where you write the weak form and it generates the solver; useful for custom transport problems. `python` `c++`
- [ParaView](https://www.paraview.org) — Post-processing and visualisation for everything above, scriptable in Python for reproducible figures. `gui` `python`

## Data & Benchmarks

- [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry) — Thermochemical, thermophysical, and spectral data for tens of thousands of compounds; free for interactive use. `database` `reference`
- [NIST ThermoData Engine (TDE) free datasets](https://www.nist.gov/mml/acmd/trc) — Critically evaluated thermophysical property data and the TRC source archive. `dataset` `commercial-free-tier`
- [DETHERM](https://dechema.de/en/detherm.html) — DECHEMA's thermophysical property database, ~10 million data points; institutional subscription, but the free search shows what data exists before you pay. `database` `commercial-free-tier`
- [DIPPR 801 sample set](https://www.aiche.org/dippr) — Evaluated pure-component properties; a public sample of ~100 compounds is available for teaching. `dataset`
- [ChemSep component database](https://www.chemsep.org/downloads) — ~430 compounds with UNIFAC groups and parameters, distributed as an open XML file that other tools can read. `dataset` `xml`
- [Tennessee Eastman process simulator](https://github.com/camaramm/tennessee-eastman-profBraatz) — The canonical plant-wide control and fault-detection benchmark, with 21 fault scenarios. `matlab` `fortran` `benchmark`
- [Open Reaction Database](https://open-reaction-database.org) — Structured reaction records with conditions and yields; increasingly the substrate for reaction ML. `dataset` `api`

## Learning Resources

- [Introduction to Chemical Engineering Analysis (Doherty, MIT OCW 10.10)](https://ocw.mit.edu/courses/10-10-introduction-to-chemical-engineering-analysis-fall-2005/) — Full lecture notes and problem sets on balances and process analysis. `course` `free`
- [LearnChemE](https://learncheme.com) — Hundreds of short screencasts, interactive simulations, and ConcepTests covering the whole undergraduate curriculum, from CU Boulder. `course` `interactive`
- [APMonitor / Process Dynamics and Control course](https://apmonitor.com/pdc) — Free 12-week course with Python exercises and the TCLab hardware; the best open route into industrial control. `course` `python`
- [Computational Thermodynamics with Clapeyron.jl notebooks](https://github.com/ClapeyronThermo/introduction-to-computational-thermodynamics) — Pluto notebooks walking from ideal gases to SAFT with runnable code. `julia` `notebooks`
- [Chemical Process Dynamics and Controls (LibreTexts)](https://eng.libretexts.org/Bookshelves/Industrial_and_Systems_Engineering/Chemical_Process_Dynamics_and_Controls_(Woolf)) — Complete open textbook, CC-licensed, with worked examples. `book` `free`
- [CBE30338 Chemical Process Control](https://github.com/jckantor/CBE30338) — Jeff Kantor's notebook-based course on process dynamics, control, and optimisation, runnable end to end. `notebooks` `python`
- [Cantera tutorials and examples](https://cantera.org/stable/examples/index.html) — Runnable scripts for equilibrium, flames, reactor networks, and surface chemistry. `tutorial` `python`
- [Perry's Chemical Engineers' Handbook — open equivalents index](https://en.wikibooks.org/wiki/Introduction_to_Chemical_Engineering_Processes) — Wikibooks' open process-engineering text; not Perry's, but free and improving. `book` `free`
- [Software Carpentry for scientific computing](https://software-carpentry.org/lessons/) — Shell, Git, and Python fundamentals; the missing prerequisite for most of this list. `course` `free`

## Community & Conferences

- [AIChE Annual Meeting](https://www.aiche.org/conferences) — The largest chemical engineering meeting; the CAST division sessions are where process systems engineering work lands. `conference`
- [AIChE CAST Division](https://www.aiche.org/cast) — Computing and Systems Technology division: newsletters, awards, and the open-source software sessions. `community`
- [ESCAPE / European Symposium on Computer Aided Process Engineering](https://efce.info) — EFCE's annual CAPE symposium; proceedings are a good survey of what's current in flowsheet optimisation. `conference`
- [FOCAPD / FOCAPO](https://focapo-cpc.org) — Small, high-signal meetings on process design and operations, held on a multi-year cycle. `conference`
- [r/ChemicalEngineering](https://www.reddit.com/r/ChemicalEngineering/) — Large practitioner community; good for "which tool do people actually use" questions. `forum`
- [Eng-Tips Chemical Engineering forums](https://www.eng-tips.com/threadminder.cfm?pid=1) — Long-running professional forum with searchable archives of design and troubleshooting threads. `forum`
- [DWSIM user forum](https://dwsim.org/forum/) — Active support community for open flowsheeting, including property package questions. `forum`
- [Cantera users group](https://groups.google.com/g/cantera-users) — Where mechanism and solver questions get answered by the developers. `mailing-list`

## Related Lists

- [awesome-chemoinformatics](https://github.com/open-cheme-hub/awesome-chemoinformatics) — Molecular modelling, QSAR, and ML for chemistry.
- [awesome-bioengineering](https://github.com/open-cheme-hub/awesome-bioengineering) — Bioprocess and metabolic modelling.
- [awesome-general-engineering](https://github.com/open-cheme-hub/awesome-general-engineering) — CAD/CAE, controls, and embedded.
- [templates](https://github.com/open-cheme-hub/templates) — Starting files for balances, reactor design, and safety reviews.

---

## Contributing

Found something missing, or a link that's rotted? See [CONTRIBUTING.md](CONTRIBUTING.md). One-line
additions are merged quickly.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own
licences — check before you deploy anything.
