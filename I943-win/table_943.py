#!/usr/bin/env python3
"""#943 (win): 48 rough starts on start a's K = 7 and K = 0 states at D 40.02, set against #681's logs (the control) and #721's start-b runs (R_b). From I721-win/table_721.py.

usage: python table_943.py [--selftest] [--raw DIR]      (venv-t151 python, from this folder; reads logs/K7_D40_rough.log and logs/K0_D40_rough.log)
DIR is a checkout of github.com/nmoinvaz/choptuik-large-d-raw (default the push worktree below) holding I681-win/, I721-win/ and I721-win2/.

Rules (README.md of this folder, fixed before the runs):
 - acceptance 1: each of the first 12 bounds of each run is within |a - b| / b <= 1e-3 of #681's printed bound (I681-win/logs/K7_D40_rough.log, K0_D40_rough.log).
 - acceptance 2: bound of a run = the median of its bounds (geometric mean of the two middle ones for an even count), R_a = median(K 7) / median(K 0) over the starts of each;
   bootstrap 10000 resamples of each run's bounds with replacement, random.Random(701), the 2.5th and 97.5th percentiles of R_a (#701's table_701.verdict, imported, not
   copied); HOLDS if the point and the interval lie inside [1/3, 3], FAILS if the point is outside and the interval entirely outside, UNDECIDED otherwise.
 - acceptance 3: R_a / R_b with R_b = median(K 7 b) / median(K 0 b) from #721's logs (I721-win/logs/K7b_D40_rough.log, I721-win2/logs/K0b_D40_rough.log). One joint bootstrap,
   10000 resamples, random.Random(701), each resample drawing with replacement, in this order, a's K 7, a's K 0, b's K 7, b's K 0 (n draws each, n = that run's number of
   bounds), the ratio (median a7 / median a0) / (median b7 / median b0), the 2.5th and 97.5th percentiles. EXCLUDES 1 if both ends lie on one side of 1 (the start sets R),
   CONTAINS 1 otherwise (this sample cannot tell). R_b is recomputed from the logs and must equal #721's (6.06, 4.56 to 9.26), else it is flagged.
 The error bars are bootstrap spreads over the random starts, not enclosures. Quartiles of n bounds are the geometric means of the order statistics n/4 and n/4 + 1 (Q1) and
 3n/4 and 3n/4 + 1 (Q3).
--selftest: planted samples of 48 with a known ratio that must come out HOLDS, FAILS and UNDECIDED, the HOLDS sample with its K = 7 bounds times 10 (the mutation, must come
out FAILS); R_a / R_b planted at 1 (must CONTAIN 1) and at 1/6 (must EXCLUDE 1) with the mutation (a's K 7 times 6 on the first, must EXCLUDE 1); the control with one reference
bound changed by 1% (must be flagged); and the four-run bootstrap's own reduction (a = b gives a ratio of exactly 1 at the point)."""
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
NCTRL = 12
NSTARTS = 48
NBOOT = 10000
RB_721 = (6.06, 4.56, 9.26)


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


