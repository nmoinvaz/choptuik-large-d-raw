#!/usr/bin/env python3
"""I230-mac: re-sample the stretch of #212's edge T (Im = y2 = 3 omega / 2, from Re 1.157 to aL = 0.3) that the kf 23
count left at the initial spacing, and recompute the windings of U and full.

    python3 t_check.py HP_DIR I212_DATA STATE_KF23.npz OUT_DIR [--h=0.03]

Why: the moment code's planted test (hp/modecount_moment_planted.py, History) found that the count can miss whole
2 pi turns on T, whose phase grows by 11-20 rad per unit of Re: an interval of the initial grid (0.57) then turns by
about 2 pi, looks flat and is never bisected or verified. In #212's kf 23 record the last two intervals of T
(Re 1.157 to 0.871, h 0.286, step +0.043 rad; Re 0.871 to 0.300, h 0.571, step +0.226 rad) were never bisected, while
the phase grows by about 17 rad per unit of Re on T just before them and by 20 on T0 just after.

Method: the two intervals are re-sampled from scratch, uniformly with spacing at most h, then bisected until every
phase step of g is at most pi/4, then every step above pi/8 is bisected once more and checked against the whole
(the count's rules). g is the count's (its record's expected zeros and trend, the candidate poles from the state), so
the new steps replace the two old ones in T's phase change. Reading, fixed before the run: if T's phase change is
unchanged, #212's U +8 and full +24 at kf 23 stand; if it changes by 2 pi k, U changes by k and full by 2k, and #212's
kf 23 U and full are corrected to those values (a discrepancy to report, not a fix of #212's record). Determinants go
to OUT_DIR/modecount_D61.0264_M48_kf23_T_evals.jsonl.
"""
import json
import math
import os
import sys
import time

import numpy as np

hp, i212, state, out = sys.argv[1:5]
h = float(([a.split("=", 1)[1] for a in sys.argv[5:] if a.startswith("--h=")] or ["0.03"])[0])
sys.path.insert(0, hp)
import modecount_moment as MM  # noqa: E402
from modecount_common import setup  # noqa: E402

r, ev = MM.load_count(i212, "D61.0264_M48_kf23")
Q = MM.poles_from_state(state, r)
assert len(Q) == r["n_candidate_poles_factored"]
K = np.array([complex(*z) for z in r["expected_zeros"]])
pc = r["trend"]
st = setup(f"{hp}/data/seeds/local/up23_D61.0264.npz", M=48, kf=23, fmax=1e-15)
cache_path = os.path.join(out, "modecount_D61.0264_M48_kf23_T_evals.jsonl")
cache = {}
if os.path.exists(cache_path):
    for line in open(cache_path):
        e = json.loads(line)
        cache[(e["re"], e["im"])] = e
cf = open(cache_path, "a")


EVK = np.array([complex(*k) for k in ev])
EVV = list(ev.values())


def lng(lam):
    key = (float(lam.real), float(lam.imag))
    i = int(np.argmin(np.abs(EVK - lam)))
    if abs(EVK[i] - lam) < 1e-9:
        v = EVV[i]
    else:
        if key not in cache:
            t = time.time()
            la, arg, pmin, pmax = st.det(*key)
            cache[key] = dict(re=key[0], im=key[1], lnabs=la, arg=arg, pmin=pmin, pmax=pmax, sec=round(time.time() - t, 1))
            cf.write(json.dumps(cache[key]) + "\n")
            cf.flush()
            print(f"  det at {key[0]:.6f} {key[1]:+.6f}i: {cache[key]['sec']} s", flush=True)
        v = complex(cache[key]["lnabs"], cache[key]["arg"])
    return v + complex(np.sum(np.log(lam - Q)) - np.sum(np.log(lam - K))) - complex(np.polyval(pc, lam))


def wrap(a):
    return math.remainder(a, 2 * math.pi)


e = r["edges"]["T"]
z0, z1 = complex(*e["z0"]), complex(*e["z1"])
L = abs(z1 - z0)
S = e["samples"]
ts = [s[0] for s in S]
# the old steps of the two unrefined intervals (the last two of T)
old = [wrap(S[i + 1][2] - S[i][2]) for i in (len(S) - 3, len(S) - 2)]
ta, tb = ts[-3], ts[-1]
n = max(2, int(math.ceil((tb - ta) * L / h)))
vals = {ta + (tb - ta) * i / n: None for i in range(n + 1)}
pt = lambda t: z0 + t * (z1 - z0)
for t in vals:
    vals[t] = lng(pt(t))
# the old middle sample (Re 0.871) is kept as a node if it is not on the grid
tm = ts[-2]
vals[tm] = lng(pt(tm))
tol = math.pi / 4
step = lambda a, b: wrap(vals[b].imag - vals[a].imag)
changed = True
while changed:
    changed = False
    T = sorted(vals)
    for a, b in zip(T[:-1], T[1:]):
        if abs(step(a, b)) > tol:
            vals[0.5 * (a + b)] = lng(pt(0.5 * (a + b)))
            changed = True
T = sorted(vals)
bad = 0
for a, b in zip(T[:-1], T[1:]):
    d = step(a, b)
    if abs(d) > tol / 2:
        m = 0.5 * (a + b)
        vals[m] = lng(pt(m))
        if abs(wrap(vals[m].imag - vals[a].imag) + wrap(vals[b].imag - vals[m].imag) - d) > 1e-6:
            bad += 1
T = sorted(vals)
steps = [step(a, b) for a, b in zip(T[:-1], T[1:])]
new = sum(steps)
dT = new - sum(old)
k = dT / (2 * math.pi)
dphi = {name: r["edges"][name]["dphi"] for name in r["edges"]}
U_old = r["boxes"]["U"]["winding_g"]
full_old = r["boxes"]["full"]["winding_g"]
res = dict(stretch_re=[pt(ta).real, pt(tb).real], im=pt(ta).imag, points=len(T), new_determinants=len(cache), h=h,
           old_steps=old, new_phase_change=new, change=dT, turns=k, max_step=max(abs(s) for s in steps),
           verify_mismatch=bad, T_dphi_old=dphi["T"], T_dphi_new=dphi["T"] + dT, U_old=U_old,
           U_new=U_old + dT / (2 * math.pi), full_old=full_old, full_new=full_old + dT / math.pi,
           time=time.strftime("%Y-%m-%d %H:%M:%S"))
with open(os.path.join(out, "t_check.jsonl"), "a") as fo:
    fo.write(json.dumps(res) + "\n")
print(f"T from Re {pt(ta).real:.4f} to {pt(tb).real:.4f} at Im {pt(ta).imag:.4f}: {len(T)} points, max step "
      f"{res['max_step']:.3f} rad, verification mismatches {bad}; phase change {new:+.4f} rad, the count's two steps "
      f"{sum(old):+.4f} rad: {k:+.4f} turns")
print(f"T: {dphi['T']:+.4f} -> {res['T_dphi_new']:+.4f}; U wind(g) {U_old:+.4f} -> {res['U_new']:+.4f}; "
      f"full {full_old:+.4f} -> {res['full_new']:+.4f}")
