#!/usr/bin/env python3
"""#1025 k_c test at D 18.25 (win2b), AMENDED version (the coordinator's tightening of "within 0.02": the det-linear estimate against the k_c 63 root; README Part 3, Amendment 1): planted controls for
kc_compare2.py, merge_fine.py (step 0.02), read_fine.py (step 0.02) and dip_fit2.py on 56-point planted scans (lambda 1.30 to 2.40 at 0.02), and the det-linear estimate of kc_compare2.py against xfkappa's own
`changes()` (d185_scan_read.py, blob 7c9d400f, in/) on a real scan. Each case runs the script as a subprocess on files in a fresh directory (left in place); it passes when the output has the wanted line and
not the unwanted one. Exit 0 only if every case passes. (The first version, plant_checks_d1825_v1.py c98856e2, tested the bracket rule and passed 26 cases at 23:29:08 UTC.)
usage: plant_checks_d1825.py PYTHON HERE_DIR"""
import importlib.util, json, os, subprocess, sys, tempfile

PY, HERE = sys.argv[1], sys.argv[2]
COMP, MERGE, READ, DIP = (os.path.join(HERE, n) for n in ("kc_compare2.py", "merge_fine.py", "read_fine.py", "dip_fit2.py"))
LAMS = [round(1.30 + 0.02 * i, 2) for i in range(56)]
tmp = tempfile.mkdtemp(prefix="d1825_plant_")
R63 = ["--r63", "1.3885,1.7425,2.3187", "--ori63", "plus-to-minus,minus-to-plus,plus-to-minus", "--band", "0.02"]


def rec(lam, sign, ln, robust=True, D=18.25):
    return dict(D=D, kc=55, lam=lam, sign=float(sign), ln=ln, noise=[float(sign)] * 2, noise_robust=robust, f64_sign=1.0, f64_ln=ln + 1.0, state="planted.npy", sec=1)


def put(name, rows):
    f = os.path.join(tmp, name)
    open(f, "w").write("".join(json.dumps(r) + "\n" for r in rows))
    return f


def run(script, *args):
    p = subprocess.run([PY, script, *args], capture_output=True, text=True)
    return p.stdout + p.stderr


bad = 0


def check(name, out, want, notwant=None):
    global bad
    ok = want in out and (notwant is None or notwant not in out)
    bad += not ok
    print(f"plant {name}: wanted '{want}'" + (f", not '{notwant}'" if notwant else "") + f" -> {'ok' if ok else 'WRONG'}")
    if not ok:
        print(out)


def signs(flips, start=+1):
    s, out = start, {}
    for l in LAMS:
        if round(l, 2) in flips:
            s = -s
        out[l] = s
    return out


LN0 = -1900.0
# full(flips, ln_over): constant ln|det| = LN0 except the given points, so a change's det-linear estimate is its bracket's midpoint unless ln_over tilts it


def full(flips, start=+1, ln_over=None, **kw):
    ln_over = ln_over or {}
    return [rec(l, s, ln_over.get(round(l, 2), LN0), **kw) for l, s in signs(flips, start).items()]


