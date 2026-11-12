#!/usr/bin/env python3
"""The replica spread of the lambda_phys circle against the cut (criteria P1 to P8 of predictions_cut.json, fixed before the run).
usage: python analyze_cut.py               reads cut_588.jsonl and ../replicas_588.jsonl (the kf 22 and 25 values of the same circle); prints the table and the verdicts; exit 1 if a criterion fails
       python analyze_cut.py --selftest    synthetic replicas with a planted growth of the spread with the cut: the spreads are recovered within 15 percent, the per-step ratio table gives the
                                           planted ratio, bit-equal controls pass, a control moved by one ulp fails, an unresolved replica is not counted
       python analyze_cut.py --mutate=control   the real data with one control moved by an ulp: P4 must fail (exit 1)
Definitions as in ../analyze_588.py: s = sqrt(sum |z_r - zmean|^2 / (N - 1)) over the shifted replicas (tags 1..10) that resolve with winding +1, complex position, a sample std with relative
uncertainty about 24 percent for N 10, not a bound. Own estimate = the control a's zeros_est. Controls: tags a and b (rep 0, no move) must give the same zero bit for bit."""
import json, math, os, random, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(os.path.dirname(HERE), "replicas_588.jsonl")
NEW_KFS = [21, 23, 24, 26, 28, 29]
ALL_KFS = [21, 22, 23, 24, 25, 26, 28, 29]


def spread(zs):
    m = sum(zs) / len(zs)
    return m, math.sqrt(sum(abs(z - m) ** 2 for z in zs) / (len(zs) - 1))


def good_reps(R):
    return [r for r in R if r["tag"].isdigit() and r["resolved"] and round(r["winding"]) == 1 and r["zero"]]


def analyze(recs, old, mutate_control=False):
    """one row per new cut from the cut records, plus the kf 22 and 25 rows of the same circle from #588's replica records"""
    rows = {}
    for kf in NEW_KFS:
        R = [r for r in recs if r["kf"] == kf]
        a = [r for r in R if r["tag"] == "a"]
        b = [r for r in R if r["tag"] == "b"]
        za = tuple(a[0]["zero"]) if a and a[0]["zero"] else None
        zb = tuple(b[0]["zero"]) if b and b[0]["zero"] else None
        if mutate_control and kf == NEW_KFS[0] and za:
            za = (za[0] + math.ulp(za[0]), za[1])
        good = good_reps(R)
        zs = [complex(*r["zero"]) for r in good]
        m, s = spread(zs) if len(zs) >= 3 else (None, None)
        rows[kf] = dict(kf=kf, n=len(zs), n_all=len([r for r in R if r["tag"].isdigit()]), complete=len([r for r in R if r["tag"].isdigit()]) == 10 and za is not None and zb is not None,
                        ctl_ok=za is not None and za == zb, zero=complex(*za) if za else None, est=a[0]["est"] if a and a[0].get("est") is not None else None, mean=m, s=s,
                        dev=abs(complex(*za) - m) if (za and m is not None) else None, rep_est=st.median([r["est"] for r in good]) if good else None, known=False)
    for kf, pre in ((22, "k22_z_re2.0446"), (25, "k25_z_re2.0446")):
        R = [r for r in old if r["circle"].startswith(pre)]
        zs = [complex(*r["zero"]) for r in R if r["rep"] > 0 and r["resolved"] and round(r["winding"]) == 1 and r["zero"]]
        m, s = spread(zs)
        rows[kf] = dict(kf=kf, n=len(zs), n_all=10, complete=True, ctl_ok=None, zero=None, est=None, mean=m, s=s, dev=None, rep_est=st.median([r["est"] for r in R if r["rep"] > 0 and r["zero"]]), known=True)
    return rows


def ratios(rows):
    """s_hi / s_lo per kf step between neighbouring cuts of ALL_KFS"""
    out = []
    for lo, hi in zip(ALL_KFS, ALL_KFS[1:]):
        a, b = rows[lo]["s"], rows[hi]["s"]
        out.append((lo, hi, (b / a) ** (1.0 / (hi - lo)) if a and b else None))
    return out


def verdicts(rows, pred):
    v = {}
    pk = {int(k): x for k, x in pred["predicted_s"].items()}
    f = pred["band_factor"]
    inside = [kf for kf in NEW_KFS if rows[kf]["s"] and pk[kf] / f <= rows[kf]["s"] <= pk[kf] * f]
    v["P1"] = len(inside) >= 5
    ss = [rows[kf]["s"] for kf in ALL_KFS]
    v["P2"] = all(x is not None for x in ss) and all(a < b for a, b in zip(ss, ss[1:]))
    rr = ratios(rows)
    v["P3"] = sum(1 for _, _, r in rr if r is not None and 1.5 <= r <= 8) >= 6
    v["P4"] = all(rows[kf]["ctl_ok"] for kf in NEW_KFS)
    v["P5"] = all(rows[kf]["n"] >= 9 for kf in NEW_KFS) and sum(rows[kf]["n"] for kf in NEW_KFS) >= 58
    v["P6"] = all(rows[kf]["s"] is not None and rows[kf]["s"] < 1e-4 for kf in NEW_KFS)
    v["P7"] = sum(1 for kf in NEW_KFS if rows[kf]["s"] and rows[kf]["rep_est"] and 0.5 <= rows[kf]["rep_est"] / rows[kf]["s"] <= 2) >= 5
    v["P8"] = sum(1 for kf in NEW_KFS if rows[kf]["dev"] is not None and rows[kf]["s"] and rows[kf]["dev"] <= 3 * rows[kf]["s"]) >= 5
    return v, inside, rr


