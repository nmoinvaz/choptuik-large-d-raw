#!/usr/bin/env python3
"""#1025 D 18.5 scan at k_c 55 (win2b): planted controls for merge_scan.py and kc55_compare.py, and for winb's pinned reader (read_d18mid_1025.py, blob 017ae1da) on xfkappa's D 18 and D 18.5
scans. Each case runs the script as a subprocess on synthetic scan files in a fresh directory (left in place); it passes when the output has the wanted line and not the unwanted one.
Exit 0 only if every case passes; the driver does not start the scan otherwise.
usage: plant_checks_kc55.py PYTHON IN_DIR HERE_DIR"""
import json, os, subprocess, sys, tempfile

PY, IN, HERE = sys.argv[1], sys.argv[2], sys.argv[3]
MERGE, COMP, READ = os.path.join(HERE, "merge_scan.py"), os.path.join(HERE, "kc55_compare.py"), os.path.join(IN, "read_d18mid_1025.py")
LAMS = [round(1.55 + 0.01 * i, 2) for i in range(86)]
tmp = tempfile.mkdtemp(prefix="kc55_plant_")


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


def signs(flips):                       # starts minus; the sign flips at each lambda in flips (a change in (lambda - 0.01, lambda))
    s, out = -1, {}
    for l in LAMS:
        if round(l, 2) in flips:
            s = -s
        out[l] = s
    return out


lnv = lambda l: -1900.0 + 3.0 * abs(l - 2.20)
full = lambda flips, **kw: [rec(l, s, lnv(l), **kw) for l, s in signs(flips).items()]


def halves(flips=(1.68,), rep_sign=None, rep_dln=0.0, drop=None, D=18.5):
    sg = signs(flips)
    A = [rec(1.97, sg[1.97], lnv(1.97), D=D)] + [rec(l, sg[l], lnv(l), D=D) for l in LAMS if l < 1.97 and l != drop]
    B = [rec(1.97, rep_sign if rep_sign is not None else sg[1.97], lnv(1.97) + rep_dln, D=D)] + [rec(l, sg[l], lnv(l), D=D) for l in LAMS if l >= 1.98 and l != drop]
    return A, B


