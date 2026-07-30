#!/usr/bin/env python3
"""Execute every runnable template and check it produces the right answers.

    python scripts/run_template_smoke_tests.py
    python scripts/run_template_smoke_tests.py --quick   # skip the notebook

This is the machine-readable verification manifest the spec asks for in section
7.5, expressed as code rather than as a YAML file describing code. Each check
records the command, the expected value, the tolerance, and where the expected
value comes from — so a failure tells you which physical claim broke, not just
that a script exited non-zero.

Numerical expectations are derived from first principles wherever possible
(a closed-form solution, a conservation law, a limiting case), because a
regression test that only compares against last week's output cannot tell you
the code was ever correct.
"""

from __future__ import annotations

import argparse
import dataclasses
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


@dataclasses.dataclass
class Result:
    name: str
    ok: bool
    detail: str
    seconds: float


def check(name: str, ok: bool, detail: str, t0: float) -> Result:
    return Result(name=name, ok=ok, detail=detail, seconds=time.time() - t0)


def run(cmd: list[str], cwd: pathlib.Path = TEMPLATES) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)


# ---------------------------------------------------------------------------
# unit_conversions.py
# ---------------------------------------------------------------------------

def test_unit_conversions() -> list[Result]:
    results: list[Result] = []

    t0 = time.time()
    proc = run([sys.executable, "-m", "doctest", "unit_conversions.py"])
    results.append(check("unit_conversions: doctests", proc.returncode == 0,
                         proc.stdout.strip() or proc.stderr.strip() or "all doctests pass", t0))

    t0 = time.time()
    proc = run([sys.executable, "unit_conversions.py"])
    results.append(check("unit_conversions: self-test runs", proc.returncode == 0,
                         "exit 0" if proc.returncode == 0 else proc.stderr[-300:], t0))

    # Round-trip identity: converting out and back must return the original.
    # This catches an inverted factor, which a one-way spot check does not.
    t0 = time.time()
    sys.path.insert(0, str(TEMPLATES))
    import unit_conversions as uc  # noqa: E402

    failures = []
    for quantity, units in uc.FACTORS.items():
        base = next(iter(units))
        for unit in units:
            there = uc.convert(1.0, base, unit)
            back = uc.convert(there, unit, base)
            if abs(back - 1.0) > 1e-9:
                failures.append(f"{quantity}:{base}<->{unit} round trip = {back}")
    results.append(check(
        f"unit_conversions: round trip over {sum(len(u) for u in uc.FACTORS.values())} units",
        not failures, "; ".join(failures[:3]) or "all round trips exact to 1e-9", t0))

    # Absolute anchors, each with a source.
    t0 = time.time()
    anchors = [
        ("1 atm -> Pa", uc.convert(1, "atm", "Pa"), 101325.0, 0.0, "definition of the standard atmosphere"),
        ("100 degC -> degF", uc.convert_temperature(100, "degC", "degF"), 212.0, 1e-9, "definition of the Fahrenheit scale"),
        ("0 degC -> K", uc.convert_temperature(0, "degC", "K"), 273.15, 1e-9, "definition of the Celsius scale"),
        ("1 kWh -> MJ", uc.convert(1, "kWh", "MJ"), 3.6, 1e-12, "1 kW x 3600 s"),
        ("1 cP -> Pa.s", uc.convert(1, "cP", "Pa.s"), 1e-3, 0.0, "definition of the poise"),
        ("1 inch -> mm", uc.convert(1, "in", "mm"), 25.4, 1e-12, "international inch, exact"),
    ]
    bad = [f"{label}: got {got}, expected {want}" for label, got, want, tol, _ in anchors
           if abs(got - want) > max(tol, abs(want) * 1e-12)]
    results.append(check("unit_conversions: absolute anchors", not bad,
                         "; ".join(bad) or f"{len(anchors)} anchors exact", t0))

    # Affine temperature must be refused by the linear converter.
    t0 = time.time()
    try:
        uc.convert(100, "degC", "degF")
        ok, detail = False, "convert() accepted a temperature; it must raise"
    except ValueError:
        ok, detail = True, "convert() correctly refuses affine temperature scales"
    results.append(check("unit_conversions: rejects affine temperature", ok, detail, t0))

    # Cross-quantity conversion needs a density it does not have.
    t0 = time.time()
    try:
        uc.convert(1, "kg/h", "m3/h")
        ok, detail = False, "convert() accepted a cross-quantity conversion; it must raise"
    except ValueError:
        ok, detail = True, "convert() correctly refuses mass -> volume without a density"
    results.append(check("unit_conversions: rejects cross-quantity", ok, detail, t0))

    return results


