#!/usr/bin/env python3
"""#1025 D 18.0625 scan above the first window (win2b): planted controls for merge_up.py, rate_up.py and winb's pinned reader read_d18mid_1025.py (blob 017ae1da) on 41-point
planted scans (lambda 1.95 to 2.35), and the reader again on xfkappa's D 18 and D 18.5 scans. Each case runs the script as a subprocess on files in a fresh directory (left in place);
it passes when the output has the wanted line and not the unwanted one. Exit 0 only if every case passes; the driver does not start the scan otherwise.
usage: plant_checks_up.py PYTHON IN_DIR HERE_DIR"""
import json, os, subprocess, sys, tempfile

PY, IN, HERE = sys.argv[1], sys.argv[2], sys.argv[3]
MERGE, RATE, READ = os.path.join(HERE, "merge_up.py"), os.path.join(HERE, "rate_up.py"), os.path.join(IN, "read_d18mid_1025.py")
LAMS = [round(1.95 + 0.01 * i, 2) for i in range(41)]
tmp = tempfile.mkdtemp(prefix="d18up_plant_")


def rec(lam, sign, ln, robust=True, D=18.0625):
    return dict(D=D, kc=63, lam=lam, sign=float(sign), ln=ln, noise=[float(sign)] * 2, noise_robust=robust, f64_sign=1.0, f64_ln=ln + 1.0, state="planted.npy", sec=1)


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


up = lambda l: 1 if l <= 2.10 else -1                 # plus up to 2.10, minus from 2.11: a plus-to-minus change in (2.10, 2.11)
lnv = lambda l: -1900.0 + 3.0 * abs(l - 2.15)         # a V with its minimum at 2.15


def halves(rep_sign=None, rep_dln=0.0, drop=None, D=18.0625, f=up):
    A = [rec(1.95, f(1.95), lnv(1.95), D=D)] + [rec(l, f(l), lnv(l), D=D) for l in LAMS if 1.95 < l <= 2.15 and l != drop]
    B = [rec(1.95, rep_sign if rep_sign is not None else f(1.95), lnv(1.95) + rep_dln, D=D)] + [rec(l, f(l), lnv(l), D=D) for l in LAMS if l >= 2.16 and l != drop]
    return A, B