def table(rows, pred):
    pk = {int(k): x for k, x in pred["predicted_s"].items()}
    print("| kf | replicas used | s | predicted | s / predicted | s per kf step from the previous cut | controls a = b | control zero | own estimate (control) | replicas' own estimate, median | that / s | control from the replica mean | flag (s > 3 x estimate) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    rr = {hi: r for lo, hi, r in ratios(rows)}
    for kf in ALL_KFS:
        r = rows[kf]
        if r["s"] is None:
            print(f"| {kf} | {r['n']} of {r['n_all']} | n/a | | | | {'yes' if r['ctl_ok'] else 'NO'} | | | | | | |")
            continue
        src = " (#588)" if r["known"] else ""
        pr = f"{pk[kf]:.2e}" if kf in pk else "(measured)"
        rat = f"{r['s'] / pk[kf]:.2f}" if kf in pk else ""
        step = f"{rr[kf]:.2f}" if rr.get(kf) else ""
        z = f"{r['zero'].real:.7f}{r['zero'].imag:+.7f}i" if r["zero"] else ""
        est = f"{r['est']:.1e}" if r["est"] else ""
        flag = ("**FLAG**" if r["est"] and r["s"] > 3 * r["est"] else "no") if not r["known"] else ""
        dev = f"{r['dev']:.2e}" if r["dev"] is not None else ""
        print(f"| {kf}{src} | {r['n']} of {r['n_all']} | {r['s']:.2e} | {pr} | {rat} | {step} | {'yes' if r['ctl_ok'] else ('NO' if r['ctl_ok'] is False else '')} | {z} | {est} | "
              f"{r['rep_est']:.1e} | {r['rep_est'] / r['s']:.2f} | {dev} | {flag} |")


if __name__ == "__main__":
    pred = json.load(open(os.path.join(HERE, "predictions_cut.json")))
    old = [json.loads(l) for l in open(OLD)]
    if "--selftest" in sys.argv:
        rng = random.Random(9)
        truth = {kf: 1e-8 * 3.0 ** (kf - 21) for kf in NEW_KFS}   # a planted spread growing 3x a kf step, in the complex plane (rms)
        recs = []
        for kf in NEW_KFS:
            z0 = complex(2.0435, 0.0)
            for t in ("a", "b"):
                recs.append(dict(circle=f"k{kf}_phys", kf=kf, rep=0, tag=t, winding=1.0, resolved=True, zero=[z0.real, z0.imag], est=truth[kf]))
            for r in range(1, 11):
                z = z0 + complex(rng.gauss(0, truth[kf] / math.sqrt(2)), rng.gauss(0, truth[kf] / math.sqrt(2)))
                recs.append(dict(circle=f"k{kf}_phys", kf=kf, rep=r, tag=str(r), winding=1.0, resolved=True, zero=[z.real, z.imag], est=truth[kf]))
        rows = analyze(recs, old)
        pooled = math.sqrt(st.mean((rows[kf]["s"] / truth[kf]) ** 2 for kf in NEW_KFS))
        ok = abs(pooled - 1) < 0.15
        print(f"planted spreads 1e-8 x 3^(kf-21), pooled s / planted {pooled:.2f}:", "ok" if ok else "FAIL")
        g = math.exp(st.mean(math.log(r) for lo, hi, r in ratios(rows) if (lo, hi) in ((23, 24), (28, 29)) and r))
        good = 2.0 < g < 4.5
        print(f"per-step ratio between planted neighbours 23-24 and 28-29, geometric mean {g:.2f} (planted 3, 15 percent per spread plus the sampling of 10 replicas):", "ok" if good else "FAIL")
        ok &= good
        good = all(rows[kf]["ctl_ok"] for kf in NEW_KFS)
        print("bit-equal controls:", "pass" if good else "FAIL (must pass)")
        ok &= good
        rows_m = analyze(recs, old, mutate_control=True)
        good = not rows_m[NEW_KFS[0]]["ctl_ok"]
        print("control moved by one ulp:", "fails" if good else "STILL PASSES (must fail)")
        ok &= good
        recs2 = [dict(r) for r in recs]
        for r in recs2:
            if r["kf"] == 24 and r["tag"] == "3":
                r["resolved"] = False
        rows2 = analyze(recs2, old)
        good = rows2[24]["n"] == 9 and rows[24]["n"] == 10
        print("an unresolved replica is not counted:", "ok" if good else "FAIL")
        ok &= good
        sys.exit(0 if ok else 1)
    recs = [json.loads(l) for l in open(os.path.join(HERE, "cut_588.jsonl"))]
    rows = analyze(recs, old, mutate_control="--mutate=control" in sys.argv)
    table(rows, pred)
    undone = [kf for kf in NEW_KFS if not rows[kf]["complete"]]
    if undone:
        print(f"\nincomplete cuts {undone}: no verdicts yet")
        sys.exit(2)
    v, inside, rr = verdicts(rows, pred)
    print("\nratio per kf step between neighbouring cuts:", ", ".join(f"{lo}-{hi}: {r:.2f}" for lo, hi, r in rr))
    cross = [kf for kf in ALL_KFS if rows[kf]["s"] and rows[kf]["s"] > 1e-4]
    print("first cut with s above 1e-4:", cross[0] if cross else "none up to kf 29")
    print(f"P1 inside the factor-3 band at {len(inside)} of 6 cuts: {inside}")
    for k, ok in v.items():
        print(f"{k}: {'holds' if ok else 'FAILS'}")
    sys.exit(0 if all(v.values()) else 1)
