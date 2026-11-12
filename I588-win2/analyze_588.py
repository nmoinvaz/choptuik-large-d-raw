#!/usr/bin/env python3
"""Spread of the zero positions of the twelve R 0.06 circles under ulp replicas (#588; criteria Q1 to Q6 of predictions_588.json, fixed before the run).
usage: python analyze_588.py               reads replicas_588.jsonl; prints the table (per zero: the replica spread beside the circle's own estimate, the flag) and the verdicts; exit 1 if a criterion fails
       python analyze_588.py --selftest    synthetic replicas of known scatter: the spread is recovered within 15 percent, a bit-equal control passes, a control moved by one ulp fails
       python analyze_588.py --mutate=control   the real data with the control of the first circle moved by one ulp: the control check (Q4) must fail (exit 1)
Definitions. Replicas 1..10 of a circle count if resolved with winding +1 and a zero. Spread s = sqrt(sum |z_r - zmean|^2 / (N - 1)) over the counted replicas (complex plane, the std of the position, not of
one component); it is a sample std over about 10 ulp replicas (relative uncertainty about 1/sqrt(2 (N - 1)), 24 percent), not a bound. Own estimate = the stored circle's zeros_est (its n0/2 against n0
power sums). Flag: s > 3 x own estimate. Control: replica 0 (no move, freshly evaluated) has the stored zero exactly."""
import json, math, os, random, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def spread(zs):
    m = sum(zs) / len(zs)
    return m, math.sqrt(sum(abs(z - m) ** 2 for z in zs) / (len(zs) - 1))


def analyze(circles, recs, mutate_control=False):
    rows = []
    for k, c in enumerate(circles):
        R = [r for r in recs if r["circle"] == c["name"]]
        ctl = [r for r in R if r["rep"] == 0]
        zc = tuple(ctl[0]["zero"]) if ctl and ctl[0]["zero"] else None
        if mutate_control and k == 0 and zc:
            zc = (zc[0] + math.ulp(zc[0]), zc[1])
        ctl_ok = zc == tuple(c["zero"])
        good = [r for r in R if r["rep"] > 0 and r["resolved"] and round(r["winding"]) == 1 and r["zero"]]
        zs = [complex(*r["zero"]) for r in good]
        if len(zs) >= 3:
            m, s = spread(zs)
        else:
            m, s = None, None
        z0 = complex(*c["zero"])
        rows.append(dict(name=c["name"], kf=c["kf"], zero=z0, est=c["est"], n=len(zs), n_all=len([r for r in R if r["rep"] > 0]), ctl_ok=ctl_ok, mean=m, s=s,
                         dev=abs(z0 - m) if m is not None else None, maxdev=max(abs(z - z0) for z in zs) if zs else None, ratio=s / c["est"] if s else None,
                         flag=bool(s is not None and s > 3 * c["est"]), rep_est=st.median([r["est"] for r in good]) if good else None))
    return rows


def verdicts(rows, pred):
    v = {}
    lo, hi = pred["bounds"]["all"]
    v["Q1"] = all(r["s"] is not None and lo <= r["s"] <= hi for r in rows)
    a, b = [r for r in rows if r["name"] == "k27_z_re1.9028_im+0.9160"][0], [r for r in rows if r["name"] == "k27_z_re2.3966_im+0.5477"][0]
    v["Q2"] = bool(a["s"] and b["s"] and pred["bounds"]["A"][0] <= a["s"] <= pred["bounds"]["A"][1] and pred["bounds"]["B"][0] <= b["s"] <= pred["bounds"]["B"][1])
    nflag = sum(r["flag"] for r in rows)
    v["Q3"] = pred["flagged"][0] <= nflag <= pred["flagged"][1]
    k22 = [r["ratio"] for r in rows if r["kf"] == 22 and r["ratio"]]
    v["Q4"] = len(k22) == 4 and st.median(k22) > 100
    v["Q5"] = all(r["ctl_ok"] for r in rows)
    v["Q6"] = sum(r["n"] for r in rows) >= 118 and all(r["n"] >= 9 for r in rows)
    v["Q7"] = sum(1 for r in rows if r["dev"] is not None and r["dev"] <= 3 * r["s"]) >= 11
    return v, nflag


if __name__ == "__main__":
    import replicas_588 as RP
    circles = RP.circles()
    pred = json.load(open(os.path.join(HERE, "predictions_588.json")))
    if "--selftest" in sys.argv:
        rng = random.Random(5)
        recs = []
        for c in circles:
            recs.append(dict(circle=c["name"], rep=0, winding=1.0, resolved=True, zero=list(c["zero"]), est=c["est"]))
            for r in range(1, 11):
                z = complex(*c["zero"]) + complex(rng.gauss(0, 2e-5 / math.sqrt(2)), rng.gauss(0, 2e-5 / math.sqrt(2)))
                recs.append(dict(circle=c["name"], rep=r, winding=1.0, resolved=True, zero=[z.real, z.imag], est=c["est"]))
        rows = analyze(circles, recs)
        pooled = math.sqrt(st.mean(r["s"] ** 2 for r in rows))
        ok = abs(pooled / 2e-5 - 1) < 0.15
        print(f"known scatter 2e-5 (complex rms), pooled recovered {pooled:.2e}:", "ok" if ok else "FAIL")
        good = all(r["ctl_ok"] for r in rows)
        print("bit-equal controls:", "pass" if good else "FAIL (must pass)")
        ok &= good
        rows_m = analyze(circles, recs, mutate_control=True)
        good = not rows_m[0]["ctl_ok"]
        print("control moved by one ulp:", "fails" if good else "STILL PASSES (must fail)")
        ok &= good
        sys.exit(0 if ok else 1)
    recs = [json.loads(l) for l in open(os.path.join(HERE, "replicas_588.jsonl"))]
    rows = analyze(circles, recs, mutate_control="--mutate=control" in sys.argv)
    print("| circle | kf | stored zero | own estimate | replicas used | replica spread s | s / estimate | flag (s > 3 x est) | replicas' own estimate (median) | stored zero from the replica mean | control bit equal |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r["s"] is None:
            print(f"| {r['name']} | {r['kf']} | | {r['est']:.1e} | {r['n']} of {r['n_all']} | n/a | | | | | {'yes' if r['ctl_ok'] else 'NO'} |")
            continue
        print(f"| {r['name']} | {r['kf']} | {r['zero'].real:.6f}{r['zero'].imag:+.6f}i | {r['est']:.1e} | {r['n']} of {r['n_all']} | {r['s']:.2e} | {r['ratio']:.1f} | {'**FLAG**' if r['flag'] else 'no'} | {r['rep_est']:.1e} | {r['dev']:.2e} | {'yes' if r['ctl_ok'] else 'NO'} |")
    v, nflag = verdicts(rows, pred)
    print(f"\nflagged {nflag} of {len(rows)}")
    for k, ok in v.items():
        print(f"{k}: {'holds' if ok else 'FAILS'}")
    sys.exit(0 if all(v.values()) else 1)
