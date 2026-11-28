#!/usr/bin/env python3
"""#1109 stage 1e on macm3: builds post_1e.md from ne.out, ne/ (the saved iterate), ne_root.jsonl/.exit and the two state files.
Needs numpy (z[-1] of the states): run with the venv python from this folder.
Usage: python3 make_post_1e.py DATA_COMMIT TIME_UTC > post_1e.md"""
import json, os, sys
import numpy as np
from ne_summary import parse, report, reading
from roots_summary import load

d = os.path.dirname(os.path.abspath(__file__))
raw = os.path.dirname(d)
commit, when = sys.argv[1], sys.argv[2]
REF, SLOPE = 0.0455917, 0.785
text = open(os.path.join(d, "ne.out")).read()
outs, steps0, stop = parse(text)
rd = np.load(os.path.join(raw, "I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy"))
ne = np.load(os.path.join(d, "ne/sol_ne1_D23.0000.npy"))
dD = float(ne[-1] - rd[-1])
dz = float(np.linalg.norm(ne - rd))
ev, fin, rc = load(d, "ne_root")
x = fin[-1]
root = x["lam_lin"]
S = root - REF
pred = SLOPE * dD
lo0, hi0 = 0.0455917 + pred - 0.004, 0.0455917 + pred + 0.004
b = x["bracket"]
rk = reading(outs, stop)
f1 = {fr["f"]: fr for fr in outs[0]["fracs"]}
print(f"#1109 stage 1e on macm3: nonlinear elimination at k_c 127, D 23.0 from R0, runner t5-macm3, {when}. Raw: `I1109-macm3/` (`ne/`, `ne_root.*`), raw-data commit {commit}.\n")
print(f"**Reading {rk}: the elimination stops at outer 1, the zero is not reached; the root of its last iterate (dDelta {dD:+.4e}) is {root:.9f}, "
      f"{S:+.4e} from 0.0455917, which is {S / pred:.2f} times the linear estimate {SLOPE} x dDelta = {pred:+.4e}.** "
      f"The iterate's robust bracket is [{b[0]!r}, {b[1]!r}], so its root shift lies between {b[0] - REF:+.4e} and {b[1] - REF:+.4e}, at least "
      f"{(b[1] - REF) / pred:.2f} times the linear estimate. The run ended exit 4 (last point not robust), as w01 and w10 did.\n")
print("### Step 1: nonlinear elimination (`i1101_weakdir.py ne ... --outer=6`; output `ne.out`, table `ne_summary.txt` by `ne_summary.py`)\n")
rep = []
report(text, out=rep.append)
print("\n".join(rep))
print(f"\nRun 07:39:05 to 08:00:46 UTC, exit 0, 1301 s, OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6, nice 10, RSS 6.3 GiB at the first J and SVD (one sample). "
      f"The record system was reproduced at the start (|F| 3.1959e-10 against 3.1949e-10, 4179 steps). The saved iterate `ne/sol_ne1_D23.0000.npy` has |dz| {dz:.4e} against R0 "
      f"(Delta alone {abs(dD):.4e}; dDelta from the state files' `z[-1]`).")
print("\nBy the rule the fraction with the smallest final chord |F| is taken: "
      f"fraction 0.125 (|F| {f1['0.125']['Fend']:.4e}). Fraction 1.0 cut |U_w^T F| to {f1['1.0']['uwf']:.4e} ({outs[0]['uwf'] / f1['1.0']['uwf']:.2f}x) at dDelta "
      f"{f1['1.0']['Delta'] - outs[0]['Delta']:+.4e}, but the chord on the strong band diverged (|F| minimum {min(f1['1.0']['chord']):.2e}, final {f1['1.0']['Fend']:.4e}). "
      f"Fraction 0.5 ended at |F| {f1['0.5']['Fend']:.4e} ({(f1['0.5']['Fend'] / f1['0.125']['Fend'] - 1) * 100:+.1f}% against the one taken) with |U_w^T F| {f1['0.5']['uwf']:.4e} "
      f"({outs[0]['uwf'] / f1['0.5']['uwf']:.2f}x), after a chord that stalled at {min(f1['0.5']['chord']):.2e} and drifted up. Outer 1's |U_w^T F| is "
      f"{outs[1]['uwf']:.4e}, {outs[0]['uwf'] / outs[1]['uwf']:.3f}x below outer 0's: the elimination's own stop.")
