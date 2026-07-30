<!--
  GENERATED FILE — DO NOT EDIT.

  Produced by scripts/generate_markdown_lists.py from the canonical records in
  catalog/resources/. Edit the YAML and re-run the generator; a hand edit here
  is overwritten on the next build and fails CI in the meantime.
-->

# Awesome Bioengineering [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Open resources for bioprocess engineering, metabolic modelling, synthetic biology, biomaterials, and tissue engineering.

**70 entries.** Every entry is free to use. Descriptions say what a tool *does*, not how good it is.

Entries carry a verification marker only when something was actually checked — see [verification methodology](../docs/verification-methodology.md). An entry with no marker has not been independently verified.

**Contributions welcome** — see [CONTRIBUTING.md](../CONTRIBUTING.md).

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
- [Catalyst.jl](https://github.com/SciML/Catalyst.jl) — Domain-specific language for reaction networks in Julia that compiles to ODE, SDE, or jump-process models. `julia`
- [OpenFOAM](https://www.openfoam.com) — General CFD; the mixer and multiphase tutorials are the usual starting point for stirred-tank mixing time and shear studies. No bioreactor-specific case ships with it. `c++` `cfd`
- [PyFOOMB](https://github.com/MicroPhen/pyFOOMB) — Object-oriented bioprocess modelling with parameter estimation, uncertainty quantification, and support for multi-experiment fitting. `python` `parameter-estimation`

## Genome-Scale Metabolic Models

- [BiGG Models](http://bigg.ucsd.edu) — Curated repository of high-quality genome-scale models with standardised identifiers and an API. `database`
- [CarveMe](https://github.com/cdanielmachado/carveme) — Top-down reconstruction that carves a species model out of a universal model in seconds, well suited to hundreds of genomes. `python`
- [COBRA Toolbox](https://opencobra.github.io/cobratoolbox/) — The MATLAB counterpart, with a much larger set of specialised methods including thermodynamic and expression-integrated analyses. `matlab`
- [COBRApy](https://opencobra.github.io/cobrapy/) — Constraint-based reconstruction and analysis in Python: FBA, pFBA, FVA, gene deletions, and model editing. The default entry point. `python`
- [cobrapy sampling — OptGPSampler](https://opencobra.github.io/cobrapy/building_model/sampling/) — Uniform flux sampling for when a single FBA optimum isn't a defensible answer. `python`
- [ETFL / thermodynamic FBA (pytfa)](https://github.com/EPFL-LCSB/pytfa) — Adds thermodynamic constraints and expression-and-allocation constraints so flux solutions are physically reachable. `python`
- [Memote](https://memote.readthedocs.io) — Standardised test suite that scores a metabolic model's quality — mass balance, annotation coverage, consistency — and produces a report you can put in a paper. `python` `qa`
- [MICOM](https://github.com/micom-dev/micom) — Community-level metabolic modelling for microbiomes, with trade-offs between community and individual growth. `python`
- [ModelSEED / KBase](https://www.kbase.us) — Automated draft reconstruction from an annotated genome, with gap-filling and a hosted environment for the whole pipeline. `platform`
- [OptKnock / OptFlux strain design](https://www.optflux.org) — Computational strain design (OptKnock, OptGene) with a GUI, aimed at metabolic engineers rather than programmers. `java` `gui`

## Kinetic & Whole-Cell Modelling

- [Basico](https://github.com/copasi/basico) — Simple Python API over COPASI so its solvers are scriptable in a notebook. `python`
- [BioNetGen](https://bionetgen.org) — Rule-based modelling for systems with combinatorial complexity — receptor states, phosphorylation cascades — where writing every species is hopeless. `rule-based`
- [COPASI](https://copasi.org) — Biochemical network simulator with steady-state, time-course, stochastic, and parameter-estimation methods behind a usable GUI. `c++` `gui`
- [libRoadRunner](https://libroadrunner.org) — High-performance SBML simulation engine with JIT compilation; what you use when a parameter sweep needs a million integrations. `c++` `python`
- [Tellurium](http://tellurium.analogmachine.org) — Python environment for systems biology built on libRoadRunner and Antimony, with fast SBML simulation and parameter scans. `python` `sbml`
- [Whole-Cell Model of *E. coli* (Covert Lab)](https://github.com/CovertLab/wcEcoli) — The most complete published whole-cell model; enormous, instructive, and a benchmark for integration. `python` `research`

## Synthetic Biology

- [Benchling (free academic tier)](https://www.benchling.com/academic) — Cloud molecular biology suite: sequence design, cloning simulation, and an ELN. Free for academic labs. `commercial-free-tier`
- [Benchling alternatives — pydna](https://github.com/BjornFJohansson/pydna) — Simulates cloning, Gibson assembly, and PCR in code so a construction plan is reproducible and diffable. `python`
- [Cello](https://github.com/CIDARLAB/cello) — Compiles Verilog descriptions of logic into genetic circuits with characterised gates; the clearest demonstration of design automation for biology. `java` `design-automation`
- [DNA Chisel](https://github.com/Edinburgh-Genome-Foundry/DnaChisel) — Sequence optimisation under constraints: codon usage, restriction sites, GC content, synthesis manufacturability. `python`
- [Edinburgh Genome Foundry toolset](https://edinburgh-genome-foundry.github.io) — A dozen focused libraries for assembly planning, primer design, sequence validation, and lab report generation. `python`
- [iGEM Registry of Standard Biological Parts](http://parts.igem.org) — The community parts registry, with characterisation data of variable but often useful quality. `database`
- [Ribosome binding site calculator (open reimplementations)](https://github.com/hsalis/Ribosome-Binding-Site-Calculator-v1.0) — Thermodynamic prediction of translation initiation rate for RBS design. `python`
- [SBOL — Synthetic Biology Open Language](https://sbolstandard.org) — Data standard for genetic designs, with  and  implementations; the interchange format between design tools. `java` `python` `pysbol3` `libsbolj` `standard`
- [SnapGene Viewer](https://www.snapgene.com/snapgene-viewer) — Free viewer for annotated plasmid maps and sequence files; reads almost everything. `gui` `commercial-free-tier`
- [SynBioHub](https://synbiohub.org) — Repository for sharing genetic designs in SBOL with provenance and versioning. `database`

## Protein & Enzyme Engineering

- [BRENDA](https://www.brenda-enzymes.org) — The comprehensive enzyme kinetics database: kcat, Km, inhibitors, and conditions, extracted from the literature. `database`
- [ColabFold](https://github.com/sokrypton/ColabFold) — AlphaFold2 and related models made runnable in a notebook in minutes rather than a cluster in days. `python` `notebook`
- [ESM / ESMFold](https://github.com/facebookresearch/esm) — Protein language models for embeddings, variant effect prediction, and single-sequence structure prediction. `python` `pytorch`
- [FoldX alternatives — FoldSeek](https://github.com/steineggerlab/foldseek) — Structure search across the whole AlphaFold database in seconds, for finding remote structural homologues. `c++`
- [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) — Inverse folding: given a backbone, propose sequences that fold to it, with high experimental success rates. `python`
- [PyRosetta](https://www.pyrosetta.org) — Python bindings to Rosetta for scripted design protocols. `python` `commercial-free-tier`
- [Rosetta Commons (free academic licence)](https://www.rosettacommons.org) — The reference suite for protein design, docking, and structure prediction; free to academics. `c++` `commercial-free-tier`

## Biomaterials

- [FEBio](https://febio.org) — Finite element solver purpose-built for biological materials: hyperelasticity, poroelasticity, growth and remodelling. `c++` `fea`
- [Gibbon](https://www.gibboncode.org) — MATLAB toolbox for computational biomechanics: meshing, FEBio interfacing, and image-based model generation. `matlab`
- [Materials Project — biocompatible alloys subset](https://materialsproject.org) — Computed properties for the metals and ceramics used in implants, with an open API. `database` `api`
- [PolyInfo / Polymer Genome open subsets](https://polymergenome.org) — Property data and ML predictions for polymers, including degradation and mechanical properties relevant to implants. `database`
- [trimesh](https://trimsh.org) — Mesh loading, repair, boolean operations, and mass properties in Python; the glue for any geometry pipeline. `python`

## Tissue Engineering & Biofabrication

- [CellProfiler](https://cellprofiler.org) — Pipeline-based quantitative image analysis for high-content screening, no coding required. `python` `gui`
- [Chaste](https://chaste.github.io) — Cambridge's simulation library for cardiac electrophysiology and cell-based tissue models, with strong testing culture. `c++`
- [CompuCell3D](https://compucell3d.org) — Multi-cell modelling environment (cellular Potts) for morphogenesis, cell sorting, and tissue growth. `c++` `python` `gui`
- [Fiji / ImageJ](https://fiji.sc) — Image analysis for histology, live-cell imaging, and scaffold characterisation, with a plugin for nearly everything. `java` `gui`
- [PhysiCell](http://physicell.org) — Agent-based simulator for multicellular systems with diffusive substrates; scales to millions of cells. `c++`
- [Slic3r / PrusaSlicer for bioprinting](https://github.com/prusa3d/PrusaSlicer) — Open slicers adapted for extrusion bioprinting; full G-code control matters more than a vendor's fixed profile. `c++` `gui`

## Bioinformatics Crossover

- [Bioconda](https://bioconda.github.io) — Conda channel with 8000+ bioinformatics packages; makes reproducible bio environments tractable. `packaging`
- [Bioconductor](https://bioconductor.org) — The R ecosystem for omics analysis, with rigorous package review and vignettes. `r`
- [Biopython](https://biopython.org) — Sequence handling, file parsing, and interfaces to the major biological databases. `python`
- [Galaxy](https://galaxyproject.org) — Web platform for running and sharing analyses with full provenance, usable without a terminal. `platform`
- [nf-core](https://nf-co.re) — Community-curated, peer-reviewed Nextflow pipelines with consistent structure and testing. `nextflow` `workflow`
- [scikit-bio](https://scikit.bio) — Core data structures and algorithms for sequences, alignments, and diversity analysis. `python`

## Standards, Data & Reproducibility

- [BioModels](https://www.ebi.ac.uk/biomodels/) — Repository of curated, annotated published models you can load and rerun. `database`
- [FAIRDOMHub](https://fairdomhub.org) — Data, model, and SOP management for systems biology projects, built around FAIR principles. `platform`
- [MIRIAM & MIASE guidelines](https://co.mbine.org/standards) — Minimum information standards for annotating and simulating models, from the COMBINE community. `standard`
- [protocols.io](https://www.protocols.io) — Versioned, citable experimental protocols; the fix for "as previously described". `platform`
- [SBML](https://sbml.org) — The systems biology markup language; if a model can't be exported to SBML, it can't easily be reused. `standard` `xml`

## Learning Resources

- [Build-A-Cell open community resources](https://www.buildacell.org) — Materials and talks from the synthetic cell community, useful for bottom-up bioengineering. `community` `course`
- [COBRApy documentation tutorials](https://cobrapy.readthedocs.io/en/latest/getting_started.html) — Worked from a first FBA to gene-deletion screens; do these before reading papers. `tutorial` `free`
- [iGEM team wiki archive](http://igem.org/Main_Page) — Two decades of team wikis: a large, uneven, and genuinely useful record of what synthetic biology projects actually attempted. `archive`
- [MIT 20.320 Analysis of Biomolecular and Cellular Systems (OCW)](https://ocw.mit.edu/courses/20-320-analysis-of-biomolecular-and-cellular-systems-fall-2012/) — Quantitative modelling of receptor binding, signalling, and pharmacokinetics. `course` `free`
- [Systems Biology: Constraint-Based Reconstruction and Analysis (Palsson) course notes](https://systemsbiology.ucsd.edu) — The canonical treatment of genome-scale modelling, with accompanying tutorials. `course` `book`

## Community & Conferences

- [Bioengineering Stack Exchange](https://bioinformatics.stackexchange.com) — Nearest Q&A site for computational bio questions, with knowledgeable answerers. `forum`
- [COMBINE](https://co.mbine.org) — The standards community behind SBML, SBOL, and SED-ML; annual meetings and open working groups. `community`
- [ESBES — European Society of Biochemical Engineering Sciences](https://efce.info/ESBES.html) — Bioprocess engineering across Europe, with an active early-career section. `community` `conference`
- [iGEM Competition](https://igem.org) — Annual student synthetic biology competition; the parts, wikis, and safety guidance are all public. `community`
- [Metabolic Engineering (International Metabolic Engineering Society)](https://www.aiche.org/sbe) — Biennial meeting, the reference venue for strain engineering. `conference`
- [SEED — Synthetic Biology: Engineering, Evolution & Design](https://synbioconference.org) — The main synthetic biology conference. `conference`

## Related Lists

- [Awesome Chemical Engineering](awesome-chemical-engineering.md)
- [Awesome Chemoinformatics](awesome-chemoinformatics.md)
- [Awesome Medical Engineering](awesome-medical-engineering.md)

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own licences.
