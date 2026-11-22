#!/usr/bin/env python3
"""#1025 win2b, where the k_c-stable branch of lambda_1 breaks: the D 18.375 scans at k_c 55 and k_c 63 (the coordinator's reading, fixed before the run): the k_c 55 root's det-linear estimate within 0.01 of the
k_c 63 root's means the root is stable at D 18.375; no k_c 55 root in the window, or one further off, means it breaks by D 18.375.
usage: kc_break_compare.py SCAN55.jsonl SCAN63.jsonl [--tol 0.01]
Definitions. A root is a ROBUST change of the hybrid sign (two consecutive points of different sign, both passing the 1e-15 noise test); its det-linear estimate `lin` and its estimator range (the span of four estimates,
information) are computed by `changes()` of xfkappa's d185_scan_read.py (raw I1025-mac/d18, blob 7c9d400f, in/), the same code d18f_read.py uses. A change that touches a non-robust point is listed and not counted.
For each k_c 63 root: the nearest k_c 55 robust change by estimate, difference d = lin(k_c 55) - lin(k_c 63) (the sign is printed); |d| <= TOL: STABLE at this D; |d| > TOL: BREAKS (the k_c 55 root is further off);
no k_c 55 robust change: BREAKS (no k_c 55 root in the window). No k_c 63 root: reported, not covered by the fixed reading. More than one k_c 63 root: each is paired and reported, the overall line says OTHER (the fixed
reading is for one root). A k_c 55 robust change paired with no k_c 63 root is listed. Orientation is printed as information and not used (orientation readings wait for xfkappa's sign-convention check)."""
import importlib.util, json, os, sys
import numpy as np
args = sys.argv[1:]
tol = 0.01
if "--tol" in args:
    i = args.index("--tol"); tol = float(args[i + 1]); del args[i:i + 2]
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("d185_scan_read", os.path.join(here, "in", "d185_scan_read.py"))
mod = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0]]; spec.loader.exec_module(mod)


def load(fn):
    return sorted((json.loads(l) for l in open(fn) if l.strip()), key=lambda r: r["lam"])


def ori(S, br):
    a = [r for r in S if abs(r["lam"] - br[0]) < 1e-9][0]
    return "minus-to-plus" if a["sign"] < 0 else "plus-to-minus"


S55, S63 = load(args[0]), load(args[1])
f3 = lambda x: f"{x:.3f}"
print(f"D {S55[0]['D']}: k_c 55 scan {len(S55)} points (lambda {f3(S55[0]['lam'])} to {f3(S55[-1]['lam'])}), k_c 63 scan {len(S63)} points (lambda {f3(S63[0]['lam'])} to {f3(S63[-1]['lam'])}); "
      f"rule: the k_c 55 root's det-linear estimate within {tol} of the k_c 63 root's")
res = {}
for name, S in (("k_c 63", S63), ("k_c 55", S55)):
    rob, non = mod.changes(S)
    res[name] = rob
    for c in rob:
        print(f"{name} robust change in ({f3(c['br'][0])}, {f3(c['br'][1])}), {ori(S, c['br'])}: det-linear estimate {c['lin']:.6f}, estimator range [{c['lo']:.6f}, {c['hi']:.6f}] ({c['n_est']} estimates)")
    for c in non:
        print(f"{name} change in ({f3(c['br'][0])}, {f3(c['br'][1])}), {ori(S, c['br'])}: NOT ROBUST (a point fails its noise test), not counted, det-linear estimate {c['lin']:.6f}")
    if not rob and not non:
        print(f"{name}: no change of the hybrid sign over the window")
r63, r55 = res["k_c 63"], res["k_c 55"]
verd = []
used = set()
for c in r63:
    mid = c["lin"]
    if not r55:
        print(f"PAIRING k_c 63 root {mid:.6f}: no k_c 55 robust change in the window -> BREAKS (no k_c 55 root there)")
        verd.append("BREAKS"); continue
    j = min(range(len(r55)), key=lambda k: abs(r55[k]["lin"] - mid))
    used.add(j)
    d = r55[j]["lin"] - mid
    o63, o55 = ori(S63, c["br"]), ori(S55, r55[j]["br"])
    ov = "overlap" if not (r55[j]["hi"] < c["lo"] or c["hi"] < r55[j]["lo"]) else "do not overlap"
    v = "STABLE" if abs(d) <= tol + 1e-12 else "BREAKS"
    verd.append(v)
    print(f"PAIRING k_c 63 root {mid:.6f} (bracket ({f3(c['br'][0])}, {f3(c['br'][1])}), {o63}) with the nearest k_c 55 robust change in ({f3(r55[j]['br'][0])}, {f3(r55[j]['br'][1])}), {o55}, estimate {r55[j]['lin']:.6f}: "
          f"k_c 55 minus k_c 63 = {d:+.6f} -> {v}" + (f" ({'within' if v == 'STABLE' else 'beyond'} {tol}; the k_c 55 root is further off)" if v == "BREAKS" else f" (within {tol})")
          + f". Information: orientation {'the same' if o63 == o55 else 'the opposite'}; the estimator ranges {ov}")
for j, c in enumerate(r55):
    if j not in used:
        print(f"k_c 55 robust change in ({f3(c['br'][0])}, {f3(c['br'][1])}), estimate {c['lin']:.6f}: paired with no k_c 63 root")
if not r63:
    print("NO k_c 63 ROOT in the window: the fixed reading does not cover this")
if len(r63) == 1:
    print(f"READING: {'the root is STABLE at D 18.375 (the k_c 55 estimate within ' + str(tol) + ' of the k_c 63 root)' if verd[0] == 'STABLE' else 'the root BREAKS by D 18.375 (' + ('no k_c 55 root in the window' if not r55 else 'the k_c 55 root is further off than ' + str(tol)) + ')'}")
else:
    print(f"READING: OTHER, {len(r63)} k_c 63 robust change(s) (the fixed reading is for one root); pairings {verd}")
print(f"SUMMARY: k_c 63 {len(r63)} robust change(s), k_c 55 {len(r55)} robust change(s); verdicts {verd}")
