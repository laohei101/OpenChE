#!/usr/bin/env python3
"""Reactor design skeleton: CSTR and PFR sizing for a liquid-phase reaction.

Purpose
-------
A working starting point for reactor sizing coursework and early-stage design.
It sets up one reaction, solves the CSTR design equation and integrates the PFR
design equation, compares the two volumes, and sweeps conversion so you can see
where each configuration wins.

The worked case is the saponification of ethyl acetate:

    CH3COOC2H5 + NaOH  ->  CH3COONa + C2H5OH        A + B -> C + D

second order overall, first order in each reactant, run in dilute aqueous
solution so density change is negligible. Kinetics are a literature-consistent
Arrhenius fit, not a measurement -- see KINETICS below.

Author   : Open ChemE Hub contributors
Licence  : MIT
Depends  : numpy, scipy, matplotlib
           pip install numpy scipy matplotlib

What to change first
--------------------
1. `Kinetics` -- your rate law, k0, and Ea.
2. `Feed` -- concentrations, volumetric flow, temperature.
3. `rate_of_disappearance_A()` if your rate law isn't power-law in A and B.
Everything downstream follows from those three.

Assumptions baked in (change deliberately, not accidentally)
------------------------------------------------------------
- Isothermal. No energy balance is solved. For anything exothermic and
  concentrated this is the assumption that gets people hurt -- see
  `energy_balance_note()` at the bottom before you trust a number.
- Constant density, so volumetric flow is constant through the reactor and
  conversion maps linearly onto concentration.
- Perfect mixing in the CSTR, perfect plug flow in the PFR. Real vessels sit
  between; a tanks-in-series or dispersion model is the next refinement.
- Single reaction, no side products, no catalyst deactivation.
- Steady state.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

R_GAS = 8.314462618  # J/(mol*K)


# ==========================================================================
# 1. Problem definition -- edit this block
# ==========================================================================


@dataclass(frozen=True)
class Kinetics:
    """Arrhenius parameters for -r_A = k * C_A * C_B.

    k0 units follow from the rate law: for overall second order and
    concentrations in mol/m3, k has units m3/(mol*s).

    The values below give k = 1.1e-4 m3/(mol*s) at 298 K, i.e. 0.11 L/(mol*s),
    which is the order of magnitude reported for ethyl acetate saponification
    in dilute aqueous solution. Replace with your own regression and record
    where it came from -- a rate constant with no provenance is a guess.

    Watch the units when you substitute a literature value: rate constants for
    this reaction are almost always tabulated in L/(mol*s), and 1 L/(mol*s) is
    1e-3 m3/(mol*s). Getting this wrong sizes your reactor 1000x too small,
    and the result still looks like a number.
    """

    k0: float = 1.26e4  # m3/(mol*s), pre-exponential factor
    Ea: float = 46_000.0  # J/mol, activation energy
    order_A: float = 1.0
    order_B: float = 1.0

    def k(self, T_K: float) -> float:
        """Rate constant at temperature T [K]."""
        return self.k0 * np.exp(-self.Ea / (R_GAS * T_K))


@dataclass(frozen=True)
class Feed:
    """Feed conditions. Concentrations in mol/m3 (= mmol/L), flow in m3/s."""

    C_A0: float = 100.0  # mol/m3 ethyl acetate  (0.1 mol/L)
    C_B0: float = 100.0  # mol/m3 sodium hydroxide (0.1 mol/L)
    v0: float = 1.0e-4  # m3/s volumetric flow    (0.1 L/s = 6 L/min)
    T_K: float = 298.15  # K, isothermal operating temperature

    @property
    def F_A0(self) -> float:
        """Molar feed rate of A [mol/s]."""
        return self.C_A0 * self.v0

    @property
    def theta_B(self) -> float:
        """Feed ratio C_B0/C_A0 [-]. 1.0 is stoichiometric for A + B -> products."""
        return self.C_B0 / self.C_A0


# Default problem instance -- the CLI overrides these.
KINETICS = Kinetics()
FEED = Feed()


# ==========================================================================
# 2. Rate law
# ==========================================================================


def concentrations(X: float, feed: Feed) -> tuple[float, float]:
    """Concentrations of A and B at conversion X, constant density.

    For A + B -> C + D with stoichiometric coefficients of 1:

        C_A = C_A0 (1 - X)
        C_B = C_A0 (theta_B - X)

    If your stoichiometry is A + b*B -> products, the second becomes
    C_A0 * (theta_B - b*X). Change it here and nowhere else.
    """
    C_A = feed.C_A0 * (1.0 - X)
    C_B = feed.C_A0 * (feed.theta_B - X)
    return C_A, C_B


def rate_of_disappearance_A(X: float, feed: Feed, kin: Kinetics) -> float:
    """-r_A at conversion X [mol/(m3*s)]. Always positive for X < X_limit.

    Returns a tiny positive floor rather than zero at complete conversion, so
    the PFR integrand doesn't divide by zero at the endpoint. That floor is a
    numerical convenience: it means the reported volume near X -> 1 is a lower
    bound, and physically the volume there is unbounded anyway.
    """
    C_A, C_B = concentrations(X, feed)
    C_A = max(C_A, 1e-12)
    C_B = max(C_B, 1e-12)
    k = kin.k(feed.T_K)
    return k * C_A**kin.order_A * C_B**kin.order_B


def limiting_conversion(feed: Feed) -> float:
    """Maximum conversion of A allowed by stoichiometry.

    With sub-stoichiometric B, B runs out first and caps X_A at theta_B.
    Irreversible reaction, so equilibrium doesn't bind; for a reversible
    reaction you would compare against X_eq here instead.
    """
    return min(1.0, feed.theta_B)


# ==========================================================================
# 3. Design equations
# ==========================================================================


def cstr_volume(X: float, feed: Feed, kin: Kinetics) -> float:
    """CSTR volume for conversion X [m3].

        V = F_A0 * X / (-r_A)|_exit

    The rate is evaluated at *exit* conditions, which is the whole point of a
    CSTR: the entire vessel sits at the lowest concentration in the system.
    That is why a CSTR is bigger than a PFR for any positive-order reaction.
    """
    _validate_conversion(X, feed)
    return feed.F_A0 * X / rate_of_disappearance_A(X, feed, kin)


def pfr_volume(X: float, feed: Feed, kin: Kinetics) -> float:
    """PFR volume for conversion X [m3].

        V = F_A0 * integral(0 -> X) dX / (-r_A)

    Integrated numerically so the same function works for any rate law you
    substitute above, including ones with no closed form.
    """
    _validate_conversion(X, feed)
    integrand = lambda x: 1.0 / rate_of_disappearance_A(x, feed, kin)  # noqa: E731
    integral, abserr = quad(integrand, 0.0, X, limit=200)
    if abserr > 1e-3 * abs(integral):
        print(f"  [warn] PFR quadrature error {abserr:.3g} is large relative to {integral:.3g}")
    return feed.F_A0 * integral


def space_time(volume_m3: float, feed: Feed) -> float:
    """Space time tau = V / v0 [s]. Mean residence time when density is constant."""
    return volume_m3 / feed.v0


def conversion_for_cstr_volume(V_m3: float, feed: Feed, kin: Kinetics) -> float:
    """Inverse problem: what conversion does an existing CSTR of volume V give?

    This is the question you actually get asked in a plant -- the vessel exists,
    what can it do. Solved by root-finding on V(X) - V = 0.
    """
    X_max = limiting_conversion(feed) - 1e-9
    f = lambda X: cstr_volume(X, feed, kin) - V_m3  # noqa: E731
    if f(1e-9) > 0:
        return 0.0
    if f(X_max) < 0:
        return X_max
    return brentq(f, 1e-9, X_max, xtol=1e-10)


def cstrs_in_series(n: int, X_total: float, feed: Feed, kin: Kinetics) -> list[float]:
    """Volumes of n equal-conversion-increment CSTRs in series [m3 each].

    Equal increments are not the optimal split -- minimising total volume gives
    unequal stages -- but it is the standard first comparison and shows the
    convergence towards PFR behaviour as n grows. Try n = 1, 2, 5, 20.
    """
    _validate_conversion(X_total, feed)
    volumes = []
    X_prev = 0.0
    for i in range(1, n + 1):
        X_i = X_total * i / n
        # Each tank: V_i = F_A0 (X_i - X_{i-1}) / (-r_A at X_i)
        V_i = feed.F_A0 * (X_i - X_prev) / rate_of_disappearance_A(X_i, feed, kin)
        volumes.append(V_i)
        X_prev = X_i
    return volumes


def _validate_conversion(X: float, feed: Feed) -> None:
    X_max = limiting_conversion(feed)
    if not 0.0 <= X < X_max:
        raise ValueError(
            f"Conversion {X} is outside the reachable range [0, {X_max}). "
            f"With C_B0/C_A0 = {feed.theta_B:.3f}, B limits conversion of A."
        )


# ==========================================================================
# 4. Reporting
# ==========================================================================


def design_report(X_target: float, feed: Feed, kin: Kinetics) -> dict[str, float]:
    """Size both reactor types at X_target and print a comparison."""
    k = kin.k(feed.T_K)
    V_cstr = cstr_volume(X_target, feed, kin)
    V_pfr = pfr_volume(X_target, feed, kin)

    print("=" * 68)
    print(f"REACTOR SIZING  --  target conversion X_A = {X_target:.3f}")
    print("=" * 68)
    print("\nOperating point")
    print(f"  Temperature            {feed.T_K:>12.2f} K   ({feed.T_K - 273.15:.1f} degC)")
    print(f"  Rate constant k        {k:>12.4g} m3/(mol*s)")
    print(f"  Feed C_A0              {feed.C_A0:>12.1f} mol/m3")
    print(f"  Feed C_B0              {feed.C_B0:>12.1f} mol/m3   (theta_B = {feed.theta_B:.2f})")
    print(f"  Volumetric flow v0     {feed.v0:>12.4g} m3/s     ({feed.v0 * 3.6e6:.1f} L/h)")
    print(f"  Molar feed F_A0        {feed.F_A0:>12.4g} mol/s")
    print(f"  Max conversion         {limiting_conversion(feed):>12.3f} (stoichiometric limit)")

    print("\nSizing")
    print(f"  {'':22s}{'CSTR':>16s}{'PFR':>16s}")
    print(f"  {'Volume [m3]':22s}{V_cstr:>16.5g}{V_pfr:>16.5g}")
    print(f"  {'Volume [L]':22s}{V_cstr * 1000:>16.4g}{V_pfr * 1000:>16.4g}")
    print(f"  {'Space time [s]':22s}{space_time(V_cstr, feed):>16.4g}{space_time(V_pfr, feed):>16.4g}")
    print(f"  {'Space time [min]':22s}{space_time(V_cstr, feed) / 60:>16.4g}"
          f"{space_time(V_pfr, feed) / 60:>16.4g}")
    print(f"\n  V_CSTR / V_PFR = {V_cstr / V_pfr:.3f}")
    print("  A positive-order reaction always gives a ratio > 1: the CSTR runs")
    print("  its whole volume at the low exit concentration, the PFR does not.")

    print("\nCSTRs in series at the same total conversion")
    print(f"  {'n':>4s}{'total V [L]':>16s}{'vs single CSTR':>18s}{'vs PFR':>12s}")
    for n in (1, 2, 3, 5, 10, 25):
        vols = cstrs_in_series(n, X_target, feed, kin)
        V_tot = sum(vols)
        print(f"  {n:>4d}{V_tot * 1000:>16.4g}{V_tot / V_cstr:>18.3f}{V_tot / V_pfr:>12.3f}")
    print("  As n grows the series approaches the PFR -- that is the standard")
    print("  argument for a cascade when a single tube is impractical.")

    return {
        "V_cstr_m3": V_cstr,
        "V_pfr_m3": V_pfr,
        "tau_cstr_s": space_time(V_cstr, feed),
        "tau_pfr_s": space_time(V_pfr, feed),
        "k": k,
    }


def sweep_conversion(feed: Feed, kin: Kinetics, plot: bool = False) -> None:
    """Volume vs conversion for both reactor types, printed and optionally plotted."""
    X_max = limiting_conversion(feed)
    X = np.linspace(0.05, min(0.95, X_max - 1e-6), 19)
    V_cstr = np.array([cstr_volume(x, feed, kin) for x in X])
    V_pfr = np.array([pfr_volume(x, feed, kin) for x in X])

    print("\nConversion sweep")
    print(f"  {'X_A':>6s}{'V_CSTR [L]':>14s}{'V_PFR [L]':>14s}{'ratio':>10s}")
    for x, vc, vp in zip(X, V_cstr, V_pfr):
        print(f"  {x:>6.2f}{vc * 1000:>14.4g}{vp * 1000:>14.4g}{vc / vp:>10.3f}")
    print("\n  Note how both curves steepen towards high conversion. Chasing the")
    print("  last few percent costs disproportionate volume -- which is usually")
    print("  the argument for a recycle rather than a bigger reactor.")

    if plot:
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

        ax1.plot(X, V_cstr * 1000, "o-", label="CSTR", lw=2)
        ax1.plot(X, V_pfr * 1000, "s-", label="PFR", lw=2)
        ax1.set_xlabel("Conversion of A, $X_A$ [-]")
        ax1.set_ylabel("Reactor volume [L]")
        ax1.set_title("Volume required vs conversion")
        ax1.legend()
        ax1.grid(alpha=0.3)

        # Levenspiel plot: the area interpretation of the two design equations.
        X_fine = np.linspace(0.001, min(0.95, X_max - 1e-6), 300)
        inv_rate = np.array([1.0 / rate_of_disappearance_A(x, feed, kin) for x in X_fine])
        ax2.plot(X_fine, inv_rate * feed.F_A0 * 1000, "k-", lw=2)
        ax2.fill_between(X_fine, 0, inv_rate * feed.F_A0 * 1000, alpha=0.15,
                         label="PFR volume = area under curve")
        X_mark = 0.8 if 0.8 < X_max else X_max * 0.9
        h = feed.F_A0 / rate_of_disappearance_A(X_mark, feed, kin) * 1000
        ax2.add_patch(plt.Rectangle((0, 0), X_mark, h, fill=False, ec="crimson", lw=2,
                                    label=f"CSTR volume = rectangle at X={X_mark:.2f}"))
        ax2.set_xlabel("Conversion of A, $X_A$ [-]")
        ax2.set_ylabel(r"$F_{A0}/(-r_A)$  [L]")
        ax2.set_title("Levenspiel plot")
        ax2.legend(fontsize=8)
        ax2.grid(alpha=0.3)

        fig.tight_layout()
        fig.savefig("reactor_design.png", dpi=150)
        print("\n  Saved plot to reactor_design.png")


def energy_balance_note() -> None:
    """Print the caveat that matters most before anyone builds anything."""
    print("\n" + "=" * 68)
    print("BEFORE YOU USE THESE NUMBERS")
    print("=" * 68)
    print("""
