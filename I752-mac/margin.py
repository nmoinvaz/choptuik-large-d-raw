#!/usr/bin/env python3
"""#752: the own test's margin at Newton step 1 of every octo-double attempt in #742's logs (P, L, M; the default own
test). Y is the iterate's |dz| after step 0, W the lam 1 trial's own correction at step 1 (the accepted step's new
|dz|, or the refused trial's raw |dz_t|); the own test takes lam 1 at step 1 when W < Y. Log parsing only.
usage: python3 margin.py RAW [--selftest]
--selftest runs the parser on planted lines (an accepted attempt, a refused one, a base polish) and exits 1 when it
reads them wrong."""
import re
import sys

STEP = re.compile(r"^\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+),")
TRIAL = re.compile(r"^\s+on (\d+) trial lam 1: max\|F\| (\S+); raw \|dz_t\| (\S+) vs \|dz\| (\S+)")
ATT = re.compile(r"^\s+a (\S+): re-seeded")
DONE = re.compile(r"^\s+a (\S+) -> D (\S+):")


def attempts(lines):
    out, cur = [], None
    for ln in lines:
        m = ATT.match(ln)
        if m:
            cur = dict(a=m.group(1), steps={}, trials={})
            out.append(cur)
            continue
        if cur is None:
            continue
        m = TRIAL.match(ln)
        if m:
            cur["trials"][int(m.group(1))] = float(m.group(3))
            continue
        m = STEP.match(ln)
        if m:
            cur["steps"][int(m.group(1))] = dict(dz0=float(m.group(4)), dz1=float(m.group(5)), lam=float(m.group(6)))
            continue
        m = DONE.match(ln)
        if m:
            cur["D"] = m.group(2)
            cur = None
    return out


def margin(at):
    s0, s1 = at["steps"].get(0), at["steps"].get(1)
    if s0 is None or (s1 is None and 1 not in at["trials"]):
        return None
    Y = s0["dz1"]
    if 1 in at["trials"]:
        W, how = at["trials"][1], "refused"
    else:
        W, how = s1["dz1"], "accepted" if s1["lam"] == 1 else f"lam {s1['lam']:g}"
    return dict(start=s0["dz0"], lam0=s0["lam"], Y=Y, W=W, ratio=W / Y, how=how)


def selftest():
    acc = ["    a 0.5000: re-seeded (ok), 24.22 s",
           "  on 0: |F| 9.37e-34 -> 3.17e-16, |dz| 9.36e-08 -> 3.85e-16, lam 1, dDelta -3.20e-14, piv 8.6e-16..4.2e+15, 145.2 s",
           "  on 1: |F| 3.17e-16 -> 6.12e-28, |dz| 3.85e-16 -> 2.62e-17, lam 1, dDelta -9.88e-24, piv 2.5e-20..4.2e+15, 155.55 s",
           "    a 0.500 -> D 117.5: predicted |F| 4.77e-14, od 6 steps"]
    ref = ["    a 1.0000: re-seeded (ok), 23.23 s",
           "  on 0: |F| 1.49e-29 -> 1.39e-15, |dz| 1.95e-07 -> 1.68e-15, lam 1, dDelta -6.93e-14, piv 2.9e-15..5.0e+15, 141.07 s",
           "    on 1 trial lam 1: max|F| 1.39e-28; raw |dz_t| 2.977e-15 vs |dz| 1.683e-15 (not <); refused, 112.8 s",
           "  on 1: |F| 1.39e-15 -> 6.94e-16, |dz| 1.68e-15 -> 8.42e-16, lam 0.5, dDelta +1.37e-23, piv 1.2e-15..5.0e+15, 239.61 s"]
    base = ["  on 0: |F| 2.01e-34 -> 5.86e-27, |dz| 4.07e-13 -> 7.16e-23, lam 1, dDelta +1.57e-20, piv 3.0e-20..3.6e+15, 194.37 s"]
    got = [margin(a) for a in attempts(base + acc + ref)]
    want = [(0.06805, "accepted"), (1.772, "refused")]
    ok = len(got) == 2 and all(g is not None and abs(g["ratio"] / w[0] - 1) < 1e-3 and g["how"] == w[1] for g, w in zip(got, want))
    print(f"selftest: {[(round(g['ratio'], 4), g['how']) for g in got if g]} (expected {want}): {'passed' if ok else 'FAILED'}")
    return 0 if ok else 1


if "--selftest" in sys.argv:
    sys.exit(selftest())
raw = sys.argv[1]
print("| run | a | D reached | start \\|dz\\| | lam at step 0 | Y = \\|dz\\| after step 0 | W = own correction at step 1 | W / Y | step 1 |")
print("|---|---|---|---|---|---|---|---|---|")
for run in ("P", "L", "M"):
    lines = open(f"{raw}/I742-win/logs/{run}.log", encoding="utf-8", errors="replace").read().splitlines()
    for at in attempts(lines):
        g = margin(at)
        if g:
            print(f"| {run} | {at['a']} | {at.get('D', '(stopped)')} | {g['start']:.2e} | {g['lam0']:g} | {g['Y']:.2e} | {g['W']:.3e} | "
                  f"{g['ratio']:.3f} | {g['how']} |")
