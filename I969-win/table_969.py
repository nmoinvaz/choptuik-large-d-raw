#!/usr/bin/env python3
"""#969 (win): tables and the verdict by the issue's criteria, from logs/c_alongb_d1e-20.log and logs/c_alongb_d1e-19.log. From I968-win/table_968.py.

usage: python table_969.py [--selftest] [--logs DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones for an even count, as table_701.median).
m_rand(delta) is #963's median at the same delta (I963-win/README.md): 5.4593e-24 at 1e-20 and 2.6809e-22 at 1e-19.
 - ALONG THE ROOT SET if m(1e-20) <= 1e-3 m_rand(1e-20) and m(1e-19) <= 1e-3 m_rand(1e-19).
 - NOT ALONG if m / m_rand is in [0.1, 10] at both.   UNDECIDED otherwise.   INCOMPLETE if a run printed fewer than 12 bounds.
 - With #968's ALONG A FAMILY for a - c, 'along' for b - c as well makes the set at least two-dimensional (the cosine of a - c and b - c is 0.234, orth.log)."""
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R963 = r"C:\Users\nathan\Source\choptuik-large-d-raw\I963-win\logs"
RUNS = [("c_alongb_d1e-20", "1e-20", 5.4593e-24), ("c_alongb_d1e-19", "1e-19", 2.6809e-22)]
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
    r = dict(maxF=None, bounds=[], prods=[], res=[], mu0=None)
    if not os.path.exists(path):
        return r
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\r\n")
        m = START.match(ln)
        if m:
            r["bounds"].append(float(m.group(3)))
            r["prods"].append(int(m.group(5)))
            r["res"].append(m.group(4))
        elif r["maxF"] is None and HEAD.search(ln):
            r["maxF"] = HEAD.search(ln).group(1)
        elif MU.match(ln):
            r["mu0"] = MU.match(ln).group(1)
    return r


def verdict(ms, rand=None):
    """ms = [m(1e-20), m(1e-19)], None where a run is incomplete. Returns (word, why)."""
    rand = rand or [x[2] for x in RUNS]
    if any(m is None for m in ms):
        return "INCOMPLETE", "a run printed fewer than 12 bounds"
    r = [m / q for m, q in zip(ms, rand)]
    if all(x <= 1e-3 for x in r):
        word = "ALONG THE ROOT SET"
    elif all(0.1 <= x <= 10 for x in r):
        word = "NOT ALONG"
    else:
        word = "UNDECIDED"
    return word, f"m / m_rand {r[0]:.3g} at 1e-20, {r[1]:.3g} at 1e-19"


def reading(word):
    return {"ALONG THE ROOT SET": "with #968's a - c also along (ALONG A FAMILY) and the cosine 0.234 between a - c and b - c, the set of roots near c is at least two-dimensional",
            "NOT ALONG": "b - c is not a null direction by this test, so one null direction (a - c) is shown so far",
            "UNDECIDED": "neither reading is fixed by the criteria",
            "INCOMPLETE": "no decision by the criteria"}[word]


def report(logs):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _, _ in RUNS}
    print("| run | delta | printed max abs F | bounds printed | m (median of the bounds) | m_rand (#963) | m / m_rand | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    ms = []
    for lab, d, q in RUNS:
        r = R[lab]
        m = median(r["bounds"][:N]) if len(r["bounds"]) >= N else None
        ms.append(m)
        pr = sorted(r["prods"][:N])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:N] if x >= CAP)} of {len(r['prods'][:N])}"
        worst = f"{max(float(x) for x in r['res'][:N]):.1e}" if r["res"] else "-"
        print(f"| {lab} | {d} | {r['maxF'] or '-'} | {len(r['bounds'])} | {f'{m:.4e}' if m else '-'} | {q:.4e} | {f'{m / q:.4g}' if m else '-'} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nThe bounds of each run, start 0 to 11:\n")
    print("| start | " + " | ".join(lab for lab, _, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(N):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _, _ in RUNS) + " |")
    word, why = verdict(ms)
    print(f"\nVerdict by the pre-set criteria: **{word}** ({why}); {reading(word)}.")
    return word


def selftest(bad=0):
    def mk(td, name, bounds):
        with open(os.path.join(td, f"{name}.log"), "w") as f:
            f.write("X.npz: D 40.020065 32x121 K 0, max|F| 1.0e-30\n  right-hand sides: rough (independent normal entries)\n")
            for i, b in enumerate(bounds):
                f.write(f"  start {i}: max|x| {1 / b:.3e}, bound on the smallest gain {b:.3e}, max|J x - v| 1.0e-17, 67 products\n")
            f.write("  start 0, x / max|x|: mu +1.00e+00; w1 max 4.0e-02\n")
    rand = [x[2] for x in RUNS]
    base = [1 + 0.1 * i for i in range(N)]
    gm = lambda b: math.exp(sum(math.log(x) for x in sorted(b)[N // 2 - 1:N // 2 + 1]) / 2)
    cases = {"along": ((1e-5, 1e-6), "ALONG THE ROOT SET"), "along at the edge": ((0.9e-3, 0.9e-3), "ALONG THE ROOT SET"), "just above the bar": ((1.1e-3, 1e-6), "UNDECIDED"),
             "not along": ((1.0, 0.7), "NOT ALONG"), "not along near the edges": ((0.11, 9.5), "NOT ALONG"), "just under 0.1": ((0.09, 1.0), "UNDECIDED"),
             "just over 10": ((1.0, 11.0), "UNDECIDED"), "one along, one not": ((1e-5, 1.0), "UNDECIDED"), "in between": ((5e-3, 5e-3), "UNDECIDED")}
    with tempfile.TemporaryDirectory() as td:
        for name, (fac, want) in cases.items():
            for (lab, _, q), f in zip(RUNS, fac):
                mk(td, lab, [b * q * f / gm(base) for b in base])
            ms = [median(parse(os.path.join(td, f"{lab}.log"))["bounds"]) for lab, _, _ in RUNS]
            got, _ = verdict(ms)
            ok = got == want
            print(f"  {name}: verdict {got} (want {want}) {'ok' if ok else 'WRONG'}")
            bad += not ok
        ms = [5e-3 * q for q in rand]
        word, _ = verdict(ms)
        mut = open(__file__).read().replace("all(x <= 1e-3 for x in r)", "all(x <= 1e-2 for x in r)")
        ns = {"__file__": __file__}
        exec(compile(mut.split("def reading")[0], "mut", "exec"), ns)
        wm, _ = ns["verdict"](ms)
        ok = word == "UNDECIDED" and wm == "ALONG THE ROOT SET"
        print(f"  mutated along bar (1e-2): the 5e-3 case reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the bar'}")
        bad += not ok
        w1, _ = verdict([None, rand[1]])
        ok = w1 == "INCOMPLETE"
        print(f"  an incomplete run: {w1} (want INCOMPLETE) {'ok' if ok else 'WRONG'}")
        bad += not ok
        ok = abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12 and median([3.0, 1.0, 2.0]) == 2.0
        print(f"  median: geometric mean of the two middle ones for 12, the middle one for 3: {'ok' if ok else 'WRONG'}")
        bad += not ok
        for lab, d, q in RUNS:
            p = parse(os.path.join(R963, f"c_d{d}.log"))
            if len(p["bounds"]) >= N:
                m = median(p["bounds"][:N])
                ok = abs(m / q - 1) < 5e-5
                print(f"  #963's c_d{d}: median {m:.4e} against m_rand {q:.4e} {'ok' if ok else 'WRONG'}")
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
