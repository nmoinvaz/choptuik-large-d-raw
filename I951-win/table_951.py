#!/usr/bin/env python3
"""#951 (win): start c at D 40.02. The two solves' records (Delta, max|F|, whether each counts), the distances of c's roots to a's and b's, the 48 rough bounds of each run, R_c with its bootstrap
interval, and the verdict by the rule fixed in README.md before the solves. From I943-win/table_943.py and I701-win/table_701.py.

usage: python table_951.py [--selftest] [--raw DIR]      (venv-t151 python, from this folder; reads solves/k7c_D40.jsonl, solves/k0c_D40_mutnorows.jsonl, their npz, logs/K7c_D40_rough.log, logs/K0c_D40_rough.log)
DIR is a checkout of github.com/nmoinvaz/choptuik-large-d-raw (default the push worktree below) holding I671-win/, I701-win/, I721-win/, I721-win2/ and I943-win/.

Rules (README.md of this folder, fixed before the solves):
 - a solve counts if its record says ok with the last Newton max|F| <= 1e-36. A root RE-FINDS a's or b's if the max-norm of (zh + zl) differences to it is <= 1e-30 (the double-double resolution of a stored state).
 - bound of a run = the median of its bounds (geometric mean of the two middle ones for an even count); R = median(K 7) / median(K 0); the 95% interval is the 2.5th and 97.5th percentile of 10000
   bootstrap resamples of each run's bounds with replacement, random.Random(701) (table_701.verdict, imported). R_a and R_b are recomputed from their logs and must equal 0.98 (0.60 to 1.43) and
   6.06 (4.56 to 9.26), else flagged.
 - verdict: CLASSES if the point R_c lies inside R_a's interval or inside R_b's, SPREAD if outside both (the unrounded endpoints, inclusive). Context, not the rule: R_c's own interval, R_c / R_a and
   R_c / R_b with the joint bootstrap of table_943.ratio_ab against 1.
 The error bars are bootstrap spreads over the random starts, not enclosures.
--selftest: planted samples with R about 1, about 6, between, above and below the two intervals (CLASSES a, CLASSES b, SPREAD x3), the R about 1 sample with its K 7 bounds times 3 (the mutation, must flip
to SPREAD), the interval endpoints themselves, and planted roots at distances 1e-31 (re-found), 1e-29 (distinct) and identical (re-found, the mutation of the distinct case)."""
import json
import math
import os
import random
import sys

import flint
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402
import table_701 as t701  # noqa: E402
import table_943 as t943  # noqa: E402

flint.ctx.prec = 400
RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw-754"
NSTARTS = 48
F_LIMIT = 1e-36
REFOUND = 1e-30
RA_943 = (0.98, 0.60, 1.43)
RB_721 = (6.06, 4.56, 9.26)


def judge(rc, ia, ib):
    """The rule: the point rc against the intervals (lo, hi) of R_a and R_b."""
    if ia[0] <= rc <= ia[1]:
        return "CLASSES (inside R_a's interval)"
    if ib[0] <= rc <= ib[1]:
        return "CLASSES (inside R_b's interval)"
    return "SPREAD (outside both)"


def distance(zc, zr):
    """(max-norm, 2-norm) of the difference of two double-double states (zh, zl)."""
    dz = (zc[0] - zr[0]) + (zc[1] - zr[1])
    return float(np.abs(dz).max()), float(np.linalg.norm(dz))


def refound(d):
    return d <= REFOUND


def verdict_c(c7, c0, a7, a0, b7, b0, nboot=t701.NBOOT):
    """R_c with its interval, R_a and R_b with theirs, the verdict word and the two context ratios."""
    pa, ca, _ = t701.verdict(a7, a0, nboot=nboot)
    pb, cb, _ = t701.verdict(b7, b0, nboot=nboot)
    pc, cc, _ = t701.verdict(c7, c0, nboot=nboot)
    word = judge(pc, ca, cb)
    ra = t943.ratio_ab(c7, c0, a7, a0, nboot=nboot)
    rb = t943.ratio_ab(c7, c0, b7, b0, nboot=nboot)
    return dict(pa=pa, ca=ca, pb=pb, cb=cb, pc=pc, cc=cc, word=word, ra=ra, rb=rb)


