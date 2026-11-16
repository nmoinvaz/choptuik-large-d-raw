"""#903: Delta of the fixed-order chain's states (and rung 142's base) against #603's chain at the same D, both from their
eight parts summed exactly, where #603 has a state at that D (its chain from 225.13125 steps by a = 1 as this one does).
    python3 delta_cmp_903.py RAW SCRATCH/i903   (from hp/, with the #523 build on PYTHONPATH)"""
import glob
import os
import sys
import mpmath as mp
import numpy as np
from octo_corrector import load_o

raw, o = sys.argv[1], sys.argv[2]
mp.mp.dps = 60


def delta(p):
    return mp.fsum(mp.mpf(float(np.asarray(q)[-1])) for q in load_o(p)[0])


print("D          Delta(ks 142)                     Delta_142 - Delta_603")
for p in [os.path.join(o, "ladder/k142_from140/base_pin3_D225.1312.npz")] + sorted(glob.glob(os.path.join(o, "chain_fixed/anm_pin3_D*.npz"))):
    tag = os.path.basename(p).split("_D")[1]
    ref = glob.glob(f"{raw}/I603-win2/chain/anm_pin3_D{tag}") or glob.glob(f"{raw}/I603-win2/base/base_pin3_D{tag}")
    if ref:
        a = delta(p)
        print(f"{tag[:-4]:<10} {mp.nstr(a, 25):<33} {mp.nstr(a - delta(ref[0]), 6)}")
