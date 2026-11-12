#!/usr/bin/env python3
"""Spread of det M under single-ulp moves of the argument at the five points of #585 (criteria P1 to P5 of predictions_585.json, fixed before the run).
usage: python analyze_585.py              reads evals_585.jsonl, prints the table and the verdicts, writes sigma_585.json (pooled near and far std); exit 1 if a criterion fails
       python analyze_585.py --selftest   synthetic evaluations: noise of a known sigma is recovered within 15 percent, a smooth function reports below 1e-12, the
                                          repeats check passes on bit-equal repeats and fails with one repeat shifted by an ulp
       python analyze_585.py --mutate=repeat   the real data with one repeat shifted by an ulp: P4 must fail (exit 1)
Definitions: values = reference + 25 Re moves + 25 Im moves (51); std with ddof 1 of ln|det| and of wrap(arg - arg_ref); deviation = value - reference; derivative =
|d ln det / d lam| from the points at Re -+ 1e-3 ((delta ln|det|, wrapped delta arg) / 2e-3); smooth change over 25 ulps = derivative * 25 * ulp(Re)."""
import json, math, os, random, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TWO_PI = 2 * math.pi


def wrap(x):
    return math.remainder(x, TWO_PI)


def analyze(recs, points):
    out = {}
    for p in points:
        R = [r for r in recs if r["id"] == p["id"]]
        ref = [r for r in R if r["kind"] == "ref"][0]
        moves = [r for r in R if r["kind"] in ("re", "im")]
        reps = [r for r in R if r["kind"] == "rep"]
        dre = sorted([r for r in R if r["kind"] == "dre"], key=lambda r: r["j"])
        vl = [ref["lnabs"]] + [m["lnabs"] for m in moves]
        va = [0.0] + [wrap(m["arg"] - ref["arg"]) for m in moves]
        dl = [m["lnabs"] - ref["lnabs"] for m in moves]
        da = [wrap(m["arg"] - ref["arg"]) for m in moves]
        lo = [abs(m["lnabs"] - ref["lnabs"]) for m in moves if m["j"] <= 5]
        hi = [abs(m["lnabs"] - ref["lnabs"]) for m in moves if m["j"] >= 21]
        deriv = math.hypot(dre[1]["lnabs"] - dre[0]["lnabs"], wrap(dre[1]["arg"] - dre[0]["arg"])) / 2e-3
        smooth = deriv * 25 * math.ulp(ref["re"])
        spread = math.hypot(st.stdev(vl), st.stdev(va))
        same = all(r["lnabs"] == ref["lnabs"] and r["arg"] == ref["arg"] for r in reps)
        out[p["id"]] = dict(kind=p["kind"], n_values=len(vl), std_ln=st.stdev(vl), std_arg=st.stdev(va), max_ln=max(map(abs, dl)), max_arg=max(map(abs, da)),
                            med_lo=st.median(lo), med_hi=st.median(hi), deriv=deriv, smooth=smooth, ratio=spread / smooth if smooth > 0 else math.inf,
                            reps=len(reps), reps_identical=same, workers=len({r["worker"] for r in reps}), distinct_ln=len(set(vl)))
    return out


def verdicts(a):
    v = {}
    v["P1"] = all(1e-5 <= x["std_ln"] <= 1e-2 and 1e-5 <= x["std_arg"] <= 1e-2 for x in a.values())
    v["P2"] = all(1 / 3 <= (x["med_lo"] / x["med_hi"] if x["med_hi"] > 0 else math.inf) <= 3 for x in a.values())
    near = st.median([x["std_ln"] for x in a.values() if x["kind"] == "near"])
    far = st.median([x["std_ln"] for x in a.values() if x["kind"] == "far"])
    v["P3"] = 1 <= near / far <= 10
    v["P4"] = all(x["reps_identical"] and x["reps"] == 50 for x in a.values())
    v["P5"] = all(x["ratio"] > 1e6 for x in a.values())
    return v, near / far


def pooled(a, kind, key):
    return math.sqrt(st.mean(x[key] ** 2 for x in a.values() if x["kind"] == kind))


