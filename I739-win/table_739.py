#!/usr/bin/env python3
"""#739: per Newton step of each octo-double run (ctl, A, B), and the same attempts in #726's quad-double run beside them.
usage: python table_739.py [--selftest]          (venv-t151 python, from this folder; reads logs/ctl.log, logs/A.log, logs/B.log and ../I726-win/table_726_out.md)
A step line is `  on N [full]: |F| X -> Y, |dz| U -> V, lam L, dDelta D, piv P, T s` (the first step may lack [full]); the converged line is `  on N: |F| X converged, Delta ...`.
The end of an attempt is `octo-double Newton: N steps, max|F| Y, converged|not converged`.
--selftest: planted log lines must parse to their values, and a planted not-converged ending must read NOT converged."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STEP = re.compile(r"^\s+on (\d+)(?: \[full\])?: \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9.]+), dDelta ([+-][0-9.e+-]+), .*?, ([0-9.]+) s$")
CONV = re.compile(r"^\s+on (\d+): \|F\| ([0-9.e+-]+) converged")
END = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)")


def parse(lines):
    steps, conv, end = [], None, None
    for ln in lines:
        m = STEP.match(ln)
        if m:
            steps.append(dict(n=int(m.group(1)), F0=float(m.group(2)), F1=float(m.group(3)), dz0=float(m.group(4)), dz1=float(m.group(5)), lam=float(m.group(6)), dD=float(m.group(7)), t=float(m.group(8))))
        m = CONV.match(ln)
        if m:
            conv = float(m.group(2))
        m = END.search(ln)
        if m:
            end = dict(steps=int(m.group(1)), F=float(m.group(2)), converged=m.group(3) == "converged")
    return steps, conv, end


def selftest():
    good = ["  on 0 [full]: |F| 1.21e-35 -> 1.96e-22, |dz| 7.48e-11 -> 6.67e-22, lam 1, dDelta +1.96e-17, piv 7.6e-20..8.6e+14, 97.17 s",
            "  on 1: |F| 7.83e-89 converged, Delta 1.73373739160322127 +3.5052e-17",
            "      octo-double Newton: 5 steps, max|F| 7.8e-89, converged; double-double |F| of its first two parts 1.0e-14"]
    s, c, e = parse(good)
    ok1 = len(s) == 1 and s[0]["F1"] == 1.96e-22 and s[0]["dD"] == 1.96e-17 and s[0]["t"] == 97.17 and c == 7.83e-89 and e["converged"] and e["steps"] == 5
    bad_end = ["      octo-double Newton: 9 steps, max|F| 2.7e-49, not converged; double-double |F| of its first two parts 9.3e-17"]
    _, _, e2 = parse(bad_end)
    ok2 = e2 is not None and not e2["converged"] and e2["F"] == 2.7e-49
    # a mutated step line (a missing arrow) must not parse as a step
    s3, _, _ = parse([good[0].replace("->", "to", 1)])
    ok3 = len(s3) == 0
    two = ["  on 0 [full]: |F| 6.61e-48 -> 2.45e-78, |dz| 8.42e-39 -> 2.62e-65, lam 1, dDelta -6.96e-46, piv 9.0e-20..8.3e+14, 100.83 s",
           "base I726-win/L/anm_pin13_D112.75.npz: D 112.75, M 32",
           "  on 0 [full]: |F| 1.21e-35 -> 1.96e-22, |dz| 7.48e-11 -> 6.67e-22, lam 1, dDelta +1.96e-17, piv 7.6e-20..8.6e+14, 97.17 s",
           "      octo-double Newton: 5 steps, max|F| 7.8e-89, converged; double-double |F| of its first two parts 1.0e-14",
           "    a 0.125 -> D 112.875: predicted |F| 1.01e-14, od 5 steps -> 1.00e-14"]
    seg = segments(two[:1] + ["base polish saved as C:/x/base_pin13_D112.7500.npz"] + two[1:])
    ok4 = [x[0] for x in seg] == ["base polish", "attempt a = 0.125 to D 112.875"] and parse(seg[0][1])[0][0]["F1"] == 2.45e-78 and parse(seg[1][1])[0][0]["F1"] == 1.96e-22
    print(f"  a planted base polish and attempt split into two segments, each with its own steps: {'ok' if ok4 else 'WRONG'}")
    ok1 = ok1 and ok4
    print(f"  planted step, converged and ending lines parse to their values: {'ok' if ok1 else 'WRONG'}")
    print(f"  planted not-converged ending reads NOT converged with its floor: {'ok' if ok2 else 'WRONG'}")
    print(f"  a mutated step line (no arrow) is not read as a step: {'ok' if ok3 else 'WRONG'}")
    bad = 3 - (ok1 + ok2 + ok3)
    print("selftest", "FAILED" if bad else "passed")
    return bad


ATT = re.compile(r"^    a ([0-9.]+) -> D ([0-9.]+)")
BASE = re.compile(r"^base \S+\.npz: ")     # the base summary line, not "base polish saved as ..."


def segments(lines):
    """[(label, lines)]: the base polish ends at the `base <state>:` line, an attempt at its `    a X -> D Y:` line; the rest is unfinished"""
    out, cur = [], []
    for ln in lines:
        cur.append(ln)
        if BASE.match(ln):
            out.append(("base polish", cur))
            cur = []
        else:
            m = ATT.match(ln)
            if m:
                out.append((f"attempt a = {m.group(1)} to D {m.group(2)}", cur))
                cur = []
    if any(STEP.match(x) or END.search(x) for x in cur):
        out.append(("unfinished (the run was stopped or is running)", cur))
    return out


def qd_rows():
    """#726's quad-double attempts from D 112.75 (step L 9), from its table"""
    out = []
    p = os.path.join(RAW, "I726-win", "table_726_out.md")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            if ln.startswith("| L 9 |"):
                c = [x.strip() for x in ln.strip().strip("|").split("|")]
                out.append((c[2], c[1], c[3], c[4], c[5], c[6], c[9]))
    return out


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for name in ("ctl", "A", "B"):
        p = os.path.join(HERE, "logs", f"{name}.log")
        if not os.path.exists(p):
            continue
        for label, seg in segments(open(p, encoding="utf-8", errors="replace").read().splitlines()):
            steps, conv, end = parse(seg)
            print(f"\n### {name}, {label}\n")
            print("| Newton step | max abs F before | after | dz before | dz after | lam | Delta moved by | seconds |\n|---|---|---|---|---|---|---|---|")
            for st in steps:
                print(f"| {st['n']} | {st['F0']:.2e} | {st['F1']:.2e} | {st['dz0']:.2e} | {st['dz1']:.2e} | {st['lam']:g} | {st['dD']:+.2e} | {st['t']:.0f} |")
            if conv is not None:
                print(f"| {len(steps)} (the check) | {conv:.2e} | converged | | | | | |")
            print(f"\nending: {end}")
    q = qd_rows()
    if q:
        print("\n### #726's quad-double attempts from D 112.75 (I726-win/table_726_out.md)\n")
        print("| a | from -> to | the re-seeded prediction's qd max abs F | after the first full step | corrector steps | final qd max abs F | outcome |\n|---|---|---|---|---|---|---|")
        for a, ft, f0, f1, st, fin, oc in q:
            print(f"| {a} | {ft} | {f0} | {f1} | {st} | {fin} | {oc} |")


if __name__ == "__main__":
    main()
