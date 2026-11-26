"""hp's odd and even d/dtheta (driver.dmat_odd and form_s.dmat_even's hi + lo, plus form_s.dmat_corr's c) against
multishoot PR #67's reference entries (tests/data/dmat_mp.txt: 120-digit D split into f64 hi, lo, c) at M 8 and 16:
the largest |hp's hi + lo + c - multishoot's hi + lo + c|, of hi + lo alone, and the parts that differ.

    python3 dmat_ms_entries.py HP_DIR DMAT_MP.TXT
"""
import struct
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import mpmath as mp  # noqa: E402

import form_s  # noqa: E402
import hpkernel.driver as drv  # noqa: E402


def f(h):
    return struct.unpack("<d", struct.pack("<Q", int(h, 16)))[0]


ref = {}
for line in open(sys.argv[2]):
    if line.startswith("#") or not line.strip():
        continue
    p, m, i, j, h, lo, c = line.split()
    ref[(p, int(m), int(i), int(j))] = (f(h), f(lo), f(c))
mp.dps = 60
for M in (8, 16):
    oh, ol = drv.dmat_odd(M)
    eh, el = form_s.dmat_even(M)
    co, ce = form_s.dmat_corr(M)
    for p, (h, lo, c) in (("odd", (oh, ol, co)), ("even", (eh, el, ce))):
        h, lo, c = np.asarray(h), np.asarray(lo), np.asarray(c)
        e3 = e2 = mp.mpf(0)
        nh = nl = nc = 0
        for i in range(M):
            for j in range(M):
                rh, rl, rc = ref[(p, M, i, j)]
                a3 = mp.mpf(h[i, j]) + mp.mpf(lo[i, j]) + mp.mpf(c[i, j])
                b3 = mp.mpf(rh) + mp.mpf(rl) + mp.mpf(rc)
                e3 = max(e3, abs(a3 - b3))
                e2 = max(e2, abs(mp.mpf(h[i, j]) + mp.mpf(lo[i, j]) - b3))
                nh += h[i, j] != rh
                nl += lo[i, j] != rl
                nc += c[i, j] != rc
        print(f"M {M} {p}: max |hp hi+lo+c - multishoot| {mp.nstr(e3, 3)}; hp hi+lo against it {mp.nstr(e2, 3)}; "
              f"parts that differ: hi {nh}, lo {nl}, c {nc} of {M * M}", flush=True)
