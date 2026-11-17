#!/usr/bin/env python3
"""#721 (win): 48 rough starts on #701's start-b K = 7 state at D 40.02, set against win2's 48 rough starts on the K = 0 state. From I721-win2/table_721.py
with the K = 7 log of this folder and the K = 0 log of win2 read in place.

usage: python table_721.py [--selftest] [--raw DIR]      (venv-t151 python, from this folder; reads logs/K7b_D40_rough.log, #701's logs and win2's)
DIR is a checkout of github.com/nmoinvaz/choptuik-large-d-raw (default the push worktree below) holding I701-win/ and I721-win2/ (K = 0 log at 59e5c975).

Rules (README.md of this folder, fixed before the run):
 - acceptance 1: each of the first 12 bounds of the K = 7 run is within |a - b| / b <= 1e-3 of #701's printed bound (logs/K7b_D40_rough.log of I701-win).
   Also printed, as the control that lets the two machines be mixed: win2's first 12 K = 0 bounds against #701's K = 0 log, same rule, and (context, not a
   criterion) win2's 29 K = 7 starts from its run that stopped, against this run's starts 0-28 (same rule).
 - acceptance 2: bound of a run = the median of its bounds (the geometric mean of the two middle ones for an even count), R_b = median(K 7) / median(K 0)
   over all 48 starts of each; bootstrap 10000 resamples of each run's bounds with replacement, random.Random(701), the 2.5th and 97.5th percentiles of
   R_b (#701's table_701.verdict, imported, not copied); P2 HOLDS if the point and the interval lie inside [1/3, 3], FAILS if the point is outside and the
   interval entirely outside, UNDECIDED otherwise. The error bars are bootstrap spreads over the random starts, not enclosures. Quartiles of n bounds are
   the geometric means of the order statistics n/4 and n/4 + 1 (Q1) and 3n/4 and 3n/4 + 1 (Q3).
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

RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw-754"
TOL = 1e-3
RA = 0.98
NCTRL = 12
NSTARTS = 48


def gm(a, b):
    return math.exp(0.5 * (math.log(a) + math.log(b)))


def quart_n(v, which):
    s = sorted(v)
    n = len(s)
    k = n // 4 if which == 1 else 3 * n // 4
    return gm(s[k - 1], s[k])


def control(run, ref, n=NCTRL):
    """rows (i, run bound, ref bound, relative difference, ok) for the starts below n present in both."""
    rows = []
    for i in range(n):
        if i in run and i in ref:
            d = abs(run[i] - ref[i]) / ref[i]
            rows.append((i, run[i], ref[i], d, d <= TOL))
    return rows


def selftest():
    rng = random.Random(7)

    def sample(med, sigma, n=NSTARTS):
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
    return t.parse(open(path, encoding="utf-8", errors="replace").read()) if os.path.exists(path) else None


def bmap(r):
    return {i: s["bound"] for i, s in r["starts"].items()} if r else {}


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    raw = sys.argv[sys.argv.index("--raw") + 1] if "--raw" in sys.argv else RAW
    i701 = os.path.join(raw, "I701-win", "logs")
    w2 = os.path.join(raw, "I721-win2", "logs")
    runs = {"K7": starts_of(os.path.join(HERE, "logs", "K7b_D40_rough.log")), "K0": starts_of(os.path.join(w2, "K0b_D40_rough.log"))}
    ref = {k: bmap(starts_of(os.path.join(i701, f"{k}b_D40_rough.log"))) for k in ("K7", "K0")}
    w2k7 = bmap(starts_of(os.path.join(w2, "K7b_D40_rough.log")))
    print("### Control (acceptance 1), the first 12 bounds against #701's (relative difference, rule 1e-3)\n")
    print("| run | starts compared | max relative difference | misses |\n|---|---|---|---|")
    allok = True
    for name, k in (("K 7, this run (win)", "K7"), ("K 0, win2's run (the control for mixing the machines)", "K0")):
        rows = control(bmap(runs[k]), ref[k])
        mx = max((x[3] for x in rows), default=float("nan"))
        miss = [x[0] for x in rows if not x[4]]
        allok &= len(rows) == NCTRL and not miss
        print(f"| {name} | {len(rows)} of {NCTRL} | {mx:.1e} | {miss if miss else 'none'} |")
    print(f"\ncontrol: {'PASSES' if allok else 'MISSES or incomplete'}\n")
    rows = control(bmap(runs["K7"]), w2k7, n=NSTARTS)
    if rows:
        mx = max(x[3] for x in rows)
        print(f"Context, not a criterion: win2's K 7 run that stopped has {len(w2k7)} starts, {len(rows)} of them also in this run, largest relative difference {mx:.1e}, "
              f"misses {[x[0] for x in rows if not x[4]] or 'none'} (rule 1e-3).\n")
    print("| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual |\n|---|---|---|---|---|---|---|---|---|---|")
    B = {}
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
        if n7 != NSTARTS or n0 != NSTARTS:
            print(f"\nnot the criterion: the verdict is for {NSTARTS} starts of each run, and these have {n7} and {n0}")
        if va != v:
            print("\nthe two readings of P2 (R_b and R_b / R_a) disagree")


if __name__ == "__main__":
    main()