This model is isothermal. It solves no energy balance, so it cannot tell you:

  - the cooling duty needed to hold temperature,
  - whether the vessel can reject heat fast enough at the design volume,
  - whether multiple steady states exist (a CSTR with an exothermic reaction
    can have three, and start-up decides which one you land on),
  - whether a runaway is possible on loss of cooling.

For an exothermic reaction the next step is not a bigger conversion sweep, it
is the coupled mass and energy balance:

    dT/dz  or  Q_removed = U*A*(T - T_coolant)   vs   Q_generated = (-dH_rxn)*(-r_A)*V

and then a check of the ignition/extinction behaviour. Adiabatic temperature
rise is the first number to compute: dT_ad = C_A0 * (-dH_rxn) / (rho * cp).
If that exceeds what your materials or your relief system can take, the
reactor design problem is a safety problem before it is a sizing problem.

Ethyl acetate saponification is mildly exothermic (dH_rxn ~ -55 kJ/mol) and at
0.1 M gives dT_ad of only about 1.3 K, which is why treating it as isothermal
is defensible here and would not be at 5 M.
""")


# ==========================================================================
# 5. CLI
# ==========================================================================


def main() -> None:
    p = argparse.ArgumentParser(
        description="CSTR and PFR sizing for a second-order liquid-phase reaction.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("-X", "--conversion", type=float, default=0.90, help="target conversion of A")
    p.add_argument("-T", "--temperature", type=float, default=298.15, help="temperature [K]")
    p.add_argument("--CA0", type=float, default=100.0, help="feed concentration of A [mol/m3]")
    p.add_argument("--CB0", type=float, default=100.0, help="feed concentration of B [mol/m3]")
    p.add_argument("--v0", type=float, default=1.0e-4, help="volumetric feed flow [m3/s]")
    p.add_argument("--sweep", action="store_true", help="print a conversion sweep")
    p.add_argument("--plot", action="store_true", help="save reactor_design.png (implies --sweep)")
    p.add_argument("--existing-volume", type=float, default=None,
                   help="conversion achievable in an existing CSTR of this volume [m3]")
    args = p.parse_args()

    feed = Feed(C_A0=args.CA0, C_B0=args.CB0, v0=args.v0, T_K=args.temperature)
    kin = KINETICS

    design_report(args.conversion, feed, kin)

    if args.existing_volume is not None:
        X = conversion_for_cstr_volume(args.existing_volume, feed, kin)
        print(f"\nExisting {args.existing_volume:.4g} m3 CSTR achieves X_A = {X:.4f}")

    if args.sweep or args.plot:
        sweep_conversion(feed, kin, plot=args.plot)

    energy_balance_note()


if __name__ == "__main__":
    main()
