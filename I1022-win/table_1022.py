#!/usr/bin/env python3
"""#1022 (win): tables and the reading by the issue's criteria, from logs/c_{q0,q1,rand}_d{1e-18,1e-17}.log. From I1018-win/table_1018.py.

usage: python table_1022.py [--selftest] [--logs DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones for an even count, as table_701.median).
For each size delta (1e-18, 1e-17) m_rand(delta) is this task's own random move (seed 977) at that delta. For each row k = 0, 1: r = m(row k, delta) / m_rand(delta).
 - r <= 1e-3 reads TANGENT at that size, r in [0.1, 10] reads LEAVING the set, any other r reads UNDECIDED, a missing bound (a run with fewer than 12 bounds) reads INCOMPLETE.
 - A size reads TANGENT when both rows do, LEAVING when either row does (INCOMPLETE if any run needed is), UNDECIDED otherwise."""
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
R963 = os.path.join(RAW, "I963-win", "logs")
R1018 = os.path.join(RAW, "I1018-win", "logs")
DELTAS = ("1e-18", "1e-17")
RUNS = [(f"c_{m}_d{d}", m, d) for d in DELTAS for m in ("q0", "q1", "rand")]
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
    r = dict(maxF=None, bounds=[], bstr=[], prods=[], res=[], mu0=None)
    if not os.path.exists(path):
        return r
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\r\n")
        m = START.match(ln)
        if m:
            r["bounds"].append(float(m.group(3)))
            r["bstr"].append(m.group(3))
            r["prods"].append(int(m.group(5)))
            r["res"].append(m.group(4))
        elif r["maxF"] is None and HEAD.search(ln):
            r["maxF"] = HEAD.search(ln).group(1)
        elif MU.match(ln):
            r["mu0"] = MU.match(ln).group(1)
    return r


def med(r):
    return median(r["bounds"][:N]) if len(r["bounds"]) >= N else None


def cls(r):
    if r is None:
        return "INCOMPLETE"
    if r <= 1e-3:
        return "TANGENT"
    if 0.1 <= r <= 10:
        return "LEAVING"
    return "UNDECIDED"


def size_word(c0, c1):
    if "INCOMPLETE" in (c0, c1):
        return "INCOMPLETE"
    if "LEAVING" in (c0, c1):
        return "LEAVING"
    return "TANGENT" if c0 == c1 == "TANGENT" else "UNDECIDED"


def reading(ms):
    """ms = {(row, delta): m} with row in q0, q1, rand, None for an incomplete run. Returns ({delta: (ratio0, ratio1, class0, class1, word)}, summary)"""
    out = {}
    for d in DELTAS:
        mr = ms.get(("rand", d))
        rr = [None if (ms.get((k, d)) is None or mr is None) else ms[(k, d)] / mr for k in ("q0", "q1")]
        c = [cls(x) for x in rr]
        out[d] = (rr[0], rr[1], c[0], c[1], size_word(*c))
    words = [out[d][4] for d in DELTAS]
    if "INCOMPLETE" in words:
        s = "INCOMPLETE"
    elif words == ["TANGENT", "TANGENT"]:
        s = "TANGENT at both sizes"
    elif words[0] == "TANGENT" and words[1] == "LEAVING":
        s = "TANGENT at 1e-18, LEAVING at 1e-17"
    elif words[0] == "LEAVING":
        s = "LEAVING already at 1e-18"
    else:
        s = "mixed: 1e-18 " + words[0] + ", 1e-17 " + words[1]
    return out, s


def meaning(s):
    return {"TANGENT at both sizes": "the tangency of both out-of-plane directions holds out to 1e-17 of max|z| (370 times the longer chord b - c, 2.7e-20), so the four-dimensional set does not curve away from its tangent space by that size",
            "TANGENT at 1e-18, LEAVING at 1e-17": "the set curves away from its tangent space between 1e-18 and 1e-17 of max|z| (the extent of the flat part is between 37 and 370 times the longer chord)",
            "LEAVING already at 1e-18": "the set curves away from its tangent space by 1e-18 of max|z| (37 times the longer chord)",
            "INCOMPLETE": "a run needed did not print 12 bounds, no reading by the criteria"}.get(s, "neither reading is fixed by the criteria")


def series(m_of):
    """m along each row at 1e-20 .. 1e-17 against the random move at the same size: from the stored logs of #963 (random) and #1018 (rows)"""
    rows = []
    for d in ("1e-20", "1e-19"):
        rand = parse(os.path.join(R963, f"c_d{d}.log"))
        rows.append((d, med(rand), [med(parse(os.path.join(R1018, f"c_q{k}_d{d}.log"))) for k in (0, 1)]))
    for d in DELTAS:
        rows.append((d, m_of.get(("rand", d)), [m_of.get((f"q{k}", d)) for k in (0, 1)]))
    return rows


def fmt(x, f=".4e"):
    return "-" if x is None else format(x, f)


