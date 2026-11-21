#!/usr/bin/env python3
"""#1025 D 18.0625 scan (win2b): planted controls for the two pinned scripts the scan's end uses (winb's merge_d18mid_1025.py b8b47a44 and read_d18mid_1025.py 017ae1da,
raw I1025-win/d18mid, unchanged, in in/). Each case writes synthetic scan files in a fresh directory (left in place) and runs the pinned script as a subprocess; a case passes
when the script's output has the wanted line and not the unwanted one. Exit 0 only if every case passes; the driver stops otherwise.
usage: plant_checks.py PYTHON IN_DIR"""
import json, os, subprocess, sys, tempfile

PY, IN = sys.argv[1], sys.argv[2]
MERGE, READ = os.path.join(IN, "merge_d18mid_1025.py"), os.path.join(IN, "read_d18mid_1025.py")
LAMS = [round(1.70 + 0.01 * i, 2) for i in range(26)]
tmp = tempfile.mkdtemp(prefix="d18mid_plant_")


def rec(lam, sign, ln, robust=True, f64=1.0):
    return dict(D=18.0625, kc=63, lam=lam, sign=float(sign), ln=ln, noise=[float(sign)] * 2, noise_robust=robust, f64_sign=f64, f64_ln=ln + 1.0, state="planted.npy", sec=1)


def put(name, rows):
    f = os.path.join(tmp, name)
    open(f, "w").write("".join(json.dumps(r) + "\n" for r in rows))
    return f


def run(script, *args):
    p = subprocess.run([PY, script, *args], capture_output=True, text=True)
    return p.stdout + p.stderr


def lnf(l):
    return -1900.0 + 3.0 * abs(l - 1.80)            # a planted ln|det| with its minimum at 1.80


def sgn(l, up=(1.775,), down=(1.807,)):                # minus below 1.775, plus up to 1.807, minus above
    return 1 if (up[0] < l < down[0]) else -1


def halves(rep_sign=None, rep_dln=0.0, drop=None):
    A = [rec(1.82, sgn(1.82), lnf(1.82))] + [rec(l, sgn(l), lnf(l)) for l in LAMS if l <= 1.81 and l != drop]
    Bp = [rec(1.82, rep_sign if rep_sign is not None else sgn(1.82), lnf(1.82) + rep_dln)] + [rec(l, sgn(l), lnf(l)) for l in LAMS if l >= 1.83 and l != drop]
    return A, Bp


bad = 0


def check(name, out, want, notwant=None):
    global bad
    ok = want in out and (notwant is None or notwant not in out)
    bad += not ok
    print(f"plant {name}: wanted '{want}'" + (f", not '{notwant}'" if notwant else "") + f" -> {'ok' if ok else 'WRONG'}")
    if not ok:
        print(out)


# merge
A, B = halves()
m = os.path.join(tmp, "m_good.jsonl")
check("merge, repeat equal", run(MERGE, put("a1.jsonl", A), put("b1.jsonl", B), m), "merged 26 points", "FAIL")
check("merge, repeat ln|det| differs by 1e-3", run(MERGE, put("a2.jsonl", halves(rep_dln=1e-3)[0]), put("b2.jsonl", halves(rep_dln=1e-3)[1]), os.path.join(tmp, "m2.jsonl")), "-> FAIL", "merged 26")
check("merge, repeat sign differs", run(MERGE, put("a3.jsonl", halves(rep_sign=-sgn(1.82))[0]), put("b3.jsonl", halves(rep_sign=-sgn(1.82))[1]), os.path.join(tmp, "m3.jsonl")), "-> FAIL", "merged 26")
A4, B4 = halves(); B4 = B4[1:]
check("merge, no repeated point", run(MERGE, put("a4.jsonl", A4), put("b4.jsonl", B4), os.path.join(tmp, "m4.jsonl")), "no repeated point in both files -> FAIL", "merged 26")
A5, B5 = halves(drop=1.95)
check("merge, lambda 1.95 missing", run(MERGE, put("a5.jsonl", A5), put("b5.jsonl", B5), os.path.join(tmp, "m5.jsonl")), "missing lambda: [1.95]", "merged 26")
check("merge, no merged file written when the check fails", str(os.path.exists(os.path.join(tmp, "m2.jsonl")) or os.path.exists(os.path.join(tmp, "m3.jsonl"))), "False")
# reader, on the merged planted scan: minus-to-plus at 1.775 (between 1.77 and 1.78), plus-to-minus at 1.807 (between 1.80 and 1.81), ln|det| minimum at 1.80
out = run(READ, m)
check("reader, planted two changes: first", out, "change in (1.77, 1.78): minus-to-plus, ROBUST")
check("reader, planted two changes: second", out, "change in (1.80, 1.81): plus-to-minus, ROBUST")
check("reader, planted two changes: gap", out, "centre to centre 0.030")
check("reader, planted minimum at 1.80 sits next to the change at (1.80, 1.81)", out, "ln|det| local minimum at 1.80 (ln -1900.000000): beside a change", "WITHOUT a change")
# one point of the first change not robust: the change is listed as not robust and the gap line is absent
rows = [rec(l, sgn(l), lnf(l), robust=(l != 1.78)) for l in LAMS]
out = run(READ, put("r_nr.jsonl", rows))
check("reader, a point of the first change fails its noise test", out, "NOT ROBUST (a point fails its noise test)", "two robust changes")
# orientation flipped
rows = [rec(l, -sgn(l), lnf(l)) for l in LAMS]
out = run(READ, put("r_flip.jsonl", rows))
check("reader, signs negated: orientation swaps", out, "change in (1.77, 1.78): plus-to-minus, ROBUST")
# a ln|det| minimum with no sign change at all
rows = [rec(l, 1, lnf(l)) for l in LAMS]
out = run(READ, put("r_nochange.jsonl", rows))
check("reader, no change, a minimum", out, "no change of the hybrid sign over the window")
check("reader, no change, the minimum is without a change", out, "ln|det| local minimum at 1.80 (ln -1900.000000): WITHOUT a change")
# the real scans of xfkappa (D 18 and D 18.5), as winb tested the reader
out = run(READ, os.path.join(IN, "d18_scan_1025.jsonl"))
check("reader on xfkappa's D 18 scan: lower change", out, "change in (1.77, 1.78): minus-to-plus, ROBUST")
check("reader on xfkappa's D 18 scan: upper change", out, "change in (1.80, 1.81): plus-to-minus, ROBUST")
check("reader on xfkappa's D 18 scan: gap", out, "centre to centre 0.030")
out = run(READ, os.path.join(IN, "d185_scan_1025.jsonl"))
check("reader on xfkappa's D 18.5 scan: one change", out, "change in (1.67, 1.68): minus-to-plus, ROBUST", "two robust changes")
print("plant_checks", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