def synth(points, sigma, seed=1, slope=50.0, mutate_repeat=False):
    rng = random.Random(seed)
    recs = []
    for p in points:
        x, y = p["re"], p["im"]
        base = (3.0, 1.0)
        mk = lambda kind, j, re_, im, la, ar: recs.append(dict(id=p["id"], kind=kind, j=j, re=re_, im=im, lnabs=la, arg=ar, worker=0))
        mk("ref", 0, x, y, base[0], base[1])
        xr = x
        for j in range(1, 26):
            xr = math.nextafter(xr, math.inf)
            mk("re", j, xr, y, base[0] + slope * (xr - x) + rng.gauss(0, sigma), base[1] + rng.gauss(0, sigma))
        yr = y
        for j in range(1, 26):
            yr = math.nextafter(yr, math.inf)
            mk("im", j, x, yr, base[0] + rng.gauss(0, sigma), base[1] + slope * (yr - y) + rng.gauss(0, sigma))
        for r in range(50):
            mk("rep", r, x, y, base[0], base[1])
        mk("dre", -1, x - 1e-3, y, base[0] - slope * 1e-3, base[1])
        mk("dre", 1, x + 1e-3, y, base[0] + slope * 1e-3, base[1])
    if mutate_repeat:
        r = [r for r in recs if r["kind"] == "rep"][7]
        r["lnabs"] += 1e-12
    return recs


if __name__ == "__main__":
    points = json.load(open(os.path.join(HERE, "points_585.json")))
    if "--selftest" in sys.argv:
        ok = True
        a = analyze(synth(points, 3e-4), points)
        got = pooled(a, "near", "std_ln"), pooled(a, "far", "std_ln"), pooled(a, "near", "std_arg"), pooled(a, "far", "std_arg")
        good = all(abs(g / 3e-4 - 1) < 0.15 for g in got)
        print("known sigma 3e-4, recovered pooled std (near ln, far ln, near arg, far arg):", " ".join(f"{g:.2e}" for g in got), "ok" if good else "FAIL")
        ok &= good
        a0 = analyze(synth(points, 0.0), points)
        z = max(max(x["std_ln"], x["std_arg"]) for x in a0.values())
        good = z < 1e-12
        print(f"smooth function (sigma 0, slope 50): largest std {z:.2e} (must be below 1e-12)", "ok" if good else "FAIL")
        ok &= good
        v, _ = verdicts(analyze(synth(points, 3e-4), points))
        good = v["P4"]
        print("bit-equal repeats: P4", "holds" if good else "FAIL", "(must hold)")
        ok &= good
        v, _ = verdicts(analyze(synth(points, 3e-4, mutate_repeat=True), points))
        good = not v["P4"]
        print("one repeat shifted by 1e-12: P4", "fails" if good else "STILL HOLDS", "(must fail)")
        ok &= good
        sys.exit(0 if ok else 1)
    recs = [json.loads(l) for l in open(os.path.join(HERE, "evals_585.jsonl"))]
    if "--mutate=repeat" in sys.argv:
        r = [r for r in recs if r["kind"] == "rep" and r["id"] == "N1"][7]
        r["lnabs"] = math.nextafter(r["lnabs"], math.inf)
    a = analyze(recs, points)
    print("| point | kind | values | std ln\\|det\\| | std arg | max \\|dev\\| ln | max \\|dev\\| arg | median \\|dev\\| j<=5 | j>=21 | \\|dlnf/dlam\\| | smooth change over 25 ulp | spread / smooth | distinct ln values | 50 repeats bit equal | workers |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, x in a.items():
        print(f"| {k} | {x['kind']} | {x['n_values']} | {x['std_ln']:.2e} | {x['std_arg']:.2e} | {x['max_ln']:.2e} | {x['max_arg']:.2e} | {x['med_lo']:.2e} | {x['med_hi']:.2e} | {x['deriv']:.3g} | {x['smooth']:.2e} | {x['ratio']:.2e} | {x['distinct_ln']} | {'yes' if x['reps_identical'] else 'NO'} ({x['reps']}) | {x['workers']} |")
    v, nf = verdicts(a)
    print(f"\nnear/far median std ln ratio {nf:.2f}")
    for k, ok in v.items():
        print(f"{k}: {'holds' if ok else 'FAILS'}")
    sig = dict(near_ln=pooled(a, "near", "std_ln"), near_arg=pooled(a, "near", "std_arg"), far_ln=pooled(a, "far", "std_ln"), far_arg=pooled(a, "far", "std_arg"),
               note="pooled (root mean square) of the per-point std over the two near points N1, N2 and over the three far points F1 to F3")
    if "--mutate=repeat" not in sys.argv:
        json.dump(sig, open(os.path.join(HERE, "sigma_585.json"), "w"), indent=1)
    print("pooled sigma:", {k: f"{x:.3e}" for k, x in sig.items() if k != "note"})
    sys.exit(0 if all(v.values()) else 1)
