#!/usr/bin/env python3
"""#721: 48 rough starts on #701's start-b pair at D 40.02. The control (the first 12 bounds of each run against #701's), the statistics of the 48 bounds of
each run, R_b = median(K 7) / median(K 0) with its bootstrap interval and the verdict by #701's rule, and the 12-start value recomputed from the first 12.

usage: python table_721.py [--selftest]      (venv-t177 python, from this folder; reads logs/K7b_D40_rough.log, logs/K0b_D40_rough.log and #701's logs)
Rules (README.md of this folder, fixed before the run): control = |a - b| / b <= 1e-3 against #701's printed bound for each of the first 12 starts; bound of a
run = the median of its bounds (the geometric mean of the two middle ones for an even count), R_b = median(K 7) / median(K 0); bootstrap: 10000 resamples of
each run's bounds with replacement, random.Random(701), the 2.5th and 97.5th percentiles of R_b (#701's table_701.verdict, which is imported, not copied);
P2 HOLDS if the point and the interval lie inside [1/3, 3], FAILS if the point is outside and the interval entirely outside, UNDECIDED otherwise. The error
bars are bootstrap spreads over the random starts, not enclosures. Quartiles of n bounds are the geometric means of the order statistics n/4 and n/4 + 1
(Q1) and 3n/4 and 3n/4 + 1 (Q3).
--selftest: planted samples of 48 with a known ratio that must come out HOLDS, FAILS and UNDECIDED, the HOLDS sample with its K = 7 bounds times 10 (the
mutation, must come out FAILS), and a control with one reference bound changed by 1% (must be flagged)."""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402
import table_701 as t701  # noqa: E402

I701 = r"D:\choptuik-large-d-raw-push\I701-win"
TOL = 1e-3
RA = 0.98
NCTRL = 12


def gm(a, b):
    return math.exp(0.5 * (math.log(a) + math.log(b)))


def quart_n(v, which):
    s = sorted(v)
    n = len(s)
    k = n // 4 if which == 1 else 3 * n // 4
    return gm(s[k - 1], s[k])


def inside(x):
    return 1 / 3.0 <= x <= 3.0


def control(run, ref):
    """rows (i, run bound, ref bound, relative difference, ok) for the first 12 starts present in both."""
    rows = []
    for i in range(NCTRL):
        if i in run and i in ref:
            d = abs(run[i] - ref[i]) / ref[i]
            rows.append((i, run[i], ref[i], d, d <= TOL))
    return rows


