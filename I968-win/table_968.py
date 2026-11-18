#!/usr/bin/env python3
"""#968 (win): tables and the verdict by the issue's criteria, from logs/c_along_d1e-20.log, c_along_d1e-19.log, c_along_d1e-18.log. From I963-win/table_963.py.

usage: python table_968.py [--selftest] [--logs DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). m = the median of a run's 12 bounds (geometric mean of the two middle ones for an even count, as table_701.median).
m_rand(delta) is #963's median at the same delta (I963-win/README.md): 5.4593e-24, 2.6809e-22, 4.0592e-21 at 1e-20, 1e-19, 1e-18.
 - ALONG A FAMILY if m(1e-20) <= 1e-3 m_rand(1e-20) and m(1e-19) <= 1e-3 m_rand(1e-19).
 - NOT ALONG A FAMILY if m / m_rand is in [0.1, 10] at both 1e-20 and 1e-19.   UNDECIDED otherwise.   INCOMPLETE if a run of 1e-20 or 1e-19 printed fewer than 12 bounds.
 - m(1e-18) and its ratio to m_rand(1e-18) are reported, not part of the verdict."""
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R963 = r"C:\Users\nathan\Source\choptuik-large-d-raw\I963-win\logs"
RUNS = [("c_along_d1e-20", "1e-20", 5.4593e-24), ("c_along_d1e-19", "1e-19", 2.6809e-22), ("c_along_d1e-18", "1e-18", 4.0592e-21)]
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
    """ms = [m(1e-20), m(1e-19), m(1e-18)], None where a run is incomplete. Returns (word, why)."""
    rand = rand or [x[2] for x in RUNS]
    if ms[0] is None or ms[1] is None:
        return "INCOMPLETE", "a run of 1e-20 or 1e-19 printed fewer than 12 bounds"
    r = [m / q if m is not None else None for m, q in zip(ms, rand)]
    if r[0] <= 1e-3 and r[1] <= 1e-3:
        word = "ALONG A FAMILY"
    elif all(0.1 <= x <= 10 for x in r[:2]):
        word = "NOT ALONG A FAMILY"
    else:
        word = "UNDECIDED"
    why = f"m / m_rand {r[0]:.3g} at 1e-20, {r[1]:.3g} at 1e-19" + (f", {r[2]:.3g} at 1e-18 (reported only)" if r[2] is not None else ", 1e-18 incomplete")
    return word, why


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
    print(f"\nVerdict by the pre-set criteria: **{word}** ({why}).")
    return word


def selftest(bad=0):
    def mk(td, name, bounds, prods=None, mu="+1.00e+00", maxF="1.0e-30", tail=True):
        with open(os.path.join(td, f"{name}.log"), "w") as f:
            f.write(f"X.npz: D 40.020065 32x121 K 0, max|F| {maxF}\n  right-hand sides: rough (independent normal entries)\n")
            for i, b in enumerate(bounds):
                f.write(f"  start {i}: max|x| {1 / b:.3e}, bound on the smallest gain {b:.3e}, max|J x - v| 1.0e-17, {(prods or [67] * 99)[i]} products\n")
            if tail:
                f.write(f"  start 0, x / max|x|: mu {mu}; w1 max 4.0e-02\n  best bound on the smallest gain (max norm) {min(bounds):.3e}; the bounds of the starts span a factor 2.0\n")
    rand = [x[2] for x in RUNS]
    base = [1 + 0.1 * i for i in range(N)]
    cases = {  # name: (ratios to m_rand at 1e-20, 1e-19, 1e-18, want)
        "along": ((1e-5, 1e-6, 5.0), "ALONG A FAMILY"), "along at the edge": ((0.9e-3, 0.9e-3, 1.0), "ALONG A FAMILY"),
        "just above the along bar": ((1.1e-3, 1e-6, 1.0), "UNDECIDED"),
        "not along": ((1.0, 0.7, 2.0), "NOT ALONG A FAMILY"), "not along near the edges": ((0.11, 9.5, 1e-6), "NOT ALONG A FAMILY"),
        "just under 0.1": ((0.09, 1.0, 1.0), "UNDECIDED"), "just over 10": ((1.0, 11.0, 1.0), "UNDECIDED"),
        "one along, one not": ((1e-5, 1.0, 1.0), "UNDECIDED"), "in between": ((5e-3, 5e-3, 1.0), "UNDECIDED"),
        "1e-18 does not matter": ((1e-5, 1e-6, 1e9), "ALONG A FAMILY")}
    gm = lambda b: math.exp(sum(math.log(x) for x in sorted(b)[N // 2 - 1:N // 2 + 1]) / 2)
    with tempfile.TemporaryDirectory() as td:
        for name, (fac, want) in cases.items():
            for (lab, _, q), f in zip(RUNS, fac):
                mk(td, lab, [b * q * f / gm(base) for b in base])
            ms = [median(parse(os.path.join(td, f"{lab}.log"))["bounds"]) for lab, _, _ in RUNS]
            got, _ = verdict(ms)
            ok = got == want
            print(f"  {name}: verdict {got} (want {want}) {'ok' if ok else 'WRONG'}")
            bad += not ok
        # the control of the verdict: with the along bar mutated from 1e-3 to 1e-2 the planted 5e-3 case must change
        ms = [5e-3 * q for q in rand]
        word, _ = verdict(ms)
        mut = open(__file__).read().replace("r[0] <= 1e-3 and r[1] <= 1e-3", "r[0] <= 1e-2 and r[1] <= 1e-2")
        ns = {"__file__": __file__}
        exec(compile(mut.split("def report")[0], "mut", "exec"), ns)
        wm, _ = ns["verdict"](ms)
        ok = word == "UNDECIDED" and wm == "ALONG A FAMILY"
        print(f"  mutated along bar (1e-2): the 5e-3 case reads {wm} against {word} {'ok' if ok else 'WRONG, the test cannot see the bar'}")
        bad += not ok
        # incomplete runs
        w1, _ = verdict([None, rand[1], rand[2]])
        w2, _ = verdict([rand[0], rand[1], None])
        ok = w1 == "INCOMPLETE" and w2 == "NOT ALONG A FAMILY"
        print(f"  incomplete 1e-20 run: {w1}; incomplete 1e-18 run only: {w2} (want INCOMPLETE, a verdict) {'ok' if ok else 'WRONG'}")
        bad += not ok
        ok = abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12 and median([3.0, 1.0, 2.0]) == 2.0
        print(f"  median: geometric mean of the two middle ones for 12, the middle one for 3: {'ok' if ok else 'WRONG'}")
        bad += not ok
        # the parser and m_rand on #963's real logs: its medians must equal the constants above to 5 digits
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
