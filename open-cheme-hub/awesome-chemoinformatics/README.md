# Awesome Chemoinformatics [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Open tools for representing, searching, predicting, and visualising molecules and reactions.

Cheminformatics has the best open tooling of any chemistry-adjacent field — RDKit alone covers what
several commercial suites charge for. The hard part isn't finding software, it's knowing which of
forty molecular fingerprints, six file formats, and a dozen ML frameworks to reach for. This list is
organised by the question you're trying to answer.

Everything here is free to use. Descriptions say what a tool does, not how good it is.

**Contributions welcome** — see the
[organisation contributing guide](https://github.com/open-cheme-hub/.github/blob/main/CONTRIBUTING.md).

---

## Contents

- [Molecular Representations & Toolkits](#molecular-representations--toolkits)
- [File Formats & Interoperability](#file-formats--interoperability)
- [Cheminformatics Pipelines & Workflow Tools](#cheminformatics-pipelines--workflow-tools)
- [Descriptors & Fingerprints](#descriptors--fingerprints)
- [QSAR / QSPR](#qsar--qspr)
- [Machine Learning for Chemistry](#machine-learning-for-chemistry)
- [Reaction Prediction & Retrosynthesis](#reaction-prediction--retrosynthesis)
- [Molecular Simulation & Quantum Chemistry](#molecular-simulation--quantum-chemistry)
- [Chemical Databases](#chemical-databases)
- [Visualisation](#visualisation)
- [Benchmarks & Evaluation](#benchmarks--evaluation)
- [Learning Resources](#learning-resources)
- [Community](#community)
- [Related Lists](#related-lists)

---

## Molecular Representations & Toolkits

- [RDKit](https://www.rdkit.org) — The foundational open cheminformatics toolkit: substructure search, conformers, descriptors, fingerprints, reaction handling, drawing. If a tutorial says "import rdkit", this is why. `python` `c++` `java`
- [Open Babel](https://openbabel.org) — Format conversion across 110+ chemical file formats, plus force-field optimisation, conformer search, and fingerprint generation from the command line. `c++` `python` `cli`
- [OpenChemLib](https://github.com/Actelion/openchemlib) — Java toolkit with an excellent 2D structure editor, canonical coding, and conformer generation; the engine behind DataWarrior. `java` `javascript`
- [Indigo](https://lifescience.opensource.epam.com/indigo/) — Toolkit focused on correct handling of stereochemistry, tautomers, and Markush structures, with a good reaction engine. `c++` `python` `java`
- [CDK — Chemistry Development Kit](https://cdk.github.io) — Long-running Java library for structure handling, descriptors, and fingerprints; still the backbone of many JVM pipelines. `java`
- [datamol](https://docs.datamol.io) — Ergonomic wrapper over RDKit that makes the common 80% of molecule handling a one-liner, with sane defaults for sanitisation and standardisation. `python`
- [SELFIES](https://github.com/aspuru-guzik-group/selfies) — String representation where every string is a valid molecule, which removes a whole class of failure from generative models. `python`
- [molvs / ChEMBL Structure Pipeline](https://github.com/chembl/ChEMBL_Structure_Pipeline) — Standardisation, salt stripping, charge normalisation, and tautomer canonicalisation as ChEMBL itself applies them. `python`

## File Formats & Interoperability

- [InChI](https://www.inchi-trust.org) — IUPAC's canonical structure identifier and its hash, InChIKey; the closest thing chemistry has to a primary key. `standard` `c`
- [SMILES / OpenSMILES specification](http://opensmiles.org) — The open specification for the line notation everything else builds on. `standard`
- [CIF and Chemical Markup Language (CML)](https://www.xml-cml.org) — XML schema for chemical data with rich metadata; verbose, but survives archiving better than ad-hoc formats. `standard` `xml`
- [PDBx/mmCIF tools — `gemmi`](https://gemmi.readthedocs.io) — Fast library for macromolecular structure files, maps, and symmetry; useful whenever small molecules meet protein structures. `c++` `python`
- [Open Reaction Database schema](https://github.com/open-reaction-database/ord-schema) — Protocol-buffer schema for reaction records including conditions, workup, and analytical data. `python` `protobuf`

## Cheminformatics Pipelines & Workflow Tools

- [KNIME Analytics Platform](https://www.knime.com) — Visual workflow environment; the community and Vernalis extensions make it a full cheminformatics stack without writing code. Free desktop version. `gui` `java` `commercial-free-tier`
- [KNIME RDKit nodes](https://github.com/rdkit/knime-rdkit) — Official RDKit node collection for KNIME: substructure filters, descriptor calculation, diversity picking, R-group decomposition. `knime`
- [Galaxy ChemicalToolBox](https://github.com/bgruening/galaxytools) — Cheminformatics and docking tools packaged for the Galaxy platform, with reproducible histories and no local installation. `galaxy` `web`
- [Snakemake](https://snakemake.readthedocs.io) — Rule-based workflow engine that scales the same file from laptop to cluster; our own pipelines use it. `python` `workflow`
- [Nextflow](https://www.nextflow.io) — Dataflow workflow language with strong container and cloud support, dominant in bio-adjacent pipelines. `groovy` `workflow`
- [Luigi / Prefect for chemistry pipelines](https://github.com/PrefectHQ/prefect) — General task orchestration when your pipeline needs retries, scheduling, and observability more than it needs bioinformatics conventions. `python`

## Descriptors & Fingerprints

- [Mordred](https://github.com/mordred-descriptor/mordred) — Calculates ~1800 2D and 3D molecular descriptors, with clear provenance for each definition. `python`
- [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) — 1875 descriptors and 12 fingerprint types via CDK, scriptable from the command line. `java` `cli`
- [Mol2vec](https://github.com/samoturk/mol2vec) — Unsupervised embeddings of substructures, trained word2vec-style, as a drop-in alternative to fingerprints. `python`
- [MAP4 / MHFP](https://github.com/reymond-group/map4) — MinHashed atom-pair fingerprints that behave well for very large and very small molecules alike. `python`
- [CATS pharmacophore descriptors in `CATS2D`](https://github.com/dahvida/CATS2D) — Topological pharmacophore descriptors for scaffold hopping, where ECFP similarity is too literal. `python`

## QSAR / QSPR

- [DeepChem](https://deepchem.io) — Batteries-included library for molecular ML: featurisers, splitters, model zoo, and the MoleculeNet loaders. `python` `tensorflow` `pytorch`
- [QSARtuna](https://github.com/MolecularAI/QSARtuna) — Automated QSAR model building with hyperparameter search, uncertainty estimation, and reproducible model cards, from AstraZeneca. `python`
- [DCEKit](https://github.com/hkaneko1985/dcekit) — Data chemometrics toolkit including applicability-domain methods for deciding when a QSAR prediction should be trusted. `python`
- [OECD QSAR Toolbox](https://qsartoolbox.org) — Read-across, category formation, and regulatory-grade QSAR workflows; free registration, used for REACH dossiers. `gui` `regulatory`
- [VEGA QSAR](https://www.vegahub.eu) — Free platform of validated QSAR models for toxicity and environmental endpoints, each reporting applicability domain and reliability. `gui` `java` `regulatory`
- [scikit-mol](https://github.com/EBjerrum/scikit-mol) — RDKit featurisers as scikit-learn transformers so molecules drop straight into a `Pipeline` with proper cross-validation. `python`

## Machine Learning for Chemistry

- [Chemprop](https://chemprop.readthedocs.io) — Directed message-passing neural networks for property prediction; a strong, well-documented baseline that's hard to beat on small datasets. `python` `pytorch`
- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io) — Graph neural network primitives and dataset loaders, the substrate under most custom molecular GNNs. `python` `pytorch`
- [DGL-LifeSci](https://lifesci.dgl.ai) — Deep Graph Library models for molecules and proteins, with pretrained weights for common endpoints. `python`
- [MACE](https://github.com/ACEsuit/mace) — Equivariant machine-learning interatomic potentials achieving near-DFT accuracy for energies and forces at MD cost. `python` `pytorch`
- [SchNetPack](https://github.com/atomistic-machine-learning/schnetpack) — Toolbox for continuous-filter convolutional networks on atomistic systems, with training and MD integration. `python`
- [REINVENT](https://github.com/MolecularAI/REINVENT4) — Generative molecular design with reinforcement learning and scoring components for multi-parameter optimisation. `python`
- [GuacaMol](https://github.com/BenevolentAI/guacamol) — Benchmark suite for de novo design, with goal-directed and distribution-learning tasks so generative claims are comparable. `python` `benchmark`
- [Uncertainty toolbox for molecular models](https://github.com/uncertainty-toolbox/uncertainty-toolbox) — Calibration metrics and recalibration methods, because a molecular property prediction without an error bar isn't a measurement. `python`

## Reaction Prediction & Retrosynthesis

- [AiZynthFinder](https://github.com/MolecularAI/aizynthfinder) — Monte-Carlo tree search retrosynthesis with template extraction and stock-compound termination; runs on a laptop. `python`
- [ASKCOS](https://github.com/ASKCOS/askcos-core) — MIT's synthesis planning suite: forward prediction, retrosynthesis, condition recommendation, and reaction feasibility. `python` `web`
- [rxnmapper](https://github.com/rxn4chemistry/rxnmapper) — Atom-mapping from a transformer's attention weights, fast and surprisingly accurate without templates. `python`
- [RXNMapper / IBM RXN models](https://github.com/rxn4chemistry) — Sequence-to-sequence models for forward reaction prediction and retrosynthesis over SMILES. `python`
- [Reaction Decoder Tool (RDT)](https://github.com/asad/ReactionDecoder) — Atom-atom mapping and reaction classification from first principles rather than learned templates. `java`
- [RDChiral](https://github.com/connorcoley/rdchiral) — Correct application of retrosynthetic templates with chirality preserved; the piece most naive template code gets wrong. `python`

## Molecular Simulation & Quantum Chemistry

- [Psi4](https://psicode.org) — Modern open quantum chemistry package (DFT, MP2, coupled cluster) with a clean Python API for scripted workflows. `c++` `python`
- [PySCF](https://pyscf.org) — Quantum chemistry as a Python library rather than an input-file program; ideal for method development and embedding in pipelines. `python`
- [xtb](https://github.com/grimme-lab/xtb) — Semi-empirical tight-binding methods (GFN1/GFN2) giving usable geometries and energies orders of magnitude faster than DFT. `fortran` `cli`
- [CREST](https://github.com/crest-lab/crest) — Conformer and rotamer ensemble sampling driven by xtb; the standard first step before any DFT refinement. `fortran` `cli`
- [OpenMM](https://openmm.org) — GPU-accelerated molecular dynamics with a Python API and custom force expressions, usable as a library inside larger workflows. `python` `c++` `gpu`
- [ORCA (free for academic use)](https://orcaforum.kofo.mpg.de) — Comprehensive quantum chemistry program, free to academics after registration; strong for spectroscopy and transition metals. `commercial-free-tier`
- [ASE — Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase/) — Python interface that drives dozens of calculators with one API, so you can swap xtb for DFT without rewriting the script. `python`

## Chemical Databases

- [PubChem](https://pubchem.ncbi.nlm.nih.gov) — ~120 million compounds with bioassay data, safety information, and a well-documented REST API (PUG-REST). Public domain. `database` `api`
- [ChEMBL](https://www.ebi.ac.uk/chembl/) — Manually curated bioactivity data from the medicinal chemistry literature, with measured activities against defined targets. CC BY-SA. `database` `api`
- [ZINC22](https://cartblanche22.docking.org) — Billions of purchasable compounds in 3D, ready for docking, filterable by vendor and lead-likeness. `database`
- [Crystallography Open Database](https://www.crystallography.net/cod/) — Open collection of ~500 000 experimental crystal structures of small molecules and minerals. `database` `public-domain`
- [DrugBank (open data subset)](https://go.drugbank.com/releases/latest#open-data) — Approved drug names, identifiers, and structures under CC0; the full dataset needs a licence. `database` `commercial-free-tier`
- [SureChEMBL](https://www.surechembl.org) — Chemistry extracted from patents, updated continuously; where compounds appear years before the literature. `database`
- [Open Reaction Database](https://open-reaction-database.org) — Community reaction dataset with structured conditions and yields, designed to be machine-readable from the start. `database` `api`
- [NIST WebBook](https://webbook.nist.gov/chemistry) — Thermochemical and spectroscopic reference data with clear provenance for each measurement. `database`
- [COCONUT](https://coconut.naturalproducts.net) — Aggregated open natural-product structures from 50+ sources, deduplicated and annotated. `database`

## Visualisation

- [3Dmol.js](https://3dmol.csb.pitt.edu) — WebGL molecular viewer that embeds in any page with a few lines of JavaScript; ideal for teaching pages and notebooks. `javascript` `web`
- [NGL Viewer / nglview](https://github.com/nglviewer/nglview) — High-performance structure viewer with a Jupyter widget, good for large biomolecular assemblies. `javascript` `python` `jupyter`
- [PyMOL (open-source build)](https://github.com/schrodinger/pymol-open-source) — The community build of PyMOL: publication-quality rendering, scriptable in Python. `python` `c`
- [Mol*](https://molstar.org) — The viewer now behind RCSB PDB and PDBe; handles very large structures and volumetric data in the browser. `typescript` `web`
- [Avogadro 2](https://two.avogadro.cc) — Cross-platform molecular editor and visualiser with builder tools and interfaces to quantum chemistry packages. `c++` `gui`
- [DataWarrior](https://openmolecules.org/datawarrior/) — Free chemical data visualisation and analysis: scatter plots linked to structures, SAR tables, clustering. Underrated. `java` `gui`
- [py3Dmol](https://pypi.org/project/py3Dmol/) — Thin Python wrapper putting 3Dmol.js views straight into Jupyter cells. `python` `jupyter`
- [molplotly](https://github.com/wjm41/molplotly) — Adds structure tooltips to Plotly scatter plots, which turns any embedding plot into an explorable chemical space. `python`

## Benchmarks & Evaluation

- [MoleculeNet](https://moleculenet.org) — The standard benchmark collection for molecular property prediction, with recommended splits. `benchmark` `dataset`
- [Therapeutics Data Commons](https://tdcommons.ai) — Curated ML tasks across ADMET, HTS, and synthesis, with leaderboards and consistent splits. `benchmark` `python`
- [Polaris](https://polarishub.io) — Benchmark platform emphasising realistic splits and error analysis over leaderboard chasing. `benchmark` `python`
- [Dataset splitting strategies (RDKit Discussions)](https://github.com/rdkit/rdkit/discussions) — Not a package but a recurring discussion worth reading: random splits inflate molecular ML results, scaffold and temporal splits show whether a model generalises. `methodology`

## Learning Resources

- [Getting Started with the RDKit in Python](https://www.rdkit.org/docs/GettingStartedInPython.html) — The official tutorial; still the fastest path from zero to useful. `tutorial` `free`
- [Practical Cheminformatics with Open Source Software](https://github.com/PatWalters/practical_cheminformatics_tutorials) — Pat Walters' notebook series on the tasks people actually do: clustering, SAR, model building, and their pitfalls. `notebooks` `free`
- [TeachOpenCADD](https://projects.volkamerlab.org/teachopencadd/) — Structured talktorials covering compound data acquisition, filtering, docking, and ML, all runnable. `notebooks` `course`
- [Deep Learning for Molecules and Materials](https://dmol.pub) — Free online book with runnable code, from linear regression to equivariant networks. `book` `free`
- [Cheminformatics OLCC course materials](https://chem.libretexts.org) — Full open course on cheminformatics fundamentals, from a multi-university collaboration. `course` `free`
- [Is Life Worth Living? — Pat Walters' blog](http://practicalcheminformatics.blogspot.com) — Long-running blog on evaluation, benchmarks, and why a published model may not work on your data. `blog`

## Community

- [RDKit UGM](https://github.com/rdkit/UGM_Hackathon) — Annual user group meeting; slides and hackathon notebooks are posted publicly every year. `conference`
- [RDKit Discussions](https://github.com/rdkit/rdkit/discussions) — Where the maintainers answer; searchable and consistently high quality. `forum`
- [Open Molecular Software Foundation](https://omsf.io) — Nonprofit supporting open molecular science projects including OpenFF and OpenMM. `community`
- [Blue Obelisk movement](https://blueobelisk.github.io) — The long-running open chemistry data and standards community; much of the format work above traces here. `community`

## Related Lists

- [awesome-chemical-engineering](https://github.com/open-cheme-hub/awesome-chemical-engineering) — Process simulation and thermodynamics.
- [awesome-bioengineering](https://github.com/open-cheme-hub/awesome-bioengineering) — Metabolic models and synthetic biology.
- [workflows](https://github.com/open-cheme-hub/workflows) — A runnable RDKit conformer pipeline using several tools listed here.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own
licences.