print("\n### Step 2: root of the iterate (`d18_secant.py run ... --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2`, RAYON_NUM_THREADS=2, `ne_root.jsonl`)\n")
print(f"Bracket from the order's formula: centre 0.0455917 + {SLOPE} x dDelta = {0.0455917 + pred!r}, LO {lo0:.7f}, HI {hi0:.7f} (+-0.004); the run used (0.0396709, 0.0476709). No exit 2, nothing widened.\n")
print("| iterate | evaluations | exit | status | final robust bracket (width) | det-linear root | root - 0.0455917 | Brent end | seconds |")
print("|---|---|---|---|---|---|---|---|---|")
print(f"| ne1 | {x['n_eval']} | {rc} | {x['status']} | [{b[0]!r}, {b[1]!r}] ({x['width']:.3e}) | {root!r} | {S:+.6e} | {x['lam_brent']!r} | {x['sec']} |\n")
print("Evaluations (lambda, hybrid sign, float64 sign, dln, robust, seconds):\n")
print("; ".join(f"{e['lam']!r} {int(e['sign']):+d} {int(e['f64_sign']):+d} {e['dln']:.2e} {'R' if e['robust'] else 'NOT robust'} {e['sec']}" for e in ev))
print("\n### Reading\n")
print("| item | value |\n|---|---|")
print(f"| outer steps run; stop | 2 (outer 0, outer 1); stop line printed: {stop} |")
print(f"| |U_w^T F| outer 0 -> outer 1 | {outs[0]['uwf']:.4e} -> {outs[1]['uwf']:.4e} (bar (a): >= 2x per step to <= 1e-12) |")
print(f"| dDelta of the iterate from R0 | {dD:+.10e} |")
print(f"| root - 0.0455917 | {S:+.6e}; robust range {b[0] - REF:+.4e} to {b[1] - REF:+.4e} |")
print(f"| linear estimate {SLOPE} x dDelta | {pred:+.6e} |")
print(f"| root shift / dDelta | {S / dD:.3f} (w01 0.7868, w10 0.7838; robust range {(b[0] - REF) / dD:.2f} to {(b[1] - REF) / dD:.2f}) |")
print("\n### Failed or disagrees\n")
print(f"- The order's comparison reads \"root - 0.0455917 with -0.785 x dDelta\"; the bracket formula and the w01/w10 ratios (+0.787, +0.784) have the other sign, which I used: +0.785 x dDelta = {pred:+.4e}. With the order's sign the figure would be {-pred:+.4e}, opposite to the root shift {S:+.4e}.")
print(f"- The iterate differs from R0 in more than Delta (|dz| {dz:.3e} against |dDelta| {abs(dD):.3e}: the chord steps on the strong band and the re-frozen RK steps, 4183 against 4179); w01 and w10 moved along R0's weak vector. The two sets of shifts are not like for like; I did not separate the parts.")
print("- Exit 4: the last det-linear point (lambda 0.04031715064433497, dln 2.54) was not robust; its hybrid sign +1 is not trusted. Taken at face value the root lies in [0.04031715064433497, 0.04032159856405092].")
print("- The float64 sign is +1 at 0.04037853 and 0.0403216 where the hybrid sign is -1 (as for w01 and r0); the hybrid sign is the one used.")
print("- Nothing was pushed or posted from this Mac.")
print("\n### Recommended tasks\n")
print(f"- **Roots of the fraction 0.5 and 0.25 iterates (dDelta {f1['0.5']['Delta'] - outs[0]['Delta']:+.3e}, {f1['0.25']['Delta'] - outs[0]['Delta']:+.3e}).** What: `i1101_weakdir.py valley --save` at those fractions (the `ne` run saves only the taken one), then `d18_secant.py run` on each. Why: the root shift over dDelta is 0.78 for pure weak-vector moves and {S / dD:.2f} for the 0.125 iterate; the two further points show whether it grows with dDelta or with the chord corrections. Acceptance: roots with exit 0 or 4, shift / dDelta at each, compared with 0.785 and {S / dD:.2f}. Depends on: R0's `jac` and `svd` files (mm5's stay on its machine, #1109 comment 7232733432; here `jac` takes about 500 s).")
