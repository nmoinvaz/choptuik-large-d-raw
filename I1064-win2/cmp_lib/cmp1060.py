#!/usr/bin/env python3
"""cmp1060.py: the comparator of #1060 (states of anm_run.py, eight parts zh zl z2..z7 and a `meta`).
  cmp1060.py bits REF NEW [--mutate [KEY]] the verdict is Delta and the exactly summed parts (each component's eight parts summed as exact rationals: Delta, the last component, and every S_i
                                          equal), with D_str and the step's a equal; exit 0 when they are, 1 when not. Per part, the bytes that differ and M1 (max |dpart| / max |part|)
                                          are printed as information. --mutate: one byte of NEW's KEY (z3 by default; z7 is the smallest) flipped in memory first (the control: the
                                          verdict must be a difference, exit 1).
  cmp1060.py close REF NEW [--tol 1e-100] the agreement of two states that need not be bit for bit, three readings (exact sums at 600 bits):
                                          Delta   |Delta(NEW) - Delta(REF)| / |Delta(REF)|, Delta the last component;
                                          M1      per part k, max_i |NEW_k,i - REF_k,i| / max_i |REF_k,i| (the issue's words: "each part's max");
                                          M2      max_i |S(NEW)_i - S(REF)_i| / max_i |S(REF)_i|, S_i the eight parts of component i summed exactly (the representation does not enter).
                                          Exit 0 when Delta and M2 are at or below --tol, 1 when not (M1 is printed, see --plant).
  cmp1060.py files REF NEW [--mutate]    every numeric array of two npz files (the series `jet_pin3_*`, the prediction `pred_pin3_*`) byte for byte, `meta` apart (its json keys that differ are
                                          named; the source path and the like are expected to). Exit 0 when all arrays are identical, 1 when not. --mutate flips one byte of NEW's first array (the control).
  cmp1060.py plant EPS REF OUT.npz        OUT = REF with every component's exact sum moved by EPS * max|S| * s_i (s_i in [-1, 1], a fixed pattern), split again into eight parts by greedy rounding
                                          to nearest, the planted test of `close`: EPS 1e-120 must pass it (M2, Delta), EPS 1e-90 must fail it; M1 shows what the parts' own representation does."""
import json
import sys

import mpmath as mp
import numpy as np

mp.mp.prec = 600
KEYS = ["zh", "zl"] + [f"z{i}" for i in range(2, 8)]


def load(p):
    d = np.load(p, allow_pickle=False)
    return {k: np.asarray(d[k]) for k in d.files}


def meta(d):
    return json.loads(str(d["meta"]))


def sums(d):
    n = len(d["zh"])
    return [mp.fsum(mp.mpf(float(d[k][i])) for k in KEYS if k in d) for i in range(n)]


def exact(d):
    """each component's parts summed as exact rationals"""
    from fractions import Fraction
    return [sum((Fraction(float(d[k][i])) for k in KEYS if k in d), Fraction(0)) for i in range(len(d["zh"]))]


def cmd_bits(a, b, mutate):
    A, B = load(a), load(b)
    if mutate:
        key = mutate if isinstance(mutate, str) else "z3"
        B[key] = B[key].copy()
        B[key].view(np.uint8).reshape(-1)[0] ^= 1
    ma, mb = meta(A), meta(B)
    bad = {}
    for k in KEYS:
        if k in A and k in B:
            n = int(np.sum(A[k].view(np.uint8) != B[k].view(np.uint8))) if A[k].shape == B[k].shape else -1
            if n:
                bad[k] = n
        elif (k in A) != (k in B):
            bad[k] = -1
    sD = ma["D_str"] == mb["D_str"]
    sa = ma["a"] == mb["a"]
    EA, EB = exact(A), exact(B)
    dD = EB[-1] - EA[-1]
    dS = max(abs(x - y) for x, y in zip(EA, EB))
    sums_equal = dD == 0 and dS == 0
    m1 = {k: float(np.max(np.abs(B[k] - A[k])) / np.max(np.abs(A[k]))) if np.max(np.abs(A[k])) > 0 else float("nan") for k in KEYS if k in A and k in B}
    print(f"bits{' (--mutate: one byte of NEW ' + (mutate if isinstance(mutate, str) else 'z3') + ' flipped)' if mutate else ''}: D_str equal {sD} ({ma['D_str'][:14]}, {mb['D_str'][:14]}), a equal {sa} ({ma['a']!r}, {mb['a']!r})")
    print(f"  exactly summed parts: Delta difference {mp.nstr(mp.mpf(dD.numerator) / dD.denominator, 4) if dD else 0}, max |dS_i| {mp.nstr(mp.mpf(dS.numerator) / dS.denominator, 4) if dS else 0}: {'equal' if sums_equal else 'DIFFER'}")
    print(f"  information: parts with differing bytes {bad if bad else 'none'} ({len(KEYS)} parts compared); M1 per part " + ", ".join(f"{k} {v:.1e}" for k, v in m1.items()))
    ok = sD and sa and sums_equal
    print("identical" if ok else "DIFFERENT")
    return 0 if ok else 1


