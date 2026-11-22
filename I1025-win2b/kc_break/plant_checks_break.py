#!/usr/bin/env python3
"""#1025 k_c break scan at D 18.375 (win2b): planted controls for kc_break_compare.py, merge_repeat.py, read_fine.py (step 0.01) and dip_fit3.py on 19-point planted scans (lambda 1.62 to 1.80 at 0.01), and the
det-linear estimate of kc_break_compare.py against xfkappa's own `changes()` on a real scan. Each case runs the script as a subprocess on files in a fresh directory (left in place); it passes when the output has the
wanted line and not the unwanted one. Exit 0 only if every case passes; the driver does not start the scans otherwise.
usage: plant_checks_break.py PYTHON HERE_DIR"""
import importlib.util, json, os, subprocess, sys, tempfile
import numpy as np

PY, HERE = sys.argv[1], sys.argv[2]
CMP, MRG, READ, DIP = (os.path.join(HERE, n) for n in ("kc_break_compare.py", "merge_repeat.py", "read_fine.py", "dip_fit3.py"))
LAMS = [round(1.62 + 0.01 * i, 2) for i in range(19)]
tmp = tempfile.mkdtemp(prefix="kcbreak_plant_")
LN0 = -1900.0


def rec(lam, sign, ln, robust=True, D=18.375, kc=55):
    return dict(D=D, kc=kc, lam=lam, sign=float(sign), ln=ln, noise=[float(sign)] * 2, noise_robust=robust, f64_sign=1.0, f64_ln=ln + 1.0, state="planted.npy", sec=1)


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


def scan(flips, ln_over=None, kc=55, nonrobust=(), start=-1):
    """minus below the first flip, then alternating; ln constant LN0 except ln_over; a flip at L is a change in (L - 0.01, L), its det-linear estimate the bracket midpoint unless tilted"""
    ln_over = ln_over or {}
    s, rows = start, []
    for l in LAMS:
        if round(l, 2) in flips:
            s = -s
        rows.append(rec(l, s, ln_over.get(round(l, 2), LN0), robust=(round(l, 2) not in nonrobust), kc=kc))
    return rows


def CMP_(r55, r63):
    return run(CMP, put(f"s55_{len(os.listdir(tmp))}.jsonl", r55), put(f"s63_{len(os.listdir(tmp))}.jsonl", r63))


s63 = scan((1.71,), kc=63)                                         # k_c 63: a change in (1.70, 1.71), estimate 1.705
out = CMP_(scan((1.71,)), s63)
check("compare, the k_c 55 change in the same bracket: difference 0, STABLE", out, "k_c 55 minus k_c 63 = +0.000000 -> STABLE (within 0.01)")
check("compare, the reading for a stable root", out, "READING: the root is STABLE at D 18.375 (the k_c 55 estimate within 0.01 of the k_c 63 root)")
check("compare, the estimates are the bracket midpoints", out, "k_c 63 robust change in (1.700, 1.710), minus-to-plus: det-linear estimate 1.705000")
out = CMP_(scan((1.73,)), s63)
check("compare, the k_c 55 change 0.02 away: BREAKS, further off", out, "k_c 55 minus k_c 63 = +0.020000 -> BREAKS (beyond 0.01; the k_c 55 root is further off)")
check("compare, the reading for a root further off", out, "READING: the root BREAKS by D 18.375 (the k_c 55 root is further off than 0.01)", "STABLE at D 18.375")
out = CMP_(scan((1.72,)), s63)
check("compare, the k_c 55 change exactly 0.010 away is within the bar", out, "k_c 55 minus k_c 63 = +0.010000 -> STABLE (within 0.01)")
out = CMP_(scan((1.70,)), s63)
check("compare, the k_c 55 change below: the sign of the difference is printed", out, "k_c 55 minus k_c 63 = -0.010000 -> STABLE")
out = CMP_(scan((1.72,), ln_over={1.72: LN0 - 3.0}), s63)
check("compare, a tilted estimate: the bracket midpoint 1.715 would be 0.010 away, the estimate 1.719526 is 0.0145 away: BREAKS", out, "estimate 1.719526: k_c 55 minus k_c 63 = +0.014526 -> BREAKS")
out = CMP_(scan(()), s63)
check("compare, no k_c 55 change in the window: BREAKS (no k_c 55 root)", out, "PAIRING k_c 63 root 1.705000: no k_c 55 robust change in the window -> BREAKS (no k_c 55 root there)")
check("compare, no k_c 55 change: the reading", out, "READING: the root BREAKS by D 18.375 (no k_c 55 root in the window)")
out = CMP_(scan((1.71,)), scan((), kc=63))
check("compare, no k_c 63 change: the fixed reading does not cover it", out, "NO k_c 63 ROOT in the window: the fixed reading does not cover this", "READING: the root")
out = CMP_(scan((1.71,), nonrobust=(1.71,)), s63)
check("compare, a non-robust k_c 55 change is not counted", out, "k_c 55 change in (1.700, 1.710), minus-to-plus: NOT ROBUST (a point fails its noise test), not counted, det-linear estimate 1.705000")
check("compare, a non-robust k_c 55 change only: BREAKS (no robust k_c 55 root)", out, "READING: the root BREAKS by D 18.375 (no k_c 55 root in the window)", "STABLE at D 18.375")
out = CMP_(scan((1.71,), start=+1), s63)
check("compare, the orientation of the k_c 55 change is the opposite: information", out, "Information: orientation the opposite")
out = CMP_(scan((1.71, 1.73)), scan((1.65, 1.71), kc=63))
check("compare, two k_c 63 changes: OTHER", out, "READING: OTHER, 2 k_c 63 robust change(s) (the fixed reading is for one root)")
out = CMP_(scan((1.71, 1.77)), s63)
check("compare, a second k_c 55 change with no k_c 63 root near it is listed", out, "k_c 55 robust change in (1.760, 1.770), estimate 1.765000: paired with no k_c 63 root")
# the estimate against xfkappa's own changes() on a real scan (the k_c 63 D 18.5 scan, one change in (1.67, 1.68), det-linear 1.677016)
real = os.path.join(HERE, "in", "kc63_d185_merged_1.55-2.40.jsonl")
spec = importlib.util.spec_from_file_location("d185_scan_read", os.path.join(HERE, "in", "d185_scan_read.py"))
mod = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0]]; spec.loader.exec_module(mod)
S = sorted((json.loads(l) for l in open(real) if l.strip()), key=lambda r: r["lam"])
rob, non = mod.changes(S)
out = run(CMP, real, real)
mine = [float(w.split("estimate ")[1].split(",")[0]) for w in out.splitlines() if w.startswith("k_c 63 robust change")]
ok = len(rob) == len(mine) == 1 and abs(rob[0]["lin"] - mine[0]) < 5e-7
bad += not ok
print(f"plant estimate against xfkappa's changes() on the k_c 63 D 18.5 scan: his lin {[c['lin'] for c in rob]}, this script's {mine} -> {'ok' if ok else 'WRONG'}")
check("compare, a scan against itself on real data: difference 0, STABLE, 1.677016", out, "k_c 55 minus k_c 63 = +0.000000 -> STABLE")
# merge_repeat
M = ("1.62", "19", "0.01", "1.71", "18.375", "55")