M = ("1.55", "86", "1.97", "18.5")
A, B = halves()
m = os.path.join(tmp, "m_good.jsonl")
check("merge, repeat equal", run(MERGE, *M, put("a1.jsonl", A), put("b1.jsonl", B), m), "merged 86 points (1.55 to 2.40)", "FAIL")
A2, B2 = halves(rep_dln=1e-3)
check("merge, repeat ln|det| differs by 1e-3", run(MERGE, *M, put("a2.jsonl", A2), put("b2.jsonl", B2), os.path.join(tmp, "m2.jsonl")), "-> FAIL", "merged 86")
A3, B3 = halves(rep_sign=-1)          # the planted sign at 1.97 is plus (the change is at 1.68)
check("merge, repeat sign differs", run(MERGE, *M, put("a3.jsonl", A3), put("b3.jsonl", B3), os.path.join(tmp, "m3.jsonl")), "-> FAIL", "merged 86")
A4, B4 = halves(); B4 = B4[1:]
check("merge, no repeated point", run(MERGE, *M, put("a4.jsonl", A4), put("b4.jsonl", B4), os.path.join(tmp, "m4.jsonl")), "no repeated point in both files -> FAIL", "merged 86")
A5, B5 = halves(drop=2.40)
check("merge, lambda 2.40 missing", run(MERGE, *M, put("a5.jsonl", A5), put("b5.jsonl", B5), os.path.join(tmp, "m5.jsonl")), "missing lambda: [2.4]", "merged 86")
A6, B6 = halves(D=19.0)
check("merge, records at another D", run(MERGE, *M, put("a6.jsonl", A6), put("b6.jsonl", B6), os.path.join(tmp, "m6.jsonl")), "records at a D other than 18.5", "merged 86")
A7, B7 = halves(); A7.append(dict(B7[1]))
check("merge, a second point in both files", run(MERGE, *M, put("a7.jsonl", A7), put("b7.jsonl", B7), os.path.join(tmp, "m7.jsonl")), "are [1.97, 1.98], not [1.97] -> FAIL", "merged 86")
check("merge, no merged file written when a check fails", str(any(os.path.exists(os.path.join(tmp, n)) for n in ("m2.jsonl", "m3.jsonl", "m4.jsonl", "m5.jsonl", "m6.jsonl", "m7.jsonl"))), "False")
# kc55_compare on planted scans, default k_c 63 coverage 1.55 to 2.10 and root 1.6772
c = lambda flips, *extra, **kw: run(COMP, put(f"c_{'_'.join(map(str, flips)) or 'none'}_{len(os.listdir(tmp))}.jsonl", full(flips, **kw)), *extra)
out = c((1.68,))
check("compare, change (1.67, 1.68) against the k_c 63 root 1.6772: STABLE", out, "k_c 55 change in (1.67, 1.68), minus-to-plus, ROBUST: STABLE")
check("compare, the k_c 63 root is MATCHED", out, "k_c 63 root 1.6772: MATCHED, k_c 55 robust change minus-to-plus in (1.67, 1.68)")
out = c((1.67,))
check("compare, change (1.66, 1.67) straddles the band edge: UNDETERMINED", out, "k_c 55 change in (1.66, 1.67), minus-to-plus, ROBUST: UNDETERMINED at the 0.01 step", "STABLE")
check("compare, the k_c 63 root is UNDETERMINED", out, "k_c 63 root 1.6772: UNDETERMINED at the 0.01 step", "MATCHED")
out = c((1.70,))
check("compare, change (1.69, 1.70) is 0.0128 or more away: k_c 55 ONLY", out, "k_c 55 change in (1.69, 1.70), minus-to-plus, ROBUST: k_c 55 ONLY", "STABLE")
check("compare, the k_c 63 root has no k_c 55 change near it: k_c 63 ONLY", out, "k_c 63 root 1.6772: k_c 63 ONLY", "MATCHED")
out = c(())
check("compare, no change at all", out, "SUMMARY: 0 robust k_c 55 change(s) in 1.55 to 2.40; none")
check("compare, no change: the k_c 63 root is k_c 63 ONLY", out, "k_c 63 root 1.6772: k_c 63 ONLY")
out = c((1.68, 2.25))
check("compare, a change above the k_c 63 coverage is not compared", out, "k_c 55 change in (2.24, 2.25), plus-to-minus, ROBUST: not compared (k_c 63 is not scanned over this bracket", "k_c 55 ONLY")
out = c((1.68, 2.25), "--cov63", "1.55,2.40", "--r63", "1.6772")
check("compare, the coverage widened and no k_c 63 root there: k_c 55 ONLY", out, "k_c 55 change in (2.24, 2.25), plus-to-minus, ROBUST: k_c 55 ONLY")
out = c((1.68, 2.25), "--cov63", "1.55,2.40", "--r63", "1.6772,2.245")
check("compare, a second k_c 63 root 2.245 inside the bracket's band: STABLE", out, "k_c 55 change in (2.24, 2.25), plus-to-minus, ROBUST: STABLE")
check("compare, the second k_c 63 root is MATCHED", out, "k_c 63 root 2.245: MATCHED")
out = run(COMP, put("c_nr.jsonl", [rec(l, s, lnv(l), robust=(l != 1.68)) for l, s in signs((1.68,)).items()]))
check("compare, the change has a non-robust point: not counted", out, "NOT ROBUST (a point fails its noise test), not counted", "STABLE")
check("compare, the k_c 63 root with only a non-robust change near it: UNDETERMINED", out, "k_c 63 root 1.6772: UNDETERMINED at the 0.01 step (k_c 55 change(s) touching its band: (1.67, 1.68) not robust)")
check("compare, a k_c 63 root outside the k_c 55 window is not compared", run(COMP, put("c_w.jsonl", full((1.68,))), "--r63", "1.6772,3.0", "--cov63", "1.55,3.1"), "k_c 63 root 3.0: outside the k_c 55 window, not compared")
# the pinned reader on xfkappa's scans, as in the other planted checks
out = run(READ, os.path.join(IN, "d18_scan_1025.jsonl"))
check("reader on xfkappa's D 18 scan: lower change", out, "change in (1.77, 1.78): minus-to-plus, ROBUST")
check("reader on xfkappa's D 18 scan: upper change", out, "change in (1.80, 1.81): plus-to-minus, ROBUST")
out = run(READ, os.path.join(IN, "d185_scan_1025.jsonl"))
check("reader on xfkappa's D 18.5 scan (k_c 63): one change", out, "change in (1.67, 1.68): minus-to-plus, ROBUST", "two robust changes")
out = run(COMP, os.path.join(IN, "d185_scan_1025.jsonl"))
check("compare on xfkappa's k_c 63 D 18.5 scan itself: its change (1.67, 1.68) is STABLE against 1.6772", out, "change in (1.67, 1.68), minus-to-plus, ROBUST: STABLE")
print("plant_checks_kc55", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
