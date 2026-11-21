#!/usr/bin/env python3
"""#1025 finer D 18.5 scan at k_c 55 (win2b): planted controls for merge_fine.py and read_fine.py on 21-point planted scans (lambda 1.660 to 1.700 at 0.002), and read_fine.py against winb's pinned
reader (read_d18mid_1025.py, blob 017ae1da) on three real 0.01 scans (the k_c 55 and k_c 63 D 18.5 scans and xfkappa's D 18 scan): the same changes, the same minima, and xfkappa's det-linear
estimate 1.677016 on the k_c 63 scan. Each case runs the script as a subprocess on files in a fresh directory (left in place); it passes when the output has the wanted line and not the unwanted one.
Exit 0 only if every case passes; the driver does not start the scan otherwise.
usage: plant_checks_fine.py PYTHON IN_DIR HERE_DIR"""
import json, os, re, subprocess, sys, tempfile

PY, IN, HERE = sys.argv[1], sys.argv[2], sys.argv[3]
MERGE, READ, PINNED = os.path.join(HERE, "merge_fine.py"), os.path.join(HERE, "read_fine.py"), os.path.join(IN, "read_d18mid_1025.py")
LAMS = [round(1.660 + 0.002 * i, 3) for i in range(21)]
tmp = tempfile.mkdtemp(prefix="kc55fine_plant_")


def rec(lam, sign, ln, robust=True, D=18.5):
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


def signs(flips, lams=LAMS):
    s, out = -1, {}
    for l in lams:
        if round(l, 3) in flips:
            s = -s
        out[l] = s
    return out


lnv = lambda l: -1605.0 + 800.0 * abs(l - 1.680)             # a V with its minimum at 1.680
full = lambda flips, **kw: [rec(l, s, lnv(l), **kw) for l, s in signs(flips).items()]


def halves(flips=(), rep_sign=None, rep_dln=0.0, drop=None, D=18.5):
    sg = signs(flips)
    A = [rec(1.680, sg[1.68], lnv(1.680), D=D)] + [rec(l, sg[l], lnv(l), D=D) for l in LAMS if l < 1.680 and l != drop]
    B = [rec(1.680, rep_sign if rep_sign is not None else sg[1.68], lnv(1.680) + rep_dln, D=D)] + [rec(l, sg[l], lnv(l), D=D) for l in LAMS if l > 1.680 and l != drop]
    return A, B


