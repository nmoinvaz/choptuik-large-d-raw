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


# #603's states between this chain's bases (its steps shorter than 1 from 237.13 on): Delta_142 there from this chain's
# saved series at the base below, sum_k z_k u^k with u = D - D_base, each coefficient its eight parts summed exactly.
# Check: each series at the next own state's D against that state's Delta, |diff| <= JET_BAR; --mutate=base moves every
# series' base by 1e-6 and must make it fail.
JET_BAR = mp.mpf("1e-18")
mut = "--mutate=base" in sys.argv


def jet(p):
    import json
    z = np.load(p)
    m = json.loads(str(z["meta"]))
    ks = sorted((k for k in z.files if k[0] == "z" and k[1:].isdigit()), key=lambda k: int(k[1:]))
    Db = mp.mpf(m["D_str"]) + (mp.mpf("1e-6") if mut else 0)
    return Db, [mp.fsum(mp.mpf(float(z[k][n][-1])) for k in ks) for n in range(z[ks[0]].shape[0])]


def horner(c, u):
    v = mp.mpf(0)
    for x in reversed(c):
        v = v * u + x
    return v


def d_of(p):
    import json
    return mp.mpf(json.loads(str(np.load(p)["meta"]))["D_str"])


own = sorted((d_of(p), p) for p in glob.glob(os.path.join(o, "chain_fixed/anm_pin3_D*.npz")))
jets = sorted(jet(p) for p in glob.glob(os.path.join(o, "chain_fixed/jet_pin3_D*.npz")))
worst = mp.mpf(0)
for Db, c in jets:
    nxt = [(D, p) for D, p in own if D > Db + mp.mpf("1e-9")]
    if nxt:
        worst = max(worst, abs(horner(c, nxt[0][0] - Db) - delta(nxt[0][1])))
ok = worst <= JET_BAR
print(f"check: max|series at the next own state - its Delta| {mp.nstr(worst, 3)} over {len(jets)} series "
      f"(bound {mp.nstr(JET_BAR, 2)}): {'pass' if ok else 'FAIL'}{' (mutation base: must fail)' if mut else ''}")
print("D (#603)   Delta_142 from the series at base   Delta_142 - Delta_603")
for p in sorted(glob.glob(f"{raw}/I603-win2/chain/anm_pin3_D*.npz")):
    D = d_of(p)
    below = [(Db, c) for Db, c in jets if Db <= D + mp.mpf("1e-12")]
    if not below or float(D) < 237.2:
        continue
    Db, c = below[-1]
    nxt = [Dn for Dn, _ in own if Dn > Db + mp.mpf("1e-9")]
    if not nxt or D > nxt[0] + mp.mpf("1e-12"):
        continue
    a = horner(c, D - Db)
    print(f"{mp.nstr(D, 10):<10} {mp.nstr(a, 25):<27} {mp.nstr(Db, 9):<9} {mp.nstr(a - delta(p), 6)}")
sys.exit(1 if ok == mut else 0)
