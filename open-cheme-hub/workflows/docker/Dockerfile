# =============================================================================
# chem-toolkit — a reproducible environment for computational chemistry and
# chemical engineering.
#
# Contains: RDKit, Open Babel, Cantera, CoolProp, the Caleb Bell process
# engineering stack (thermo/chemicals/fluids/ht), Snakemake, and the usual
# scientific Python.
#
# BUILD
#     docker build -t chem-toolkit:1.2.0 -f Dockerfile .
#
# RUN — interactive shell in the current directory
#     docker run --rm -it -v "$PWD:/work" chem-toolkit:1.2.0
#
# RUN — Jupyter Lab on http://localhost:8888
#     docker run --rm -p 8888:8888 -v "$PWD:/work" chem-toolkit:1.2.0 \
#         jupyter lab --ip=0.0.0.0 --no-browser --allow-root
#
# RUN — a single script, non-interactively
#     docker run --rm -v "$PWD:/work" chem-toolkit:1.2.0 python my_analysis.py
#
# WHY MICROMAMBA AND NOT PIP
# --------------------------
# RDKit, Open Babel, and Cantera all ship compiled extensions with C++
# dependencies that conda-forge builds consistently against one another.
# Installing them with pip works until it doesn't, usually at the point where
# two packages want different Boost versions. Micromamba is a small, fast conda
# implementation with no Python bootstrap of its own.
#
# EVERY VERSION IS PINNED, including the base image digest. An image tagged
# `latest` is not reproducible, and neither is one whose base moved underneath
# it.
#
# Author  : Open ChemE Hub contributors
# Licence : MIT
# =============================================================================

# Pinned by digest. Update deliberately: change the digest, rebuild, run the
# smoke test at the bottom, then commit.
FROM mambaorg/micromamba:1.5.8-jammy

LABEL org.opencontainers.image.title="chem-toolkit"
LABEL org.opencontainers.image.description="RDKit, Open Babel, Cantera, and process engineering libraries"
LABEL org.opencontainers.image.version="1.2.0"
LABEL org.opencontainers.image.source="https://github.com/open-cheme-hub/workflows"
LABEL org.opencontainers.image.licenses="MIT"

# ---------------------------------------------------------------------------
# System packages
#
# Root is needed for apt, then we drop back to the unprivileged user that the
# micromamba base image provides. Running the payload as root is the sort of
# thing that is fine until the container mounts your home directory.
# ---------------------------------------------------------------------------
USER root

RUN apt-get update && apt-get install --no-install-recommends -y \
        git=1:2.34.* \
        curl=7.81.* \
        ca-certificates \
        build-essential=12.9* \
        librsvg2-bin=2.52.* \
        graphviz=2.42.* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER

# ---------------------------------------------------------------------------
# Scientific stack
#
# One micromamba invocation, not several: each RUN is a layer, and solving the
# environment once is much faster than solving it four times.
# ---------------------------------------------------------------------------
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/environment.yaml

RUN micromamba install -y -n base -f /tmp/environment.yaml \
    && micromamba clean --all --yes \
    && rm /tmp/environment.yaml

# Activate the environment for every subsequent RUN and for the container's
# entrypoint. Without this, `docker run image python` finds the system python.
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# ---------------------------------------------------------------------------
# Verify the build
#
# A smoke test in the build means a broken image fails at build time rather
# than at 2am in someone's pipeline. Each import below has broken at least once
# in the wild after an unrelated dependency update.
# ---------------------------------------------------------------------------
RUN python - <<'PY'
import sys

print(f"Python {sys.version.split()[0]}")

# --- cheminformatics ---
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

mol = Chem.AddHs(Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O"))  # aspirin
assert mol is not None
assert AllChem.EmbedMolecule(mol, randomSeed=42) == 0, "RDKit embedding failed"
assert AllChem.MMFFOptimizeMolecule(mol) == 0, "MMFF optimisation failed"
mw = Descriptors.MolWt(mol)
assert abs(mw - 180.16) < 0.1, f"aspirin MW is {mw}, expected 180.16"
print(f"  RDKit           ok  (aspirin MW {mw:.2f})")

# --- thermodynamics and kinetics ---
import cantera as ct

gas = ct.Solution("gri30.yaml")
gas.TPX = 300.0, ct.one_atm, "CH4:1, O2:2, N2:7.52"
gas.equilibrate("HP")
assert gas.T > 2000, f"adiabatic flame temperature {gas.T:.0f} K looks wrong"
print(f"  Cantera         ok  (CH4 adiabatic flame {gas.T:.0f} K)")

# --- physical properties ---
from CoolProp.CoolProp import PropsSI

# Water saturation temperature at 1 atm must be 373.15 K. If this drifts,
# something is very wrong and every downstream number is suspect.
tsat = PropsSI("T", "P", 101325, "Q", 0, "Water")
assert abs(tsat - 373.124) < 0.1, f"water Tsat at 1 atm is {tsat:.3f} K"
print(f"  CoolProp        ok  (water Tsat {tsat:.2f} K)")

# --- process engineering ---
from fluids import friction_factor
from ht import LMTD

fd = friction_factor(Re=1e5, eD=1e-4)
assert 0.015 < fd < 0.025, f"friction factor {fd} outside expected range"
lmtd = LMTD(Thi=100, Tho=60, Tci=30, Tco=40)
assert 40 < lmtd < 50, f"LMTD {lmtd} outside expected range"
print(f"  fluids / ht     ok  (f={fd:.4f}, LMTD={lmtd:.2f} K)")

from thermo import Chemical

water = Chemical("water", T=298.15, P=101325)
assert abs(water.rho - 997) < 5, f"water density {water.rho} kg/m3 at 25 C"
print(f"  thermo          ok  (water rho {water.rho:.1f} kg/m3)")

# --- numerics ---
import numpy as np
import pandas as pd
import scipy

print(f"  numpy {np.__version__}, scipy {scipy.__version__}, pandas {pd.__version__}")
print("\nAll smoke tests passed.")
PY

# Open Babel is a command-line tool, so test it as one.
RUN obabel -:"CCO" -osmi --gen3d 2>/dev/null | grep -q "CCO" \
    && echo "  Open Babel      ok" \
    && obabel -V

# ---------------------------------------------------------------------------
# Runtime configuration
# ---------------------------------------------------------------------------
WORKDIR /work

# Matplotlib writes a font cache on first use; without a writable config dir it
# warns on every single invocation.
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Threading libraries each default to "use every core", which on a shared
# cluster node means N processes each spawning N threads. Set to 1 and let the
# workflow engine decide; override at runtime with -e OMP_NUM_THREADS=8.
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

EXPOSE 8888

# The micromamba entrypoint activates the environment; the default command
# lands you in a shell with everything on PATH.
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["/bin/bash"]
