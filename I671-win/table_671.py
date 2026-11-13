#!/usr/bin/env python3
"""#671: rt_sigma.py's bounds on the K = 7 roots and their same-start K = 0 controls at D 40.020065, 50.007491 (from #643) and 54.996085, and the verdict of the rules fixed in README.md.
usage: python table_671.py          (from this folder; reads logs/{K7,K0}_{D40,D55}_{rough,smooth}.log, ../I643-win/logs/{K7_a,K0_a}_{rough,smooth}.log and table_423.py's parser)
R(D) = rough bound of the K = 7 state / rough bound of its same-start K = 0 control. The K = 7 bounds FOLLOW the K = 0 trend within a factor 3 if R(40.020065) and R(54.996085) each lie within a factor 3 of
R(50.007491) (#643, start a: 4.12). Class and 'seen by smooth' by #423's rules; the K = 7 series' own D trend is measured from its rough bounds (decades per 10 in D between D 40.02, 50.007, 54.996;
horizon-like if below -3, not horizon-like within +-1, in between otherwise; the last step scaled to 10 in D); a D's verdict uses the step that ends at it (D 40.02 uses the step from 40.02 to 50.007):
(H) edge + only rough + horizon-like; (C) centre in omega_4 + seen by smooth + not horizon-like; neither otherwise."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402

I643 = os.path.join(HERE, "..", "I643-win", "logs")
DS = (("D40", 40.020065), ("D50", 50.007491), ("D55", 54.996085))
FACTOR = 3.0
K0_423 = {"D40": 5.227e-34, "D50": 1.404e-34, "D55": 2.559e-35}       # #423's rough bounds of the `fol` K = 0 roots on 32x121


def path(k, d, kind):
    if d == "D50":
        return os.path.join(I643, f"{k}_a_{kind}.log")
    return os.path.join(HERE, "logs", f"{k}_{d}_{kind}.log")


def load(k, d, kind):
    p = path(k, d, kind)
    if not os.path.exists(p):
        return None
    r = t.parse(open(p, encoding="utf-8", errors="replace").read())
    if r["head"] is None or not r["starts"]:
        return None
    return r["head"], t.summarize(r)


def trend_class(dec):
    return "horizon-like" if dec < -3 else ("not horizon-like" if abs(dec) <= 1 else "in between")


def main():
    runs = {(k, d, kind): load(k, d, kind) for k in ("K7", "K0") for d, _ in DS for kind in ("rough", "smooth")}
    print("| D | K | kind | bound (best of 3) | starts' spread | worst residual | products | mu | E | C0 | C4 | class |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for d, D in DS:
        for k in ("K7", "K0"):
            for kind in ("rough", "smooth"):
                r = runs[(k, d, kind)]
                if r is None:
                    print(f"| {D} | {k} | {kind} | not yet | | | | | | | | |")
                    continue
                h, s = r
                f = lambda key: "n/a" if s.get(key) is None else f"{s[key]:.2f}"
                print(f"| {D} | {k} (K {h['K']}) | {kind} | {s['bound']:.3e} | {s['spread']:.1f} | {s['res']:.1e} | {s['prods']} | {f('mu')} | {f('E')} | {f('C0')} | {f('C4')} | {s.get('cls', 'n/a')} |")
    # R(D)
    print("\nR(D) = rough K = 7 bound / rough K = 0 control bound:")
    R = {}
    for d, D in DS:
        a, b = runs[("K7", d, "rough")], runs[("K0", d, "rough")]
        if a and b:
            R[d] = a[1]["bound"] / b[1]["bound"]
            print(f"  D {D}: {a[1]['bound']:.3e} / {b[1]['bound']:.3e} = {R[d]:.2f}")
    if len(R) == 3:
        for d, D in (("D40", 40.020065), ("D55", 54.996085)):
            q = R[d] / R["D50"]
            ok = 1 / FACTOR <= q <= FACTOR
            print(f"  R({D}) / R(50.007491) = {q:.2f} -> {'within' if ok else 'OUTSIDE'} a factor {FACTOR:g}")
        both = all(1 / FACTOR <= R[d] / R["D50"] <= FACTOR for d in ("D40", "D55"))
        print(f"  VERDICT on the trend: the K = 7 bounds {'FOLLOW' if both else 'DO NOT FOLLOW'} the K = 0 trend within a factor {FACTOR:g}")
    # own D trend of both series
    print("\nD trend of the rough bounds (decades per 10 in D):")
    trends = {}
    for k in ("K7", "K0"):
        rs = [(D, runs[(k, d, "rough")]) for d, D in DS]
        if all(r for _, r in rs):
            for (D1, r1), (D2, r2) in zip(rs, rs[1:]):
                dec = math.log10(r2[1]["bound"] / r1[1]["bound"]) * 10.0 / (D2 - D1)
                trends[(k, D2)] = dec
                print(f"  {k}: D {D1} -> {D2}: {r1[1]['bound']:.3e} -> {r2[1]['bound']:.3e}, {dec:+.2f} decades per 10 in D, {trend_class(dec)}")
    print("  (#423's K = 0 `fol` roots: 5.227e-34, 1.404e-34, 2.559e-35 = -0.57 and -1.48 decades per 10 in D)")
    # verdicts
    print("\nVerdict per D by #423's rules with the measured trend of the same series:")
    for k in ("K7", "K0"):
        for i, (d, D) in enumerate(DS):
            ro, sm = runs[(k, d, "rough")], runs[(k, d, "smooth")]
            if not ro or not sm:
                continue
            step = trends.get((k, DS[i][1] if i > 0 else DS[1][1]))
            tcls = None if step is None else trend_class(step)
            seen = sm[1]["bound"] / ro[1]["bound"] <= 100
            cls = ro[1].get("cls")
            v = "(H)" if cls == "edge" and not seen and tcls == "horizon-like" else ("(C)" if cls == "centre in w4" and seen and tcls == "not horizon-like" else "neither")
            print(f"  {k} D {D}: x {cls}; smooth/rough {sm[1]['bound'] / ro[1]['bound']:.2e} ({'seen' if seen else 'not seen'}); trend {tcls} ({'n/a' if step is None else f'{step:+.2f}'}) -> {v}")
    # POST-HOC sensitivity (added after the best-of-3 result was seen; not the criterion): the same ratio with the median of the three rough starts instead of the best
    print("\nPOST-HOC sensitivity, not the criterion: R from the median of the three rough starts instead of the best (the best-of-3 has a start-to-start spread of up to a factor 8):")

    def starts(k, d):
        r_ = t.parse(open(path(k, d, "rough"), encoding="utf-8", errors="replace").read())
        return sorted(v["bound"] for v in r_["starts"].values())
    Rm = {}
    for d, D in DS:
        try:
            a, b = starts("K7", d), starts("K0", d)
        except FileNotFoundError:
            continue
        Rm[d] = a[len(a) // 2] / b[len(b) // 2]
        print(f"  D {D}: K = 7 starts {', '.join(f'{x:.2e}' for x in a)} (median {a[len(a) // 2]:.2e}); K = 0 starts {', '.join(f'{x:.2e}' for x in b)} (median {b[len(b) // 2]:.2e}); R_median = {Rm[d]:.2f}")
    if len(Rm) == 3:
        for d, D in (("D40", 40.020065), ("D55", 54.996085)):
            q = Rm[d] / Rm["D50"]
            print(f"  R_median({D}) / R_median(50.007491) = {q:.2f} -> {'within' if 1 / FACTOR <= q <= FACTOR else 'OUTSIDE'} a factor {FACTOR:g}")
    print(f"\nThe K = 0 controls against #423's `fol` roots (rough bound; within a factor 3 expected):")
    for d, D in DS:
        b = runs[("K0", d, "rough")]
        if b:
            q = b[1]["bound"] / K0_423[d]
            print(f"  D {D}: {b[1]['bound']:.3e} against {K0_423[d]:.3e}: factor {q:.2f} -> {'within 3' if 1 / 3 <= q <= 3 else 'OUTSIDE 3'}")


if __name__ == "__main__":
    main()
