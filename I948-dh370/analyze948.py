"""#948: the six weakest directions of each ladder rung's base, and the verdict by the issue's rule.

    python analyze948.py FOLDER [--selftest [--mutate]]      FOLDER holds near_up_K<K>_from<P>.json, near_down_K<K>_from<P>.json and
                                                             near_D222_ks<K>.json (run948.sh near); exit 1 if the control fails

Classification of the vectors as #941's analyze941.py: the Delta mode is the vector with the largest Delta share (it must exceed 0.5),
the harmonic-3 pair the two vectors (not the Delta mode) with (p1, 3) and (m_h, 3) among their five printed components and one of them
among the two largest; sigma_pair is the geometric mean of the two, sigma_5 the fifth sigma. Control (issue): the ks 240 rung's sigma_Delta
is within 1% of #941's 5.277e-15 (5.2769e-15 printed at D 232.0, from `I941-dh370/o240_D232.0000.json`). Verdict: order 240 is converged for
the Delta mode at D 232 if sigma_Delta at K 280, 300 and 320 is within 10% of the 240 rung's, not converged if sigma_Delta changes by more
than a factor 2 from 240 to 320, and otherwise it is reported as it is. --selftest runs the rule on planted sigma_Delta(K); --mutate
swaps the planted converged series for a diverging one, so the selftest must then exit 1."""
import glob
import json
import math
import os
import re
import sys

REF941 = 5.2769e-15


def is_pair(top):
    names = {(b, k) for b, k, _ in top}
    first2 = {(b, k) for b, k, _ in top[:2]}
    return ("p1", 3) in names and ("m_h", 3) in names and bool(first2 & {("p1", 3), ("m_h", 3)})


def summary(rec):
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and is_pair(v[i]["top"])]
    out = dict(D=rec["D"], delta=d, delta_share=v[d]["delta"], pair=pair, sig=[x["sigma"] for x in v], conv=[x["conv"] for x in v],
               ok_class=v[d]["delta"] > 0.5 and len(pair) == 2)
    out["sd"] = v[d]["sigma"]
    out["spg"] = math.sqrt(v[pair[0]]["sigma"] * v[pair[1]]["sigma"]) if len(pair) == 2 else float("nan")
    out["s5"] = v[4]["sigma"]
    return out


def verdict(sd):
    """sd: {K: sigma_Delta}. 'converged' / 'not converged' / 'between', by the issue's rule"""
    s240 = sd[240]
    if all(K in sd and abs(sd[K] / s240 - 1) <= 0.10 for K in (280, 300, 320)):
        return "converged"
    if 320 in sd and (sd[320] / s240 > 2 or sd[320] / s240 < 0.5):
        return "not converged"
    return "between"


def selftest(mutate):
    flat = {240: 5.0e-15, 250: 5.1e-15, 260: 5.2e-15, 270: 5.15e-15, 280: 5.2e-15, 300: 5.3e-15, 320: 5.25e-15}
    grow = {K: 5.0e-15 * (1 + 0.15 * (K - 240) / 10) for K in flat}        # 15% per rung of 10: 2.2 times at 320
    mid = {K: 5.0e-15 * (1 + 0.004 * (K - 240)) for K in flat}             # 32% at 320
    ok = verdict(flat) == "converged" and verdict(grow) == "not converged" and verdict(mid) == "between"
    if mutate:
        ok = verdict(grow) == "converged"          # a wrong expectation: must fail
    print(f"selftest{' --mutate' if mutate else ''}: {'pass' if ok else 'FAIL'}")
    return ok


def load(folder):
    rungs = {}
    for p in sorted(glob.glob(os.path.join(folder, "near_*_K*_from*.json"))):
        m = re.search(r"near_(up|down)_K(\d+)_from(\d+)\.json$", p)
        if not m:
            continue                      # near_early_up_K240_from240.json is the 2-thread copy of near_up_K240_from240.json
        rungs[int(m.group(2))] = (os.path.basename(p), summary(json.load(open(p))))
    d222 = {}
    for p in sorted(glob.glob(os.path.join(folder, "near_D222_ks*.json"))):
        d222[int(re.search(r"ks(\d+)", p).group(1))] = summary(json.load(open(p)))
    return rungs, d222


def main(folder):
    rungs, d222 = load(folder)
    print("== D 232.0: each rung's six sigma (convergence), the Delta mode's identity and the ratios to the 240 rung")
    for K in sorted(rungs):
        name, s = rungs[K]
        print(f"ks {K}  ({name})  Delta mode = vector {s['delta'] + 1} (Delta share {s['delta_share']:.3f}), pair = vectors "
              f"{', '.join(str(i + 1) for i in s['pair'])}{'' if s['ok_class'] else '   CLASSIFICATION UNCLEAR'}")
        print("   sigma: " + "  ".join(f"{x:.3e} ({c:.0e})" for x, c in zip(s["sig"], s["conv"])))
    print("\nks    sigma_Delta   /240      sigma_pair    /240      sigma_5       /240      Delta share  Delta vector")
    base = rungs.get(240, (None, None))[1]
    for K in sorted(rungs):
        s = rungs[K][1]
        r = lambda a: f"{s[a] / base[a]:<8.4g}" if base else "-"
        print(f"{K:<5} {s['sd']:.4e}  {r('sd')}  {s['spg']:.4e}  {r('spg')}  {s['s5']:.4e}  {r('s5')}  {s['delta_share']:.3f}        {s['delta'] + 1}")
    ok = True
    if base:
        ctl = abs(base["sd"] / REF941 - 1)
        ok = ctl <= 0.01
        print(f"\ncontrol: the 240 rung's sigma_Delta {base['sd']:.4e} against #941's {REF941:.4e}: {ctl * 100:.3f}%: {'pass' if ok else 'FAIL'} (bound 1%)")
        sd = {K: rungs[K][1]["sd"] for K in rungs}
        if all(K in sd for K in (280, 300, 320)):
            print(f"verdict by the issue's rule: {verdict(sd)} (sigma_Delta(280, 300, 320) / sigma_Delta(240) = "
                  f"{', '.join(f'{sd[K] / sd[240]:.3f}' for K in (280, 300, 320))})")
        else:
            print(f"verdict: the rungs 280, 300 and 320 are not all present ({sorted(sd)}); the rule needs them")
    if d222:
        print("\n== D 222.0, by ks")
        for K in sorted(d222):
            s = d222[K]
            print(f"ks {K}: sigma_Delta {s['sd']:.4e}, sigma_pair {s['spg']:.4e}, sigma_5 {s['s5']:.4e}, Delta vector {s['delta'] + 1} "
                  f"(share {s['delta_share']:.3f}), pair vectors {', '.join(str(i + 1) for i in s['pair'])}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    sys.exit(0 if main(sys.argv[1]) else 1)
