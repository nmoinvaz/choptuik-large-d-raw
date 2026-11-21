#!/usr/bin/env python3
"""jetbits1064.py A.npz B.npz | --selftest [--break]: whether two jets are identical bit for bit: the eight parts z0..z7 of A and B compared as float64 arrays (np.array_equal on the raw bits, so -0.0 against 0.0 and NaN
payloads count as differences). Prints 'identical' or the number of differing entries per part. Exit 0 identical, 1 different, 2 shape mismatch. --selftest plants a copy (identical), a copy with one low-part entry changed by one ulp (must be found) and a
shape mismatch; --break flips the one-ulp expectation and must exit 1."""
import sys

import numpy as np


def load(p):
    z = np.load(p, allow_pickle=True)
    return [np.ascontiguousarray(z[f"z{q}"]) for q in range(8)]


def compare(A, B):
    """(identical, [differing entries per part]) or None on a shape mismatch"""
    if any(a.shape != b.shape for a, b in zip(A, B)):
        return None
    cnt = [int((a.view(np.uint64) != b.view(np.uint64)).sum()) for a, b in zip(A, B)]
    return sum(cnt) == 0, cnt


def selftest(brk):
    rng = np.random.default_rng(3)
    A = [rng.standard_normal((4, 5)) * 10.0 ** (-17 * q) for q in range(8)]
    B = [a.copy() for a in A]
    C = [a.copy() for a in A]
    C[5][2, 3] = np.nextafter(C[5][2, 3], 1.0)
    cases = [("identical copy", compare(A, B), lambda r: r is not None and r[0] and sum(r[1]) == 0),
             ("one entry of part 5 changed by one ulp", compare(A, C), lambda r: r is not None and (not r[0]) and r[1][5] == 1 and sum(r[1]) == 1),
             ("shape mismatch", compare(A, [a[:3] for a in B]), lambda r: r is None)]
    if brk:
        cases[1] = (cases[1][0], cases[1][1], lambda r: r is not None and r[0])
    bad = 0
    for name, r, chk in cases:
        ok = chk(r)
        print(f"  {name}: {r}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    r = compare(load(sys.argv[1]), load(sys.argv[2]))
    if r is None:
        print("shape mismatch")
        sys.exit(2)
    print("identical bit for bit (all eight parts, all coefficients)" if r[0] else f"DIFFERENT: differing entries per part {r[1]}")
    sys.exit(0 if r[0] else 1)
