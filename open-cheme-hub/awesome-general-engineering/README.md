# Awesome General Engineering [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Cross-cutting open tools every engineer eventually needs: CAD/CAE, control systems, signal
> processing, embedded and IoT, data handling, project management, and ethics.

The other lists in this organisation go deep in one discipline. This one covers the tools you need
regardless of discipline — the FEA solver, the control library, the oscilloscope software, the
requirements tracker, the units package that stops you from crashing a spacecraft.

Everything here is free to use.

**Contributions welcome** — see the
[organisation contributing guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md).

---

## Contents

- [CAD & Geometry](#cad--geometry)
- [CAE, FEA & Meshing](#cae-fea--meshing)
- [Control Systems](#control-systems)
- [Signal Processing & Instrumentation](#signal-processing--instrumentation)
- [Embedded & IoT](#embedded--iot)
- [Numerical Computing & Units](#numerical-computing--units)
- [Data Acquisition, SCADA & Industrial Protocols](#data-acquisition-scada--industrial-protocols)
- [Reliability & Maintenance Engineering](#reliability--maintenance-engineering)
- [Documentation & Technical Writing](#documentation--technical-writing)
- [Project & Requirements Management](#project--requirements-management)
- [Engineering Ethics & Professional Practice](#engineering-ethics--professional-practice)
- [Learning Resources](#learning-resources)
- [Related Lists](#related-lists)

---

## CAD & Geometry

- [FreeCAD](https://www.freecad.org) — Parametric 3D CAD with a proper feature tree, assembly workbench, FEM workbench, and complete Python scripting. The realistic open alternative to SolidWorks for mechanical work. `python` `c++` `gui`
- [OpenSCAD](https://openscad.org) — Constructive solid geometry defined in code, so parts are diffable, reviewable, and parametric by construction. `cli` `gui`
- [CadQuery](https://cadquery.readthedocs.io) — Python API for building parametric solids on the OCCT kernel; fluent enough to be pleasant, powerful enough for real parts. `python`
- [build123d](https://build123d.readthedocs.io) — Modern successor to CadQuery's builder API, with a cleaner selector model and good documentation. `python`
- [Open CASCADE Technology](https://dev.opencascade.org) — The geometric kernel underneath most open CAD; use directly when you need B-rep operations in your own tool. `c++`
- [LibreCAD](https://librecad.org) — Focused 2D drafting for P&IDs, layouts, and shop drawings, reading and writing DXF. `c++` `gui`
- [KiCad](https://www.kicad.org) — Schematic capture, PCB layout, and manufacturing outputs, with a strong scripting API and no seat limits. `gui` `electronics`
- [trimesh](https://trimsh.org) — Mesh loading, repair, boolean operations, and mass properties in Python; the glue for any geometry pipeline. `python`

## CAE, FEA & Meshing

- [CalculiX](http://www.calculix.de) — Nonlinear finite element solver with Abaqus-compatible input syntax; static, dynamic, thermal, and contact analyses. `fortran` `c` `fea`
- [Code_Aster](https://code-aster.org) — EDF's structural mechanics and thermomechanics solver, validated against a large public test suite; formidable and famously documented in French. `fortran` `python` `fea`
- [Elmer FEM](https://www.elmerfem.org) — Multiphysics FEM covering heat transfer, electromagnetics, acoustics, and fluid-structure interaction, with a usable GUI. `fortran` `c++` `gui`
- [Gmsh](https://gmsh.info) — Mesh generator with a scripting language and CAD kernel integration; the default meshing step for most open FEA. `c++` `python` `meshing`
- [Salome](https://www.salome-platform.org) — Pre- and post-processing platform tying CAD, meshing, and solvers into one workflow; the front end for Code_Aster. `python` `gui`
- [PrePoMax](https://prepomax.fs.um.si) — Friendly pre- and post-processor for CalculiX; makes open FEA approachable for people who learned on commercial GUIs. `gui` `windows`
- [ParaView](https://www.paraview.org) — Large-scale scientific visualisation with Python scripting for reproducible figures. `gui` `python`
- [PyVista](https://docs.pyvista.org) — Pythonic mesh and volume visualisation on VTK, ideal for notebooks and automated reporting. `python`

## Control Systems

- [python-control](https://python-control.readthedocs.io) — Transfer functions, state-space, frequency response, root locus, LQR/LQG, and describing functions. The MATLAB Control Toolbox equivalent. `python`
- [GNU Octave + Control Package](https://octave.org) — MATLAB-compatible environment; the fastest way to run existing control coursework without a licence. `octave` `matlab-compatible`
- [ControlSystems.jl](https://github.com/JuliaControl/ControlSystems.jl) — Julia control toolbox with robust control, model reduction, and automatic differentiation support. `julia`
- [do-mpc](https://www.do-mpc.com) — Nonlinear and robust model predictive control with moving horizon estimation, built on CasADi. `python` `mpc`
- [Slycot / SLICOT](https://github.com/python-control/Slycot) — The numerically careful Fortran routines behind serious control computations (Riccati equations, model reduction). `fortran` `python`
- [SIPPY](https://github.com/CPCLAB-UNIPI/SIPPY) — System identification from input-output data: ARX, ARMAX, output-error, and subspace methods. `python`
- [simupy](https://github.com/simupy/simupy) — Block-diagram-style simulation of interconnected dynamical systems in Python, without needing Simulink. `python`
- [OpenPLC](https://autonomylogic.com/openplc) — Open IEC 61131-3 PLC runtime and editor (ladder, structured text) that runs on a Raspberry Pi; ideal for control education and lab rigs. `plc` `iec-61131`

## Signal Processing & Instrumentation

- [SciPy signal](https://docs.scipy.org/doc/scipy/reference/signal.html) — Filter design, spectral estimation, resampling, and peak finding; where most signal work starts and often ends. `python`
- [PyWavelets](https://pywavelets.readthedocs.io) — Discrete and continuous wavelet transforms for transient detection and denoising. `python`
- [GNU Radio](https://www.gnuradio.org) — Software-defined radio and general streaming DSP with a graphical flowgraph editor. `c++` `python` `gui`
- [Sigrok / PulseView](https://sigrok.org) — Vendor-neutral capture and analysis for logic analysers, oscilloscopes, and multimeters, with dozens of protocol decoders. `c` `gui`
- [PyVISA](https://pyvisa.readthedocs.io) — Talks to lab instruments over GPIB, USB, serial, and Ethernet with one API; automates the whole bench. `python` `instrumentation`
- [InstrumentKit](https://github.com/instrumentkit/InstrumentKit) — Typed Python drivers for common lab instruments, so you stop parsing SCPI strings by hand. `python`
- [Nidaqmx-python and `u3` for LabJack](https://nidaqmx-python.readthedocs.io) — DAQ hardware control from Python for logging and closed-loop rigs. `python` `daq`

## Embedded & IoT

- [PlatformIO](https://platformio.org) — Cross-platform embedded build system and library manager covering hundreds of boards, with a real dependency model. `python` `embedded`
- [Zephyr RTOS](https://zephyrproject.org) — Scalable real-time OS with a strong device tree, driver model, and safety-certification path. `c` `rtos`
- [MicroPython](https://micropython.org) — Python on microcontrollers; the fastest path from idea to a running sensor node. `python` `embedded`
- [ESPHome](https://esphome.io) — YAML-configured firmware for ESP32/ESP8266 sensor nodes with dozens of sensor integrations and OTA updates. `yaml` `iot`
- [Node-RED](https://nodered.org) — Flow-based wiring of devices, APIs, and dashboards; excellent for lab data plumbing and rapid prototypes. `javascript` `iot` `gui`
- [Mosquitto](https://mosquitto.org) — Lightweight MQTT broker, the default message bus for IoT and small telemetry systems. `c` `mqtt`
- [Telegraf + InfluxDB + Grafana](https://grafana.com/oss/) — The standard open time-series stack: collect, store, and dashboard sensor and process data. `go` `time-series`
- [Home Assistant](https://www.home-assistant.io) — Surprisingly capable general device automation platform; widely repurposed for lab and facility monitoring. `python` `iot`

## Numerical Computing & Units

- [NumPy](https://numpy.org) / [SciPy](https://scipy.org) — The numerical foundation: arrays, linear algebra, optimisation, integration, statistics. `python`
- [Pint](https://pint.readthedocs.io) — Physical units with dimensional analysis and automatic conversion; catches the class of error that destroys spacecraft. `python` `units`
- [SymPy](https://www.sympy.org) — Symbolic algebra: derive equations, generate code from them, and check your algebra rather than trusting it. `python`
- [Unitful.jl](https://github.com/PainterQubits/Unitful.jl) — Zero-overhead units in Julia, checked at compile time. `julia`
- [uncertainties](https://pythonhosted.org/uncertainties/) — Propagates measurement uncertainty through calculations automatically, with correlation handling. `python`
- [Julia](https://julialang.org) — Fast, high-level language with a strong scientific ecosystem, especially for differential equations and optimisation. `julia`
- [SUNDIALS](https://computing.llnl.gov/projects/sundials) — Production-grade stiff ODE and DAE integrators. `c` `solver`

## Data Acquisition, SCADA & Industrial Protocols

- [OPC UA — `open62541`](https://www.open62541.org) — Open C implementation of OPC UA for talking to industrial equipment; the modern plant-floor protocol. `c` `opc-ua`
- [`asyncua`](https://github.com/FreeOpcUa/opcua-asyncio) — Pure-Python OPC UA client and server, the practical way to pull process data into a notebook. `python` `opc-ua`
- [pymodbus](https://pymodbus.readthedocs.io) — Modbus TCP and RTU client/server; still how a startling amount of equipment communicates. `python` `modbus`
- [ScadaBR / FUXA](https://github.com/frangoteam/FUXA) — Open web SCADA and HMI for small installations and teaching rigs. `javascript` `scada`
- [Ignition Maker Edition](https://inductiveautomation.com/ignition/maker-edition) — Full-featured industrial SCADA platform, free for personal and educational non-commercial use. `commercial-free-tier` `scada`
- [Apache Kafka / Redpanda for process telemetry](https://redpanda.com) — Durable streaming for high-rate sensor data when a historian isn't enough. `streaming`

## Reliability & Maintenance Engineering

- [`reliability`](https://reliability.readthedocs.io) — Weibull and other life-distribution fitting, accelerated life testing, and repairable systems analysis. `python`
- [`lifelines`](https://lifelines.readthedocs.io) — Survival analysis, directly applicable to time-to-failure data and censored observations. `python`
- [OpenFTA / `pyfaulttree`](https://github.com/reliability-tools/pyfaulttree) — Fault tree construction, minimal cut sets, and top-event probability calculation. `python` `risk`
- [openMAINT](https://www.openmaint.org) — Open maintenance management: asset registry, preventive schedules, work orders. `java` `web`
- [NASA Reliability Preferred Practices](https://ntrs.nasa.gov) — Free, specific, hard-won guidance documents on design for reliability. `guide` `free`

## Documentation & Technical Writing

- [Quarto](https://quarto.org) — Publishing system for technical documents that executes Python, R, and Julia; produces PDF, HTML, and Word from one source. `markdown` `publishing`
- [Sphinx](https://www.sphinx-doc.org) — Documentation generator with cross-referencing, versioning, and excellent maths support. `python` `docs`
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) — Fast, attractive documentation sites from plain Markdown with minimal configuration. `python` `docs`
- [Typst](https://typst.app) — Modern typesetting system with LaTeX-quality output and comprehensible error messages. `typesetting`
- [Mermaid](https://mermaid.js.org) — Diagrams as text — flowcharts, sequence, Gantt — that render in GitHub and stay in version control. `javascript` `diagrams`
- [draw.io / diagrams.net](https://www.diagrams.net) — General diagramming with P&ID and process shape libraries, storing editable XML inside the exported file. `gui` `diagrams`
- [Pandoc](https://pandoc.org) — Converts between essentially every document format; the universal joint of technical writing. `cli`

## Project & Requirements Management

- [Doorstop](https://doorstop.readthedocs.io) — Requirements management in version-controlled text with automatic traceability matrices; requirements review becomes code review. `python` `requirements`
- [OpenProject](https://www.openproject.org) — Project management with Gantt charts, work packages, and time tracking; self-hostable. `ruby` `web`
- [Taiga](https://www.taiga.io) — Agile project management that's pleasant to use for small engineering teams. `python` `web`
- [Plane](https://plane.so) — Modern self-hostable issue and project tracker, a lighter alternative to Jira. `typescript` `web`
- [`ganttproject`](https://www.ganttproject.biz) — Desktop scheduling with critical path and resource loading, exporting to MS Project format. `java` `gui`
- [Earned value with `pyearnedvalue`](https://github.com/project-tools/pyearnedvalue) — Computes EVM metrics (CPI, SPI, EAC) from a task list and actuals. `python`

## Engineering Ethics & Professional Practice

- [NSPE Code of Ethics for Engineers](https://www.nspe.org/resources/ethics/code-ethics) — The reference code, plus a searchable archive of Board of Ethical Review cases with reasoning. `reference` `free`
- [Online Ethics Center for Engineering and Science](https://onlineethics.org) — Case studies, teaching materials, and discussion guides across engineering disciplines. `course` `free`
- [Engineering Disasters case archive (TU Delft / Purdue open materials)](https://ethicsunwrapped.utexas.edu) — Structured case discussions — Challenger, Ford Pinto, Flint, Boeing 737 MAX — with the decision context intact. `case-studies` `free`
- [IEEE Code of Ethics](https://www.ieee.org/about/corporate/governance/p7-8.html) — Concise and widely referenced, especially for software and systems work. `reference` `free`
- [AIChE Code of Ethics](https://www.aiche.org/about/governance/code-ethics) — Chemical engineering's professional code, with explicit process safety obligations. `reference` `free`
- [Ethics of AI in engineering — ACM Code](https://www.acm.org/code-of-ethics) — Relevant whenever a model output drives a physical decision. `reference` `free`

## Learning Resources

- [MIT OpenCourseWare — Mechanical and Electrical Engineering](https://ocw.mit.edu) — Full courses with problem sets and solutions across the engineering core. `course` `free`
- [Control Systems Lectures (Brian Douglas)](https://engineeringmedia.com) — The clearest available explanations of classical and modern control; free video series. `video` `free`
- [The Missing Semester of Your CS Education](https://missing.csail.mit.edu) — Shell, Git, debugging, and automation. Engineers are rarely taught these and always need them. `course` `free`
- [Nick Higham's *Handbook of Writing for the Mathematical Sciences* notes](https://nhigham.com/blog/) — On writing technical documents that survive review. `blog`
- [Software Carpentry & Data Carpentry](https://carpentries.org) — Two-day workshops and self-paced lessons for reproducible computing. `course` `free`
- [Learn X in Y Minutes](https://learnxinyminutes.com) — Whole-language reference on one page; useful when you inherit code in a language you don't write. `reference` `free`

## Related Lists

- [awesome-chemical-engineering](https://github.com/open-cheme-hub/awesome-chemical-engineering) — Process-specific simulation and control.
- [awesome-medical-engineering](https://github.com/open-cheme-hub/awesome-medical-engineering) — Where these tools meet regulated device development.
- [templates](https://github.com/open-cheme-hub/templates) — PID tuning, unit conversion, and report starting points.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own
licences.