# ---------------------------------------------------------------------------
# reactor_design_skeleton.py
# ---------------------------------------------------------------------------

def test_reactor_design() -> list[Result]:
    results: list[Result] = []
    sys.path.insert(0, str(TEMPLATES))
    import reactor_design_skeleton as rd  # noqa: E402

    t0 = time.time()
    proc = run([sys.executable, "reactor_design_skeleton.py", "-X", "0.9"])
    results.append(check("reactor_design: runs", proc.returncode == 0,
                         "exit 0" if proc.returncode == 0 else proc.stderr[-300:], t0))

    # Closed-form check. For A + B -> products, second order, equimolar feed:
    #   tau_CSTR = X / (k C_A0 (1-X)^2)      tau_PFR = X / (k C_A0 (1-X))
    # so V_CSTR / V_PFR = 1 / (1 - X) exactly, independent of k and C_A0.
    # This is an analytical identity, not a recorded output.
    t0 = time.time()
    feed, kin = rd.Feed(), rd.Kinetics()
    bad = []
    for X in (0.5, 0.8, 0.9, 0.95):
        ratio = rd.cstr_volume(X, feed, kin) / rd.pfr_volume(X, feed, kin)
        expected = 1.0 / (1.0 - X)
        if abs(ratio - expected) / expected > 1e-6:
            bad.append(f"X={X}: ratio {ratio:.6f} != {expected:.6f}")
    results.append(check("reactor_design: V_CSTR/V_PFR = 1/(1-X) analytically", not bad,
                         "; ".join(bad) or "exact at X = 0.5, 0.8, 0.9, 0.95", t0))

    # A CSTR cascade must approach the PFR from above as n grows, and never
    # undershoot it — that would violate the design equations.
    t0 = time.time()
    X = 0.9
    v_pfr = rd.pfr_volume(X, feed, kin)
    totals = [sum(rd.cstrs_in_series(n, X, feed, kin)) for n in (1, 2, 5, 10, 25, 50)]
    monotone = all(a > b for a, b in zip(totals, totals[1:]))
    above = all(t >= v_pfr * (1 - 1e-9) for t in totals)
    results.append(check("reactor_design: CSTR cascade converges to PFR from above",
                         monotone and above,
                         f"n=1 -> {totals[0]/v_pfr:.2f}x PFR, n=50 -> {totals[-1]/v_pfr:.3f}x PFR", t0))

    # Conversion beyond the stoichiometric limit must be refused, not silently
    # extrapolated into a negative concentration.
    t0 = time.time()
    lean = rd.Feed(C_A0=100.0, C_B0=60.0)
    try:
        rd.cstr_volume(0.8, lean, kin)
        ok, detail = False, "accepted X=0.8 with theta_B=0.6; must raise"
    except ValueError:
        ok, detail = True, "refuses conversion above the stoichiometric limit"
    results.append(check("reactor_design: enforces stoichiometric limit", ok, detail, t0))

    # Round-trip the inverse problem.
    t0 = time.time()
    v = rd.cstr_volume(0.85, feed, kin)
    x_back = rd.conversion_for_cstr_volume(v, feed, kin)
    ok = abs(x_back - 0.85) < 1e-6
    results.append(check("reactor_design: sizing inverse round trip", ok,
                         f"V(X=0.85) -> X={x_back:.8f}", t0))

    return results


# ---------------------------------------------------------------------------
# pid_tuning.py
# ---------------------------------------------------------------------------

