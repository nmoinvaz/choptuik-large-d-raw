#!/usr/bin/env python3
"""#1025 k_c test at D 18.25 (win2b): planted controls for kc_compare2.py, merge_fine.py (step 0.02), read_fine.py (step 0.02) and dip_fit2.py on 56-point planted scans (lambda 1.30 to 2.40 at 0.02).
Each case runs the script as a subprocess on files in a fresh directory (left in place); it passes when the output has the wanted line and not the unwanted one. Exit 0 only if every case passes; the driver
does not start the scan otherwise.
usage: plant_checks_d1825.py PYTHON HERE_DIR"""
import json, os, subprocess, sys, tempfile

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


lnf = lambda l: -1900.0 + 30.0 * abs(l - 1.90)               # a V at 1.90 (no sign change there unless flipped)
full = lambda flips, start=+1, **kw: [rec(l, s, lnf(l), **kw) for l, s in signs(flips, start).items()]
N = lambda name, flips, *extra, start=+1, **kw: run(COMP, put(f"c_{name}.jsonl", full(flips, start, **kw)), *(extra or R63))
# all three k_c 63 roots matched, brackets wholly inside the bands
out = N("all3", (1.40, 1.76, 2.32))
check("compare, change (1.38, 1.40) wholly inside the band of 1.3885: STABLE", out, "k_c 55 change in (1.380, 1.400), plus-to-minus, ROBUST: STABLE (the bracket is wholly inside the band 1.3685 to 1.4085 of the k_c 63 root 1.3885; the k_c 63 root's orientation is plus-to-minus, the same (information))")
check("compare, change (1.74, 1.76): STABLE, orientation the same", out, "k_c 55 change in (1.740, 1.760), minus-to-plus, ROBUST: STABLE (the bracket is wholly inside the band 1.7225 to 1.7625 of the k_c 63 root 1.7425; the k_c 63 root's orientation is minus-to-plus, the same (information))")
check("compare, change (2.30, 2.32): STABLE", out, "k_c 55 change in (2.300, 2.320), plus-to-minus, ROBUST: STABLE (the bracket is wholly inside the band 2.2987 to 2.3387 of the k_c 63 root 2.3187")
check("compare, all three k_c 63 roots MATCHED", out, "k_c 63 root 2.3187: MATCHED by the k_c 55 robust change in (2.300, 2.320) (wholly inside its band)")
check("compare, the summary of three wholly stable", out, "SUMMARY: 3 robust k_c 55 change(s); stable: 3 wholly inside a band + 0 straddling a band edge; k_c-dependent: 0 k_c 55 only + 0 k_c 63 only; undetermined 0; not compared 0")
# a bracket straddling the band edge: (1.36, 1.38) is 0.0085 from 1.3885, within 0.02, but not wholly inside [1.3685, 1.4085]
out = N("straddle", (1.38, 1.76, 2.32))
check("compare, change (1.36, 1.38) straddles the band edge: STABLE by the rule, marked", out, "k_c 55 change in (1.360, 1.380), plus-to-minus, ROBUST: STABLE (within 0.02 of the k_c 63 root 1.3885: distance 0.0085 from the bracket, which straddles the band edge, so the root may be up to 0.0285 from it", "wholly inside the band 1.3685")
check("compare, the straddling case is counted separately", out, "stable: 2 wholly inside a band + 1 straddling a band edge")
# k_c 55 only and k_c 63 only
out = N("dep", (1.64, 1.76, 2.32))
check("compare, change (1.62, 1.64) is 0.1025 from the nearest k_c 63 root: k_c-DEPENDENT (k_c 55 only)", out, "k_c 55 change in (1.620, 1.640), plus-to-minus, ROBUST: k_c-DEPENDENT (k_c 55 only: no k_c 63 root within 0.02; the nearest k_c 63 root 1.7425 is 0.1025 from the bracket)")
check("compare, the root 1.3885 has no k_c 55 change within 0.02: k_c-DEPENDENT (k_c 63 only)", out, "k_c 63 root 1.3885: k_c-DEPENDENT (k_c 63 only: no k_c 55 change, robust or not, within 0.02 of it)")
check("compare, the summary of dependent", out, "k_c-dependent: 1 k_c 55 only + 1 k_c 63 only")
out = N("none", ())
check("compare, no change at all: three k_c 63 only", out, "k_c-dependent: 0 k_c 55 only + 3 k_c 63 only; undetermined 0; not compared 0")
out = run(COMP, put("c_nr.jsonl", [rec(l, s, lnf(l), robust=(l != 1.40)) for l, s in signs((1.40, 1.76, 2.32)).items()]), *R63)
check("compare, a non-robust point at the change near 1.3885: not counted", out, "NOT ROBUST (a point fails its noise test), not counted", "k_c 55 change in (1.380, 1.400), plus-to-minus, ROBUST")
check("compare, the root 1.3885 with only a non-robust change near it: UNDETERMINED", out, "k_c 63 root 1.3885: UNDETERMINED (only non-robust k_c 55 change(s) within 0.02: (1.380, 1.400))")
out = run(COMP, put("c_cov.jsonl", full((1.40, 1.76, 2.32))), *R63, "--cov63", "1.20,2.25")
check("compare, a k_c 55 change above the k_c 63 coverage is not compared", out, "k_c 55 change in (2.300, 2.320), plus-to-minus, ROBUST: not compared (k_c 63 is not scanned over this bracket", "k_c-DEPENDENT (k_c 55 only")
out = N("opp", (1.40, 1.76, 2.32), start=-1)
check("compare, the orientation of the k_c 55 change is the opposite of the k_c 63 root's: printed", out, "the k_c 63 root's orientation is plus-to-minus, the opposite (information)")
# merge_fine at step 0.02
M = ("1.30", "56", "0.02", "1.86", "18.25")
none = os.path.join(tmp, "no_prior.jsonl")


