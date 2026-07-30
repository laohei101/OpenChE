#!/usr/bin/env python3
"""PID tuning by Ziegler-Nichols and friends, with a simulated process.

Purpose
-------
Work out starting PID settings for a loop, then see what they actually do
before you type them into a DCS. The script:

  1. models a FOPDT (first order plus dead time) process, the approximation
     behind almost every tuning rule in industry,
  2. runs an open-loop step test and identifies K, tau, theta from it, the
     same way you would from a plant trend,
  3. computes controller settings from four rule sets,
  4. simulates each closed loop through a setpoint change and a load
     disturbance, and reports IAE, overshoot, and settling time.

The point is the comparison. Ziegler-Nichols is famous, aggressive, and
usually wrong for a process loop -- seeing its quarter-amplitude decay next to
an IMC-tuned response is the fastest way to understand why plants detune it.

Author   : Open ChemE Hub contributors
Licence  : MIT
Depends  : numpy, matplotlib (matplotlib only for --plot)
           pip install numpy matplotlib

What to change first
--------------------
`PROCESS` near the top: gain, time constant, dead time, and sample interval.
If you have a real step test, put your trend in `identify_fopdt()` instead of
the simulated one -- everything downstream works the same.

Conventions
-----------
- Parallel (ISA standard) PID form:

      u(t) = Kc * [ e + (1/Ti) * integral(e dt) + Td * de/dt ]

  Some vendors use an independent-gain or series form; converting between them
  changes the numbers, so check which one your controller implements before
  entering anything. Getting this wrong is the single most common cause of a
  "the textbook settings don't work" complaint.
- Derivative acts on the *measurement*, not the error, so a setpoint step does
  not produce a derivative kick. This is what real controllers do.
- Time in seconds throughout. Ti and Td in seconds, Kc dimensionless (assumes
  the controller works in percent of range on both PV and OP).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


# ==========================================================================
# 1. Process model
# ==========================================================================


@dataclass(frozen=True)
class FOPDT:
    """First order plus dead time process.

        G(s) = K * exp(-theta*s) / (tau*s + 1)

    The default is a lagged temperature loop: modest gain, four-minute time
    constant, thirty seconds of transport delay. The controllability ratio
    theta/tau = 0.125 is comfortable -- above about 1.0 a PID starts to
    struggle and you should be thinking about a Smith predictor or MPC.
    """

    K: float = 2.5  # process gain [% PV per % OP]
    tau: float = 240.0  # time constant [s]
    theta: float = 30.0  # dead time [s]

    @property
    def controllability(self) -> float:
        """theta/tau. < 0.2 easy, 0.2-1.0 normal, > 1.0 dead-time dominant."""
        return self.theta / self.tau


PROCESS = FOPDT()


def simulate_open_loop_step(
    proc: FOPDT, u_step: float = 10.0, t_end: float = 1500.0, dt: float = 1.0,
    noise_pct: float = 0.05, seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate a bump test: step the output, record the measurement.

    A little measurement noise is added by default, because identification on
    a perfectly clean trend gives a misleadingly confident answer and hides how
    sensitive the dead-time estimate is.

    Returns (t, u, y).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0.0, t_end, dt)
    u = np.zeros_like(t)
    t_step = 100.0  # let the process settle before bumping
    u[t >= t_step] = u_step

    y = np.zeros_like(t)
    delay_samples = int(round(proc.theta / dt))
    for i in range(1, len(t)):
        # Delayed input: what the process "sees" now is what we sent theta ago.
        u_delayed = u[i - delay_samples] if i >= delay_samples else 0.0
        # dy/dt = (K*u_delayed - y)/tau, explicit Euler at dt << tau.
        y[i] = y[i - 1] + dt * (proc.K * u_delayed - y[i - 1]) / proc.tau

    y += rng.normal(0.0, noise_pct, size=y.shape)
    return t, u, y


def identify_fopdt(t: np.ndarray, u: np.ndarray, y: np.ndarray) -> FOPDT:
    """Fit K, tau, theta from a step response using the two-point method.

    The 28.3%/63.2% two-point method (Smith's method) is used rather than the
    tangent-and-intercept construction, because reading a tangent slope off a
    noisy trend by eye is unreliable and this is not:

        tau   = 1.5 * (t_63 - t_28)
        theta = t_63 - tau

    Both times are measured from the moment the output was stepped.

    Replace the arguments with your own plant trend to identify a real loop.
    Requirements for a usable bump test: steady before the step, a step large
    enough to move the PV well clear of the noise (5-10% of range), no other
    disturbances during the test, and enough time afterwards to reach a new
    steady state.
    """
    i_step = int(np.argmax(np.abs(np.diff(u)) > 1e-9)) + 1
    t_step = t[i_step]
    du = u[-1] - u[0]

    y0 = float(np.mean(y[:i_step]))
    y_inf = float(np.mean(y[-int(0.1 * len(y)):]))  # average the last 10%
    dy = y_inf - y0

    K = dy / du

    def time_at_fraction(frac: float) -> float:
        target = y0 + frac * dy
        idx = np.argmax(y[i_step:] >= target) + i_step
        return float(t[idx] - t_step)

    t28 = time_at_fraction(0.283)
    t63 = time_at_fraction(0.632)

    tau = 1.5 * (t63 - t28)
    theta = max(t63 - tau, 0.0)
    return FOPDT(K=K, tau=tau, theta=theta)


# ==========================================================================
# 2. Tuning rules
# ==========================================================================


@dataclass(frozen=True)
class PIDSettings:
    """Controller settings in parallel/ISA form."""

    Kc: float
    Ti: float  # integral time [s]; np.inf for no integral action
    Td: float  # derivative time [s]; 0.0 for none
    name: str = ""

    def __str__(self) -> str:
        ti = "inf" if np.isinf(self.Ti) else f"{self.Ti:.1f}"
        return f"{self.name:<28s} Kc = {self.Kc:6.3f}   Ti = {ti:>8s} s   Td = {self.Td:6.1f} s"


def ziegler_nichols_open_loop(proc: FOPDT, mode: str = "PID") -> PIDSettings:
    """Classic Ziegler-Nichols reaction-curve rules (1942).

    Designed for quarter-amplitude decay, which means roughly 25% overshoot
    and a distinctly oscillatory response. That was a reasonable target for a
    1940s pneumatic controller on a slow loop, and it is aggressive for most
    modern process loops -- especially anything feeding a downstream unit that
    would rather not see the oscillation.

    Included because it is the reference everyone knows, and because it makes a
    good upper bound: if your tuning is more aggressive than Z-N, ask why.

    Valid roughly for 0.1 < theta/tau < 1.0. Outside that it degrades badly.
    """
    K, tau, theta = proc.K, proc.tau, proc.theta
    R = tau / theta  # inverse controllability
    if mode == "P":
        return PIDSettings(Kc=R / K, Ti=np.inf, Td=0.0, name="Ziegler-Nichols P")
    if mode == "PI":
        return PIDSettings(Kc=0.9 * R / K, Ti=3.33 * theta, Td=0.0, name="Ziegler-Nichols PI")
    return PIDSettings(Kc=1.2 * R / K, Ti=2.0 * theta, Td=0.5 * theta, name="Ziegler-Nichols PID")


def ziegler_nichols_closed_loop(Ku: float, Pu: float, mode: str = "PID") -> PIDSettings:
    """Z-N ultimate-cycle rules from a continuous-cycling test.

    Ku is the proportional gain at which the loop just oscillates with constant
    amplitude, Pu the period of that oscillation [s].

    Deliberately driving a real plant loop to sustained oscillation is rarely
    acceptable -- it upsets downstream units and can trip things. Relay
    auto-tuning gets you the same Ku and Pu from a bounded oscillation and is
    what modern auto-tuners actually do.
    """
    if mode == "P":
        return PIDSettings(Kc=0.5 * Ku, Ti=np.inf, Td=0.0, name="Z-N ultimate P")
    if mode == "PI":
        return PIDSettings(Kc=0.45 * Ku, Ti=Pu / 1.2, Td=0.0, name="Z-N ultimate PI")
    return PIDSettings(Kc=0.6 * Ku, Ti=Pu / 2.0, Td=Pu / 8.0, name="Z-N ultimate PID")


def cohen_coon(proc: FOPDT) -> PIDSettings:
    """Cohen-Coon rules, tuned for load rejection on lag-dominant processes.

    Better than Z-N when dead time is a significant fraction of the time
    constant, still aggressive. Also targets quarter-amplitude decay.
    """
    K, tau, theta = proc.K, proc.tau, proc.theta
    r = theta / tau
    Kc = (1.0 / K) * (1.0 / r) * (1.35 + 0.25 * r)
    Ti = theta * (2.5 - 2.0 * r) / (1.0 - 0.39 * r)
    Td = theta * 0.37 / (1.0 - 0.81 * r)
    return PIDSettings(Kc=Kc, Ti=Ti, Td=Td, name="Cohen-Coon PID")


def imc_pid(proc: FOPDT, lambda_c: float | None = None) -> PIDSettings:
    """IMC / lambda tuning (Rivera-Morari-Skogestad), PID form.

    One tuning knob, lambda_c, the desired closed-loop time constant. This is
    the rule set most process control engineers actually use, because lambda_c
    is a direct, explainable trade-off: larger is slower and more robust,
    smaller is faster and closer to instability.

    Rules of thumb for lambda_c:
        lambda_c = tau        conservative, very robust, good for loops feeding
                              sensitive downstream units
        lambda_c = tau/2      balanced -- the default here
        lambda_c = theta      aggressive; below this you are fighting dead time
                              and small model errors will destabilise the loop

    Never set lambda_c below the dead time. The loop cannot respond faster than
    it can see, and pretending otherwise produces a controller that is stable
    in simulation and unstable on the plant.
    """
    K, tau, theta = proc.K, proc.tau, proc.theta
    if lambda_c is None:
        lambda_c = max(tau / 2.0, 1.5 * theta)
    lambda_c = max(lambda_c, theta)  # guard against the mistake above

    # First-order Pade approximation of the dead time gives the PID form.
    Kc = (2.0 * tau + theta) / (K * (2.0 * lambda_c + theta))
    Ti = tau + theta / 2.0
    Td = tau * theta / (2.0 * tau + theta)
    return PIDSettings(Kc=Kc, Ti=Ti, Td=Td, name=f"IMC/lambda (lam={lambda_c:.0f}s)")


def amigo_pi(proc: FOPDT) -> PIDSettings:
    """AMIGO PI rules (Astrom & Hagglund, 2004).

    Modern rules balancing setpoint tracking, load rejection, and robustness
    (targeting a maximum sensitivity around 1.4). Noticeably gentler than Z-N
    and a good default when you want PI only -- which is most flow, level, and
    pressure loops, where derivative action just amplifies noise.
    """
    K, tau, theta = proc.K, proc.tau, proc.theta
    Kc = (1.0 / K) * (0.15 + (0.35 - theta * tau / (theta + tau) ** 2) * (tau / theta))
    Ti = 0.35 * theta + (13.0 * theta * tau**2) / (tau**2 + 12.0 * theta * tau + 7.0 * theta**2)
    return PIDSettings(Kc=Kc, Ti=Ti, Td=0.0, name="AMIGO PI")


# ==========================================================================
# 3. Closed-loop simulation
# ==========================================================================


def simulate_closed_loop(
    proc: FOPDT,
    pid: PIDSettings,
    t_end: float = 3000.0,
    dt: float = 0.5,
    setpoint_step: float = 10.0,
    load_step: float = 5.0,
    load_time: float = 1500.0,
    op_limits: tuple[float, float] = (0.0, 100.0),
    derivative_filter_ratio: float = 0.1,
) -> dict[str, np.ndarray | float]:
    """Simulate the loop through a setpoint change then a load disturbance.

    Implementation details that matter and are usually skipped in textbook code:

    - **Anti-windup.** Integration stops when the output is saturated and the
      error would push it further into the limit. Without this, a controller
      that hits 100% output stays there long after the PV has recovered. This
      is the number one cause of "the loop overshoots massively after a big
      upset" in real plants.
    - **Derivative on measurement.** d(PV)/dt, not d(error)/dt, so a setpoint
      step doesn't produce a spike on the output.
    - **Derivative filtering.** Raw derivative amplifies noise without bound;
      a first-order filter at Td/N (N = 10 here) is standard practice.
    """
    n = int(t_end / dt)
    t = np.arange(n) * dt
    delay_samples = int(round(proc.theta / dt))

    sp = np.full(n, setpoint_step)
    sp[: int(50 / dt)] = 0.0  # start at steady state, then step the setpoint

    load = np.zeros(n)
    load[t >= load_time] = load_step  # unmeasured disturbance at the input

    y = np.zeros(n)  # process variable
    u = np.zeros(n)  # controller output
    integral = 0.0
    y_filt_prev = 0.0
    deriv_prev = 0.0
    u_min, u_max = op_limits
    tau_d_filter = derivative_filter_ratio * pid.Td

    for i in range(1, n):
        error = sp[i] - y[i - 1]

        # --- proportional
        p_term = pid.Kc * error

        # --- derivative on measurement, filtered
        if pid.Td > 0.0:
            dy = (y[i - 1] - y_filt_prev) / dt
            alpha = dt / (tau_d_filter + dt) if tau_d_filter > 0 else 1.0
            deriv_prev = deriv_prev + alpha * (dy - deriv_prev)
            d_term = -pid.Kc * pid.Td * deriv_prev
        else:
            d_term = 0.0
        y_filt_prev = y[i - 1]

        # --- integral with conditional anti-windup
        u_unsat = p_term + pid.Kc * integral + d_term
        if np.isfinite(pid.Ti) and pid.Ti > 0:
            saturated_high = u_unsat >= u_max and error > 0
            saturated_low = u_unsat <= u_min and error < 0
            if not (saturated_high or saturated_low):
                integral += (error / pid.Ti) * dt
        u_unsat = p_term + pid.Kc * integral + d_term

        u[i] = float(np.clip(u_unsat, u_min, u_max))

        # --- process: dead time then first-order lag, disturbance at the input
        u_effective = (u[i - delay_samples] if i >= delay_samples else 0.0) + load[i]
        y[i] = y[i - 1] + dt * (proc.K * u_effective - y[i - 1]) / proc.tau

    return {
        "t": t, "y": y, "u": u, "sp": sp,
        **_performance_metrics(t, y, sp, dt, load_time),
    }


def _performance_metrics(
    t: np.ndarray, y: np.ndarray, sp: np.ndarray, dt: float, load_time: float
) -> dict[str, float]:
    """IAE, overshoot, settling time, and output travel.

    IAE (integral of absolute error) is the summary number to compare tunings
    with; overshoot and settling time say *how* the error was spent. Output
    travel matters because a controller that achieves low IAE by moving the
    valve constantly will wear out the valve -- operators notice this before
    the control engineer does.
    """
    setpoint = float(sp[-1])
    i_load = int(load_time / dt)

    iae_total = float(np.sum(np.abs(sp - y)) * dt)
    iae_setpoint = float(np.sum(np.abs(sp[:i_load] - y[:i_load])) * dt)
    iae_load = float(np.sum(np.abs(sp[i_load:] - y[i_load:])) * dt)

    y_sp_phase = y[:i_load]
    peak = float(np.max(y_sp_phase)) if len(y_sp_phase) else 0.0
    overshoot_pct = 100.0 * (peak - setpoint) / setpoint if setpoint else 0.0

    # Settling: last time the PV leaves a +/-2% band around setpoint, during
    # the setpoint-change phase only.
    band = 0.02 * setpoint
    outside = np.abs(y_sp_phase - setpoint) > band
    settle_idx = int(np.max(np.nonzero(outside)[0])) if np.any(outside) else 0
    settling_time = float(t[settle_idx])

    return {
        "IAE_total": iae_total,
        "IAE_setpoint": iae_setpoint,
        "IAE_load": iae_load,
        "overshoot_pct": overshoot_pct,
        "settling_time_s": settling_time,
    }


# ==========================================================================
# 4. Comparison and reporting
# ==========================================================================


def compare_tunings(proc: FOPDT, plot: bool = False) -> None:
    """Tune four ways, simulate all of them, print the comparison."""
    print("=" * 78)
    print("PROCESS MODEL")
    print("=" * 78)
    print(f"  Gain K              {proc.K:>10.3f} %PV/%OP")
    print(f"  Time constant tau   {proc.tau:>10.1f} s")
    print(f"  Dead time theta     {proc.theta:>10.1f} s")
    print(f"  theta/tau           {proc.controllability:>10.3f}", end="  ")
    if proc.controllability < 0.2:
        print("(lag dominant -- easy to control)")
    elif proc.controllability < 1.0:
        print("(normal -- PID works well)")
    else:
        print("(dead-time dominant -- consider a Smith predictor or MPC)")

    tunings = [
        ziegler_nichols_open_loop(proc, "PI"),
        ziegler_nichols_open_loop(proc, "PID"),
        cohen_coon(proc),
        amigo_pi(proc),
        imc_pid(proc),
        imc_pid(proc, lambda_c=proc.tau),
    ]

    print("\n" + "=" * 78)
    print("TUNING SETTINGS  (parallel/ISA form -- check your controller's form!)")
    print("=" * 78)
    for s in tunings:
        print("  " + str(s))

    print("\n" + "=" * 78)
    print("CLOSED-LOOP PERFORMANCE")
    print("  Setpoint step of 10% at t=50s, load disturbance of 5% at t=1500s")
    print("=" * 78)
    header = f"  {'Tuning':<28s}{'IAE_sp':>10s}{'IAE_load':>10s}{'OS %':>8s}{'Ts [s]':>9s}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    results = []
    for s in tunings:
        r = simulate_closed_loop(proc, s)
        results.append((s, r))
        print(f"  {s.name:<28s}{r['IAE_setpoint']:>10.1f}{r['IAE_load']:>10.1f}"
              f"{r['overshoot_pct']:>8.1f}{r['settling_time_s']:>9.0f}")

    print("""
Reading this table
------------------
  IAE_sp    error accumulated tracking the setpoint change -- lower is faster
  IAE_load  error accumulated rejecting the disturbance -- this is what most
            process loops are actually for, since setpoints rarely move
  OS %      overshoot. Above ~10% is usually unacceptable on a real unit;
            Z-N's quarter-decay target lands well above that
  Ts        time to settle within +/-2% of setpoint

The aggressive rules (Z-N, Cohen-Coon) win on IAE and lose on overshoot and
robustness. They assume your model is right. It isn't -- process gain drifts
with throughput, fouling, and catalyst age, and a controller tuned to the edge
of stability at commissioning will oscillate six months later. That is why
lambda tuning, with an explicit robustness knob, is what most plants run.

Whatever you pick, halve the gain before you put it in service and watch it for
a shift. You can always turn it up.""")

    if plot:
        _plot_comparison(results)


def _plot_comparison(results) -> None:
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    for settings, r in results:
        ax1.plot(r["t"], r["y"], lw=1.6, label=settings.name)
        ax2.plot(r["t"], r["u"], lw=1.2, label=settings.name)

    t = results[0][1]["t"]
    ax1.plot(t, results[0][1]["sp"], "k--", lw=1.2, label="setpoint")
    ax1.axvline(1500, color="gray", ls=":", lw=1)
    ax1.annotate("load disturbance", xy=(1500, ax1.get_ylim()[1] * 0.95),
                 xytext=(1560, ax1.get_ylim()[1] * 0.95), fontsize=8, color="gray")
    ax1.set_ylabel("PV [%]")
    ax1.set_title("Closed-loop response: setpoint step then load disturbance")
    ax1.legend(fontsize=8, ncol=2)
    ax1.grid(alpha=0.3)

    ax2.set_ylabel("Controller output [%]")
    ax2.set_xlabel("Time [s]")
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("pid_tuning.png", dpi=150)
    print("\nSaved plot to pid_tuning.png")


# ==========================================================================
# 5. CLI
# ==========================================================================


def main() -> None:
    p = argparse.ArgumentParser(
        description="PID tuning rules compared on a FOPDT process.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("-K", "--gain", type=float, default=2.5, help="process gain [%%PV/%%OP]")
    p.add_argument("--tau", type=float, default=240.0, help="time constant [s]")
    p.add_argument("--theta", type=float, default=30.0, help="dead time [s]")
    p.add_argument("--identify", action="store_true",
                   help="run a simulated bump test and identify the model from it")
    p.add_argument("--plot", action="store_true", help="save pid_tuning.png")
    args = p.parse_args()

    proc = FOPDT(K=args.gain, tau=args.tau, theta=args.theta)

    if args.identify:
        print("=" * 78)
        print("STEP TEST IDENTIFICATION")
        print("=" * 78)
        t, u, y = simulate_open_loop_step(proc)
        fitted = identify_fopdt(t, u, y)
        print(f"  {'':10s}{'true':>12s}{'identified':>14s}{'error':>10s}")
        for label, true_v, fit_v in (
            ("K", proc.K, fitted.K), ("tau [s]", proc.tau, fitted.tau),
            ("theta [s]", proc.theta, fitted.theta),
        ):
            err = 100.0 * (fit_v - true_v) / true_v if true_v else 0.0
            print(f"  {label:<10s}{true_v:>12.3f}{fit_v:>14.3f}{err:>9.1f}%")
        print("\n  Dead time is the hardest parameter to pin down from a noisy")
        print("  trend, and it is the one the tuning rules are most sensitive to.")
        print("  Take three bump tests, not one.\n")
        proc = fitted

    compare_tunings(proc, plot=args.plot)


if __name__ == "__main__":
    main()
