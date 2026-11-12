#!/usr/bin/env python3
"""#600: why jacobian_f64/mut1 at the D 79.7657 state differs between the Mac's c3 and this build, when the 175 other outputs of api_bits.py agree.
Calls the same Solver.jacobian_f64(zh, zl, mutate=1) as I523-mac/api_bits.py (large state, threads 2) three times, and counts NaN and inf in the result. api_bits.py hashes the raw bytes, and the
default NaN of x86 has its sign bit set (0xFFF8...) where arm64's does not (0x7FF8...), so the hash is also recomputed with every NaN set to 0x7FF8000000000000. The Mac's stored hash is printed beside.
usage: python mut1_diag.py HPDIR RAWDIR MAC_API_JSON"""
import hashlib, json, sys
import numpy as np
hp, raw, macj = sys.argv[1:4]
sys.path.insert(0, hp)
from hpkernel.driver import make_solver
from octo_corrector import load_o


def digest(a):
    a = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
    return hashlib.sha256(a.tobytes()).hexdigest()[:20] + f":{a.shape}"


st = "anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz"
z8, m = load_o(raw + "/" + st)
zh, zl = np.array(z8[0], dtype=float), np.array(z8[1], dtype=float)
D = m.get("D_str", repr(float(m["D"])))
s = make_solver(D, int(m["M"]), nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=2, kfreeze=m.get("kfreeze", 3))
s.set_segs(s.plan(zh, zl, 1e-32, 0.05))
mac = json.load(open(macj))["states"][st]["jacobian_f64/mut1"]
ref = np.asarray(s.jacobian_f64(zh, zl, mutate=0), dtype=np.float64)
print("mutate=0: NaN", int(np.isnan(ref).sum()), "inf", int(np.isinf(ref).sum()), "hash", digest(ref))
hs = []
for i in range(3):
    a = np.asarray(s.jacobian_f64(zh, zl, mutate=1), dtype=np.float64)
    nan, inf = int(np.isnan(a).sum()), int(np.isinf(a).sum())
    bits = a.view(np.uint64)
    signs = sorted({hex(int(b)) for b in bits[np.isnan(a)]})[:4]
    b = a.copy()
    b[np.isnan(b)] = np.uint64(0x7FF8000000000000).view(np.float64)
    hs.append(digest(a))
    print(f"call {i}: NaN {nan}, inf {inf}, NaN bit patterns {signs}; raw hash {digest(a)}; hash with every NaN set to 0x7FF8000000000000: {digest(b)}")
print("mac stored hash:", mac)
print("raw hash equal to the Mac's:", hs[0] == mac, "| the three calls agree with each other:", len(set(hs)) == 1)