def halves(rep_dln=0.0, drop=None, flips=(1.40, 1.76, 2.32)):
    sg = signs(flips)
    A = [rec(1.86, sg[1.86], lnf(1.86))] + [rec(l, sg[l], lnf(l)) for l in LAMS if l < 1.86 and l != drop]
    B = [rec(1.86, sg[1.86], lnf(1.86) + rep_dln)] + [rec(l, sg[l], lnf(l)) for l in LAMS if l > 1.86 and l != drop]
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
# read_fine at step 0.02 on the merged planted scan, and the dip fit's own selftest
out = run(READ, m, "--step", "0.02")
check("reader at step 0.02: the first change", out, "change in (1.38, 1.40): plus-to-minus, ROBUST")
check("reader at step 0.02: the third change", out, "change in (2.30, 2.32): plus-to-minus, ROBUST")
out = run(DIP, "selftest")
check("dip fit: its own planted truths and minimum finder pass", out, "selftest passes")
sys.path.insert(0, HERE)
import numpy as np
mdl = lambda l: -1597.0 + np.log((l - 1.906) ** 2 + 0.06 ** 2) + 4.9 * (l - 1.906) - 13.0 * (l - 1.906) ** 2     # a root pair 1.906 +- 0.06 i, no sign change
rows = [rec(l, +1, float(mdl(l))) for l in LAMS]
out = run(DIP, put("d_dip.jsonl", rows))
check("dip fit on a planted complex-pair dip near 1.906 without a change: found", out, "ln|det| local minima WITHOUT a change: [1.9]")
check("dip fit on the planted dip: l0 recovered (1.906, e 0.06)", out, "l0 1.9060")
check("dip fit on the planted dip: e recovered and resolved", out, "e 0.0600", "NOT RESOLVED at this step")
out = run(DIP, put("d_nodip.jsonl", full((1.90,))))
check("dip fit on a scan whose minimum is beside a change: none to fit", out, "ln|det| local minima WITHOUT a change: none")
print("plant_checks_d1825", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