def cmd_files(a, b, mutate):
    A, B = load(a), load(b)
    first = next(k for k in A if k != "meta" and A[k].dtype != object and A[k].size)
    if mutate:
        B[first] = B[first].copy()
        B[first].view(np.uint8).reshape(-1)[0] ^= 1
    bad, same = {}, 0
    for k in A:
        if k == "meta" or A[k].dtype == object or k not in B:
            continue
        n = int(np.sum(A[k].view(np.uint8) != B[k].view(np.uint8))) if A[k].shape == B[k].shape else -1
        if n:
            bad[k] = n
        else:
            same += 1
    miss = sorted(set(A) ^ set(B))
    mk = ""
    if "meta" in A and "meta" in B:
        ma, mb = meta(A), meta(B)
        mk = sorted(k for k in set(ma) | set(mb) if ma.get(k) != mb.get(k))
    print(f"files{' (--mutate: one byte of NEW ' + first + ' flipped)' if mutate else ''}: {same} arrays identical, differing bytes {bad if bad else 'none'}, arrays in one file only {miss if miss else 'none'}, meta keys that differ {mk}")
    print("identical" if not bad and not miss else "DIFFERENT")
    return 0 if not bad and not miss else 1


def cmd_close(a, b, tol):
    A, B = load(a), load(b)
    SA, SB = sums(A), sums(B)
    mx = max(abs(x) for x in SA)
    dD = abs(SB[-1] - SA[-1]) / abs(SA[-1])
    m2 = max(abs(x - y) for x, y in zip(SA, SB)) / mx
    m1 = {k: float(np.max(np.abs(B[k] - A[k])) / np.max(np.abs(A[k]))) if np.max(np.abs(A[k])) > 0 else float("nan") for k in KEYS if k in A and k in B}
    ok = dD <= tol and m2 <= tol
    print(f"close (tol {tol:g}): Delta REF {mp.nstr(SA[-1], 25)}, relative difference {mp.nstr(dD, 4)}; M2 (exact sums, vs max |S| {mp.nstr(mx, 6)}) {mp.nstr(m2, 4)}")
    print("  M1 per part (max |dpart| / max |part|): " + ", ".join(f"{k} {v:.1e}" for k, v in m1.items()))
    print("agree" if ok else "DISAGREE")
    return 0 if ok else 1


def cmd_plant(eps, a, out):
    A = load(a)
    S = sums(A)
    mx = max(abs(x) for x in S)
    n = len(S)
    new = {k: np.zeros(n) for k in KEYS}
    for i, x in enumerate(S):
        x = x + mp.mpf(eps) * mx * mp.mpf(((i * 7919) % 13) - 6) / 6
        for k in KEYS:
            p = float(x)
            new[k][i] = p
            x -= mp.mpf(p)
    for k in A:
        if k not in KEYS:
            new[k] = A[k]
    np.savez(out, **new)
    print(f"plant EPS {eps}: wrote {out} (exact sums moved by EPS * {mp.nstr(mx, 6)} * s_i, re-split into eight parts)")
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "bits":
        mu = False
        if "--mutate" in sys.argv:
            i = sys.argv.index("--mutate")
            mu = sys.argv[i + 1] if i + 1 < len(sys.argv) and sys.argv[i + 1].startswith("z") else True
        sys.exit(cmd_bits(sys.argv[2], sys.argv[3], mu))
    if c == "files":
        sys.exit(cmd_files(sys.argv[2], sys.argv[3], "--mutate" in sys.argv))
    if c == "close":
        tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 1e-100
        sys.exit(cmd_close(sys.argv[2], sys.argv[3], tol))
    if c == "plant":
        sys.exit(cmd_plant(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(2)
