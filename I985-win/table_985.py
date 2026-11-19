#!/usr/bin/env python3
"""#985 (win): tables and the readings by the issue's rules, from logs/*.log and x/*.json. From I972-win/table_972.py.

usage: python table_985.py [--selftest] [--logs DIR] [--x DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones), m0 the unmoved root's.
 - Control: T1's 12 'start i:' lines equal #951's first 12 (I951-win/logs/K0c_D40_rough.log) in every character (the 12 'start i, x / max|x|:' lines are compared too and reported).
 - T1: d = the number of singular values within 1e-4 of the top (rt_xcount), gap = s_(d+1)/s_d, clean at 1e-3 or below. d = 1 clean: (H2). d = 2 clean: (H4) at k = 1/2. d = 4 clean: (H4) with k = 3/2 too.
   d = 3, d >= 5 or no clean gap: none fits. For d >= 2 the smaller chord share in span(p_1..p_d) must be >= 0.99; below 0.9 the deep directions are not the root set's; between, no rule.
 - T2 at D 34.99: (H4) predicts d >= 2 (T2_35's own x) and m(1e-20) >= 100 m0.
 - T2 at D 20.04: (H4) predicts m(1e-26) / m0 in [1/3, 3] and the best bound in [1e-32, 2e-22] (applied to the unmoved root's run, the moved run's printed too; a split is reported, not chosen).
 - INCOMPLETE where a run printed fewer than 12 bounds."""
import json
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\nathan\Source\choptuik-large-d-raw\I951-win\logs\K0c_D40_rough.log"
R963 = r"C:\Users\nathan\Source\choptuik-large-d-raw\I963-win\logs"
N = 12
CAP = 250
CLEAN = 1e-3
RUNS = [("T1_c", "D 40.020065, sample c", "T1"), ("T2_35", "D 34.993266, root", "T2_35"), ("m35_d1e-20", "D 34.993266, moved 1e-20", "T2_35"),
        ("T2_20", "D 20.043653, root", "T2_20"), ("m20_d1e-26", "D 20.043653, moved 1e-26", "T2_20")]
