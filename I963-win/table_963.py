#!/usr/bin/env python3
"""#963 (win): tables and the verdict by the issue's criteria, from logs/c_d0.log, c_d1e-20.log, c_d1e-19.log, c_d1e-18.log.

usage: python table_963.py [--selftest] [--logs DIR] [--ref FILE]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones for an even count, as table_701.median), m0 the control's.
 - Control: the delta 0 run's 12 'start' lines equal #951's first 12 (logs/K0c_D40_rough.log of I951-win) as text.
 - NULL if m0 < m(1e-20) < m(1e-19) < m(1e-18) and m(1e-18) >= 100 m0 (the chain over the three nonzero delta alone is printed too, and a difference is flagged).
 - NOT NULL if m(delta) / m0 is in [1/3, 3] at all three delta.  UNDECIDED otherwise.  INCOMPLETE if a run printed fewer than 12 bounds (no decision by the criteria)."""
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\nathan\Source\choptuik-large-d-raw\I951-win\logs\K0c_D40_rough.log"
RUNS = [("c_d0", "0"), ("c_d1e-20", "1e-20"), ("c_d1e-19", "1e-19"), ("c_d1e-18", "1e-18")]
N = 12
CAP = 250
START = re.compile(r"^\s+start (\d+): max\|x\| (\S+), bound on the smallest gain (\S+), max\|J x - v\| (\S+), (\d+) products")
HEAD = re.compile(r"max\|F\| (\S+)\s*$")
MU = re.compile(r"^\s+start 0, x / max\|x\|: mu (\S+);")


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else math.sqrt(s[n // 2 - 1] * s[n // 2])


def parse(path):
    r = dict(maxF=None, bounds=[], prods=[], res=[], mu0=None, lines=[])
    if not os.path.exists(path):
        return r
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\r\n")
        m = START.match(ln)
        if m:
            r["bounds"].append(float(m.group(3)))
            r["prods"].append(int(m.group(5)))
            r["res"].append(m.group(4))
            r["lines"].append(ln)
        elif r["maxF"] is None and HEAD.search(ln):
            r["maxF"] = HEAD.search(ln).group(1)
        elif MU.match(ln):
            r["mu0"] = MU.match(ln).group(1)
    return r


def chain_up(v):
    return all(a < b for a, b in zip(v, v[1:]))


def verdict(ms):
    """ms = [m0, m(1e-20), m(1e-19), m(1e-18)], None where a run is incomplete. Returns (word, why)."""
    if any(m is None for m in ms):
        return "INCOMPLETE", "a run printed fewer than 12 bounds"
    m0, r = ms[0], [m / ms[0] for m in ms[1:]]
    full, three = chain_up(ms), chain_up(ms[1:])
    big = r[2] >= 100
    if full and big:
        word = "NULL AT THE ROOT"
    elif all(1 / 3 <= x <= 3 for x in r):
        word = "NOT NULL"
    else:
        word = "UNDECIDED"
    why = f"ratios m/m0 {r[0]:.3g}, {r[1]:.3g}, {r[2]:.3g}; rises m0 to 1e-18 {full}, over 1e-20 to 1e-18 {three}; m(1e-18) >= 100 m0 {big}"
    alt = "NULL AT THE ROOT" if (three and big) else word
    if alt != word:
        why += f"; FLAG: the reading over the three nonzero delta alone gives {alt}"
    return word, why


def control(ctrl, ref):
    a, b = ctrl["lines"][:N], ref["lines"][:N]
    if len(b) < N:
        return False, f"reference has {len(b)} start lines"
    if len(a) < N:
        return False, f"control printed {len(a)} of {N} start lines"
    bad = [i for i in range(N) if a[i] != b[i]]
    return (not bad), (f"all {N} start lines equal #951's first {N} (every printed digit)" if not bad else f"start lines differ at {bad}")


def report(logs, ref_path):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _ in RUNS}
    ref = parse(ref_path)
    ok, why = control(R["c_d0"], ref)
    print(f"Control: {'PASS' if ok else 'FAIL'}, {why}.\n")
    print("| run | delta | printed max abs F | bounds printed | m (median of the bounds) | m / m0 | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    ms = []
    for lab, d in RUNS:
        r = R[lab]
        full = len(r["bounds"]) >= N
        m = median(r["bounds"][:N]) if full else None
        ms.append(m)
        pr = sorted(r["prods"][:N])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:N] if x >= CAP)} of {len(r['prods'][:N])}"
        worst = f"{max(float(x) for x in r['res'][:N]):.1e}" if r["res"] else "-"
        ratio = f"{m / ms[0]:.4g}" if m and ms[0] else ("1" if lab == "c_d0" and m else "-")
        print(f"| {lab} | {d} | {r['maxF'] or '-'} | {len(r['bounds'])} | {f'{m:.4e}' if m else '-'} | {ratio} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nThe bounds of each run, start 0 to 11:\n")
    print("| start | " + " | ".join(lab for lab, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(N):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _ in RUNS) + " |")
    word, vwhy = verdict(ms)
    print(f"\nVerdict by the pre-set criteria: **{word}** ({vwhy}).")
    return ok, word


