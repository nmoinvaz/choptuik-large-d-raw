#!/usr/bin/env python3
"""#1057 closing: pair estimates of a fold point D* for the lowest vector's sigma after the return of the Delta mode (D 261.39 to the last state), under the fold law sigma^2 = c (D* - D) exp(-2 s D):
z = sigma^2 exp(2 s D) is linear in D with zero at D*, so each consecutive pair gives D* = D2 + z2 (D2 - D1) / (z1 - z2). Printed for s = 0 and s = 0.3274 (the frozen D-trend's slope). A fold would give a stable D*.

    fold_pairs1057.py                 the real states of this folder
    fold_pairs1057.py --selftest [--mutate]   planted: sigma from the law with D* 263.0 and s 0.3274 must give D* = 263.0 from every pair (1e-9); --mutate uses s 0 on the same planted data and must fail"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["261.3914", "261.5124", "261.6229", "261.6746", "261.7748", "261.8239", "261.9176", "262.0099"]


def pairs(D, S, s):
    z = [S[i] ** 2 * math.exp(2 * s * D[i]) for i in range(len(D))]
    return [D[i + 1] + z[i + 1] * (D[i + 1] - D[i]) / (z[i] - z[i + 1]) if z[i] > z[i + 1] else float("inf") for i in range(len(D) - 1)]


def selftest(mutate):
    D = [float(n) for n in NAMES]
    s0, Ds = 0.3274, 263.0
    S = [math.sqrt(0.01 * (Ds - d) * math.exp(-2 * s0 * d)) for d in D]
    got = pairs(D, S, 0.0 if mutate else s0)
    ok = all(abs(g - Ds) < 1e-9 for g in got)
    print(f"selftest: planted fold D* {Ds}, s {s0}, pairs read with s {0.0 if mutate else s0}: {', '.join(f'{g:.6f}' for g in got[:3])} ...: {'pass' if ok else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    D, S = [], []
    for n in NAMES:
        r = json.load(open(os.path.join(HERE, f"c3b_ks293_D{n}.json"))); D.append(r["D"]); S.append(r["vectors"][0]["sigma"])
    for s in (0.0, 0.3274):
        print(f"s = {s}: D* from the pairs " + ", ".join(f"{D[i]:.4f}-{D[i + 1]:.4f}" for i in range(len(D) - 1)))
        print("   " + ", ".join(f"{x:.3f}" for x in pairs(D, S, s)))
    print("local slope -d ln sigma / dD of the lowest vector: " + ", ".join(f"{-math.log(S[i + 1] / S[i]) / (D[i + 1] - D[i]):.3f}" for i in range(len(D) - 1)))
