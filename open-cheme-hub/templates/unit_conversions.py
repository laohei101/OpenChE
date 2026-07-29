#!/usr/bin/env python3
"""Unit conversions for chemical engineering calculations.

Purpose
-------
A dependency-free conversion layer for the units that show up in process work:
flows, pressures, temperatures, viscosities, heat transfer coefficients, and the
dimensionless groups you build from them. Written so you can copy this single
file into a project that isn't allowed to install packages.

If you *can* install packages, use `pint` instead -- it tracks dimensions
through your whole calculation rather than only at the boundaries, which catches
a class of error this module cannot. See:
https://pint.readthedocs.io

Author   : Open ChemE Hub contributors
Licence  : MIT
Depends  : Python 3.9+ standard library only (numpy optional, for arrays)

What to change first
--------------------
Nothing -- this is a library. Import it, or run `python unit_conversions.py` to
execute the self-test at the bottom. Add your own factors to the tables in the
FACTORS dict; the converter picks them up automatically.

Convention
----------
Every factor converts *to the SI base unit for that quantity*. Conversion from
A to B is therefore: value * factor[A] / factor[B]. Temperature is handled
separately because it is affine, not linear.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable

__all__ = [
    "convert",
    "convert_temperature",
    "available_units",
    "reynolds",
    "prandtl",
    "nusselt_dittus_boelter",
    "molar_flow_from_mass_flow",
    "standard_volumetric_to_molar",
    "R_GAS",
]

# --------------------------------------------------------------------------
# Physical constants (CODATA 2018)
# --------------------------------------------------------------------------

R_GAS = 8.314462618  # J/(mol*K) -- universal gas constant
G_STANDARD = 9.80665  # m/s^2 -- standard gravity
ATM = 101325.0  # Pa -- standard atmosphere
T_ZERO_C = 273.15  # K -- ice point

# --------------------------------------------------------------------------
# Conversion factors, grouped by physical quantity.
# Each value is "how many SI base units is one of these".
# --------------------------------------------------------------------------

FACTORS: Dict[str, Dict[str, float]] = {
    # ---- length -> metre -------------------------------------------------
    "length": {
        "m": 1.0,
        "km": 1000.0,
        "cm": 0.01,
        "mm": 1e-3,
        "um": 1e-6,
        "micron": 1e-6,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mile": 1609.344,
    },
    # ---- mass -> kilogram ------------------------------------------------
    "mass": {
        "kg": 1.0,
        "g": 1e-3,
        "mg": 1e-6,
        "tonne": 1000.0,
        "t": 1000.0,
        "lb": 0.45359237,
        "lbm": 0.45359237,
        "oz": 0.028349523125,
        "ton_us": 907.18474,  # short ton
        "ton_uk": 1016.0469088,  # long ton
    },
    # ---- volume -> cubic metre ------------------------------------------
    "volume": {
        "m3": 1.0,
        "L": 1e-3,
        "l": 1e-3,
        "mL": 1e-6,
        "cm3": 1e-6,
        "ft3": 0.028316846592,
        "in3": 1.6387064e-5,
        "gal_us": 3.785411784e-3,
        "gal_uk": 4.54609e-3,
        "bbl": 0.158987294928,  # oil barrel, 42 US gal
    },
    # ---- pressure -> pascal ---------------------------------------------
    # NOTE: these are ABSOLUTE pressures. Gauge pressures (psig, barg) need
    # an offset -- use gauge_to_absolute() rather than a factor.
    "pressure": {
        "Pa": 1.0,
        "kPa": 1e3,
        "MPa": 1e6,
        "bar": 1e5,
        "mbar": 100.0,
        "atm": ATM,
        "psi": 6894.757293168,
        "psia": 6894.757293168,
        "torr": 133.322368421,
        "mmHg": 133.322368421,
        "inHg": 3386.389,
        "mmH2O": 9.80665,
        "inH2O": 249.0889,
        "kgf/cm2": 98066.5,
    },
    # ---- energy -> joule -------------------------------------------------
    "energy": {
        "J": 1.0,
        "kJ": 1e3,
        "MJ": 1e6,
        "GJ": 1e9,
        "cal": 4.184,
        "kcal": 4184.0,
        "BTU": 1055.05585262,
        "MMBTU": 1.05505585262e9,
        "kWh": 3.6e6,
        "MWh": 3.6e9,
        "eV": 1.602176634e-19,
    },
    # ---- power -> watt ---------------------------------------------------
    "power": {
        "W": 1.0,
        "kW": 1e3,
        "MW": 1e6,
        "hp": 745.6998715823,  # mechanical horsepower
        "BTU/h": 0.29307107,
        "MMBTU/h": 293071.07,
        "cal/s": 4.184,
        "ton_refrigeration": 3516.8528,
    },
    # ---- dynamic viscosity -> Pa*s --------------------------------------
    "viscosity": {
        "Pa.s": 1.0,
        "mPa.s": 1e-3,
        "cP": 1e-3,
        "P": 0.1,  # poise
        "lb/(ft.s)": 1.488163944,
        "lb/(ft.h)": 4.133789e-4,
    },
    # ---- kinematic viscosity -> m^2/s -----------------------------------
    "kinematic_viscosity": {
        "m2/s": 1.0,
        "cSt": 1e-6,
        "St": 1e-4,
        "ft2/s": 0.09290304,
    },
    # ---- mass flow -> kg/s ----------------------------------------------
    "mass_flow": {
        "kg/s": 1.0,
        "kg/h": 1 / 3600.0,
        "kg/min": 1 / 60.0,
        "g/s": 1e-3,
        "t/h": 1000.0 / 3600.0,
        "t/d": 1000.0 / 86400.0,
        "lb/s": 0.45359237,
        "lb/h": 0.45359237 / 3600.0,
        "klb/h": 453.59237 / 3600.0,
    },
    # ---- volumetric flow -> m^3/s ---------------------------------------
    "volume_flow": {
        "m3/s": 1.0,
        "m3/h": 1 / 3600.0,
        "L/s": 1e-3,
        "L/min": 1e-3 / 60.0,
        "L/h": 1e-3 / 3600.0,
        "ft3/s": 0.028316846592,
        "ft3/min": 0.028316846592 / 60.0,  # cfm
        "cfm": 0.028316846592 / 60.0,
        "gpm": 3.785411784e-3 / 60.0,  # US gallons per minute
        "bbl/d": 0.158987294928 / 86400.0,
    },
    # ---- molar flow -> mol/s --------------------------------------------
    "molar_flow": {
        "mol/s": 1.0,
        "mol/h": 1 / 3600.0,
        "kmol/s": 1000.0,
        "kmol/h": 1000.0 / 3600.0,
        "lbmol/h": 453.59237 / 3600.0,
    },
    # ---- density -> kg/m^3 ----------------------------------------------
    "density": {
        "kg/m3": 1.0,
        "g/cm3": 1000.0,
        "g/mL": 1000.0,
        "kg/L": 1000.0,
        "lb/ft3": 16.018463374,
        "lb/gal_us": 119.826427,
    },
    # ---- heat transfer coefficient -> W/(m^2*K) -------------------------
    "htc": {
        "W/(m2.K)": 1.0,
        "kW/(m2.K)": 1e3,
        "cal/(s.cm2.K)": 41840.0,
        "BTU/(h.ft2.F)": 5.678263398,
    },
    # ---- thermal conductivity -> W/(m*K) --------------------------------
    "conductivity": {
        "W/(m.K)": 1.0,
        "kW/(m.K)": 1e3,
        "BTU/(h.ft.F)": 1.730734666,
        "cal/(s.cm.K)": 418.4,
    },
    # ---- specific heat -> J/(kg*K) --------------------------------------
    "specific_heat": {
        "J/(kg.K)": 1.0,
        "kJ/(kg.K)": 1e3,
        "cal/(g.K)": 4184.0,
        "BTU/(lb.F)": 4186.8,
    },
    # ---- surface tension -> N/m -----------------------------------------
    "surface_tension": {
        "N/m": 1.0,
        "mN/m": 1e-3,
        "dyn/cm": 1e-3,
    },
    # ---- area -> m^2 -----------------------------------------------------
    "area": {
        "m2": 1.0,
        "cm2": 1e-4,
        "mm2": 1e-6,
        "ft2": 0.09290304,
        "in2": 6.4516e-4,
        "acre": 4046.8564224,
        "hectare": 1e4,
    },
    # ---- time -> second --------------------------------------------------
    "time": {
        "s": 1.0,
        "min": 60.0,
        "h": 3600.0,
        "d": 86400.0,
        "week": 604800.0,
        "year": 31557600.0,  # Julian year
    },
}


# --------------------------------------------------------------------------
# Core conversion
# --------------------------------------------------------------------------


def _find_quantity(unit: str) -> str:
    """Return the quantity table containing `unit`, or raise."""
    matches = [q for q, table in FACTORS.items() if unit in table]
    if not matches:
        raise KeyError(
            f"Unknown unit {unit!r}. Call available_units() to list what is defined, "
            f"or add it to the FACTORS table."
        )
    # A unit string is deliberately unique across tables; if it ever isn't,
    # this raises rather than silently picking one.
    if len(matches) > 1:
        raise KeyError(f"Ambiguous unit {unit!r}: defined in {matches}")
    return matches[0]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert `value` from `from_unit` to `to_unit`.

    Both units must belong to the same physical quantity -- converting kg/h to
    m3/h is refused, because that needs a density and this function does not
    know one. Use molar_flow_from_mass_flow() and friends for those.

    Temperature is affine, so it is not handled here; use convert_temperature().

    Parameters
    ----------
    value : float
        Magnitude in `from_unit`.
    from_unit, to_unit : str
        Unit strings as they appear in FACTORS, e.g. "kg/h", "lb/h".

    Returns
    -------
    float
        Magnitude in `to_unit`.

    Examples
    --------
    >>> round(convert(1000.0, "kg/h", "lb/h"), 1)
    2204.6
    >>> round(convert(14.696, "psi", "bar"), 4)
    1.0133
    """
    if from_unit in ("K", "degC", "degF", "degR") or to_unit in ("K", "degC", "degF", "degR"):
        raise ValueError(
            "Temperature is an affine scale -- use convert_temperature() instead. "
            "For temperature *differences*, note 1 degC = 1 K and 1 degF = 1 degR."
        )

    q_from = _find_quantity(from_unit)
    q_to = _find_quantity(to_unit)
    if q_from != q_to:
        raise ValueError(
            f"Cannot convert {from_unit!r} ({q_from}) to {to_unit!r} ({q_to}): "
            f"different physical quantities."
        )
    return value * FACTORS[q_from][from_unit] / FACTORS[q_to][to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert an absolute temperature between K, degC, degF, and degR.

    For a temperature *difference*, do not use this -- a 10 degC rise is a 10 K
    rise, and an 18 degF rise, not whatever this returns.

    Examples
    --------
    >>> convert_temperature(25.0, "degC", "K")
    298.15
    >>> round(convert_temperature(212.0, "degF", "degC"), 6)
    100.0
    """
    to_kelvin = {
        "K": lambda t: t,
        "degC": lambda t: t + T_ZERO_C,
        "degF": lambda t: (t - 32.0) * 5.0 / 9.0 + T_ZERO_C,
        "degR": lambda t: t * 5.0 / 9.0,
    }
    from_kelvin = {
        "K": lambda t: t,
        "degC": lambda t: t - T_ZERO_C,
        "degF": lambda t: (t - T_ZERO_C) * 9.0 / 5.0 + 32.0,
        "degR": lambda t: t * 9.0 / 5.0,
    }
    if from_unit not in to_kelvin:
        raise KeyError(f"Unknown temperature unit {from_unit!r}; use K, degC, degF, or degR.")
    if to_unit not in from_kelvin:
        raise KeyError(f"Unknown temperature unit {to_unit!r}; use K, degC, degF, or degR.")

    kelvin = to_kelvin[from_unit](value)
    if kelvin < 0.0:
        raise ValueError(f"{value} {from_unit} is below absolute zero ({kelvin:.3f} K).")
    return from_kelvin[to_unit](kelvin)


def gauge_to_absolute(p_gauge: float, unit: str, p_atm_pa: float = ATM) -> float:
    """Convert a gauge pressure to absolute, in the same unit.

    Barometric pressure defaults to one standard atmosphere. On a real site,
    pass the measured value -- at 1500 m elevation the difference is about
    2.4 psi, which is enough to matter in a relief calculation.

    Examples
    --------
    >>> round(gauge_to_absolute(100.0, "psi"), 3)
    114.696
    """
    offset = convert(p_atm_pa, "Pa", unit)
    return p_gauge + offset


def absolute_to_gauge(p_abs: float, unit: str, p_atm_pa: float = ATM) -> float:
    """Convert an absolute pressure to gauge, in the same unit."""
    return p_abs - convert(p_atm_pa, "Pa", unit)


def available_units(quantity: str | None = None) -> Dict[str, Iterable[str]]:
    """List defined units, optionally for one quantity only.

    >>> "bar" in available_units("pressure")["pressure"]
    True
    """
    if quantity is None:
        return {q: sorted(table) for q, table in FACTORS.items()}
    if quantity not in FACTORS:
        raise KeyError(f"Unknown quantity {quantity!r}. Known: {sorted(FACTORS)}")
    return {quantity: sorted(FACTORS[quantity])}


# --------------------------------------------------------------------------
# Composition and flow relations that need physical properties
# --------------------------------------------------------------------------


def molar_flow_from_mass_flow(m_dot_kg_s: float, molar_mass_kg_kmol: float) -> float:
    """Mass flow (kg/s) -> molar flow (kmol/s) given molar mass in kg/kmol.

    Molar mass in kg/kmol is numerically equal to g/mol, which is how it is
    tabulated almost everywhere: water is 18.015.

    >>> round(molar_flow_from_mass_flow(1.0, 18.015), 6)
    0.055509
    """
    if molar_mass_kg_kmol <= 0:
        raise ValueError("Molar mass must be positive.")
    return m_dot_kg_s / molar_mass_kg_kmol


def standard_volumetric_to_molar(
    q_std_m3_s: float, t_std_k: float = 288.15, p_std_pa: float = ATM
) -> float:
    """Standard volumetric gas flow (m3/s) -> molar flow (mol/s), ideal gas.

    Beware: "standard conditions" is not one thing. This defaults to 15 degC
    and 1 atm (ISO 13443 / common gas industry usage). Others in circulation:

      - 0 degC, 1 atm      (IUPAC pre-1982 "normal", Nm3)
      - 20 degC, 1 atm     (many US vendors, "SCFM")
      - 60 degF, 14.696 psia (US oil and gas)

    A 15 degC vs 0 degC basis differs by about 5.5% in molar terms. Always
    state the basis next to the number.

    >>> round(standard_volumetric_to_molar(1.0), 2)
    42.29
    """
    return p_std_pa * q_std_m3_s / (R_GAS * t_std_k)


def mass_fraction_to_mole_fraction(
    mass_fractions: Dict[str, float], molar_masses: Dict[str, float]
) -> Dict[str, float]:
    """Convert a mass-fraction composition to mole fractions.

    Both dicts are keyed by component name; molar masses in kg/kmol (= g/mol).
    Mass fractions need not sum exactly to 1 -- they are normalised, and a sum
    more than 1% off raises, because that usually means a missing component.

    >>> mf = mass_fraction_to_mole_fraction(
    ...     {"water": 0.5, "ethanol": 0.5}, {"water": 18.015, "ethanol": 46.069}
    ... )
    >>> round(mf["water"], 4)
    0.7189
    """
    total = sum(mass_fractions.values())
    if not math.isclose(total, 1.0, rel_tol=0.01):
        raise ValueError(f"Mass fractions sum to {total:.4f}, not ~1.0 -- component missing?")

    moles = {c: w / molar_masses[c] for c, w in mass_fractions.items()}
    total_moles = sum(moles.values())
    return {c: n / total_moles for c, n in moles.items()}


# --------------------------------------------------------------------------
# Dimensionless groups -- SI in, dimensionless out
# --------------------------------------------------------------------------


def reynolds(rho: float, velocity: float, length: float, mu: float) -> float:
    """Reynolds number, Re = rho*v*L/mu. All arguments in SI.

    `length` is the characteristic dimension: pipe internal diameter for
    internal flow, impeller diameter for a stirred tank (with velocity as N*D),
    particle diameter for packed beds.

    >>> round(reynolds(rho=998.0, velocity=2.0, length=0.05, mu=1.002e-3), 0)
    99601.0
    """
    if mu <= 0:
        raise ValueError("Viscosity must be positive.")
    return rho * velocity * length / mu


def prandtl(cp: float, mu: float, k: float) -> float:
    """Prandtl number, Pr = cp*mu/k. SI units: J/(kg.K), Pa.s, W/(m.K).

    >>> round(prandtl(cp=4182.0, mu=1.002e-3, k=0.598), 2)
    7.01
    """
    if k <= 0:
        raise ValueError("Thermal conductivity must be positive.")
    return cp * mu / k


def nusselt_dittus_boelter(re: float, pr: float, heating: bool = True) -> float:
    """Dittus-Boelter correlation: Nu = 0.023 * Re^0.8 * Pr^n.

    n = 0.4 when the fluid is being heated, 0.3 when cooled. Validity, per the
    original work and every textbook since:

        Re > 10 000, 0.6 < Pr < 160, L/D > 10, small temperature difference,
        smooth tube, fully developed turbulent flow.

    Outside that envelope use Gnielinski, or Sieder-Tate if wall and bulk
    viscosities differ much. This function warns rather than refusing, because
    a screening calculation outside the range is still often what you want --
    just don't put it in a design basis.

    >>> round(nusselt_dittus_boelter(re=1e5, pr=7.0, heating=True), 1)
    500.9
    """
    if re < 1e4:
        print(f"  [warn] Re = {re:.3g} < 1e4: flow is not fully turbulent, correlation invalid.")
    if not 0.6 <= pr <= 160.0:
        print(f"  [warn] Pr = {pr:.3g} outside 0.6-160 validity range.")
    n = 0.4 if heating else 0.3
    return 0.023 * re**0.8 * pr**n


# --------------------------------------------------------------------------
# Self-test / demo
# --------------------------------------------------------------------------


def _demo() -> None:
    print("Unit conversions -- worked examples\n" + "=" * 44)

    print("\nFlows")
    print(f"  10 000 kg/h  = {convert(10_000, 'kg/h', 'lb/h'):>12,.1f} lb/h")
    print(f"  500 gpm      = {convert(500, 'gpm', 'm3/h'):>12,.2f} m3/h")
    print(f"  1 000 bbl/d  = {convert(1000, 'bbl/d', 'm3/h'):>12,.3f} m3/h")

    print("\nPressures")
    print(f"  150 psig     = {gauge_to_absolute(150, 'psi'):>12,.2f} psia")
    print(f"  10 barg      = {convert(gauge_to_absolute(10, 'bar'), 'bar', 'kPa'):>12,.1f} kPa abs")
    print(f"  760 mmHg     = {convert(760, 'mmHg', 'atm'):>12,.4f} atm")

    print("\nTemperatures")
    for t_c in (-40.0, 0.0, 25.0, 100.0):
        t_f = convert_temperature(t_c, "degC", "degF")
        t_k = convert_temperature(t_c, "degC", "K")
        print(f"  {t_c:>7.1f} degC = {t_f:>8.1f} degF = {t_k:>8.2f} K")

    print("\nEnergy and duty")
    print(f"  1 MMBTU/h    = {convert(1, 'MMBTU/h', 'kW'):>12,.1f} kW")
    print(f"  500 kW       = {convert(500, 'kW', 'BTU/h'):>12,.0f} BTU/h")

    print("\nComposition: 50/50 by mass water + ethanol")
    x = mass_fraction_to_mole_fraction(
        {"water": 0.5, "ethanol": 0.5}, {"water": 18.015, "ethanol": 46.069}
    )
    for comp, frac in x.items():
        print(f"  x_{comp:<8s} = {frac:.4f}")

    print("\nDimensionless groups: water at 20 degC, 2 m/s in a 50 mm pipe")
    rho, mu, cp, k = 998.2, 1.002e-3, 4182.0, 0.598
    re = reynolds(rho, 2.0, 0.05, mu)
    pr = prandtl(cp, mu, k)
    nu = nusselt_dittus_boelter(re, pr, heating=True)
    h = nu * k / 0.05
    print(f"  Re = {re:>12,.0f}")
    print(f"  Pr = {pr:>12.2f}")
    print(f"  Nu = {nu:>12.1f}   (Dittus-Boelter, heating)")
    print(f"  h  = {h:>12,.0f} W/(m2.K)  = {convert(h, 'W/(m2.K)', 'BTU/(h.ft2.F)'):,.1f} BTU/(h.ft2.F)")

    print("\nGas flow: 1 000 Sm3/h at 15 degC, 1 atm")
    n_dot = standard_volumetric_to_molar(convert(1000, "m3/h", "m3/s"))
    print(f"  = {n_dot:.3f} mol/s = {n_dot * 3.6:.2f} kmol/h")

    print("\nSanity checks")
    checks = [
        ("1 atm -> psi", convert(1, "atm", "psi"), 14.6959),
        ("1 m3/h -> gpm", convert(1, "m3/h", "gpm"), 4.40287),
        ("1 cP -> Pa.s", convert(1, "cP", "Pa.s"), 0.001),
        ("100 degC -> degF", convert_temperature(100, "degC", "degF"), 212.0),
        ("1 kWh -> MJ", convert(1, "kWh", "MJ"), 3.6),
    ]
    for label, got, expected in checks:
        ok = "OK  " if math.isclose(got, expected, rel_tol=1e-4) else "FAIL"
        print(f"  [{ok}] {label:<20s} got {got:<12.6g} expected {expected:<12.6g}")


if __name__ == "__main__":
    _demo()