def report(logs):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _, _ in RUNS}
    ms = {(mo, d): med(R[lab]) for lab, mo, d in RUNS}
    out, summ = reading(ms)
    print("| run | row | delta | printed max abs F | bounds printed | m (median of the bounds) | m_rand at this delta | m / m_rand | reading | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for lab, mo, d in RUNS:
        r = R[lab]
        m = ms[(mo, d)]
        pr = sorted(r["prods"][:N])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:N] if x >= CAP)} of {len(r['prods'][:N])}"
        worst = f"{max(float(x) for x in r['res'][:N]):.1e}" if r["res"] else "-"
        mr = ms[("rand", d)]
        if mo == "rand":
            ratio, word = "-", "reference"
        else:
            k = 0 if mo == "q0" else 1
            rr, word = out[d][k], out[d][2 + k]
            ratio = "-" if rr is None else f"{rr:.4g}"
        print(f"| {lab} | {mo} | {d} | {r['maxF'] or '-'} | {len(r['bounds'])} | {fmt(m)} | {fmt(mr)} | {ratio} | {word} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nThe bounds of each run, start 0 to 11:\n")
    print("| start | " + " | ".join(lab for lab, _, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(N):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _, _ in RUNS) + " |")
    print("\nThe extent of the scan, m along each row and the random move at each size (1e-20 and 1e-19 from #963 and #1018's logs, 1e-18 and 1e-17 from this task):\n")
    print("| delta | m_rand | m along q0 | m along q1 | q0 / m_rand | q1 / m_rand |\n|---|---|---|---|---|---|")
    for d, mr, (a, b) in series(ms):
        ra = "-" if (a is None or mr is None) else f"{a / mr:.3g}"
        rb = "-" if (b is None or mr is None) else f"{b / mr:.3g}"
        print(f"| {d} | {fmt(mr)} | {fmt(a)} | {fmt(b)} | {ra} | {rb} |")
    p = parse(os.path.join(R963, "c_d1e-18.log"))
    mine = R["c_rand_d1e-18"]
    if len(p["bounds"]) >= N and len(mine["bounds"]) >= N:
        eq = sum(1 for i in range(N) if p["bstr"][i] == mine["bstr"][i])
        eqp = sum(1 for i in range(N) if p["prods"][i] == mine["prods"][i])
        print(f"\nInformational control, the random move at 1e-18 against #963's c_d1e-18.log (the same state, bit for bit): {eq} of {N} bounds equal in every printed digit, {eqp} of {N} product counts equal, median {median(mine['bounds'][:N]):.4e} against {median(p['bounds'][:N]):.4e}.")
    print("\nReading by the pre-set criteria, per size (row 0, row 1):")
    for d in DELTAS:
        a, b, ca, cb, w = out[d]
        print(f"- {d}: q0 / m_rand {'-' if a is None else f'{a:.3g}'} ({ca}), q1 / m_rand {'-' if b is None else f'{b:.3g}'} ({cb}): **{w}**")
    print(f"\nReading: **{summ}**; {meaning(summ)}.")
    return summ