CHECKS = [("xc_selftest", 0), ("xc_selftest_mutate", 1), ("planted_p2", 0), ("xc_p2_expect2", 0), ("planted_p4", 0), ("xc_p4_expect4", 0), ("xc_p2_expect4", 1)]
START = re.compile(r"^\s+start (\d+): max\|x\| (\S+), bound on the smallest gain (\S+), max\|J x - v\| (\S+), (\d+) products")
XLINE = re.compile(r"^\s+start (\d+), x / max\|x\|:")
HEAD = re.compile(r"max\|F\| (\S+)\s*$")
MU = re.compile(r"^\s+start 0, x / max\|x\|: mu (\S+);")
BEST = re.compile(r"best bound on the smallest gain \(max norm\) (\S+);")


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else math.sqrt(s[n // 2 - 1] * s[n // 2])


def parse(path):
    r = dict(maxF=None, bounds=[], prods=[], res=[], mu0=None, best=None, slines=[], xlines=[], exists=os.path.exists(path))
    if not r["exists"]:
        return r
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\r\n")
        m = START.match(ln)
        if m:
            r["bounds"].append(float(m.group(3)))
            r["prods"].append(int(m.group(5)))
            r["res"].append(m.group(4))
            r["slines"].append(ln)
        elif XLINE.match(ln):
            r["xlines"].append(ln)
            if MU.match(ln):
                r["mu0"] = MU.match(ln).group(1)
        elif r["maxF"] is None and HEAD.search(ln):
            r["maxF"] = HEAD.search(ln).group(1)
        elif BEST.search(ln):
            r["best"] = float(BEST.search(ln).group(1))
    return r


def compare_control(path, ref=REF, n=N):
    """(ok, text): the first n 'start i:' lines and 'start i, x / max|x|:' lines of path equal ref's, character for character"""
    a, b = parse(path), parse(ref)
    if not a["exists"] or not b["exists"]:
        return False, "log missing"
    sa, sb, xa, xb = a["slines"][:n], b["slines"][:n], a["xlines"][:n], b["xlines"][:n]
    ns = sum(1 for p, q in zip(sa, sb) if p == q) if len(sa) == n and len(sb) == n else 0
    nx = sum(1 for p, q in zip(xa, xb) if p == q) if len(xa) == n and len(xb) == n else 0
    return ns == n and nx == n, f"{ns} of {n} start lines and {nx} of {n} x / max|x| lines equal #951's first {n}"


def t1_reading(d, gap, shares):
    clean = gap is not None and gap <= CLEAN
    if not clean:
        word = "NONE FITS (no clean gap)"
    elif d == 1:
        word = "(H2)"
    elif d == 2:
        word = "(H4) at k = 1/2"
    elif d == 4:
        word = "(H4) with k = 3/2 as well"
    else:
        word = f"NONE FITS (d = {d})"
    if d < 2 or not shares:
        span = "not required (d = 1)" if d < 2 else "no chord shares"
    else:
        mn = min(shares)
        span = (f"chords in the deep span (smaller share {mn:.4f} >= 0.99)" if mn >= 0.99 else
                f"the deep directions are not the root set's (smaller share {mn:.4f} < 0.9)" if mn < 0.9 else
                f"between 0.9 and 0.99 (smaller share {mn:.4f}, the issue gives no rule)")
    return word, span


def t2_35(d, m, m0):
    if m is None or m0 is None:
        return None, "incomplete"
    ratio = m / m0
    c1, c2 = d >= 2, ratio >= 100
    return c1 and c2, f"d = {d} ({'>=' if c1 else '<'} 2), m / m0 = {ratio:.4g} ({'>=' if c2 else '<'} 100)"


def t2_20(m, m0, best_root, best_moved):
    if m is None or m0 is None:
        return None, "incomplete"
    ratio = m / m0
    c1 = 1 / 3 <= ratio <= 3
    inb = lambda b: b is not None and 1e-32 <= b <= 2e-22
    b1, b2 = inb(best_root), inb(best_moved)
    why = f"m / m0 = {ratio:.4g} ({'in' if c1 else 'outside'} [1/3, 3]), best bound of the root {best_root:.3e} ({'in' if b1 else 'outside'} [1e-32, 2e-22]), of the moved run {best_moved:.3e} ({'in' if b2 else 'outside'})"
    if b1 != b2:
        return None, why + "; the two best bounds fall on different sides, not chosen"
    return c1 and b1, why


def loadj(xdir, name):
    p = os.path.join(xdir, f"{name}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def fmt(v, f="{:.3e}"):
    return "-" if v is None else f.format(v)


def report(logs, xdir):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _, _ in RUNS}
    print("Checks block (exit codes against the wanted ones):\n\n| step | wanted exit | exit file |\n|---|---|---|")
    for lab, want in CHECKS:
        p = os.path.join(logs, f"{lab}.exit")
        got = open(p).read().strip() if os.path.exists(p) else "-"
        print(f"| {lab} | {want} | {got} |")
    ok, why = compare_control(os.path.join(logs, "T1_c.log"))
    print(f"\nControl (T1 against #951's K0c_D40_rough.log): **{'EQUAL' if ok else 'NOT EQUAL'}**, {why}.")
    print("\n| run | state | printed max abs F | bounds printed | m (median of the bounds) | best bound | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    ms = {}
    for lab, st, _ in RUNS:
        r = R[lab]
        m = median(r["bounds"][:N]) if len(r["bounds"]) >= N else None
        ms[lab] = m
        pr = sorted(r["prods"][:N])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:N] if x >= CAP)} of {len(r['prods'][:N])}"
        worst = f"{max(float(x) for x in r['res'][:N]):.1e}" if r["res"] else "-"
        print(f"| {lab} | {st} | {r['maxF'] or '-'} | {len(r['bounds'])} | {fmt(m, '{:.4e}')} | {fmt(r['best'], '{:.4e}')} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nThe bounds of each run, start 0 to 11:\n")
    print("| start | " + " | ".join(lab for lab, _, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(N):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _, _ in RUNS) + " |")
    J = {k: loadj(xdir, k) for k in ("T1_c", "T2_35", "T2_20")}
    print("\nrt_xcount (the SVD of the x block):\n\n| x file | d | gap s_(d+1)/s_d | chord shares in span(p_1..p_d) | s_j / s_1, j = 1 to 6 |\n|---|---|---|---|---|")
    for k, j in J.items():
        if j is None:
            print(f"| {k} | - | - | - | - |")
            continue
        sh = "; ".join(f"{n} {v:.6f}" for n, v in (j.get("chords") or {}).items()) or "-"
        print(f"| {k} | {j['d']} | {fmt(j['gap'], '{:.2e}')} | {sh} | " + " ".join(f"{v:.1e}" for v in j["s_over_s1"][:6]) + " |")
    print("\nReadings by the pre-set rules:\n")
    j = J["T1_c"]
    if j is None:
        t1 = "INCOMPLETE (no x count)"
    else:
        w, sp = t1_reading(j["d"], j["gap"], list((j.get("chords") or {}).values()))
        t1 = f"d = {j['d']}, gap {fmt(j['gap'], '{:.2e}')}: **{w}**; {sp}"
    print(f"- T1 (D 40.02): {t1}.")
    j = J["T2_35"]
    ok, why = t2_35(j["d"] if j else 0, ms["m35_d1e-20"], ms["T2_35"]) if j else (None, "no x count")
    print(f"- T2 at D 34.993266: {'(H4) predictions HOLD' if ok else 'INCOMPLETE' if ok is None else '(H4) predictions FAIL'}; {why}.")
    ok2, why2 = t2_20(ms["m20_d1e-26"], ms["T2_20"], R["T2_20"]["best"], R["m20_d1e-26"]["best"]) if None not in (R["T2_20"]["best"], R["m20_d1e-26"]["best"]) else (None, "incomplete")
    print(f"- T2 at D 20.043653: {'(H4) predictions HOLD' if ok2 else 'INCOMPLETE OR SPLIT' if ok2 is None else '(H4) predictions FAIL'}; {why2}.")
    print(f"- T2 as a whole: {'reads (H4)' if ok and ok2 else 'does not read (H4)' if ok is False or ok2 is False else 'not decided'}.")
    return ok, ok2