def selftest():
    rng = random.Random(7)

    def sample(med, sigma, n=NSTARTS):
        return [med * math.exp(rng.gauss(0, sigma)) for _ in range(n)]
    a7, a0, b7, b0 = sample(1e-34, 0.3), sample(1e-34, 0.3), sample(6e-34, 0.3), sample(1e-34, 0.3)
    cases = [("R about 1", sample(1.0e-34, 0.3), sample(1e-34, 0.3), "CLASSES (inside R_a's interval)"),
             ("R about 6", sample(6.0e-34, 0.3), sample(1e-34, 0.3), "CLASSES (inside R_b's interval)"),
             ("R about 2.8, between", sample(2.8e-34, 0.1), sample(1e-34, 0.1), "SPREAD (outside both)"),
             ("R about 20, above", sample(2.0e-33, 0.3), sample(1e-34, 0.3), "SPREAD (outside both)"),
             ("R about 0.2, below", sample(2.0e-35, 0.3), sample(1e-34, 0.3), "SPREAD (outside both)")]
    bad = 0
    for name, c7, c0, want in cases:
        r = verdict_c(c7, c0, a7, a0, b7, b0, nboot=1000)
        print(f"  planted '{name}': R_c {r['pc']:.2f} against R_a {r['ca'][0]:.2f} to {r['ca'][1]:.2f}, R_b {r['cb'][0]:.2f} to {r['cb'][1]:.2f} -> {r['word']} (expected {want}) {'ok' if r['word'] == want else 'WRONG'}")
        bad += r["word"] != want
    c7, c0 = cases[0][1], cases[0][2]
    r = verdict_c([3 * x for x in c7], c0, a7, a0, b7, b0, nboot=1000)
    ok = r["word"].startswith("SPREAD")
    print(f"  mutation: the R about 1 sample with its K 7 bounds times 3: R_c {r['pc']:.2f} -> {r['word']} (must be SPREAD) {'ok' if ok else 'WRONG'}")
    bad += not ok
    ia, ib = (0.60, 1.43), (4.56, 9.26)
    edge = [(0.60, True), (1.43, True), (4.56, True), (9.26, True), (0.5999, False), (1.4301, False), (9.2601, False)]
    okd = all(judge(x, ia, ib).startswith("CLASSES") == inside for x, inside in edge)
    print(f"  endpoints inclusive, just outside excluded: {'ok' if okd else 'WRONG'}")
    bad += not okd
    zr = (np.linspace(-0.13, 0.13, 50), np.zeros(50))
    for name, eps, want in (("1e-31 away", 1e-31, True), ("1e-29 away", 1e-29, False), ("identical (the mutation of the distinct case)", 0.0, True)):
        zc = (zr[0].copy(), zr[1].copy())
        zc[1][17] += eps
        d = distance(zc, zr)
        ok = refound(d[0]) == want and abs(d[0] - eps) <= 1e-3 * eps + 1e-300
        print(f"  planted root {name}: max-norm {d[0]:.1e}, re-found {refound(d[0])} (expected {want}) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def starts_of(path):
    return t.parse(open(path, encoding="utf-8", errors="replace").read()) if os.path.exists(path) else None


def bounds(path):
    r = starts_of(path)
    return [s["bound"] for _, s in sorted(r["starts"].items())] if r else []


def load(path):
    z = np.load(path)
    return z["zh"], z["zl"]


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    raw = sys.argv[sys.argv.index("--raw") + 1] if "--raw" in sys.argv else RAW
    sol = os.path.join(HERE, "solves")
    recs = {"K7": t701.record(os.path.join(sol, "k7c_D40.jsonl")), "K0": t701.record(os.path.join(sol, "k0c_D40_mutnorows.jsonl"))}
    print("### Part 1, the solves of start c\n")
    print("| solve | D | grid | horizon | mutate | ok | last Newton max abs F | counts (ok and <= 1e-36) | Delta_RT | Delta_RT - Delta_hp | secs |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for k in ("K7", "K0"):
        r = recs[k]
        if not r:
            print(f"| {k} | not yet | | | | | | | | | |")
            continue
        f = r["newton"][-1]
        print(f"| {k} | {r['D']} | {r['grid'][0]}x{r['grid'][1]} | {r.get('horizon')} | {r.get('mutate')} | {r['ok']} | {f:.2e} | {'yes' if r['ok'] and f <= F_LIMIT else 'NO'} | {r['Delta_str']} | {r['diff']:+.4e} | {r['secs']:.0f} |")
    paths = {"a": ("I671-win", "k7_D40", "k0_D40_mutnorows"), "b": ("I701-win", "k7b_D40", "k0b_D40_mutnorows")}
    npz = {("c", "K7"): os.path.join(sol, "k7c_D40_D40.0201_32x121.npz"), ("c", "K0"): os.path.join(sol, "k0c_D40_mutnorows_D40.0201_32x121.npz")}
    drec = {("c", "K7"): recs["K7"], ("c", "K0"): recs["K0"]}
    for s, (d, n7, n0) in paths.items():
        npz[(s, "K7")] = os.path.join(raw, d, "solves", f"{n7}_D40.0201_32x121.npz")
        npz[(s, "K0")] = os.path.join(raw, d, "solves", f"{n0}_D40.0201_32x121.npz")
        drec[(s, "K7")] = t701.record(os.path.join(raw, d, "solves", f"{n7}.jsonl"))
        drec[(s, "K0")] = t701.record(os.path.join(raw, d, "solves", f"{n0}.jsonl"))
    Z = {k: load(p) for k, p in npz.items() if os.path.exists(p)}
    if all(k in Z for k in (("c", "K7"), ("c", "K0"))):
        print("\n### Distances (double-double states, 32x121, D 40.020065), re-found if the max-norm is <= 1e-30\n")
        print("| roots | max-norm | 2-norm | re-found | Delta difference |\n|---|---|---|---|---|")
        rows = [("K 7 c - a", ("c", "K7"), ("a", "K7")), ("K 7 c - b", ("c", "K7"), ("b", "K7")), ("K 7 a - b (reference)", ("a", "K7"), ("b", "K7")),
                ("K 0 c - a", ("c", "K0"), ("a", "K0")), ("K 0 c - b", ("c", "K0"), ("b", "K0")), ("K 0 a - b (reference)", ("a", "K0"), ("b", "K0")),
                ("c: K 7 - K 0", ("c", "K7"), ("c", "K0")), ("a: K 7 - K 0 (reference)", ("a", "K7"), ("a", "K0")), ("b: K 7 - K 0 (reference)", ("b", "K7"), ("b", "K0"))]
        for name, x, y in rows:
            if x in Z and y in Z:
                mx, l2 = distance(Z[x], Z[y])
                dd = "n/a"
                if drec.get(x) and drec.get(y):
                    dd = f"{float((flint.arb(drec[x]['Delta_str']) - flint.arb(drec[y]['Delta_str'])).mid()):+.4e}"
                print(f"| {name} | {mx:.3e} | {l2:.3e} | {'YES' if refound(mx) else 'no'} | {dd} |")
    print("\n### Part 2, the rough bounds\n")
    runs = {k: starts_of(os.path.join(HERE, "logs", f"{k}c_D40_rough.log")) for k in ("K7", "K0")}
    print("| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual max abs J x - v | header max abs F |\n|---|---|---|---|---|---|---|---|---|---|---|")
    B = {}
    for k in ("K7", "K0"):
        r = runs[k]
        if not r or not r["starts"]:
            print(f"| {k} | 0 | not yet | | | | | | | | |")
            continue
        v = [s["bound"] for _, s in sorted(r["starts"].items())]
        B[k] = v
        cap = sum(1 for s in r["starts"].values() if s["prods"] >= 250)
        res = max(s["res"] for s in r["starts"].values())
        hd = r["head"]["F"] if r["head"] else float("nan")
        print(f"| {k} | {len(v)} | {min(v):.2e} | {t943.quart_n(v, 1):.2e} | **{t701.median(v):.3e}** | {t943.quart_n(v, 3):.2e} | {max(v):.2e} | {max(v) / min(v):.1f} | {cap} of {len(v)} | {res:.1e} | {hd:.2e} |")
    for k in ("K7", "K0"):
        if k in B:
            print(f"  {k} bounds, sorted: " + ", ".join(f"{x:.2e}" for x in sorted(B[k])))
    a7, a0 = bounds(os.path.join(raw, "I943-win", "logs", "K7_D40_rough.log")), bounds(os.path.join(raw, "I943-win", "logs", "K0_D40_rough.log"))
    b7, b0 = bounds(os.path.join(raw, "I721-win", "logs", "K7b_D40_rough.log")), bounds(os.path.join(raw, "I721-win2", "logs", "K0b_D40_rough.log"))
    print(f"\n### Reference: R_a ({len(a7)} and {len(a0)} bounds, #943) and R_b ({len(b7)} and {len(b0)}, #721 with win2's K 0), recomputed from their logs\n")
    pa, ca, _ = t701.verdict(a7, a0)
    pb, cb, _ = t701.verdict(b7, b0)
    oka = len(a7) == NSTARTS == len(a0) and (round(pa, 2), round(ca[0], 2), round(ca[1], 2)) == RA_943
    okb = len(b7) == NSTARTS == len(b0) and (round(pb, 2), round(cb[0], 2), round(cb[1], 2)) == RB_721
    print(f"R_a(48) = {pa:.2f}, {ca[0]:.2f} to {ca[1]:.2f}: {'equal to #943' if oka else 'DIFFERS, FLAG'}; R_b(48) = {pb:.2f}, {cb[0]:.2f} to {cb[1]:.2f}: {'equal to #721' if okb else 'DIFFERS, FLAG'}\n")
    if "K7" in B and "K0" in B:
        n7, n0 = len(B["K7"]), len(B["K0"])
        r = verdict_c(B["K7"], B["K0"], a7, a0, b7, b0)
        print(f"### Verdict ({n7} and {n0} starts, bootstrap {t701.NBOOT} resamples, seed 701)\n")
        print("| quantity | value | 95% bootstrap interval | against |\n|---|---|---|---|")
        print(f"| R_c = median(K 7) / median(K 0) = {t701.median(B['K7']):.3e} / {t701.median(B['K0']):.3e} | **{r['pc']:.2f}** | {r['cc'][0]:.2f} to {r['cc'][1]:.2f} | R_a {r['ca'][0]:.2f} to {r['ca'][1]:.2f}, R_b {r['cb'][0]:.2f} to {r['cb'][1]:.2f}: **{r['word']}** |")
        print(f"| R_c / R_a (context) | {r['ra'][0]:.3f} | {r['ra'][1][0]:.3f} to {r['ra'][1][1]:.3f} | 1: {r['ra'][2]} |")
        print(f"| R_c / R_b (context) | {r['rb'][0]:.3f} | {r['rb'][1][0]:.3f} to {r['rb'][1][1]:.3f} | 1: {r['rb'][2]} |")
        print(f"| best ratio (context) | {min(B['K7']) / min(B['K0']):.2f} | | |")
        if n7 >= 12 and n0 >= 12:
            p12, c12, _ = t701.verdict(B["K7"][:12], B["K0"][:12])
            print(f"| R_c from the first 12 of each (context) | {p12:.2f} | {c12[0]:.2f} to {c12[1]:.2f} | |")
        if n7 != NSTARTS or n0 != NSTARTS:
            print(f"\nnot the criterion: the verdict is for {NSTARTS} starts of each run, and these have {n7} and {n0}")


if __name__ == "__main__":
    main()