def selftest(bad=0):
    def mk(td, name, bounds, f=1.0):
        with open(os.path.join(td, f"{name}.log"), "w") as fh:
            fh.write("X.npz: D 40.020065 32x121 K 0, max|F| 1.0e-30\n  right-hand sides: rough (independent normal entries)\n")
            for i, b in enumerate(bounds):
                fh.write(f"  start {i}: max|x| {1 / b:.3e}, bound on the smallest gain {b:.3e}, max|J x - v| 1.0e-17, 67 products\n")
            fh.write("  start 0, x / max|x|: mu +1.00e+00; w1 max 4.0e-02\n")
    base = [1 + 0.1 * i for i in range(N)]
    gm = lambda b: math.exp(sum(math.log(x) for x in sorted(b)[N // 2 - 1:N // 2 + 1]) / 2)
    rand = {"1e-18": 4.06e-21, "1e-17": 1e-19}
    # factors m / m_rand for (q0 18, q1 18, q0 17, q1 17)
    cases = {"all tangent": ((1e-5, 1e-6, 1e-7, 1e-6), "TANGENT at both sizes"), "all at the edge": ((0.9e-3,) * 4, "TANGENT at both sizes"),
             "one just above the bar": ((1e-6, 1.1e-3, 1e-6, 1e-6), "mixed: 1e-18 UNDECIDED, 1e-17 TANGENT"),
             "leaves at 1e-17 in row 1": ((1e-6, 1e-6, 1e-6, 0.5), "TANGENT at 1e-18, LEAVING at 1e-17"),
             "leaves at 1e-17 in row 0 at 0.1": ((1e-6, 1e-6, 0.1, 1e-6), "TANGENT at 1e-18, LEAVING at 1e-17"),
             "leaves at 1e-18 in row 0": ((2.0, 1e-6, 1e-6, 1e-6), "LEAVING already at 1e-18"),
             "one just under 0.1 at 1e-17": ((1e-6, 1e-6, 0.09, 1e-6), "mixed: 1e-18 TANGENT, 1e-17 UNDECIDED"),
             "one just over 10": ((1e-6, 1e-6, 11.0, 1e-6), "mixed: 1e-18 TANGENT, 1e-17 UNDECIDED"),
             "undecided beside leaving at 1e-17": ((1e-6, 1e-6, 5e-3, 1.0), "TANGENT at 1e-18, LEAVING at 1e-17")}
    with tempfile.TemporaryDirectory() as td:
        for name, (fac, want) in cases.items():
            for d in DELTAS:
                mk(td, f"c_rand_d{d}", [b * rand[d] / gm(base) for b in base])
            for (k, d), f in zip((("q0", "1e-18"), ("q1", "1e-18"), ("q0", "1e-17"), ("q1", "1e-17")), fac):
                mk(td, f"c_{k}_d{d}", [b * rand[d] * f / gm(base) for b in base])
            ms = {(mo, d): med(parse(os.path.join(td, f"{lab}.log"))) for lab, mo, d in RUNS}
            _, got = reading(ms)
            ok = got == want
            print(f"  {name}: reading {got} (want {want}) {'ok' if ok else 'WRONG'}")
            bad += not ok
        ms = {(mo, d): (rand[d] * (5e-3 if mo != "rand" else 1.0)) for _, mo, d in RUNS}
        _, word = reading(ms)
        mut = open(__file__).read().replace("if r <= 1e-3:", "if r <= 1e-2:")
        ns = {"__file__": __file__}
        exec(compile(mut.split("def meaning")[0], "mut", "exec"), ns)
        _, wm = ns["reading"](ms)
        ok = word.startswith("mixed") and wm == "TANGENT at both sizes"
        print(f"  mutated tangent bar (1e-2): the 5e-3 case reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the bar'}")
        bad += not ok
        mut = open(__file__).read().replace('if "LEAVING" in (c0, c1):', 'if "LEAVING" in (c0, c1) and c0 == c1:')
        ns = {"__file__": __file__}
        exec(compile(mut.split("def meaning")[0], "mut", "exec"), ns)
        ms = {(mo, d): rand[d] * (1e-6 if mo != "rand" else 1.0) for _, mo, d in RUNS}
        ms[("q1", "1e-17")] = 1.0 * rand["1e-17"]
        _, wm = ns["reading"](ms)
        _, word = reading(ms)
        ok = word == "TANGENT at 1e-18, LEAVING at 1e-17" and wm != word
        print(f"  mutated leaving rule (both rows for either): one row in the band reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the rule'}")
        bad += not ok
        mut = open(__file__).read().replace("0.1 <= r <= 10", "0.1 < r < 10")
        ns = {"__file__": __file__}
        exec(compile(mut.split("def meaning")[0], "mut", "exec"), ns)
        ok = cls(0.1) == "LEAVING" and ns["cls"](0.1) != "LEAVING" and cls(10.0) == "LEAVING" and ns["cls"](10.0) != "LEAVING"
        print(f"  mutated band edges (open for closed): the edges 0.1 and 10 read {ns['cls'](0.1)} and {ns['cls'](10.0)} against LEAVING {'ok' if ok else 'WRONG'}")
        bad += not ok
        ms = {(mo, d): rand[d] * (1e-6 if mo != "rand" else 1.0) for _, mo, d in RUNS}
        ms[("rand", "1e-17")] = None
        _, w1 = reading(ms)
        ms = {(mo, d): rand[d] * (1e-6 if mo != "rand" else 1.0) for _, mo, d in RUNS}
        ms[("q1", "1e-18")] = None
        _, w2 = reading(ms)
        ok = w1 == "INCOMPLETE" and w2 == "INCOMPLETE"
        print(f"  an incomplete random run, an incomplete row: {w1}, {w2} (want INCOMPLETE) {'ok' if ok else 'WRONG'}")
        bad += not ok
        ok = abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12 and median([3.0, 1.0, 2.0]) == 2.0
        print(f"  median: geometric mean of the two middle ones for 12, the middle one for 3: {'ok' if ok else 'WRONG'}")
        bad += not ok
        for d, q in (("1e-20", 5.4593e-24), ("1e-19", 2.6809e-22), ("1e-18", 4.0592e-21)):
            p = parse(os.path.join(R963, f"c_d{d}.log"))
            if len(p["bounds"]) >= N:
                m = median(p["bounds"][:N])
                ok = abs(m / q - 1) < 5e-5
                print(f"  #963's c_d{d}: median {m:.4e} against the stored {q:.4e} {'ok' if ok else 'WRONG'}")
                bad += not ok
            else:
                print(f"  #963's c_d{d}: log not found here, skipped")
    print("selftest", "FAILED" if bad else "passed")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logs = sys.argv[sys.argv.index("--logs") + 1] if "--logs" in sys.argv else os.path.join(HERE, "logs")
    report(logs)
