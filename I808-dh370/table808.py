#!/usr/bin/env python3
"""#808: Delta at fixed D under other held values and another plan, at #603's states (run808.sh's jobs).

    python3 -I table808.py R [--pilot] [--mutate=swap] [--plan_tag=NAME]

R is the raw folder (I808-dh370). Each job s<D>_<arm> polished #603's state at D with the held values of #608's d6 or
d10 chain (arms d6, d10, #603's plan) or with #603's own held values on a new plan (arm plan). Per job: whether the
polish converged (its last "octo-double Newton" line, max|F| <= 1e-60), its steps, the first correction's dDelta (the
linear response) and delta = Delta(polished base) - Delta(#603's state), exact sums of the eight parts at 100 digits.

Registered before the runs (#808), with E(D) = 2.2e-37 / p_min(D), #805's envelope (p_min from I805-mac/table.json):
- Control: at D 240.1244, delta(d6) and delta(d10) equal data/delta_fits.csv's Delta(fit) - Delta(d8) there,
  +3.4486e-11 and -3.3980e-11, within 1e-12 each. A failed control exits 1 and stops the work.
- The held arm's measure is x = Delta(d6) - Delta(d10), the plan arm's x = delta(plan), at the four states from 250.84.
  r = |x| / E. An arm carries the departure when 1/3 <= r <= 3 at all four, does not when r < 1e-2 at all four, and is
  unsettled otherwise. Reported beside it, not part of the verdict: x(253.53) / x(250.84), against 40.4 for a term in
  1/p_min and about 1 for a smooth one.
Exit 0 when the control passes and every job present converged; 1 when the control fails; 2 when a job is missing or
did not converge. --pilot needs only s253.5301_d10 and s240.1244_d6. --mutate=swap swaps the control's two values,
and the control must then fail. --plan_tag=NAME reads the plan arm from the jobs s<D>_NAME (plandrop: the plan arm with
--od_full_drop 1e-6, run808b.sh).
"""
import glob
import os
import re
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 100
STATES = ["240.1244", "250.8381", "251.8859", "252.6135", "253.5301"]
PMIN = {"240.1244": 7.306e-24, "250.8381": 3.074e-30, "251.8859": 9.436e-31, "252.6135": 7.287e-31, "253.5301": 7.601e-32}
K = 2.2e-37
CTRL = {"d6": 3.4486e-11, "d10": -3.3980e-11}
CTRL_TOL = 1e-12
PARTS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
END = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (not converged|converged)")
FIRST = re.compile(r"on 0: .*dDelta ([-+0-9.e]+)")


def delta_of(p):
    z = np.load(p)
    return mp.fsum(mp.mpf(float(z[k][-1])) for k in PARTS if k in z.files)


def job(R, B, D, arm):
    tag = f"s{D}_{arm}"
    lp = os.path.join(R, tag + ".log")
    if not os.path.exists(lp):
        return None
    txt = open(lp, encoding="utf-8", errors="replace").read()
    ends = END.findall(txt)
    first = FIRST.search(txt)
    bases = glob.glob(os.path.join(R, tag, "base_pin3_D*.npz"))
    out = dict(tag=tag, steps=int(ends[-1][0]) if ends else None, F=ends[-1][1] if ends else None,
               conv=bool(ends) and ends[-1][2] == "converged" and float(ends[-1][1]) <= 1e-60,
               first=float(first.group(1)) if first else None, delta=None)
    if bases:
        out["delta"] = delta_of(bases[0]) - delta_of(os.path.join(B, f"I603-win2/chain/anm_pin3_D{D}.npz"))
    return out


def main():
    R = sys.argv[1]
    B = "/home/nathan/scratch808"
    for a in sys.argv[2:]:
        if a.startswith("--B="):
            B = a[4:]
    pilot = "--pilot" in sys.argv
    ptag = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--plan_tag=")), "plan")
    ctrl = dict(CTRL)
    if "--mutate=swap" in sys.argv:
        ctrl = {"d6": CTRL["d10"], "d10": CTRL["d6"]}
        print("MUTATION swap: the control's two values exchanged; the control must fail")
    need = [("253.5301", "d10"), ("240.1244", "d6")] if pilot else [(D, a) for D in STATES for a in ("d6", "d10", "plan")]
    J = {(D, a): job(R, B, D, ptag if a == "plan" else a) for D in STATES for a in ("d6", "d10", "plan")}
    print("| job | converged | steps | max|F| | first dDelta | Delta - Delta(#603) | E = 2.2e-37/p_min |")
    print("|---|---|---|---|---|---|---|")
    for (D, a), j in J.items():
        if j is None:
            continue
        d = "none" if j["delta"] is None else mp.nstr(j["delta"], 6)
        fd = "none" if j["first"] is None else f"{j['first']:+.3e}"
        print(f"| {j['tag']} | {'yes' if j['conv'] else 'NO'} | {j['steps']} | {j['F']} | {fd} | {d} | {K / PMIN[D]:.2e} |")
    code = 0
    missing = [f"s{D}_{a}" for D, a in need if J[(D, a)] is None or not J[(D, a)]["conv"] or J[(D, a)]["delta"] is None]
    if missing:
        print("missing or not converged: " + ", ".join(missing))
        code = 2
    # the control at D 240.1244
    for a in ("d6", "d10"):
        j = J[("240.1244", a)]
        if j is None or j["delta"] is None:
            continue
        off = abs(float(j["delta"]) - ctrl[a])
        ok = off <= CTRL_TOL
        print(f"control {a} at 240.1244: delta {float(j['delta']):+.4e} against {ctrl[a]:+.4e}, off by {off:.2e} "
              f"(bar {CTRL_TOL:.0e}): {'PASS' if ok else 'FAIL'}")
        if not ok:
            code = 1
    # the verdicts at the four states from 250.84
    four = STATES[1:]
    for arm, xf in (("held, Delta(d6) - Delta(d10)", lambda D: J[(D, "d6")]["delta"] - J[(D, "d10")]["delta"]),
                    ("plan, delta(plan)", lambda D: J[(D, "plan")]["delta"])):
        try:
            xs = {D: float(xf(D)) for D in four}
        except (TypeError, KeyError):
            print(f"{arm}: incomplete")
            continue
        rs = {D: abs(xs[D]) / (K / PMIN[D]) for D in four}
        if all(1 / 3 <= r <= 3 for r in rs.values()):
            v = "carries the departure"
        elif all(r < 1e-2 for r in rs.values()):
            v = "does not carry the departure"
        else:
            v = "unsettled"
        g = abs(xs["253.5301"] / xs["250.8381"]) if xs["250.8381"] else float("inf")
        print(f"{arm}: " + ", ".join(f"{D} x {xs[D]:+.3e} r {rs[D]:.2e}" for D in four) +
              f"; verdict: {v}; x(253.53)/x(250.84) = {g:.3g} (1/p_min gives 40.4)")
    print("exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
