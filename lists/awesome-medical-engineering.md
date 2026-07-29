<!--
  GENERATED FILE — DO NOT EDIT.

  Produced by scripts/generate_markdown_lists.py from the canonical records in
  catalog/resources/. Edit the YAML and re-run the generator; a hand edit here
  is overwritten on the next build and fails CI in the meantime.
-->

# Awesome Medical Engineering [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

> Open tools and references for medical device design, biomechanics, medical imaging, regulatory affairs, clinical engineering, and health informatics.

**80 entries.** Every entry is free to use. Descriptions say what a tool *does*, not how good it is.

Entries carry a verification marker only when something was actually checked — see [verification methodology](../docs/verification-methodology.md). An entry with no marker has not been independently verified.

**Contributions welcome** — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Contents

- [Medical Device Design & Development](#medical-device-design--development)
- [Biomechanics](#biomechanics)
- [Medical Imaging](#medical-imaging)
- [Physiological Modelling & Signals](#physiological-modelling--signals)
- [Regulatory & Standards](#regulatory--standards)
- [Quality Systems & Risk Management](#quality-systems--risk-management)
- [Clinical Engineering](#clinical-engineering)
- [Health Informatics & Interoperability](#health-informatics--interoperability)
- [Datasets](#datasets)
- [Learning Resources](#learning-resources)
- [Community & Conferences](#community--conferences)
- [Related Lists](#related-lists)

---

## Medical Device Design & Development

- [FreeCAD](https://www.freecad.org) — Parametric 3D CAD with a proper feature tree, assembly workbench, FEM workbench, and complete Python scripting. The realistic open alternative to SolidWorks for mechanical work. `c++` `python` `gui`
- [KiCad](https://www.kicad.org) — Schematic capture, PCB layout, and manufacturing outputs, with a strong scripting API and no seat limits. `gui` `electronics`
- [Open Source Hardware Association (OSHWA)](https://www.oshwa.org) — Certification programme and directory for open hardware, including documented medical and laboratory devices. `hardware` `community`
- [Open Source Ventilator resources (MIT E-Vent)](https://e-vent.mit.edu) — Design documentation, testing protocols, and clinical requirements published during the 2020 ventilator effort; a rare public record of medical device development under pressure. `documentation` `hardware`
- [OpenAPS / AndroidAPS reference documentation](https://openaps.org) — The best-documented example of a patient-built closed-loop system, including its explicit safety reasoning. Not an approved device. `documentation` `community`
- [OpenSCAD](https://openscad.org) — Constructive solid geometry defined in code, so parts are diffable, reviewable, and parametric by construction. `cli` `gui`

## Biomechanics

- [Biomechanical ToolKit (BTK)](https://github.com/Biomechanical-ToolKit/BTKCore) — Reads and processes motion capture data in C3D and other gait-lab formats. `c++` `python`
- [Bonemat](https://www.bonemat.org) — Maps CT-derived bone density onto finite element meshes so subject-specific bone models use real material properties. `gui` `fea`
- [FEBio](https://febio.org) — Finite element solver purpose-built for biological materials: hyperelasticity, poroelasticity, growth and remodelling. `c++` `fea`
- [Gibbon](https://www.gibboncode.org) — MATLAB toolbox for computational biomechanics: meshing, FEBio interfacing, and image-based model generation. `matlab`
- [OpenSim](https://opensim.stanford.edu) — Musculoskeletal modelling and simulation: inverse kinematics, inverse dynamics, static optimisation, and forward simulation of movement. The field standard. `c++` `matlab` `python` `gui`
- [Pose2Sim](https://github.com/perfanalytics/pose2sim) — Markerless motion capture from ordinary video into OpenSim-ready kinematics, using multi-view pose estimation. `python`
- [PyDy](https://www.pydy.org) — Multibody dynamics from symbolic equations of motion via SymPy; useful for prosthetics and exoskeleton design studies. `python`
- [SimTK](https://simtk.org) — The project host for OpenSim and dozens of other biomechanics and biosimulation projects, with shared model repositories. `platform`

## Medical Imaging

- [3D Slicer](https://www.slicer.org) — Comprehensive platform for image visualisation, segmentation, registration, and image-guided procedures, extensible in Python. `c++` `python` `gui`
- [3D Slicer alternatives — MITK](https://www.mitk.org) — Medical imaging interaction toolkit with a strong plugin architecture for building clinical prototypes. `c++` `gui`
- [dcm4che](https://www.dcm4che.org) — Full DICOM implementation: toolkit, PACS archive, and command-line utilities for anything DICOM-shaped. `java` `dicom`
- [DICOM de-identification — CTP / deid](https://github.com/pydicom/deid) — Rule-based removal of protected health information from DICOM headers and burned-in pixel text. `python` `privacy`
- [ITK / SimpleITK](https://itk.org) — The insight toolkit: registration and segmentation algorithms underpinning much of the field, with a friendly SimpleITK API. `c++` `python`
- [ITK-SNAP](http://www.itksnap.org) — Focused, fast manual and semi-automatic segmentation tool; still what many people use to produce ground truth. `gui`
- [MONAI](https://monai.io) — PyTorch framework for medical imaging deep learning, with domain-specific transforms, networks, and evaluation. `python` `pytorch`
- [nnU-Net](https://github.com/MIC-DKFZ/nnUNet) — Self-configuring segmentation framework that remains a very strong baseline across modalities and anatomies. `python`
- [OHIF Viewer](https://ohif.org) — Zero-footprint web DICOM viewer, extensible, and the basis for many research imaging platforms. `javascript`
- [Orthanc](https://www.orthanc-server.com) — Lightweight, standalone DICOM server with a REST API; ideal for research PACS and de-identification pipelines. `c++` `dicom` `server`
- [pydicom](https://pydicom.github.io) — Reading, modifying, and writing DICOM files in Python; the practical starting point for any imaging script. `python` `dicom`
- [TotalSegmentator](https://github.com/wasserth/TotalSegmentator) — Segments 100+ anatomical structures in CT with one command; the fastest route from a scan to usable geometry. `python`

## Physiological Modelling & Signals

- [BioSPPy](https://github.com/scientisst/BioSPPy) — Biosignal processing toolbox covering filtering, segmentation, and standard feature sets. `python` `signals`
- [CellML and the Physiome Model Repository](https://models.physiomeproject.org) — Curated, executable models of physiological systems, from ion channels to whole organs. `standard` `database`
- [Chaste](https://chaste.github.io) — Cambridge's simulation library for cardiac electrophysiology and cell-based tissue models, with strong testing culture. `c++`
- [MNE-Python](https://mne.tools) — EEG and MEG analysis: preprocessing, source localisation, time-frequency, and statistics. `python` `eeg`
- [NeuroKit2](https://neuropsychology.github.io/NeuroKit/) — Processing and feature extraction for ECG, PPG, EDA, EMG, and respiration signals, with sane defaults and clear documentation. `python` `signals`
- [OpenCOR](https://opencor.ws) — Environment for editing and simulating CellML models without writing solver code. `c++` `gui`
- [WFDB Toolbox and wfdb-python](https://github.com/MIT-LCP/wfdb-python) — Reads PhysioNet waveform databases and implements the classic detection algorithms. `python` `signals`

## Regulatory & Standards

- [EU MDR 2017/745 full text (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2017/745/oj) — The regulation itself, in 24 languages, free. `regulatory` `free`
- [FDA 510(k) and De Novo databases](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm) — Searchable record of cleared devices and their summaries; the fastest way to find a predicate and see what evidence was accepted. `database` `regulatory`
- [FDA Guidance Documents database](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) — Every current FDA guidance, free. Start with "Content of Premarket Submissions for Device Software Functions". `regulatory` `free`
- [FDA Software as a Medical Device (SaMD) resources](https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd) — Framework and guidance for standalone software, including the AI/ML action plan. `regulatory` `free`
- [IEC 62304 — Medical device software lifecycle](https://www.iso.org/standard/38421.html) — The software lifecycle standard; purchase required, but the scope and structure are public and worth understanding before you write code. `standard`
- [ISO 10993 series — Biological evaluation](https://www.iso.org/standard/68936.html) — Biocompatibility testing framework for anything contacting the body. `standard`
- [ISO 13485 — Quality management systems](https://www.iso.org/standard/59752.html) — QMS requirements for device manufacturers. `standard`
- [ISO 14971 — Risk management for medical devices](https://www.iso.org/standard/72704.html) — The risk management standard everything else references. `standard`
- [MAUDE adverse event database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm) — Reported device failures and adverse events; read your device category's entries before designing, not after. `database`
- [MDCG guidance documents](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en) — Medical Device Coordination Group guidance interpreting the MDR, including MDCG 2019-11 on software qualification. `regulatory` `free`
- [openregulatory.com guides](https://openregulatory.com) — Free, plain-language walkthroughs of MDR, IEC 62304, and ISO 14971 with downloadable templates. Unusually readable. `guide` `free`

## Quality Systems & Risk Management

- [Doorstop](https://doorstop.readthedocs.io) — Requirements management in version-controlled text with automatic traceability matrices; requirements review becomes code review. `python` `requirements`
- [openregulatory templates](https://github.com/openregulatory/templates) — Markdown templates for the full technical documentation set: risk management file, software architecture, verification plans, usability engineering. `templates` `free` `regulatory`
- [SBOM tooling — syft / cyclonedx](https://github.com/anchore/syft) — Generates software bills of materials, now expected in FDA premarket cybersecurity documentation. `cli` `security`
- [Usability engineering per IEC 62366 — public summaries](https://www.iso.org/standard/63179.html) — Human factors process for devices; the FDA's separate human factors guidance is free and covers the same ground practically. `standard`

## Clinical Engineering

- [ECRI resources (selected free)](https://www.ecri.org) — Device safety alerts, hazard reports, and evaluation methodology; some material is free, most requires membership. `commercial-free-tier`
- [Health Technology Assessment toolkits (WHO)](https://www.who.int/health-technology-assessment) — Frameworks for deciding what equipment to buy and whether it is worth it. `guide` `free`
- [IEC 62353 — Recurrent test and test after repair](https://webstore.iec.ch/publication/6913) — Electrical safety testing requirements for medical electrical equipment already in service. `standard`
- [Open source medical equipment repair — iFixit Medical](https://www.ifixit.com/Device/Medical_Device) — Community service manuals and teardowns; the only public repository for some equipment. `community` `repair`
- [openMAINT](https://www.openmaint.org) — Open maintenance management: asset registry, preventive schedules, work orders. `java`
- [WHO medical device technical series](https://www.who.int/teams/health-product-policy-and-standards/assistive-and-medical-technology/medical-devices) — Free guidance on procurement, donation, maintenance, and health technology assessment, aimed at all resource settings. `guide` `free`

## Health Informatics & Interoperability

- [fhir.resources / fhirclient](https://github.com/nazrulworld/fhir.resources) — Python FHIR resource models with validation. `python`
- [HAPI FHIR](https://hapifhir.io) — Complete Java FHIR implementation with a reference server; the default way to prototype against FHIR. `java`
- [HL7 FHIR](https://www.hl7.org/fhir/) — The modern healthcare interoperability standard; specification is free and the resource model is genuinely usable. `standard` `api` `free`
- [Mirth Connect / OpenIntegrationEngine](https://github.com/openintegrationengine/engine) — Interface engine for HL7 v2 routing and transformation, which is still most of hospital integration work. `java` `integration`
- [OHDSI / OMOP Common Data Model](https://www.ohdsi.org) — Common data model and analytics stack for observational health research across institutions. `r` `sql` `standard`
- [OpenMRS](https://openmrs.org) — Open electronic medical record platform deployed widely in low-resource settings, with a large implementer community. `java` `platform`
- [SNOMED CT and LOINC browsers](https://loinc.org) — Terminology services for coding observations and clinical findings; LOINC is free, SNOMED CT is free in member countries. `terminology`
- [Synthea](https://synthetichealth.github.io/synthea/) — Generates realistic synthetic patient records with full longitudinal histories, in FHIR and CSV. No privacy risk. `java` `dataset`

## Datasets

- [Medical Segmentation Decathlon](http://medicaldecathlon.com) — Ten segmentation tasks across organs and modalities; the standard cross-task benchmark. `dataset` `benchmark`
- [OpenNeuro](https://openneuro.org) — Openly shared neuroimaging datasets in BIDS format. `dataset`
- [PhysioNet](https://physionet.org) — Waveform and clinical databases including MIMIC-IV, with credentialed access and clear data use agreements. `dataset`
- [The Cancer Imaging Archive (TCIA)](https://www.cancerimagingarchive.net) — Large de-identified imaging collections with linked clinical data. `dataset` `imaging`
- [UK Biobank imaging (application required)](https://www.ukbiobank.ac.uk) — Deep phenotyping at population scale, including imaging; access is reviewed, not open. `dataset`

## Learning Resources

- [FDA CDRH Learn](https://www.fda.gov/training-and-continuing-education/cdrh-learn) — The FDA's own free training modules on device submissions and requirements. `course` `free`
- [Introduction to Biomedical Engineering (LibreTexts)](https://eng.libretexts.org) — Open textbook covering biomechanics, biomaterials, and instrumentation. `book` `free`
- [MIT 2.75 Medical Device Design (OCW)](https://ocw.mit.edu/courses/2-75-medical-device-design-fall-2019/) — Full course on device design methodology, with real project examples. `course` `free`
- [MONAI bootcamp materials](https://github.com/Project-MONAI/tutorials) — Notebooks covering segmentation, classification, and deployment for medical imaging. `notebooks` `free`
- [openregulatory Medical Device Regulation crash courses](https://openregulatory.com/medical-device-regulation/) — What you need before your first regulatory meeting, free and short. `guide` `free`
- [OpenSim documentation and webinars](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/overview) — Tutorials from a first gait model to custom muscle actuators. `tutorial` `free`

## Community & Conferences

- [3D Slicer forum](https://discourse.slicer.org) — Extremely responsive community, including core developers. `forum`
- [AAMI](https://www.aami.org) — Association for the Advancement of Medical Instrumentation: standards, clinical engineering community, and certification. `community`
- [BMES Annual Meeting](https://www.bmes.org) — The main US biomedical engineering meeting. `conference`
- [EMBC — IEEE Engineering in Medicine and Biology Conference](https://www.embs.org) — Broad annual conference across instrumentation, imaging, and informatics. `conference`
- [MICCAI](http://www.miccai.org) — Medical image computing and computer-assisted intervention; the venue for imaging methods. `conference`
- [OHDSI community calls](https://www.ohdsi.org/community-calls/) — Weekly open calls on observational research methods and the OMOP model. `community`
- [RSNA](https://www.rsna.org) — Radiology's meeting, where imaging AI gets its clinical reality check. `conference`

## Related Lists

- [Awesome Bioengineering](awesome-bioengineering.md)
- [Awesome General Engineering](awesome-general-engineering.md)
- [Awesome Chemoinformatics](awesome-chemoinformatics.md)

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked projects retain their own licences.