C = lambda name, rows, *extra: run(COMP, put(f"c_{name}.jsonl", rows), *(extra or R63))
# (a) the three changes over the three k_c 63 roots; constant ln, so the estimates are the bracket midpoints 1.390, 1.750, 2.310
out = C("all3", full((1.40, 1.76, 2.32)))
check("compare, change (1.38, 1.40): estimate 1.390000, 0.0015 from 1.3885: STABLE", out, "k_c 55 change in (1.380, 1.400), plus-to-minus, ROBUST, det-linear estimate 1.390000: STABLE (the estimate is 0.0015 from the k_c 63 root 1.3885, within 0.02; the k_c 63 root's orientation is plus-to-minus, the same (information)) [information, the bracket reading: the bracket is wholly inside the band 1.3685 to 1.4085 of the k_c 63 root 1.3885]")
check("compare, change (1.74, 1.76): estimate 1.750000: STABLE, orientation minus-to-plus the same", out, "k_c 55 change in (1.740, 1.760), minus-to-plus, ROBUST, det-linear estimate 1.750000: STABLE (the estimate is 0.0075 from the k_c 63 root 1.7425, within 0.02; the k_c 63 root's orientation is minus-to-plus, the same (information))")
check("compare, change (2.30, 2.32): estimate 2.310000: STABLE", out, "k_c 55 change in (2.300, 2.320), plus-to-minus, ROBUST, det-linear estimate 2.310000: STABLE (the estimate is 0.0087 from the k_c 63 root 2.3187")
check("compare, all three k_c 63 roots MATCHED", out, "k_c 63 root 2.3187: MATCHED by the k_c 55 robust change in (2.300, 2.320) (estimate 2.310000, 0.0087 from it)")
check("compare, the summary of three stable, all wholly inside", out, "SUMMARY: 3 robust k_c 55 change(s); stable (the rule): 3 (information, the bracket marks: 3 wholly inside a band, 0 straddling a band edge, 0 outside every band); k_c-dependent: 0 k_c 55 only + 0 k_c 63 only; undetermined 0; not compared 0")
# (b) a bracket straddling the band edge whose estimate is within 0.02: (1.36, 1.38) with equal ln, estimate 1.370, 0.0185 from 1.3885
out = C("straddle_in", full((1.38, 1.76, 2.32)))
check("compare, bracket (1.36, 1.38) straddles the band edge, estimate 1.370000 is 0.0185 from 1.3885: STABLE, mark straddling", out, "k_c 55 change in (1.360, 1.380), plus-to-minus, ROBUST, det-linear estimate 1.370000: STABLE (the estimate is 0.0185 from the k_c 63 root 1.3885, within 0.02; the k_c 63 root's orientation is plus-to-minus, the same (information)) [information, the bracket reading: the bracket straddles the band edge, 0.0085 from the k_c 63 root 1.3885")
# (c) THE AMENDMENT CASE: the same bracket (1.36, 1.38) within 0.02 of the root by the bracket rule, but the det-linear estimate 1.36095 is 0.0276 away: k_c-DEPENDENT now
out = C("amend", full((1.38, 1.76, 2.32), ln_over={1.36: LN0 - 3.0}))
check("compare, THE AMENDMENT: bracket (1.36, 1.38) straddles the band but the estimate 1.360949 is 0.0276 from 1.3885: k_c-DEPENDENT", out, "k_c 55 change in (1.360, 1.380), plus-to-minus, ROBUST, det-linear estimate 1.360949: k_c-DEPENDENT (k_c 55 only: the estimate is 0.0276 from the nearest k_c 63 root 1.3885, farther than 0.02) [information, the bracket reading: the bracket straddles the band edge, 0.0085 from the k_c 63 root 1.3885", "STABLE (the estimate is 0.0276")
check("compare, the amendment case: the k_c 63 root 1.3885 is then k_c 63 only", out, "k_c 63 root 1.3885: k_c-DEPENDENT (k_c 63 only: no k_c 55 change, robust or not, has its det-linear estimate within 0.02 of it)")
check("compare, the amendment case: the summary", out, "stable (the rule): 2 (information, the bracket marks: 2 wholly inside a band, 0 straddling a band edge, 0 outside every band); k_c-dependent: 1 k_c 55 only + 1 k_c 63 only")
# (d) the opposite tilt: the bracket (1.34, 1.36) is 0.0285 from the root by the bracket, estimate pulled to the high end 1.35905 is still 0.0295 away: dependent; and a far change
out = C("far", full((1.64, 1.76, 2.32)))
check("compare, change (1.62, 1.64): estimate 1.630000 is 0.1125 from the nearest k_c 63 root 1.7425: k_c-DEPENDENT (k_c 55 only)", out, "k_c 55 change in (1.620, 1.640), plus-to-minus, ROBUST, det-linear estimate 1.630000: k_c-DEPENDENT (k_c 55 only: the estimate is 0.1125 from the nearest k_c 63 root 1.7425, farther than 0.02) [information, the bracket reading: the bracket is outside the band, 0.1025 from the nearest k_c 63 root 1.7425]")
check("compare, the root 1.3885 has no k_c 55 change near it: k_c 63 only", out, "k_c 63 root 1.3885: k_c-DEPENDENT (k_c 63 only")
out = C("none", full(()))
check("compare, no change at all: three k_c 63 only", out, "k_c-dependent: 0 k_c 55 only + 3 k_c 63 only; undetermined 0; not compared 0")
# (e) a non-robust point at the change near 1.3885: listed with its estimate, not counted; the root is UNDETERMINED
out = C("nr", full((1.40, 1.76, 2.32), robust=True)[:0] + [rec(l, s, LN0, robust=(l != 1.40)) for l, s in signs((1.40, 1.76, 2.32)).items()])
check("compare, a non-robust point at the change near 1.3885: not counted, with its estimate", out, "k_c 55 change in (1.380, 1.400), plus-to-minus, NOT ROBUST (a point fails its noise test), not counted, det-linear estimate 1.390000", "STABLE (the estimate is 0.0015")
check("compare, the root 1.3885 with only a non-robust change near it: UNDETERMINED", out, "k_c 63 root 1.3885: UNDETERMINED (only non-robust k_c 55 change(s) with the estimate within 0.02: (1.380, 1.400) estimate 1.390000)")
# (f) coverage and orientation
out = run(COMP, put("c_cov.jsonl", full((1.40, 1.76, 2.32))), *R63, "--cov63", "1.20,2.25")
check("compare, a k_c 55 change above the k_c 63 coverage is not compared", out, "det-linear estimate 2.310000: not compared (k_c 63 is not scanned over this bracket", "k_c-DEPENDENT (k_c 55 only")
out = C("opp", full((1.40, 1.76, 2.32), start=-1))
check("compare, the orientation of the k_c 55 change is the opposite of the k_c 63 root's: printed", out, "the k_c 63 root's orientation is plus-to-minus, the opposite (information)")
# (g) the estimate against xfkappa's own code on a real scan (the k_c 63 D 18.5 scan, one change in (1.67, 1.68), det-linear 1.677016)
real = os.path.join(HERE, "in", "kc63_d185_merged_1.55-2.40.jsonl")
spec = importlib.util.spec_from_file_location("d185_scan_read", os.path.join(HERE, "in", "d185_scan_read.py"))
mod = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0]]; spec.loader.exec_module(mod)
S = [json.loads(l) for l in open(real) if l.strip()]
rob, non = mod.changes(sorted(S, key=lambda r: r["lam"]))
xl = [c["lin"] for c in rob]
out = run(COMP, real, "--r63", "1.6772", "--band", "0.02")
mine = [float(w.split("estimate ")[1].split(":")[0]) for w in out.splitlines() if w.startswith("k_c 55 change") and "det-linear estimate" in w]
ok = len(xl) == len(mine) == 1 and abs(xl[0] - mine[0]) < 5e-7
bad += not ok
print(f"plant estimate against xfkappa's changes() on the k_c 63 D 18.5 scan: his lin {xl}, this script's {mine} -> {'ok' if ok else 'WRONG'}")
check("compare on the k_c 63 D 18.5 scan itself: det-linear estimate 1.677016 is STABLE against 1.6772", out, "det-linear estimate 1.677016: STABLE (the estimate is 0.0002 from the k_c 63 root 1.6772, within 0.02")
# (h) merge_fine at step 0.02, the reader at step 0.02 and the dip fit, as before
M = ("1.30", "56", "0.02", "1.86", "18.25")
none = os.path.join(tmp, "no_prior.jsonl")