prior_ok = put("prior_ok.jsonl", [rec(1.94, 1, -1900.1, D=18.0625), rec(1.95, 1, lnv(1.95), D=18.0625)])
prior_bad = put("prior_bad.jsonl", [rec(1.95, 1, lnv(1.95) + 5e-3, D=18.0625)])
A, B = halves()
m = os.path.join(tmp, "m_good.jsonl")
out = run(MERGE, put("a1.jsonl", A), put("b1.jsonl", B), m, prior_ok)
check("merge, repeat equal", out, "merged 41 points (1.95 to 2.35)", "FAIL")
check("merge, the prior scan agrees", out, "-> AGREES (information, not a gate)")
check("merge, the prior scan differs by 5e-3: reported, the merge still written", run(MERGE, put("a1b.jsonl", A), put("b1b.jsonl", B), os.path.join(tmp, "m_pd.jsonl"), prior_bad), "-> DIFFERS (information, not a gate)", "no merged scan")
A2, B2 = halves(rep_dln=1e-3)
check("merge, repeat ln|det| differs by 1e-3", run(MERGE, put("a2.jsonl", A2), put("b2.jsonl", B2), os.path.join(tmp, "m2.jsonl"), prior_ok), "-> FAIL", "merged 41")
A3, B3 = halves(rep_sign=-1)
check("merge, repeat sign differs", run(MERGE, put("a3.jsonl", A3), put("b3.jsonl", B3), os.path.join(tmp, "m3.jsonl"), prior_ok), "-> FAIL", "merged 41")
A4, B4 = halves(); B4 = B4[1:]
check("merge, no repeated point", run(MERGE, put("a4.jsonl", A4), put("b4.jsonl", B4), os.path.join(tmp, "m4.jsonl"), prior_ok), "no repeated point in both files -> FAIL", "merged 41")
A5, B5 = halves(drop=2.35)
check("merge, lambda 2.35 missing", run(MERGE, put("a5.jsonl", A5), put("b5.jsonl", B5), os.path.join(tmp, "m5.jsonl"), prior_ok), "missing lambda: [2.35]", "merged 41")
A6, B6 = halves(D=18.125)
check("merge, records at another D", run(MERGE, put("a6.jsonl", A6), put("b6.jsonl", B6), os.path.join(tmp, "m6.jsonl"), prior_ok), "records at a D other than 18.0625", "merged 41")
A7, B7 = halves(); A7.append(rec(2.16, up(2.16), lnv(2.16)))
check("merge, a second point in both files", run(MERGE, put("a7.jsonl", A7), put("b7.jsonl", B7), os.path.join(tmp, "m7.jsonl"), prior_ok), "are [1.95, 2.16], not [1.95] -> FAIL", "merged 41")
check("merge, no merged file written when a check fails", str(any(os.path.exists(os.path.join(tmp, n)) for n in ("m2.jsonl", "m3.jsonl", "m4.jsonl", "m5.jsonl", "m6.jsonl", "m7.jsonl"))), "False")
# rate_up and the reader on a merged planted scan with a plus-to-minus change in (2.10, 2.11) and a V minimum at 2.15 (minus on both sides: beside no change)
out = run(RATE, m)
check("rate, planted change (2.10, 2.11)", out, "plus-to-minus change in (2.10, 2.11), ROBUST: from D 18's root 1.8074339746330934 the rise is 0.2926 to 0.3026 in 0.0625 D, i.e. 4.681 to 4.841 per unit D")
check("rate, one robust change places the root", out, "RATE: 1 robust plus-to-minus change(s) place the root", "not there")
out = run(READ, m)
check("reader, planted plus-to-minus change", out, "change in (2.10, 2.11): plus-to-minus, ROBUST")
check("reader, the V minimum at 2.15 has the same sign on both sides", out, "ln|det| local minimum at 2.15 (ln -1900.000000): WITHOUT a change")
# no change at all: all plus, ln|det| rising
rows = [rec(l, 1, lnv(l)) for l in LAMS]
f = put("none.jsonl", rows)
out = run(RATE, f)
check("rate, no change: the root is not there", out, "RATE: no robust plus-to-minus change from 1.95 to 2.35: the root is not there")
out = run(READ, f)
check("reader, no change", out, "no change of the hybrid sign over the window")
check("reader, no change: the V minimum at 2.15 is WITHOUT a change", out, "ln|det| local minimum at 2.15 (ln -1900.000000): WITHOUT a change")
# a change whose second point fails its noise test
rows = [rec(l, up(l), lnv(l), robust=(l != 2.11)) for l in LAMS]
f = put("nr.jsonl", rows)
out = run(RATE, f)
check("rate, the change has a non-robust point: not counted", out, "NOT ROBUST (a point fails its noise test)", "place the root")
check("rate, the change has a non-robust point: the root is not placed", out, "the root is not there")
check("reader, a non-robust point at the change", run(READ, f), "NOT ROBUST (a point fails its noise test)")
# a minus-to-plus change only (the other orientation): no plus-to-minus change
rows = [rec(l, -up(l), lnv(l)) for l in LAMS]
f = put("flip.jsonl", rows)
check("rate, only a minus-to-plus change: not a plus-to-minus change", run(RATE, f), "the root is not there")
check("reader, signs negated: minus-to-plus", run(READ, f), "change in (2.10, 2.11): minus-to-plus, ROBUST")
# xfkappa's real scans, as in plant_checks.py
out = run(READ, os.path.join(IN, "d18_scan_1025.jsonl"))
check("reader on xfkappa's D 18 scan: lower change", out, "change in (1.77, 1.78): minus-to-plus, ROBUST")
check("reader on xfkappa's D 18 scan: upper change", out, "change in (1.80, 1.81): plus-to-minus, ROBUST")
out = run(RATE, os.path.join(IN, "d18_scan_1025.jsonl"))
check("rate on xfkappa's D 18 scan: its own plus-to-minus change (1.80, 1.81) is read against D 18's root", out, "plus-to-minus change in (1.80, 1.81), ROBUST")
print("plant_checks_up", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
