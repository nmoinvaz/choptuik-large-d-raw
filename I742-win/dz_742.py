#!/usr/bin/env python3
"""#742: per attempt of the chain, the iterate's |dz| at the start (the first Newton step's step before it is taken), the re-seeded prediction's |F|, the first full step's |F|, and the series' state (a_max, order ratio 5, |z_N|).
usage: python dz_742.py [--selftest]        (venv-t151 python, from this folder; reads logs/P.log, L.log, N.log, M.log as far as they exist)
The `step K: D X, ... |z_N| Z, ratios 2-5 A B C E, a_max V, T s` line precedes the attempt; the attempt's Newton steps follow (`  on K [full]: |F| A -> B, |dz| C -> D, lam L, ...`) and the line `    a X -> D Y: ...` ends it.
--selftest: planted lines must parse to their values and a changed digit must not read as the planted one."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPLINE = re.compile(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.([0-9.e+-]+), \|z_1\| ([0-9.e+-]+), \|z_N\| ([0-9.e+-]+), ratios 2-5 ([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+), a_max ([0-9.]+)")
NEWTON = re.compile(r"^\s+on (\d+)(?: \[full\])?: \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9.]+)")
END = re.compile(r"^    a ([0-9.]+) -> D ([0-9.]+):")
RESEED = re.compile(r"^    a ([0-9.]+): re-seeded")


def attempts(lines, run):
    out, info, cur, a = [], None, None, None
    for ln in lines:
        m = STEPLINE.match(ln)
        if m:
            info = dict(D=float(m.group(2)), zN=float(m.group(6)), r5=float(m.group(10)), amax=float(m.group(11)))
            continue
        m = RESEED.match(ln)
        if m:
            cur, a = [], float(m.group(1))
            continue
        if cur is not None:
            m = NEWTON.match(ln)
            if m and int(m.group(1)) == 0:
                cur.append(dict(F0=float(m.group(2)), F1=float(m.group(3)), dz0=float(m.group(4)), lam=float(m.group(6))))
            m = END.match(ln)
            if m:
                out.append(dict(run=run, info=info, a=a, to=float(m.group(2)), done=True, **(cur[0] if cur else {})))
                cur = None
    if cur is not None and info is not None:
        out.append(dict(run=run, info=info, a=a, to=None, done=False, **(cur[0] if cur else {})))
    return out


def selftest():
    good = ["step 3: D 117.0, pivots 3.0e-20..3.6e+15, |z_1| 1.15e-03, |z_N| 2.87e-27, ratios 2-5 141.8 42.7 3.6 3.3, a_max 2.615, 148 s",
            "    a 1.0000: re-seeded (ok), 23.23 s",
            "  on 0: |F| 1.49e-29 -> 1.39e-15, |dz| 1.95e-07 -> 1.68e-15, lam 1, dDelta -6.93e-14, piv 2.9e-15..5.0e+15, 141.07 s",
            "    a 1.000 -> D 118.0: predicted |F| 1.0e-14"]
    r = attempts(good, "T")[0]
    ok1 = r["info"]["D"] == 117.0 and r["info"]["amax"] == 2.615 and r["info"]["r5"] == 3.3 and r["dz0"] == 1.95e-7 and r["F0"] == 1.49e-29 and r["F1"] == 1.39e-15 and r["a"] == 1.0 and r["to"] == 118.0
    bad = [x.replace("1.95e-07", "1.96e-07") for x in good]
    ok2 = attempts(bad, "T")[0]["dz0"] != 1.95e-7
    print(f"  planted lines parse to their values: {'ok' if ok1 else 'WRONG'}")
    print(f"  a changed digit is not read as the planted value: {'ok' if ok2 else 'WRONG'}")
    print("selftest", "FAILED" if not (ok1 and ok2) else "passed")
    return 0 if (ok1 and ok2) else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("| run | from D | a | to D | iterate abs dz at the start | re-seeded prediction max abs F | after the first full step | lam of the first step | a_max | order ratio 5 | z_N |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for run in ("P", "L", "N", "M"):
        p = os.path.join(HERE, "logs", f"{run}.log")
        if not os.path.exists(p):
            continue
        for r in attempts(open(p, encoding="utf-8", errors="replace").read().splitlines(), run):
            if r.get("info") is None or "dz0" not in r:
                continue
            i = r["info"]
            to = "(unfinished)" if r["to"] is None else f"{r['to']:g}"
            print(f"| {run} | {i['D']:g} | {r['a']:g} | {to} | {r['dz0']:.2e} | {r['F0']:.2e} | {r['F1']:.2e} | {r['lam']:g} | {i['amax']:.3f} | {i['r5']:.1f} | {i['zN']:.2e} |")


if __name__ == "__main__":
    main()