def halves(rep_dln=0.0, drop=None, flips=(1.40, 1.76, 2.32)):
    sg = signs(flips)
    A = [rec(1.86, sg[1.86], LN0)] + [rec(l, sg[l], LN0) for l in LAMS if l < 1.86 and l != drop]
    B = [rec(1.86, sg[1.86], LN0 + rep_dln)] + [rec(l, sg[l], LN0) for l in LAMS if l > 1.86 and l != drop]
    return A, B


A, B = halves()
m = os.path.join(tmp, "m_good.jsonl")
out = run(MERGE, *M, put("a1.jsonl", A), put("b1.jsonl", B), m, none)
check("merge at step 0.02, repeat equal", out, "merged 56 points (1.300 to 2.400)", "-> FAIL")
check("merge at step 0.02: no prior scan, no PRIOR line", out, "REPEAT CHECK at lambda 1.860", "PRIOR SCAN")
A2, B2 = halves(rep_dln=1e-3)
check("merge at step 0.02, repeat ln|det| differs by 1e-3", run(MERGE, *M, put("a2.jsonl", A2), put("b2.jsonl", B2), os.path.join(tmp, "m2.jsonl"), none), "-> FAIL", "merged 56")
A3, B3 = halves(drop=2.40)
check("merge at step 0.02, lambda 2.40 missing", run(MERGE, *M, put("a3.jsonl", A3), put("b3.jsonl", B3), os.path.join(tmp, "m3.jsonl"), none), "missing lambda: [2.4]", "merged 56")
out = run(READ, m, "--step", "0.02")
check("reader at step 0.02: the first change", out, "change in (1.38, 1.40): plus-to-minus, ROBUST")
check("reader at step 0.02: the third change", out, "change in (2.30, 2.32): plus-to-minus, ROBUST")
out = run(DIP, "selftest")
check("dip fit: its own planted truths and minimum finder pass", out, "selftest passes")
import numpy as np
mdl = lambda l: -1597.0 + np.log((l - 1.906) ** 2 + 0.06 ** 2) + 4.9 * (l - 1.906) - 13.0 * (l - 1.906) ** 2     # a root pair 1.906 +- 0.06 i, no sign change
rows = [rec(l, +1, float(mdl(l))) for l in LAMS]
out = run(DIP, put("d_dip.jsonl", rows))
check("dip fit on a planted complex-pair dip near 1.906 without a change: found", out, "ln|det| local minima WITHOUT a change: [1.9]")
check("dip fit on the planted dip: l0 recovered (1.906, e 0.06)", out, "l0 1.9060")
check("dip fit on the planted dip: e recovered and resolved", out, "e 0.0600", "NOT RESOLVED at this step")
V = lambda l: -1900.0 + 30.0 * abs(l - 1.90)
out = run(DIP, put("d_nodip.jsonl", [rec(l, s, V(l)) for l, s in signs((1.90,)).items()]))
check("dip fit on a scan whose minimum is beside a change: none to fit", out, "ln|det| local minima WITHOUT a change: none")
print("plant_checks_d1825", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
