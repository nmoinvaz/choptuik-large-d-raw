#!/usr/bin/env python3
"""#742: the crawling attempts D 117 to 118 at a = 1, per Newton step: the iterate's |dz|, each trial's residual and the trial's own correction |dz_t|, from the two logs.
usage: python crawl_742.py [--selftest]        (venv-t151 python, from this folder; reads logs/L.log (own test, the last, unfinished attempt) and logs/N.log (--od_accept natural))
Own test lines:      `    on K trial lam X: max|F| Y; raw |dz_t| Z vs |dz| W (not <); refused, T s`  (the trial's own Newton correction Z against the iterate's step W).
Natural test lines:  `    on K trial lam X: max|F| Y; simplified correction / |dz| = R (bound B); refused|accepted, T s`  (the simplified correction through the iterate's LU is R x |dz|, which is printed as |dz_t|).
Step lines:          `  on K [full]: |F| A -> B, |dz| C -> D, lam L, dDelta E, piv ..., T s` (the first value of |dz| is the iterate's step before the step).
--selftest: planted lines of both kinds must parse to their values, and a planted line with a changed number must not read as the planted value."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = re.compile(r"^\s+on (\d+)(?: \[full\])?: \|F\| ([0-9.e+-]+) -> ([0-9.e+-]+), \|dz\| ([0-9.e+-]+) -> ([0-9.e+-]+), lam ([0-9.]+), dDelta ([+-][0-9.e+-]+)")
OWN = re.compile(r"^\s+on (\d+) trial lam ([0-9.]+): max\|F\| ([0-9.e+-]+); raw \|dz_t\| ([0-9.e+-]+) vs \|dz\| ([0-9.e+-]+) \(not <\); refused")
NAT = re.compile(r"^\s+on (\d+) trial lam ([0-9.]+): max\|F\| ([0-9.e+-]+); simplified correction / \|dz\| = ([0-9.e+-]+) \(bound ([0-9.]+)\); (refused|accepted)")


def parse(lines):
    """{step: dict(F0, F1, dz0, dz1, lam, trials=[(lam, Ftrial, dz_t, outcome)])}; dz0 is the iterate's |dz|, dz_t the trial's own correction"""
    steps, trials = {}, {}
    for ln in lines:
        m = OWN.match(ln)
        if m:
            trials.setdefault(int(m.group(1)), []).append((float(m.group(2)), float(m.group(3)), float(m.group(4)), "refused"))
            continue
        m = NAT.match(ln)
        if m:
            k = int(m.group(1))
            trials.setdefault(k, []).append((float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(6), float(m.group(5))))
            continue
        m = STEP.match(ln)
        if m:
            steps[int(m.group(1))] = dict(F0=float(m.group(2)), F1=float(m.group(3)), dz0=float(m.group(4)), dz1=float(m.group(5)), lam=float(m.group(6)), dD=float(m.group(7)))
    for k, s in steps.items():
        s["trials"] = trials.get(k, [])
    for k, t in trials.items():
        if k not in steps:
            steps[k] = dict(F0=None, F1=None, dz0=None, dz1=None, lam=None, dD=None, trials=t)     # a step still running
    return steps


def selftest():
    own = ["    on 1 trial lam 1: max|F| 1.39e-28; raw |dz_t| 2.977e-15 vs |dz| 1.683e-15 (not <); refused, 112.8 s",
           "  on 1: |F| 1.39e-15 -> 6.94e-16, |dz| 1.68e-15 -> 8.42e-16, lam 0.5, dDelta +1.37e-23, piv 1.2e-15..5.0e+15, 239.61 s"]
    nat = ["    on 1 trial lam 1: max|F| 2.18e-19; simplified correction / |dz| = 9.612e-01 (bound 0.750); refused, 27.4 s",
           "    on 1 trial lam 0.5: max|F| 9.55e-20; simplified correction / |dz| = 5.018e-01 (bound 0.875); accepted, 29.8 s",
           "  on 1: |F| 8.47e-20 -> 9.55e-20, |dz| 2.45e-09 -> 2.47e-09, lam 0.5, dDelta -6.88e-16, piv 2.2e-18..5.0e+15, 143.69 s"]
    a, b = parse(own)[1], parse(nat)[1]
    ok1 = a["F0"] == 1.39e-15 and a["dz0"] == 1.68e-15 and a["trials"][0][:3] == (1.0, 1.39e-28, 2.977e-15) and a["lam"] == 0.5
    ok2 = b["dz0"] == 2.45e-9 and b["trials"][0][3] == "refused" and b["trials"][1][3] == "accepted" and abs(b["trials"][1][2] - 0.5018) < 1e-12 and b["trials"][1][4] == 0.875
    mut = parse([own[0].replace("2.977e-15", "2.978e-15")])[1]["trials"][0][2]
    ok3 = mut != 2.977e-15
    print(f"  planted own-test lines parse to their values: {'ok' if ok1 else 'WRONG'}")
    print(f"  planted natural-test lines parse to their values: {'ok' if ok2 else 'WRONG'}")
    print(f"  a changed number is not read as the planted one: {'ok' if ok3 else 'WRONG'}")
    bad = 3 - (ok1 + ok2 + ok3)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def last_attempt(lines):
    """the lines after the last re-seed line of an attempt (the crawling attempt is the last, unfinished one)"""
    idx = [i for i, ln in enumerate(lines) if re.match(r"^    a [0-9.]+: re-seeded", ln)]
    return lines[idx[-1]:] if idx else lines


def show(title, steps, natural):
    print(f"\n### {title}\n")
    if natural:
        print("| Newton step | max abs F before | the iterate's abs dz | trials: lam, trial max abs F, simplified correction (ratio x abs dz), outcome | accepted lam | max abs F after |\n|---|---|---|---|---|---|")
    else:
        print("| Newton step | max abs F before | the iterate's abs dz | trials: lam, trial max abs F, the trial's own correction abs dz_t, outcome | accepted lam | max abs F after |\n|---|---|---|---|---|---|")
    for k in sorted(steps):
        s = steps[k]
        tr = []
        for t in s["trials"]:
            if natural:
                dz = (t[2] * s["dz0"]) if s["dz0"] else float("nan")
                tr.append(f"{t[0]:g}: {t[1]:.2e}, {dz:.3e} ({t[2]:.4f} x {s['dz0']:.2e}), {t[3]}")
            else:
                tr.append(f"{t[0]:g}: {t[1]:.2e}, {t[2]:.3e} (abs dz {s['dz0']:.2e}), refused" if s["dz0"] else f"{t[0]:g}: {t[1]:.2e}, {t[2]:.3e}, refused")
        f0 = "" if s["F0"] is None else f"{s['F0']:.2e}"
        dz0 = "" if s["dz0"] is None else f"{s['dz0']:.2e}"
        lam = "" if s["lam"] is None else f"{s['lam']:g}"
        f1 = "(running)" if s["F1"] is None else f"{s['F1']:.2e}"
        print(f"| {k} | {f0} | {dz0} | {'<br>'.join(tr) if tr else '(none, lam 1 accepted at once)'} | {lam} | {f1} |")


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for name, natural, title in (("L", False, "own test (`--od_accept own`, the default), a = 1 from D 117, stopped at Newton step 9"),
                                 ("N", True, "`--od_accept natural`, a = 1 from D 117, stopped after four crawling steps")):
        p = os.path.join(HERE, "logs", f"{name}.log")
        steps = parse(last_attempt(open(p, encoding="utf-8", errors="replace").read().splitlines()))
        show(title, steps, natural)


if __name__ == "__main__":
    main()