M = ("1.660", "21", "0.002", "1.680", "18.5")
prior = put("prior.jsonl", [rec(1.66, -1, -1604.311), rec(1.68, -1, lnv(1.680)), rec(1.70, -1, -1604.727)])
A, B = halves()
m = os.path.join(tmp, "m_good.jsonl")
out = run(MERGE, *M, put("a1.jsonl", A), put("b1.jsonl", B), m, prior)
check("merge, repeat equal", out, "merged 21 points (1.660 to 1.700)", "-> FAIL")
check("merge, the prior scan: 1.680 agrees (the planted ln is the same)", out, "PRIOR SCAN at lambda 1.680 (the 0.01 scan, D 18.5): sign -1 against -1; ln|det| -1605.0 against -1605.0, difference 0.000e+00 (bar 1e-6) -> AGREES")
check("merge, the prior scan: 1.660 differs (planted ln -1604.311 against the V's -1605.0+16=-1589)", out, "PRIOR SCAN at lambda 1.660 (the 0.01 scan, D 18.5): sign -1 against -1;", "no merged")
check("merge, a prior value that differs is DIFFERS", out, "-> DIFFERS (information, not a gate)")
A2, B2 = halves(rep_dln=1e-3)
check("merge, repeat ln|det| differs by 1e-3", run(MERGE, *M, put("a2.jsonl", A2), put("b2.jsonl", B2), os.path.join(tmp, "m2.jsonl"), prior), "-> FAIL", "merged 21")
A3, B3 = halves(rep_sign=+1)
check("merge, repeat sign differs", run(MERGE, *M, put("a3.jsonl", A3), put("b3.jsonl", B3), os.path.join(tmp, "m3.jsonl"), prior), "-> FAIL", "merged 21")
A4, B4 = halves(); B4 = B4[1:]
check("merge, no repeated point", run(MERGE, *M, put("a4.jsonl", A4), put("b4.jsonl", B4), os.path.join(tmp, "m4.jsonl"), prior), "no repeated point in both files -> FAIL", "merged 21")
A5, B5 = halves(drop=1.700)
check("merge, lambda 1.700 missing", run(MERGE, *M, put("a5.jsonl", A5), put("b5.jsonl", B5), os.path.join(tmp, "m5.jsonl"), prior), "missing lambda: [1.7]", "merged 21")
A6, B6 = halves(D=19.0)
check("merge, records at another D", run(MERGE, *M, put("a6.jsonl", A6), put("b6.jsonl", B6), os.path.join(tmp, "m6.jsonl"), prior), "records at a D other than 18.5", "merged 21")
A7, B7 = halves(); A7.append(dict(B7[1]))
check("merge, a second point in both files", run(MERGE, *M, put("a7.jsonl", A7), put("b7.jsonl", B7), os.path.join(tmp, "m7.jsonl"), prior), "are [1.68, 1.682], not [1.68] -> FAIL", "merged 21")
check("merge, no merged file written when a check fails", str(any(os.path.exists(os.path.join(tmp, n)) for n in ("m2.jsonl", "m3.jsonl", "m4.jsonl", "m5.jsonl", "m6.jsonl", "m7.jsonl"))), "False")
# read_fine on planted scans (--ends -,- : the 0.01 scan's endpoint signs)
R = lambda flips, *extra, **kw: run(READ, put(f"r_{'_'.join(map(str, flips)) or 'none'}_{len(os.listdir(tmp))}.jsonl", full(flips, **kw)), "--ends", "-,-", *extra)
out = R((1.676, 1.684))
check("reader, a planted pair: the first change", out, "change in (1.674, 1.676): minus-to-plus, ROBUST")
check("reader, a planted pair: the second change", out, "change in (1.682, 1.684): plus-to-minus, ROBUST")
check("reader, a planted pair: positions and gap", out, "FINE READING: PAIR. Two robust changes inside the window: minus-to-plus in (1.674, 1.676) and plus-to-minus in (1.682, 1.684); gap between the brackets 0.006 to 0.010, centre to centre 0.0080")
check("reader, a planted pair: the endpoints are consistent", out, "-> consistent")
out = R(())
check("reader, no change, a V minimum at 1.680: a near miss, resolved", out, "FINE READING: NEAR MISS. No robust change; the ln|det| minimum is resolved: an interior local minimum WITHOUT a change at 1.680")
check("reader, no change: the minimum's depth is printed", out, "ln|det| local minimum at 1.680 (ln -1605.000000): WITHOUT a change (below the left neighbour by 1.6000, the right by 1.6000)")
rows = [rec(l, -1, -1600.0 + 100.0 * (l - 1.66)) for l in LAMS]                 # ln rising from the left edge: the minimum is at the edge
out = run(READ, put("r_edge.jsonl", rows), "--ends", "-,-")
check("reader, no change, the minimum at the scan edge: not resolved", out, "FINE READING: NO CHANGE, MINIMUM NOT RESOLVED", "NEAR MISS")
out = R((1.680,))
check("reader, one change only: OTHER, not covered", out, "FINE READING: OTHER. 1 robust change(s) inside the window; the fixed reading covers 0 and 2", "PAIR")
check("reader, one change only: the endpoint signs are inconsistent with the 0.01 scan", out, "-> INCONSISTENT")
out = R((1.668, 1.672, 1.688, 1.692))
check("reader, four changes: OTHER", out, "FINE READING: OTHER. 4 robust change(s)", "PAIR")
out = run(READ, put("r_nr.jsonl", [rec(l, s, lnv(l), robust=(l != 1.676)) for l, s in signs((1.676, 1.684)).items()]), "--ends", "-,-")
check("reader, a pair with a non-robust point: one change is not counted, so OTHER", out, "NOT ROBUST (a point fails its noise test)", "PAIR")
check("reader, the non-robust change is noted", out, "(1 non-robust change(s) not counted)")
rows = [r for r in full((1.676, 1.684)) if abs(r["lam"] - 1.670) > 1e-9]
check("reader, a grid gap is flagged", run(READ, put("r_gap.jsonl", rows), "--ends", "-,-"), "GRID GAPS")
# against the pinned reader on real 0.01 scans
for name, fn in (("the k_c 55 D 18.5 scan", os.path.join(HERE, "scan_merged.jsonl")), ("the k_c 63 D 18.5 scan (merged, 1.55 to 2.40)", os.path.join(IN, "kc63_d185_merged_1.55-2.40.jsonl")),
                 ("xfkappa's D 18 scan", os.path.join(IN, "d18_scan_1025.jsonl"))):
    po, mo = run(PINNED, fn), run(READ, fn, "--step", "0.01")
    pc = [l for l in po.splitlines() if l.startswith("change in")]
    mc = [l for l in mo.splitlines() if l.startswith("change in")]
    pm = [l for l in po.splitlines() if l.startswith("ln|det| local minimum")]
    mm = [l for l in mo.splitlines() if l.startswith("ln|det| local minimum")]
    ok = len(pc) == len(mc) and all(m.startswith(p) for p, m in zip(pc, mc)) and len(pm) == len(mm) and all(m.startswith(p) for p, m in zip(pm, mm)) and (len(pc) + len(pm)) > 0
    bad += not ok
    print(f"plant read_fine against the pinned reader on {name}: {len(pc)} change line(s) and {len(pm)} minimum line(s) the same -> {'ok' if ok else 'WRONG'}")
    if not ok:
        print(po, mo, sep="\n")
out = run(READ, os.path.join(IN, "kc63_d185_merged_1.55-2.40.jsonl"), "--step", "0.01")
check("reader on the k_c 63 D 18.5 scan: xfkappa's det-linear estimate", out, "det-linear estimate 1.677016")
print("plant_checks_fine", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