def ratio_ab(a7, a0, b7, b0, nboot=NBOOT, seed=701):
    """(point, (lo, hi), word) of (median a7 / median a0) / (median b7 / median b0) by the joint bootstrap described above."""
    pt = (t701.median(a7) / t701.median(a0)) / (t701.median(b7) / t701.median(b0))
    rng = random.Random(seed)
    s = []
    for _ in range(nboot):
        m7a = t701.median([rng.choice(a7) for _ in a7])
        m0a = t701.median([rng.choice(a0) for _ in a0])
        m7b = t701.median([rng.choice(b7) for _ in b7])
        m0b = t701.median([rng.choice(b0) for _ in b0])
        s.append((m7a / m0a) / (m7b / m0b))
    s.sort()
    lo, hi = s[int(0.025 * nboot)], s[int(0.975 * nboot) - 1]
    word = "EXCLUDES 1" if (lo > 1 or hi < 1) else "CONTAINS 1"
    return pt, (lo, hi), word


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
        print(f"  planted '{name}': R_a {pt:.2f}, interval {ci[0]:.2f} to {ci[1]:.2f} -> {v} (expected {want}) {'ok' if v == want else 'WRONG'}")
        bad += v != want
    b7, b0 = sample(6e-34, 0.3), sample(1e-34, 0.3)
    a7, a0 = sample(6e-34, 0.3), sample(1e-34, 0.3)
    same = ratio_ab(a7, a0, b7, b0, nboot=2000)
    low = ratio_ab(sample(1e-34, 0.3), sample(1e-34, 0.3), b7, b0, nboot=2000)
    mut2 = ratio_ab([6 * x for x in a7], a0, b7, b0, nboot=2000)
    for name, r, want in (("R_a = R_b about 6", same, "CONTAINS 1"), ("R_a about 1, R_b about 6", low, "EXCLUDES 1"),
                          ("mutation: R_a = R_b with a's K 7 times 6", mut2, "EXCLUDES 1")):
        print(f"  planted '{name}': R_a / R_b {r[0]:.2f}, interval {r[1][0]:.2f} to {r[1][1]:.2f} -> {r[2]} (expected {want}) {'ok' if r[2] == want else 'WRONG'}")
        bad += r[2] != want
    ident = ratio_ab(b7, b0, b7, b0, nboot=200)
    print(f"  four-run bootstrap with a = b: point {ident[0]:.12f} (must be 1 to 1e-12) {'ok' if abs(ident[0] - 1) < 1e-12 else 'WRONG'}")
    bad += abs(ident[0] - 1) >= 1e-12
    ref = {i: 1e-33 * (1 + 0.1 * i) for i in range(NCTRL)}
    same_c = control(dict(ref), ref)
    okc = len(same_c) == NCTRL and all(r[4] for r in same_c)
    m = dict(ref)
    m[5] *= 1.01
    missc = [r[0] for r in control(m, ref) if not r[4]] == [5]
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
    i681 = os.path.join(raw, "I681-win", "logs")
    runs = {"K7": starts_of(os.path.join(HERE, "logs", "K7_D40_rough.log")), "K0": starts_of(os.path.join(HERE, "logs", "K0_D40_rough.log"))}
    ref = {k: bmap(starts_of(os.path.join(i681, f"{k}_D40_rough.log"))) for k in ("K7", "K0")}
    print("### Control (acceptance 1), the first 12 bounds against #681's (relative difference, rule 1e-3)\n")
    print("| run | starts compared | max relative difference | misses |\n|---|---|---|---|")
    allok = True
    for name, k in (("K 7", "K7"), ("K 0", "K0")):
        rows = control(bmap(runs[k]), ref[k])
        mx = max((x[3] for x in rows), default=float("nan"))
        miss = [x[0] for x in rows if not x[4]]
        allok &= len(rows) == NCTRL and not miss
        print(f"| {name} | {len(rows)} of {NCTRL} | {mx:.1e} | {miss if miss else 'none'} |")
    print(f"\ncontrol: {'PASSES' if allok else 'MISSES or incomplete'}\n")
    print("| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual max abs J x - v |\n|---|---|---|---|---|---|---|---|---|---|")
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
    # start b, #721: K 7 on this laptop, K 0 win2's
    b7 = bmap(starts_of(os.path.join(raw, "I721-win", "logs", "K7b_D40_rough.log")))
    b0 = bmap(starts_of(os.path.join(raw, "I721-win2", "logs", "K0b_D40_rough.log")))
    b7v, b0v = [b7[i] for i in sorted(b7)], [b0[i] for i in sorted(b0)]
    print(f"\n### Start b (#721), recomputed from its logs: {len(b7v)} K 7 and {len(b0v)} K 0 bounds\n")
    pb, cb, vb = t701.verdict(b7v, b0v)
    okb = len(b7v) == NSTARTS and len(b0v) == NSTARTS and round(pb, 2) == RB_721[0] and round(cb[0], 2) == RB_721[1] and round(cb[1], 2) == RB_721[2]
    print(f"R_b(48) = {pb:.2f}, interval {cb[0]:.2f} to {cb[1]:.2f}, {vb}; #721 said {RB_721[0]}, {RB_721[1]} to {RB_721[2]}: {'equal, control ok' if okb else 'DIFFERS, FLAG'}\n")
    if "K7" in B and "K0" in B:
        n7, n0 = len(B["K7"]), len(B["K0"])
        print(f"### Verdict ({n7} and {n0} starts, bootstrap {NBOOT} resamples, seed 701)\n")
        print("| quantity | value | 95% bootstrap interval | against |\n|---|---|---|---|")
        pt, ci, v = t701.verdict(B["K7"], B["K0"])
        print(f"| R_a = median(K 7) / median(K 0) | {pt:.2f} | {ci[0]:.2f} to {ci[1]:.2f} | [1/3, 3]: **{v}** |")
        pr, cr, wr = ratio_ab(B["K7"], B["K0"], b7v, b0v)
        print(f"| R_a / R_b (R_b = {pb:.2f}) | {pr:.3f} | {cr[0]:.3f} to {cr[1]:.3f} | 1: **{wr}** |")
        print(f"| best ratio (context) | {min(B['K7']) / min(B['K0']):.2f} | | |")
        if n7 >= NCTRL and n0 >= NCTRL:
            p12, c12, v12 = t701.verdict(B["K7"][:NCTRL], B["K0"][:NCTRL])
            print(f"| R_a from the first {NCTRL} of each (#681: 0.98) | {p12:.2f} | {c12[0]:.2f} to {c12[1]:.2f} | [1/3, 3]: {v12} |")
        if n7 != NSTARTS or n0 != NSTARTS:
            print(f"\nnot the criterion: the verdict is for {NSTARTS} starts of each run, and these have {n7} and {n0}")


if __name__ == "__main__":
    main()