def selftest():
    rng = random.Random(7)

    def sample(med, sigma, n=48):
        return [med * math.exp(rng.gauss(0, sigma)) for _ in range(n)]
    k0 = sample(1e-34, 0.3)
    k7 = sample(1.2e-34, 0.3)
    cases = [("R about 1.2, narrow starts", k7, k0, "HOLDS"),
             ("R about 8, narrow starts", sample(8e-34, 0.15), sample(1e-34, 0.15), "FAILS"),
             ("R about 3.2, wide starts", sample(3.2e-34, 1.0), sample(1e-34, 1.0), "UNDECIDED"),
             ("mutation: the HOLDS sample's K = 7 bounds times 10", [10 * x for x in k7], k0, "FAILS")]
    bad = 0
    for name, a, b, want in cases:
        pt, ci, v = t701.verdict(a, b, nboot=2000)
        print(f"  planted '{name}': R_b {pt:.2f}, interval {ci[0]:.2f} to {ci[1]:.2f} -> {v} (expected {want}) {'ok' if v == want else 'WRONG'}")
        bad += v != want
    ref = {i: 1e-33 * (1 + 0.1 * i) for i in range(NCTRL)}
    same = control(dict(ref), ref)
    okc = len(same) == NCTRL and all(r[4] for r in same)
    mut = dict(ref)
    mut[5] *= 1.01
    missc = [r[0] for r in control(mut, ref) if not r[4]] == [5]
    print(f"  control: identical -> {'all ok' if okc else 'WRONG'}; start 5 changed by 1% -> flagged {'ok' if missc else 'WRONG'}")
    bad += (not okc) + (not missc)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def starts_of(path):
    r = t.parse(open(path, encoding="utf-8", errors="replace").read()) if os.path.exists(path) else None
    return r


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    runs, ref, B = {}, {}, {}
    for k in ("K7", "K0"):
        runs[k] = starts_of(os.path.join(HERE, "logs", f"{k}b_D40_rough.log"))
        r701 = starts_of(os.path.join(I701, "logs", f"{k}b_D40_rough.log"))
        ref[k] = {i: s["bound"] for i, s in r701["starts"].items()}
    print("### Control, the first 12 bounds against #701's (relative difference, rule 1e-3)\n")
    print("| K | starts compared | max relative difference | misses |\n|---|---|---|---|")
    allok = True
    for k in ("K7", "K0"):
        r = runs[k]
        rows = control({i: s["bound"] for i, s in r["starts"].items()}, ref[k]) if r else []
        mx = max((x[3] for x in rows), default=float("nan"))
        miss = [x[0] for x in rows if not x[4]]
        allok &= len(rows) == NCTRL and not miss
        print(f"| {k} | {len(rows)} of {NCTRL} | {mx:.1e} | {miss if miss else 'none'} |")
    print(f"\ncontrol: {'PASSES' if allok else 'MISSES or incomplete'}\n")
    print("| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual |\n|---|---|---|---|---|---|---|---|---|---|")
    for k in ("K7", "K0"):
        r = runs[k]
        if not r or not r["starts"]:
            print(f"| {k} | 0 | not yet | | | | | | | |")
            continue
        v = [s["bound"] for _, s in sorted(r["starts"].items())]
        B[k] = v
        cap = sum(1 for s in r["starts"].values() if s["prods"] >= 250)
        res = max(s["res"] for s in r["starts"].values())
        print(f"| {k} | {len(v)} | {min(v):.2e} | {quart_n(v, 1):.2e} | **{t701.median(v):.3e}** | {quart_n(v, 3):.2e} | {max(v):.2e} | {max(v) / min(v):.1f} | {cap} of {len(v)} | {res:.1e} |")
    for k in ("K7", "K0"):
        if k in B:
            print(f"  {k} bounds, sorted: " + ", ".join(f"{x:.2e}" for x in sorted(B[k])))
    if "K7" in B and "K0" in B:
        n7, n0 = len(B["K7"]), len(B["K0"])
        print(f"\n### Verdict ({n7} and {n0} starts, bootstrap 10000 resamples of each run, seed 701)\n")
        print("| quantity | value | 95% bootstrap interval | against [1/3, 3] |\n|---|---|---|---|")
        pt, ci, v = t701.verdict(B["K7"], B["K0"])
        print(f"| R_b = median(K 7) / median(K 0) | {pt:.2f} | {ci[0]:.2f} to {ci[1]:.2f} | **{v}** |")
        pa, ca, va = t701.verdict(B["K7"], B["K0"], scale=RA)
        print(f"| R_b / R_a (R_a = {RA}) | {pa:.2f} | {ca[0]:.2f} to {ca[1]:.2f} | {va} |")
        print(f"| best ratio (context) | {min(B['K7']) / min(B['K0']):.2f} | | |")
        if n7 >= NCTRL and n0 >= NCTRL:
            p12, c12, v12 = t701.verdict(B["K7"][:NCTRL], B["K0"][:NCTRL])
            print(f"| R_b from the first {NCTRL} of each (#701: 5.90, 2.13 to 14.67) | {p12:.2f} | {c12[0]:.2f} to {c12[1]:.2f} | {v12} |")
        if va != v:
            print("\nthe two readings of P2 (R_b and R_b / R_a) disagree")


if __name__ == "__main__":
    main()
