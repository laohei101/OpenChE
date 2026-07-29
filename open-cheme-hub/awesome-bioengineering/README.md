# Awesome Bioengineering [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Open resources for bioprocess engineering, metabolic modelling, synthetic biology, biomaterials,
> and tissue engineering.

Bioengineering sits where chemical engineering, molecular biology, and materials science overlap,
and its tooling is scattered across all three. A bioprocess engineer needs kinetics and mass
transfer; a metabolic engineer needs constraint-based optimisation; a synthetic biologist needs
sequence design and part registries. This list covers all of it, organised so you can find the
half you didn't train in.

Everything here is free to use.

**Contributions welcome** — see the
[organisation contributing guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md).

---

## Contents

- [Bioprocess Modelling & Control](#bioprocess-modelling--control)
- [Genome-Scale Metabolic Models](#genome-scale-metabolic-models)
- [Kinetic & Whole-Cell Modelling](#kinetic--whole-cell-modelling)
- [Synthetic Biology](#synthetic-biology)
- [Protein & Enzyme Engineering](#protein--enzyme-engineering)
- [Biomaterials](#biomaterials)
- [Tissue Engineering & Biofabrication](#tissue-engineering--biofabrication)
- [Bioinformatics Crossover](#bioinformatics-crossover)
- [Standards, Data & Reproducibility](#standards-data--reproducibility)
- [Learning Resources](#learning-resources)
- [Community & Conferences](#community--conferences)
- [Related Lists](#related-lists)

---

## Bioprocess Modelling & Control

- [BioSTEAM](https://biosteam.readthedocs.io) — Fast techno-economic analysis and process simulation for biorefineries, with unit operations, costing, and uncertainty propagation built in. `python` `tea`
- [PyFOOMB](https://github.com/MicroPhen/pyFOOMB) — Object-oriented bioprocess modelling with parameter estimation, uncertainty quantification, and support for multi-experiment fitting. `python` `parameter-estimation`
- [bioprocess-control (`pyIDES`)](https://github.com/bioprocess-tools/pyides) — Fed-batch feeding strategy design and soft-sensor implementations for substrate-limited fermentation. `python` `control`
- [Bioreactor CFD cases for OpenFOAM](https://github.com/OpenFOAM/OpenFOAM-dev) — Stirred-tank and airlift tutorial cases covering mixing time, kLa estimation, and shear distribution. `c++` `cfd`
- [Aspen alternatives for fermentation — DWSIM bio templates](https://dwsim.org) — Flowsheeting for downstream recovery trains: centrifugation, filtration, chromatography, drying. `gui`
- [SciML `Catalyst.jl` for bioreactions](https://github.com/SciML/Catalyst.jl) — Symbolic reaction networks that compile to deterministic ODEs or stochastic jump processes, useful when copy numbers are low. `julia`
- [kLa and mass-transfer correlations in `bioengineering-utils`](https://github.com/bioprocess-tools/bioeng-utils) — Van 't Riet and Garcia-Ochoa correlations for oxygen transfer, with power-number lookups for standard impellers. `python`

## Genome-Scale Metabolic Models

- [COBRApy](https://opencobra.github.io/cobrapy/) — Constraint-based reconstruction and analysis in Python: FBA, pFBA, FVA, gene deletions, and model editing. The default entry point. `python`
- [COBRA Toolbox](https://opencobra.github.io/cobratoolbox/) — The MATLAB counterpart, with a much larger set of specialised methods including thermodynamic and expression-integrated analyses. `matlab`
- [Memote](https://memote.readthedocs.io) — Standardised test suite that scores a metabolic model's quality — mass balance, annotation coverage, consistency — and produces a report you can put in a paper. `python` `qa`
- [ModelSEED / KBase](https://www.kbase.us) — Automated draft reconstruction from an annotated genome, with gap-filling and a hosted environment for the whole pipeline. `web` `platform`
- [CarveMe](https://github.com/cdanielmachado/carveme) — Top-down reconstruction that carves a species model out of a universal model in seconds, well suited to hundreds of genomes. `python`
- [BiGG Models](http://bigg.ucsd.edu) — Curated repository of high-quality genome-scale models with standardised identifiers and an API. `database`
- [ETFL / thermodynamic FBA (`pytfa`)](https://github.com/EPFL-LCSB/pytfa) — Adds thermodynamic constraints and expression-and-allocation constraints so flux solutions are physically reachable. `python`
- [MICOM](https://github.com/micom-dev/micom) — Community-level metabolic modelling for microbiomes, with trade-offs between community and individual growth. `python`
- [cobrapy sampling — `OptGPSampler`](https://opencobra.github.io/cobrapy/building_model/sampling/) — Uniform flux sampling for when a single FBA optimum isn't a defensible answer. `python`
- [OptKnock / OptFlux strain design](https://www.optflux.org) — Computational strain design (OptKnock, OptGene) with a GUI, aimed at metabolic engineers rather than programmers. `java` `gui`

## Kinetic & Whole-Cell Modelling

- [Tellurium](http://tellurium.analogmachine.org) — Python environment for systems biology built on libRoadRunner and Antimony, with fast SBML simulation and parameter scans. `python` `sbml`
- [COPASI](https://copasi.org) — Biochemical network simulator with steady-state, time-course, stochastic, and parameter-estimation methods behind a usable GUI. `c++` `gui`
- [libRoadRunner](https://libroadrunner.org) — High-performance SBML simulation engine with JIT compilation; what you use when a parameter sweep needs a million integrations. `c++` `python`
- [BioNetGen](https://bionetgen.org) — Rule-based modelling for systems with combinatorial complexity — receptor states, phosphorylation cascades — where writing every species is hopeless. `rule-based`
- [Whole-Cell Model of *E. coli* (Covert Lab)](https://github.com/CovertLab/wcEcoli) — The most complete published whole-cell model; enormous, instructive, and a benchmark for integration. `python` `research`
- [Basico](https://github.com/copasi/basico) — Simple Python API over COPASI so its solvers are scriptable in a notebook. `python`

## Synthetic Biology

- [SBOL — Synthetic Biology Open Language](https://sbolstandard.org) — Data standard for genetic designs, with `pySBOL3` and `libSBOLj` implementations; the interchange format between design tools. `standard` `python` `java`
- [Benchling (free academic tier)](https://www.benchling.com/academic) — Cloud molecular biology suite: sequence design, cloning simulation, and an ELN. Free for academic labs. `web` `commercial-free-tier`
- [SnapGene Viewer](https://www.snapgene.com/snapgene-viewer) — Free viewer for annotated plasmid maps and sequence files; reads almost everything. `gui` `commercial-free-tier`
- [Benchling alternatives — `pydna`](https://github.com/BjornFJohansson/pydna) — Simulates cloning, Gibson assembly, and PCR in code so a construction plan is reproducible and diffable. `python`
- [DNA Chisel](https://github.com/Edinburgh-Genome-Foundry/DnaChisel) — Sequence optimisation under constraints: codon usage, restriction sites, GC content, synthesis manufacturability. `python`
- [iGEM Registry of Standard Biological Parts](http://parts.igem.org) — The community parts registry, with characterisation data of variable but often useful quality. `database`
- [Cello](https://github.com/CIDARLAB/cello) — Compiles Verilog descriptions of logic into genetic circuits with characterised gates; the clearest demonstration of design automation for biology. `java` `design-automation`
- [Edinburgh Genome Foundry toolset](https://edinburgh-genome-foundry.github.io) — A dozen focused libraries for assembly planning, primer design, sequence validation, and lab report generation. `python`
- [SynBioHub](https://synbiohub.org) — Repository for sharing genetic designs in SBOL with provenance and versioning. `web` `database`
- [Ribosome binding site calculator (open reimplementations)](https://github.com/hsalis/Ribosome-Binding-Site-Calculator-v1.0) — Thermodynamic prediction of translation initiation rate for RBS design. `python`

## Protein & Enzyme Engineering

- [ColabFold](https://github.com/sokrypton/ColabFold) — AlphaFold2 and related models made runnable in a notebook in minutes rather than a cluster in days. `python` `notebook`
- [ESM / ESMFold](https://github.com/facebookresearch/esm) — Protein language models for embeddings, variant effect prediction, and single-sequence structure prediction. `python` `pytorch`
- [Rosetta Commons (free academic licence)](https://www.rosettacommons.org) — The reference suite for protein design, docking, and structure prediction; free to academics. `c++` `commercial-free-tier`
- [PyRosetta](https://www.pyrosetta.org) — Python bindings to Rosetta for scripted design protocols. `python` `commercial-free-tier`
- [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) — Inverse folding: given a backbone, propose sequences that fold to it, with high experimental success rates. `python`
- [FoldX alternatives — `FoldSeek`](https://github.com/steineggerlab/foldseek) — Structure search across the whole AlphaFold database in seconds, for finding remote structural homologues. `c++`
- [BRENDA](https://www.brenda-enzymes.org) — The comprehensive enzyme kinetics database: kcat, Km, inhibitors, and conditions, extracted from the literature. `database`

## Biomaterials

- [PolyInfo / Polymer Genome open subsets](https://polymergenome.org) — Property data and ML predictions for polymers, including degradation and mechanical properties relevant to implants. `database`
- [PyMesh / trimesh for scaffold geometry](https://trimsh.org) — Mesh processing for porous scaffold design: porosity, surface-area-to-volume, and printability checks. `python`
- [Gibbon toolbox for MATLAB](https://www.gibboncode.org) — Open toolbox for computational biomechanics and biomaterial FEA, with FEBio integration and meshing utilities. `matlab`
- [FEBio](https://febio.org) — Finite element solver purpose-built for biological materials: hyperelasticity, poroelasticity, growth and remodelling. `c++` `fea`
- [Materials Project — biocompatible alloys subset](https://materialsproject.org) — Computed properties for the metals and ceramics used in implants, with an open API. `database` `api`
- [pyDRT for degradation modelling](https://github.com/biomaterials-tools/pydrt) — Fits hydrolytic and enzymatic degradation kinetics to mass-loss and molecular-weight data. `python`

## Tissue Engineering & Biofabrication

- [Slic3r / PrusaSlicer for bioprinting](https://github.com/prusa3d/PrusaSlicer) — Open slicers adapted for extrusion bioprinting; full G-code control matters more than a vendor's fixed profile. `c++` `gui`
- [BioPrint toolpath planning — `bioprint-planner`](https://github.com/biofab-tools/bioprint-planner) — Generates infill patterns and toolpaths for hydrogel constructs with viability-aware speed limits. `python`
- [CompuCell3D](https://compucell3d.org) — Multi-cell modelling environment (cellular Potts) for morphogenesis, cell sorting, and tissue growth. `c++` `python` `gui`
- [PhysiCell](http://physicell.org) — Agent-based simulator for multicellular systems with diffusive substrates; scales to millions of cells. `c++`
- [Chaste](https://chaste.github.io) — Cambridge's simulation library for cardiac electrophysiology and cell-based tissue models, with strong testing culture. `c++`
- [Fiji / ImageJ](https://fiji.sc) — Image analysis for histology, live-cell imaging, and scaffold characterisation, with a plugin for nearly everything. `java` `gui`
- [CellProfiler](https://cellprofiler.org) — Pipeline-based quantitative image analysis for high-content screening, no coding required. `python` `gui`

## Bioinformatics Crossover

- [Biopython](https://biopython.org) — Sequence handling, file parsing, and interfaces to the major biological databases. `python`
- [Bioconda](https://bioconda.github.io) — Conda channel with 8000+ bioinformatics packages; makes reproducible bio environments tractable. `packaging`
- [Galaxy](https://galaxyproject.org) — Web platform for running and sharing analyses with full provenance, usable without a terminal. `web` `platform`
- [nf-core](https://nf-co.re) — Community-curated, peer-reviewed Nextflow pipelines with consistent structure and testing. `nextflow` `workflow`
- [scikit-bio](https://scikit.bio) — Core data structures and algorithms for sequences, alignments, and diversity analysis. `python`
- [Bioconductor](https://bioconductor.org) — The R ecosystem for omics analysis, with rigorous package review and vignettes. `r`

## Standards, Data & Reproducibility

- [SBML](https://sbml.org) — The systems biology markup language; if a model can't be exported to SBML, it can't easily be reused. `standard` `xml`
- [MIRIAM & MIASE guidelines](https://co.mbine.org/standards) — Minimum information standards for annotating and simulating models, from the COMBINE community. `standard`
- [BioModels](https://www.ebi.ac.uk/biomodels/) — Repository of curated, annotated published models you can load and rerun. `database`
- [FAIRDOMHub](https://fairdomhub.org) — Data, model, and SOP management for systems biology projects, built around FAIR principles. `platform`
- [protocols.io](https://www.protocols.io) — Versioned, citable experimental protocols; the fix for "as previously described". `platform`

## Learning Resources

- [Systems Biology: Constraint-Based Reconstruction and Analysis (Palsson) course notes](https://systemsbiology.ucsd.edu) — The canonical treatment of genome-scale modelling, with accompanying tutorials. `course` `book`
- [COBRApy documentation tutorials](https://cobrapy.readthedocs.io/en/latest/getting_started.html) — Worked from a first FBA to gene-deletion screens; do these before reading papers. `tutorial` `free`
- [Bioprocess Engineering Principles (Doran) problem companions](https://github.com/bioprocess-teaching) — Community-written Python solutions to the standard bioprocess textbook problems. `python` `notebooks`
- [MIT 20.320 Analysis of Biomolecular and Cellular Systems (OCW)](https://ocw.mit.edu/courses/20-320-analysis-of-biomolecular-and-cellular-systems-fall-2012/) — Quantitative modelling of receptor binding, signalling, and pharmacokinetics. `course` `free`
- [iGEM team wiki archive](http://igem.org/Main_Page) — Two decades of team wikis: a large, uneven, and genuinely useful record of what synthetic biology projects actually attempted. `archive`
- [Build-A-Cell open community resources](https://www.buildacell.org) — Materials and talks from the synthetic cell community, useful for bottom-up bioengineering. `community` `course`

## Community & Conferences

- [COMBINE](https://co.mbine.org) — The standards community behind SBML, SBOL, and SED-ML; annual meetings and open working groups. `community`
- [SEED — Synthetic Biology: Engineering, Evolution & Design](https://synbioconference.org) — The main synthetic biology conference. `conference`
- [Metabolic Engineering (International Metabolic Engineering Society)](https://www.aiche.org/sbe) — Biennial meeting, the reference venue for strain engineering. `conference`
- [ESBES — European Society of Biochemical Engineering Sciences](https://efce.info/ESBES.html) — Bioprocess engineering across Europe, with an active early-career section. `community` `conference`
- [iGEM Competition](https://igem.org) — Annual student synthetic biology competition; the parts, wikis, and safety guidance are all public. `community`
- [Bioengineering Stack Exchange](https://bioinformatics.stackexchange.com) — Nearest Q&A site for computational bio questions, with knowledgeable answerers. `forum`

## Related Lists

- [awesome-chemical-engineering](https://github.com/open-cheme-hub/awesome-chemical-engineering) — Reactor design, mass transfer, and downstream unit operations.
- [awesome-chemoinformatics](https://github.com/open-cheme-hub/awesome-chemoinformatics) — Molecular modelling and enzyme substrate design.
- [awesome-medical-engineering](https://github.com/open-cheme-hub/awesome-medical-engineering) — Where biomaterials meet regulatory pathways.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own
licences.
