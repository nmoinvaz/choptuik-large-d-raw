#!/usr/bin/env python3
"""#701: start b at D 40.02. The two solves' records (Delta_RT, Delta_RT - Delta_hp, DD = Delta(K 7) - Delta(K 0), whether each solve counts), the 12 rough bounds of each state, R_b = median(K 7) / median(K 0)
with its bootstrap interval, R_b / R_a, and the verdicts of the rules fixed in README.md.
usage: python table_701.py [--selftest]          (venv-t151 python, from this folder; reads solves/k7b_D40.jsonl, solves/k0b_D40_mutnorows.jsonl, logs/K7b_D40_rough.log, logs/K0b_D40_rough.log)
Bound of a run = the median of its 12 rough bounds (the geometric mean of the 6th and 7th smallest). Bootstrap: 10000 resamples of each run's 12 bounds with replacement, random.Random(701), the 2.5th
and 97.5th percentiles of R_b (the rule of #681's table_681.py). P1 holds if |DD| < 1e-15. P2 (the issue's verdict rule on R_b): HOLDS if the point and the 95% interval lie inside [1/3, 3], FAILS if the point
is outside and the interval entirely outside, UNDECIDED otherwise; the same test on R_b / R_a (R_a = 0.98) is printed beside it. A solve counts if its record says ok with the last Newton max|F| <= 1e-36.
--selftest: planted samples with a known ratio that must come out HOLDS, FAILS and UNDECIDED, and the same HOLDS sample with its K = 7 bounds multiplied by 10 (the mutation), which must come out FAILS."""
import json
import math
import os
import random
import sys

import flint

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402

flint.ctx.prec = 400
WINDOW = 3.0
NBOOT = 10000
RA = 0.98
P1_LIMIT = 1e-15
F_LIMIT = 1e-36


