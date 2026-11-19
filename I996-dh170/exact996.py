#!/usr/bin/env python3
"""#996: the exact orders sigma_0 .. sigma_M of hier's model M are those of the full problem, so every model M' >= M gives the same sigma_j for j <= M (k = 2j + 1 <= 2M + 1).
Two runs of different M at the same or different digits must agree there, a precision check that needs no higher-digit run of the same M: M 7 at 120 digits against M 9 at 120
and against M 9 at 180 (k <= 9, the orders the 180-digit run has), M 5 at 120 against M 7 and M 9 at 120, M 3 against the others. Printed: the largest relative difference over
the exact orders of the pair, and the k where it occurs, from the 20-digit JSONs (K 18) and the 15-digit log of the 180-digit run (K 9).
    python exact996.py"""
import json
import os
import re

import mpmath as mp

mp.mp.dps = 30
HERE = os.path.dirname(os.path.abspath(__file__))


def js(name):
    d = json.load(open(os.path.join(HERE, name)))
    return [mp.mpc(mp.mpf(a), mp.mpf(b)) for a, b in d["sigma_str"]]


def log(name):
    out = {}
    for line in open(os.path.join(HERE, name)):
        m = re.match(r"^k (\d+): sigma_(\d+) = \(([^ ]+) ([+-] ?[^ ]+)j\)", line)
        if m:
            out[int(m.group(2))] = mp.mpc(mp.mpf(m.group(3)), mp.mpf(m.group(4).replace(" ", "")))
    return out


R = {"M3_60": js("trunc_hier_M3_K18_J1000_w1.0000.json"), "M3_120": js("trunc_hier_M3_K18_J1000_w1.0000_dps120.json"),
     "M5_60": js("trunc_hier_M5_K18_J1000_w1.0000.json"), "M5_120": js("trunc_hier_M5_K18_J1000_w1.0000_dps120.json"),
     "M7_120": js("trunc_hier_M7_K18_J1000_w1.0000_dps120.json"), "M9_120": js("trunc_hier_M9_K18_J1000_w1.0000_dps120.json"),
     "M9_180": js("trunc_hier_M9_K15_J1000_w1.0000_dps180.json"), "M7_180": js("trunc_hier_M7_K15_J1000_w1.0000_dps180.json")}
MOF = {"M3_60": 3, "M3_120": 3, "M5_60": 5, "M5_120": 5, "M7_120": 7, "M9_120": 9, "M9_180": 9, "M7_180": 7}


def pair(a, b):
    n = min(MOF[a], MOF[b], len(R[a]) - 1, len(R[b]) - 1)
    worst, at = mp.mpf(0), 0
    for j in range(n + 1):
        d = abs(R[a][j] - R[b][j]) / abs(R[a][j])
        if d > worst:
            worst, at = d, j
    return n, worst, at


print("exact orders sigma_0 .. sigma_n (n = min(M, M'), and what the shorter run reached), largest relative difference, 20-digit JSONs:")
for a, b in [("M3_60", "M3_120"), ("M5_60", "M5_120"), ("M3_120", "M5_120"), ("M3_120", "M7_120"), ("M3_120", "M9_120"), ("M5_120", "M7_120"), ("M5_120", "M9_120"),
             ("M7_120", "M9_120"), ("M7_120", "M9_180"), ("M7_120", "M7_180"), ("M7_180", "M9_120"), ("M9_120", "M9_180"), ("M3_60", "M5_60")]:
    n, w, at = pair(a, b)
    print(f"  {a:>7} against {b:<7}: sigma_0..sigma_{n}: largest {mp.nstr(w, 3):>9} at sigma_{at}")


# the same in the coordinator's units: |sigma_j^[M] - sigma_j^[M']| over |Delta sigma_{M+1}| (Delta sigma_{M+1} = sigma_{M+1}^[M'] - sigma_{M+1}^[M], M' the next model run), 1% = 0.01
print("\nthe exact orders of the next-larger model against this one, as a fraction of Delta sigma_{M+1} (the 1% rule, 120-digit runs):")
for M, Mn in [(3, 5), (5, 7), (7, 9)]:
    a, b = R[f"M{M}_120"], R[f"M{Mn}_120"]
    dsh = abs(b[M + 1] - a[M + 1])
    row = []
    for j in range(M + 1):
        row.append(abs(a[j] - b[j]) / dsh)
    worst = max(range(M + 1), key=lambda j: row[j])
    print(f"  M {M} against M {Mn}: |Delta sigma_{M + 1}| = {mp.nstr(dsh, 4)}; |sigma_j difference| / that, j = 0..{M}: " + ", ".join(mp.nstr(x, 2) for x in row)
          + f"  -> largest {mp.nstr(row[worst], 2)} at sigma_{worst}: {'within 1%' if row[worst] <= 0.01 else 'OVER 1%'}")
