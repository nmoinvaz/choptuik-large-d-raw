#!/usr/bin/env python3
"""The kf 31 extension of the cut run (criteria Q1 to Q5 of predictions_kf31.json, fixed before the run).
usage: python analyze_kf31.py               reads cut_588.jsonl (kf 29 and kf 31 records) and ../replicas_588.jsonl; prints the table and the verdicts; exit 1 if a criterion fails
       python analyze_kf31.py --selftest    planted spreads (kf 29 at 8.8e-5, kf 31 at 7e-4 and at a wrong 1e-5): Q1 and Q2 hold on the first and FAIL on the second, a bit-equal control passes, one moved by an ulp fails
       python analyze_kf31.py --mutate=control   the real data with the kf 31 control moved by an ulp: Q3 must fail (exit 1)
Definitions as analyze_cut.py (same functions): s over the shifted replicas (tags 1..10) that resolve with winding +1, complex plane; own estimate = control a's zeros_est."""
import json, math, os, random, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_cut as A
A.NEW_KFS = [31, 29]    # analyze() takes the control of the first one for --mutate=control
PRED = 7.3e-4           # 8.83e-5 (kf 29) x 8.32 (the geometric mean of the four ratios between neighbouring odd cuts, odd_harmonics.txt)


def verdicts(rows):
    r31, r29 = rows[31], rows[29]
    v = {}
    v["Q1"] = bool(r31["s"] and PRED / 3 <= r31["s"] <= PRED * 3)
    v["Q2"] = bool(r31["s"] and r29["s"] and 4 <= r31["s"] / r29["s"] <= 20)
    v["Q3"] = bool(r31["ctl_ok"])
    v["Q4"] = r31["n"] >= 9
    v["Q5"] = bool(r31["s"] and r31["rep_est"] and 0.25 <= r31["rep_est"] / r31["s"] <= 4)
    return v


def table(rows):
    print("| kf | replicas used | s | s / 7.3e-4 | s / s(29) | controls a = b | control zero | own estimate (control) | replicas' own estimate, median | that / s |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for kf in (29, 31):
        r = rows[kf]
        if r["s"] is None:
            print(f"| {kf} | {r['n']} of {r['n_all']} | n/a | | | {'yes' if r['ctl_ok'] else 'NO'} | | | | |")
            continue
        z = f"{r['zero'].real:.7f}{r['zero'].imag:+.7f}i" if r["zero"] else ""
        print(f"| {kf} | {r['n']} of {r['n_all']} | {r['s']:.3e} | {r['s'] / PRED:.2f} | {(r['s'] / rows[29]['s']):.2f} | {'yes' if r['ctl_ok'] else 'NO'} | {z} | {r['est']:.1e} | {r['rep_est']:.1e} | {r['rep_est'] / r['s']:.2f} |")


if __name__ == "__main__":
    old = [json.loads(l) for l in open(A.OLD)]
    if "--selftest" in sys.argv:
        rng = random.Random(31)

        def mk(s31):
            recs = []
            for kf, s in ((29, 8.8e-5), (31, s31)):
                z0 = complex(2.0435, 0.0)
                for t in ("a", "b"):
                    recs.append(dict(circle=f"k{kf}_phys", kf=kf, rep=0, tag=t, winding=1.0, resolved=True, zero=[z0.real, z0.imag], est=s))
                for r in range(1, 11):
                    z = z0 + complex(rng.gauss(0, s / math.sqrt(2)), rng.gauss(0, s / math.sqrt(2)))
                    recs.append(dict(circle=f"k{kf}_phys", kf=kf, rep=r, tag=str(r), winding=1.0, resolved=True, zero=[z.real, z.imag], est=s))
            return recs
        ok = True
        v = verdicts(A.analyze(mk(7e-4), old))
        good = v["Q1"] and v["Q2"] and v["Q3"] and v["Q4"] and v["Q5"]
        print("planted s(31) 7e-4:", "all criteria hold" if good else f"FAIL {v}")
        ok &= good
        v = verdicts(A.analyze(mk(1e-5), old))
        good = (not v["Q1"]) and (not v["Q2"])
        print("planted s(31) 1e-5 (wrong):", "Q1 and Q2 fail, as they must" if good else f"STILL HOLD {v}")
        ok &= good
        v = verdicts(A.analyze(mk(7e-4), old, mutate_control=True))
        good = not v["Q3"]
        print("control moved by one ulp:", "Q3 fails" if good else "Q3 STILL HOLDS (must fail)")
        ok &= good
        sys.exit(0 if ok else 1)
    recs = [json.loads(l) for l in open(os.path.join(HERE, "cut_588.jsonl"))]
    rows = A.analyze(recs, old, mutate_control="--mutate=control" in sys.argv)
    table(rows)
    if not rows[31]["complete"]:
        print(f"\nkf 31 incomplete: {rows[31]['n_all']} of 10 shifted replicas; no verdicts yet")
        sys.exit(2)
    v = verdicts(rows)
    print(f"\ns(31) = {rows[31]['s']:.3e} against the prediction {PRED:.1e} (band {PRED / 3:.1e} to {PRED * 3:.1e}); s(31)/s(29) = {rows[31]['s'] / rows[29]['s']:.2f}; first cut above 1e-4 among 21 to 31: " + ("31" if rows[31]["s"] > 1e-4 and rows[29]["s"] < 1e-4 else "see the table"))
    for k, ok in v.items():
        print(f"{k}: {'holds' if ok else 'FAILS'}")
    sys.exit(0 if all(v.values()) else 1)