def gmean(a, b):
    return math.exp(0.5 * (math.log(a) + math.log(b)))


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else gmean(s[n // 2 - 1], s[n // 2])


def quart(v, which):
    s = sorted(v)
    if len(s) < 12:
        return None
    return gmean(s[2], s[3]) if which == 1 else gmean(s[8], s[9])


def inside(x):
    return 1 / WINDOW <= x <= WINDOW


def verdict(k7, k0, scale=1.0, seed=701, nboot=NBOOT):
    """k7, k0: lists of 12 bounds. Returns (point R_b, (lo, hi) of its interval, verdict) with R_b divided by `scale` (1 for R_b, R_a for R_b / R_a)."""
    pt = median(k7) / median(k0) / scale
    rng = random.Random(seed)
    s = sorted(median([rng.choice(k7) for _ in k7]) / median([rng.choice(k0) for _ in k0]) / scale for _ in range(nboot))
    lo, hi = s[int(0.025 * nboot)], s[int(0.975 * nboot) - 1]
    if inside(pt) and inside(lo) and inside(hi):
        v = "HOLDS"
    elif (not inside(pt)) and (hi < 1 / WINDOW or lo > WINDOW):
        v = "FAILS"
    else:
        v = "UNDECIDED"
    return pt, (lo, hi), v


def selftest():
    rng = random.Random(7)

    def sample(med, sigma, n=12):
        return [med * math.exp(rng.gauss(0, sigma)) for _ in range(n)]
    cases = []
    k0 = sample(1e-34, 0.3)
    k7 = sample(1.2e-34, 0.3)
    cases.append(("R about 1.2, narrow starts", k7, k0, "HOLDS"))
    cases.append(("R about 8, narrow starts", sample(8e-34, 0.15), sample(1e-34, 0.15), "FAILS"))
    cases.append(("R about 4, starts spread by a factor of ~20", sample(4e-34, 1.2), sample(1e-34, 1.2), "UNDECIDED"))
    cases.append(("mutation: the HOLDS sample's K = 7 bounds times 10", [10 * x for x in k7], k0, "FAILS"))
    bad = 0
    for name, a, b, want in cases:
        pt, ci, v = verdict(a, b, nboot=2000)
        print(f"  planted '{name}': R_b {pt:.2f}, interval {ci[0]:.2f} to {ci[1]:.2f} -> {v} (expected {want}) {'ok' if v == want else 'WRONG'}")
        bad += v != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def record(path):
    """last jsonl record of a solve."""
    if not os.path.exists(path):
        return None
    rows = [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]
    return rows[-1] if rows else None


def cls_of(c):
    fl = c["fields"]
    F = max(f["max"] for f in fl.values())
    E = max(max(f["P"], f["M"]) for f in fl.values()) / F
    C0 = max(f["C"] for f in fl.values()) / F
    C4 = fl["w4"]["C"] / F
    return "edge" if E >= 0.5 and E >= 3 * C0 else ("centre in w4" if C4 >= 0.5 and C4 >= 3 * E else "mixed")


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    recs = {"K7": record(os.path.join(HERE, "solves", "k7b_D40.jsonl")), "K0": record(os.path.join(HERE, "solves", "k0b_D40_mutnorows.jsonl"))}
    print("| solve | D | grid | horizon | mutate | ok | last Newton max abs F | counts (ok and <= 1e-36) | Delta_RT | Delta_RT - Delta_hp | secs |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for k in ("K7", "K0"):
        r = recs[k]
        if not r:
            print(f"| {k} | not yet | | | | | | | | | |")
            continue
        f = r["newton"][-1]
        print(f"| {k} | {r['D']} | {r['grid'][0]}x{r['grid'][1]} | {r.get('horizon')} | {r.get('mutate')} | {r['ok']} | {f:.2e} | {'yes' if r['ok'] and f <= F_LIMIT else 'NO'} | {r['Delta_str']} | {r['diff']:+.4e} | {r['secs']:.0f} |")
    if all(recs.values()):
        dd = flint.arb(recs["K7"]["Delta_str"]) - flint.arb(recs["K0"]["Delta_str"])
        ddf = float(dd.mid())
        print(f"\nDD = Delta(K 7) - Delta(K 0) = {ddf:+.4e}  ->  P1 (|DD| < {P1_LIMIT:g}): {'HOLDS' if abs(ddf) < P1_LIMIT else 'FAILS'}; |DD| {'>=' if abs(ddf) >= 1e-12 else '<'} 1e-12")
    B, runs = {}, {}
    for k in ("K7", "K0"):
        p = os.path.join(HERE, "logs", f"{k}b_D40_rough.log")
        r = t.parse(open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else None
        if r and r["starts"]:
            runs[k] = r
    print("\n| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual | classes (edge / centre in w4 / mixed) |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for k in ("K7", "K0"):
        r = runs.get(k)
        if not r:
            print(f"| {k} | 0 | not yet | | | | | | | | |")
            continue
        v = [s["bound"] for _, s in sorted(r["starts"].items())]
        B[k] = v
        n = len(v)
        q1, q3 = quart(v, 1), quart(v, 3)
        cap = sum(1 for s in r["starts"].values() if s["prods"] >= 250)
        res = max(s["res"] for s in r["starts"].values())
        cc = {"edge": 0, "centre in w4": 0, "mixed": 0}
        for c in r["content"].values():
            cc[cls_of(c)] += 1
        fm = lambda x: "n/a" if x is None else f"{x:.2e}"
        note = "" if n == 12 else f" (only {n})"
        print(f"| {k} | {n}{note} | {min(v):.2e} | {fm(q1)} | **{median(v):.3e}** | {fm(q3)} | {max(v):.2e} | {max(v) / min(v):.1f} | {cap} of {n} | {res:.1e} | {cc['edge']} / {cc['centre in w4']} / {cc['mixed']} |")
    for k in ("K7", "K0"):
        if k in B:
            print(f"  {k} bounds, sorted: " + ", ".join(f"{x:.2e}" for x in sorted(B[k])))
    if len(B.get("K7", [])) == 12 and len(B.get("K0", [])) == 12:
        pt, ci, v = verdict(B["K7"], B["K0"])
        print(f"\nR_b = median(K 7) / median(K 0) = {median(B['K7']):.3e} / {median(B['K0']):.3e} = {pt:.2f}, bootstrap 95% interval {ci[0]:.2f} to {ci[1]:.2f} (10000 resamples, seed 701)")
        print(f"  best-of-12 ratio (context) {min(B['K7']) / min(B['K0']):.2f}")
        print(f"  P2 by the issue's rule (R_b in [1/3, 3]): {v}")
        pa, ca, va = verdict(B["K7"], B["K0"], scale=RA)
        print(f"  R_b / R_a (R_a = {RA}) = {pa:.2f}, interval {ca[0]:.2f} to {ca[1]:.2f}: {va}")
        if va != v:
            print("  the two readings of P2 disagree (README, choice 1)")
        if recs["K7"] and recs["K0"]:
            p1 = abs(ddf) < P1_LIMIT
            print(f"  P1 {'holds' if p1 else 'fails'}, P2 (rule on R_b) {v.lower()}; the counts of the solves: K 7 {'yes' if recs['K7']['ok'] and recs['K7']['newton'][-1] <= F_LIMIT else 'NO'}, K 0 {'yes' if recs['K0']['ok'] and recs['K0']['newton'][-1] <= F_LIMIT else 'NO'}")
    else:
        print("\nverdict not formed: fewer than 12 starts in some run")


if __name__ == "__main__":
    main()