def selftest(bad=0):
    def mk(td, name, bounds, prods=None, mu="+1.00e+00", maxF="1.0e-30", tail=True):
        with open(os.path.join(td, f"{name}.log"), "w") as f:
            f.write(f"X.npz: D 40.020065 32x121 K 0, max|F| {maxF}\n  right-hand sides: rough (independent normal entries)\n")
            for i, b in enumerate(bounds):
                f.write(f"  start {i}: max|x| {1 / b:.3e}, bound on the smallest gain {b:.3e}, max|J x - v| 1.0e-17, {(prods or [67] * 99)[i]} products\n")
            if tail:
                f.write(f"  start 0, x / max|x|: mu {mu}; w1 max 4.0e-02\n  best bound on the smallest gain (max norm) {min(bounds):.3e}; the bounds of the starts span a factor 2.0\n")
    base = [1e-35 * (1 + 0.1 * i) for i in range(N)]
    m0 = median(base)
    cases = {  # name: (factors of m0 at 1e-20, 1e-19, 1e-18, want)
        "null": ([2, 30, 400], "NULL AT THE ROOT"), "null at exactly 100": ([1.5, 20, 100.0], "NULL AT THE ROOT"),
        "not null": ([1.1, 0.8, 2.9], "NOT NULL"), "not null near the edges": ([0.34, 2.95, 0.5], "NOT NULL"),
        "rises but under 100": ([2, 10, 99], "UNDECIDED"), "big but not rising": ([3, 2, 400], "UNDECIDED"),
        "outside the band once": ([1.1, 3.5, 1.0], "UNDECIDED")}
    with tempfile.TemporaryDirectory() as td:
        for name, (fac, want) in cases.items():
            for lab, f in zip(["c_d0", "c_d1e-20", "c_d1e-19", "c_d1e-18"], [1.0] + fac):
                mk(td, lab, [b * f for b in base])
            ms = [median(parse(os.path.join(td, f"{lab}.log"))["bounds"]) for lab, _ in RUNS]
            got, _ = verdict(ms)
            ok = got == want
            print(f"  {name}: verdict {got} (want {want}) {'ok' if ok else 'WRONG'}")
            bad += not ok
        # the control of the verdict: with the 100x rule mutated to 1000x a planted 400x null must stop reading as NULL
        ms = [m0, 2 * m0, 30 * m0, 400 * m0]
        word, _ = verdict(ms)
        mut = (lambda s: s.replace("r[2] >= 100", "r[2] >= 1000"))(open(__file__).read())
        ns = {"__file__": __file__}
        exec(compile(mut.split("def selftest")[0], "mut", "exec"), ns)
        wm, _ = ns["verdict"](ms)
        ok = word == "NULL AT THE ROOT" and wm != word
        print(f"  mutated 100x rule (1000x): 400x case reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the threshold'}")
        bad += not ok
        # an incomplete run (11 bounds) gives INCOMPLETE, and a control with one digit changed fails
        mk(td, "c_d1e-18", [b * 400 for b in base][:11], tail=False)
        r = parse(os.path.join(td, "c_d1e-18.log"))
        word, _ = verdict([m0, m0, m0, median(r["bounds"]) if len(r["bounds"]) >= N else None])
        ok = word == "INCOMPLETE"
        print(f"  11 bounds: {word} (want INCOMPLETE) {'ok' if ok else 'WRONG'}")
        bad += not ok
        mk(td, "ref", base)
        mk(td, "ctl", base)
        okc, _ = control(parse(os.path.join(td, "ctl.log")), parse(os.path.join(td, "ref.log")))
        mk(td, "ctl", [base[0] * 1.01] + base[1:])
        okm, _ = control(parse(os.path.join(td, "ctl.log")), parse(os.path.join(td, "ref.log")))
        ok = okc and not okm
        print(f"  control compare: equal logs {okc}, one bound changed by 1% (a printed digit) {okm} (want True, False) {'ok' if ok else 'WRONG'}")
        bad += not ok
        # median convention, checked by hand: bounds 1..12 give sqrt(6 * 7)
        ok = abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12 and median([3.0, 1.0, 2.0]) == 2.0
        print(f"  median: geometric mean of the two middle ones for 12, the middle one for 3: {'ok' if ok else 'WRONG'}")
        bad += not ok
        # the parser on the real #951 log: 48 starts, first header max|F| 6.91e-31, start 0 mu +1.00e+00
        if os.path.exists(REF):
            p = parse(REF)
            ok = len(p["bounds"]) >= 48 and p["maxF"] == "6.91e-31" and p["mu0"] == "+1.00e+00" and p["prods"][0] == 73
            print(f"  parse of #951's K0c log: {len(p['bounds'])} bounds, max|F| {p['maxF']}, mu {p['mu0']}, products[0] {p['prods'][0]} {'ok' if ok else 'WRONG'}")
            bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logs = sys.argv[sys.argv.index("--logs") + 1] if "--logs" in sys.argv else os.path.join(HERE, "logs")
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else REF
    ok, word = report(logs, ref)
    sys.exit(0 if ok else 1)