def test_pid_tuning() -> list[Result]:
    results: list[Result] = []
    sys.path.insert(0, str(TEMPLATES))
    import pid_tuning as pid  # noqa: E402

    t0 = time.time()
    proc = run([sys.executable, "pid_tuning.py", "--identify"])
    results.append(check("pid_tuning: runs", proc.returncode == 0,
                         "exit 0" if proc.returncode == 0 else proc.stderr[-300:], t0))

    # Identification must recover the model it was given, from a noisy step.
    # 10% is generous and still catches a broken two-point method.
    t0 = time.time()
    proc_model = pid.FOPDT(K=2.5, tau=240.0, theta=30.0)
    t, u, y = pid.simulate_open_loop_step(proc_model, seed=0)
    fitted = pid.identify_fopdt(t, u, y)
    errs = {
        "K": abs(fitted.K - proc_model.K) / proc_model.K,
        "tau": abs(fitted.tau - proc_model.tau) / proc_model.tau,
        "theta": abs(fitted.theta - proc_model.theta) / proc_model.theta,
    }
    ok = all(v < 0.10 for v in errs.values())
    results.append(check("pid_tuning: identifies a known FOPDT within 10%", ok,
                         ", ".join(f"{k} {v:.1%}" for k, v in errs.items()), t0))

    # A closed loop with integral action must reach setpoint. Steady-state
    # offset is the definitive symptom of broken integral action or windup.
    t0 = time.time()
    bad = []
    for settings in (pid.imc_pid(proc_model), pid.amigo_pi(proc_model)):
        r = pid.simulate_closed_loop(proc_model, settings, t_end=6000.0, load_step=0.0)
        final = float(r["y"][-1])
        target = float(r["sp"][-1])
        if abs(final - target) / target > 0.02:
            bad.append(f"{settings.name}: settled at {final:.2f} vs setpoint {target}")
    results.append(check("pid_tuning: integral action removes offset", not bad,
                         "; ".join(bad) or "IMC and AMIGO both reach setpoint within 2%", t0))

    # Ziegler-Nichols should be measurably more aggressive than lambda tuning.
    # If this inverts, a tuning formula has been transcribed wrongly.
    t0 = time.time()
    zn = pid.simulate_closed_loop(proc_model, pid.ziegler_nichols_open_loop(proc_model, "PID"))
    imc = pid.simulate_closed_loop(proc_model, pid.imc_pid(proc_model))
    ok = zn["overshoot_pct"] > imc["overshoot_pct"]
    results.append(check("pid_tuning: Z-N overshoots more than IMC", ok,
                         f"Z-N {zn['overshoot_pct']:.1f}% vs IMC {imc['overshoot_pct']:.1f}%", t0))

    return results


# ---------------------------------------------------------------------------
# mass_balance_notebook.ipynb
# ---------------------------------------------------------------------------

def test_notebook() -> list[Result]:
    t0 = time.time()
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        return [check("mass_balance_notebook: executes", True,
                      "SKIPPED (nbclient not installed; pip install -r requirements-dev.txt)", t0)]

    path = TEMPLATES / "mass_balance_notebook.ipynb"
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(TEMPLATES)}})
    try:
        client.execute()
    except Exception as exc:
        return [check("mass_balance_notebook: executes", False, f"{type(exc).__name__}: {str(exc)[:300]}", t0)]

    # The notebook asserts its own balances; a silent pass is not enough, so
    # confirm the closure message actually appeared in the output.
    text = "\n".join(
        out.get("text", "")
        for cell in nb.cells if cell.cell_type == "code"
        for out in cell.get("outputs", [])
    )
    closed = "All balances close" in text and "Both components close" in text
    return [check("mass_balance_notebook: executes and all balances close", closed,
                  "closure messages found in output" if closed else "closure assertions did not report", t0)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true", help="skip the notebook execution test")
    args = ap.parse_args()

    print("=" * 78)
    print("TEMPLATE SMOKE TESTS")
    print("=" * 78)

    results: list[Result] = []
    results += test_unit_conversions()
    results += test_reactor_design()
    results += test_pid_tuning()
    if not args.quick:
        results += test_notebook()

    print()
    for r in results:
        mark = " ok " if r.ok else "FAIL"
        print(f"  [{mark}] {r.name}  ({r.seconds:.1f}s)")
        print(f"         {r.detail}")

    failed = [r for r in results if not r.ok]
    print()
    print(f"  {len(results) - len(failed)}/{len(results)} checks passed")
    if failed:
        print(f"\n  {len(failed)} FAILED:")
        for r in failed:
            print(f"    {r.name}: {r.detail}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
