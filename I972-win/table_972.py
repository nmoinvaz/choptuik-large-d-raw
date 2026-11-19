#!/usr/bin/env python3
"""#972 (win): tables and the verdict by the issue's criteria, from logs/c_{orth,sum}_d{1e-20,1e-19}.log. From I969-win/table_969.py.

usage: python table_972.py [--selftest] [--logs DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones for an even count, as table_701.median).
m_rand(delta) is #963's median at the same delta (I963-win/README.md): 5.4593e-24 at 1e-20 and 2.6809e-22 at 1e-19.
 - IN THE ROOT SET if all four m (orth and sum, 1e-20 and 1e-19) are <= 1e-3 m_rand at the same delta.
 - NOT IN THE ROOT SET if any of the four m / m_rand is in [0.1, 10].   UNDECIDED otherwise.   INCOMPLETE if a run printed fewer than 12 bounds."""
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R963 = r"C:\Users\nathan\Source\choptuik-large-d-raw\I963-win\logs"
RUNS = [(f"c_{m}_d{d}", m, d, q) for m in ("orth", "sum") for d, q in (("1e-20", 5.4593e-24), ("1e-19", 2.6809e-22))]
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
    """ms = the four m in RUNS order, None where a run is incomplete. Returns (word, why)."""
    rand = rand or [x[3] for x in RUNS]
    if any(m is None for m in ms):
        return "INCOMPLETE", "a run printed fewer than 12 bounds"
    r = [m / q for m, q in zip(ms, rand)]
    if all(x <= 1e-3 for x in r):
        word = "IN THE ROOT SET"
    elif any(0.1 <= x <= 10 for x in r):
        word = "NOT IN THE ROOT SET"
    else:
        word = "UNDECIDED"
    return word, "m / m_rand " + ", ".join(f"{x:.3g}" for x in r) + " (orth 1e-20, orth 1e-19, sum 1e-20, sum 1e-19)"


def reading(word):
    return {"IN THE ROOT SET": "both directions in the plane of a, b, c are tangent at both deltas, consistent with a two-dimensional set of roots through the samples, so the RT system lacks at least two conditions there",
            "NOT IN THE ROOT SET": "at least one direction in the plane of a, b, c is not tangent, so a two-dimensional set of roots through the samples is not shown (a union of curves or a curved surface is possible)",
            "UNDECIDED": "neither reading is fixed by the criteria",
            "INCOMPLETE": "no decision by the criteria"}[word]


def report(logs):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _, _, _ in RUNS}
    print("| run | mode | delta | printed max abs F | bounds printed | m (median of the bounds) | m_rand (#963) | m / m_rand | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    ms = []
    for lab, mo, d, q in RUNS:
        r = R[lab]
        m = median(r["bounds"][:N]) if len(r["bounds"]) >= N else None
        ms.append(m)
        pr = sorted(r["prods"][:N])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:N] if x >= CAP)} of {len(r['prods'][:N])}"
        worst = f"{max(float(x) for x in r['res'][:N]):.1e}" if r["res"] else "-"
        print(f"| {lab} | {mo} | {d} | {r['maxF'] or '-'} | {len(r['bounds'])} | {f'{m:.4e}' if m else '-'} | {q:.4e} | {f'{m / q:.4g}' if m else '-'} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nThe bounds of each run, start 0 to 11:\n")
    print("| start | " + " | ".join(lab for lab, _, _, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(N):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _, _, _ in RUNS) + " |")
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
    rand = [x[3] for x in RUNS]
    base = [1 + 0.1 * i for i in range(N)]
    gm = lambda b: math.exp(sum(math.log(x) for x in sorted(b)[N // 2 - 1:N // 2 + 1]) / 2)
    cases = {"all in": ((1e-5, 1e-6, 1e-7, 1e-6), "IN THE ROOT SET"), "all at the edge": ((0.9e-3,) * 4, "IN THE ROOT SET"),
             "one just above the bar": ((1e-6, 1.1e-3, 1e-6, 1e-6), "UNDECIDED"), "one in the band": ((1e-6, 1e-6, 1.0, 1e-6), "NOT IN THE ROOT SET"),
             "last in the band": ((1e-6, 1e-6, 1e-6, 0.11), "NOT IN THE ROOT SET"), "all not": ((1.0, 0.7, 2.0, 9.5), "NOT IN THE ROOT SET"),
             "one just under 0.1": ((1e-6, 0.09, 1e-6, 1e-6), "UNDECIDED"), "one just over 10": ((1e-6, 1e-6, 11.0, 1e-6), "UNDECIDED"),
             "one at 1e-2 and one at 50": ((1e-2, 1e-6, 50.0, 1e-6), "UNDECIDED"), "in between": ((5e-3,) * 4, "UNDECIDED"),
             "one band value beside an in-between": ((5e-3, 1e-6, 1e-6, 1.0), "NOT IN THE ROOT SET")}
    with tempfile.TemporaryDirectory() as td:
        for name, (fac, want) in cases.items():
            for (lab, _, _, q), f in zip(RUNS, fac):
                mk(td, lab, [b * q * f / gm(base) for b in base])
            ms = [median(parse(os.path.join(td, f"{lab}.log"))["bounds"]) for lab, _, _, _ in RUNS]
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
        ok = word == "UNDECIDED" and wm == "IN THE ROOT SET"
        print(f"  mutated in-set bar (1e-2): the 5e-3 case reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the bar'}")
        bad += not ok
        mut = open(__file__).read().replace("any(0.1 <= x <= 10 for x in r)", "all(0.1 <= x <= 10 for x in r)")
        ns = {"__file__": __file__}
        exec(compile(mut.split("def reading")[0], "mut", "exec"), ns)
        ms = [1e-6 * q for q in rand[:3]] + [1.0 * rand[3]]
        wm, _ = ns["verdict"](ms)
        word, _ = verdict(ms)
        ok = word == "NOT IN THE ROOT SET" and wm == "UNDECIDED"
        print(f"  mutated not rule (all for any): one in the band reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the rule'}")
        bad += not ok
        w1, _ = verdict([None] + [q for q in rand[1:]])
        ok = w1 == "INCOMPLETE"
        print(f"  an incomplete run: {w1} (want INCOMPLETE) {'ok' if ok else 'WRONG'}")
        bad += not ok
        ok = abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12 and median([3.0, 1.0, 2.0]) == 2.0
        print(f"  median: geometric mean of the two middle ones for 12, the middle one for 3: {'ok' if ok else 'WRONG'}")
        bad += not ok
        for d, q in (("1e-20", 5.4593e-24), ("1e-19", 2.6809e-22)):
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