def with_rep(rows, rep_dln=0.0, rep_sign=None, drop=None, kc=55, D=18.375, extra=None):
    rs = [dict(r, kc=kc, D=D) for r in rows if round(r["lam"], 2) != drop]
    base = [r for r in rows if round(r["lam"], 2) == 1.71][0]
    rs.append(dict(base, kc=kc, D=D, ln=base["ln"] + rep_dln, sign=base["sign"] if rep_sign is None else rep_sign))
    if extra:
        rs.append(dict(base, kc=kc, D=D))
    return rs


base = scan((1.71,))
mg = os.path.join(tmp, "mr_good.jsonl")
out = run(MRG, put("r1.jsonl", with_rep(base)), mg, *M)
check("repeat, equal: merged", out, "merged 19 points (1.620 to 1.800)", "-> FAIL")
check("repeat, equal: the check line", out, "REPEAT CHECK at lambda 1.710: sign first +1 second +1")
check("repeat, ln|det| differs by 1e-3: FAIL", run(MRG, put("r2.jsonl", with_rep(base, rep_dln=1e-3)), os.path.join(tmp, "mr2.jsonl"), *M), "-> FAIL", "merged 19")
check("repeat, the sign differs: FAIL", run(MRG, put("r3.jsonl", with_rep(base, rep_sign=-1)), os.path.join(tmp, "mr3.jsonl"), *M), "-> FAIL", "merged 19")
check("repeat, no repeated point: FAIL", run(MRG, put("r4.jsonl", base), os.path.join(tmp, "mr4.jsonl"), *M), "REPEAT CHECK: the lambda occurring more than once are [], not [1.71] -> FAIL", "merged 19")
check("repeat, lambda 1.80 missing", run(MRG, put("r5.jsonl", with_rep(base, drop=1.80)), os.path.join(tmp, "mr5.jsonl"), *M), "missing lambda: [1.8]", "merged 19")
check("repeat, records at another k_c", run(MRG, put("r6.jsonl", with_rep(base, kc=63)), os.path.join(tmp, "mr6.jsonl"), *M), "records at another D or k_c", "merged 19")
check("repeat, the point three times: FAIL", run(MRG, put("r7.jsonl", with_rep(base, extra=True)), os.path.join(tmp, "mr7.jsonl"), *M), "-> FAIL", "merged 19")
check("repeat, no merged file written when a check fails", str(any(os.path.exists(os.path.join(tmp, n)) for n in ("mr2.jsonl", "mr3.jsonl", "mr4.jsonl", "mr5.jsonl", "mr6.jsonl", "mr7.jsonl"))), "False")
# read_fine at step 0.01 and dip_fit3
out = run(READ, mg, "--step", "0.01")
check("reader at step 0.01: the change", out, "change in (1.70, 1.71): minus-to-plus, ROBUST")
check("dip fit 3: its own planted truths pass", run(DIP, "selftest"), "selftest passes")
mdl = lambda l: -1597.0 + np.log((l - 1.70) ** 2 + 0.05 ** 2) + 4.9 * (l - 1.70) - 13.0 * (l - 1.70) ** 2        # a root pair 1.70 +- 0.05 i, no sign change
out = run(DIP, put("d_dip.jsonl", [rec(l, -1, float(mdl(l))) for l in LAMS]))
check("dip fit 3 on a planted pair inside the scan: found, l0 and e recovered, resolved", out, "l0 1.70000", "NOT RESOLVED")
check("dip fit 3 on that dip: the resolved statement", out, "resolved at this step, l0 inside the window, the model fits better than the quartic")
out = run(DIP, put("d_none.jsonl", scan((1.71,))))
check("dip fit 3 on a scan with no dip: none", out, "ln|det| local minima WITHOUT a change: none")
print("plant_checks_break", "passes" if bad == 0 else f"FAILS ({bad} wrong)", f"(files in {tmp})")
sys.exit(1 if bad else 0)