def selftest(bad=0):
    def chk(name, got, want):
        nonlocal bad
        good = got == want
        print(f"  {name}: {got} (want {want}) {'ok' if good else 'WRONG'}")
        bad += not good

    for name, args, want in (("d 1 clean", (1, 1e-5, []), "(H2)"), ("d 2 clean", (2, 1e-5, [1.0, 1.0]), "(H4) at k = 1/2"), ("d 4 clean", (4, 1e-5, [1.0, 1.0]), "(H4) with k = 3/2 as well"),
                             ("d 3 clean", (3, 1e-5, [1.0, 1.0]), "NONE FITS (d = 3)"), ("d 5 clean", (5, 1e-5, [1.0]), "NONE FITS (d = 5)"),
                             ("d 2 gap at the bar", (2, 1e-3, [1.0]), "(H4) at k = 1/2"), ("d 2 gap just above the bar", (2, 1.1e-3, [1.0]), "NONE FITS (no clean gap)"),
                             ("d 2 no gap value", (2, None, [1.0]), "NONE FITS (no clean gap)"), ("d 1 gap just above", (1, 1.1e-3, []), "NONE FITS (no clean gap)")):
        chk(f"T1 {name}", t1_reading(*args)[0], want)
    for name, sh, want in (("shares 0.995, 0.999", [0.995, 0.999], "deep span"), ("share 0.99 exactly", [0.99, 1.0], "deep span"), ("share 0.989", [0.989, 1.0], "between"),
                           ("share 0.9", [0.9, 1.0], "between"), ("share 0.89", [0.89, 1.0], "not the root set's")):
        sp = t1_reading(2, 1e-5, sh)[1]
        chk(f"T1 span {name}", "deep span" if sp.startswith("chords in") else "not the root set's" if "not the root set's" in sp else "between" if sp.startswith("between") else sp, want)
    for name, (d, m, m0), want in (("d 2 ratio just over 100", (2, 1.001e-24, 1e-26), True), ("d 2 ratio 99", (2, 0.99e-24, 1e-26), False), ("d 1 ratio 1000", (1, 1e-23, 1e-26), False), ("d 4 ratio 1e4", (4, 1e-22, 1e-26), True)):
        chk(f"T2_35 {name}", t2_35(d, m, m0)[0], want)
    for name, (m, m0, b1, b2), want in (("ratio 1, best in", (1e-26, 1e-26, 1e-27 * 1e5, 1e-27 * 1e5), True), ("ratio 3", (3e-26, 1e-26, 1e-30 * 1e5, 1e-30 * 1e5), True), ("ratio 3.2", (3.2e-26, 1e-26, 1e-25, 1e-25), False),
                                        ("ratio 1/3", (1e-26, 3e-26, 1e-25, 1e-25), True), ("ratio 0.3", (0.3e-26, 1e-26, 1e-25, 1e-25), False), ("best below", (1e-26, 1e-26, 9e-33, 9e-33), False),
                                        ("best above", (1e-26, 1e-26, 3e-22, 3e-22), False), ("best split", (1e-26, 1e-26, 1e-25, 3e-22), None)):
        chk(f"T2_20 {name}", t2_20(m, m0, b1, b2)[0], want)
    chk("T2 incomplete", t2_35(2, None, 1e-26)[0], None)
    mut = open(__file__).read().replace("ratio >= 100", "ratio >= 10")
    ns = {"__file__": __file__}
    exec(compile(mut.split("def loadj")[0], "mut", "exec"), ns)
    chk("mutated bar 100 -> 10 (the ratio 50 case)", (t2_35(2, 5e-25, 1e-26)[0], ns["t2_35"](2, 5e-25, 1e-26)[0]), (False, True))
    mut = open(__file__).read().replace("gap is not None and gap <= CLEAN", "gap is not None and gap <= 1e-2")
    ns = {"__file__": __file__}
    exec(compile(mut.split("def loadj")[0], "mut", "exec"), ns)
    chk("mutated clean gap 1e-3 -> 1e-2 (gap 5e-3)", (t1_reading(2, 5e-3, [1.0])[0], ns["t1_reading"](2, 5e-3, [1.0])[0]), ("NONE FITS (no clean gap)", "(H4) at k = 1/2"))
    with tempfile.TemporaryDirectory() as td:
        ref, a = os.path.join(td, "ref.log"), os.path.join(td, "a.log")
        starts = [f"  start {i}: max|x| {1 + i:.3e}, bound on the smallest gain {1 / (1 + i):.3e}, max|J x - v| 1.0e-17, 67 products" for i in range(48)]
        xs = [f"  start {i}, x / max|x|: mu +1.00e+00; w1 max 4.0e-02" for i in range(48)]
        open(ref, "w").write("H.npz: D 40 32x121 K 0, max|F| 1.0e-30\n  rhs\n" + "\n".join(starts) + "\n" + "\n".join(xs) + "\n  best bound on the smallest gain (max norm) 1e-36; x\n")

        def mk(s, x, tail="  saved x of 12 starts to X.npz\n"):
            open(a, "w", newline="").write("H.npz: D 40 32x121 K 0, max|F| 1.0e-30\r\n  rhs\r\n" + "\r\n".join(s) + "\r\n" + "\r\n".join(x) + "\r\n  best bound on the smallest gain (max norm) 5e-36; y\r\n" + tail)
        mk(starts[:12], xs[:12])
        chk("control, equal (CRLF, other best line, a saved line)", compare_control(a, ref)[0], True)
        s2 = list(starts[:12])
        s2[7] = s2[7].replace("1.000e+00", "1.000e-00").replace("8.000e+00", "8.001e+00")
        mk(s2, xs[:12])
        chk("control, one character changed in start 7", compare_control(a, ref)[0], False)
        x2 = list(xs[:12])
        x2[11] = x2[11].replace("+1.00e+00", "-1.00e+00")
        mk(starts[:12], x2)
        chk("control, one x line changed", compare_control(a, ref)[0], False)
        mk(starts[:11], xs[:11])
        chk("control, 11 starts", compare_control(a, ref)[0], False)
        chk("control, log missing", compare_control(os.path.join(td, "none.log"), ref)[0], False)
        chk("control, #951's own log against itself", compare_control(REF, REF)[0] if os.path.exists(REF) else True, True)
    chk("median: geometric mean of the two middle ones for 12", abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12, True)
    p = parse(os.path.join(R963, "c_d1e-20.log"))
    if len(p["bounds"]) >= N:
        chk("#963's c_d1e-20 median re-read", abs(median(p["bounds"][:N]) / 5.4593e-24 - 1) < 5e-5, True)
    print("selftest", "FAILED" if bad else "passed")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logs = sys.argv[sys.argv.index("--logs") + 1] if "--logs" in sys.argv else os.path.join(HERE, "logs")
    xdir = sys.argv[sys.argv.index("--x") + 1] if "--x" in sys.argv else os.path.join(HERE, "x")
    report(logs, xdir)
