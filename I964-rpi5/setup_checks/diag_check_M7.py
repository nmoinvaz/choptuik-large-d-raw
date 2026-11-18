# diagnostic for the failed inner_nb check at M 7: the yardstick's spread over several scipy rtols, and both backends at 1e-13
import sys, os, time
HERE = "/home/nathan/Source/choptuik-large-d-964/solver/inner_stokes"
os.chdir(HERE); sys.path.insert(0, HERE)
import numpy as np
import inner_nb as N
import inner_np as I
import hier as H
M = 7
x = N._point(M)
h = H.Hier(M)
low, pol = h.radii(x)
radii = [0.2] + list(low.values()) + list(pol.values())
used = {(0.2, 1), (0.2, 3)} | {(low[nu], nu) for nu in low if nu >= 5} | {(pol[nu], nu) for nu in pol if nu >= 5}
orig = I.Inner

def mk(rt):
    class C(orig):
        def jumps(self, r1s=(0.2,), r0=None, rtol=1e-12):
            return orig.jumps(self, r1s, r0, rt)
    return C

def run_scipy(rt):
    I.Inner = mk(rt); R = H.demixed_multi(x, M, radii); I.Inner = orig; return R

def run_numba(rt):
    I.Inner = N.InnerNB; N.RTOL_OVERRIDE = rt; R = H.demixed_multi(x, M, radii); I.Inner = orig; N.RTOL_OVERRIDE = None; return R

def ent(R):
    out = {}
    for r in R:
        for li, nu in enumerate(range(1, M + 1, 2)):
            if (r, nu) in used:
                out[(r, nu)] = complex(*R[r][2 * li:2 * li + 2])
    return out

rts = [1e-12, 0.9e-12, 0.8e-12, 0.6e-12, 0.4e-12, 1e-13]
S = {}
for rt in rts:
    t = time.time(); S[rt] = ent(run_scipy(rt)); print(f"scipy rtol {rt:g}: {time.time()-t:.1f} s", flush=True)
NB = {}
for rt in [1e-12, 0.8e-12, 1e-13]:
    t = time.time(); NB[rt] = ent(run_numba(rt)); print(f"numba rtol {rt:g}: {time.time()-t:.1f} s", flush=True)
print("entry                scipy-spread(rtol 1e-12..4e-13) | numba-scipy @1e-12 | numba-scipy @1e-13 | numba spread(1e-12,0.8e-12) | rel |numba-scipy|@1e-12")
for k in sorted(S[1e-12]):
    vals = np.array([S[rt][k] for rt in rts[:5]])
    spread = np.ptp(vals.real) + 0j; spread = max(np.ptp(vals.real), np.ptp(vals.imag))
    d12 = abs(NB[1e-12][k] - S[1e-12][k]); d13 = abs(NB[1e-13][k] - S[1e-13][k])
    nsp = abs(NB[1e-12][k] - NB[0.8e-12][k])
    print(f"xi {k[0]:.4f} r_{k[1]}  {spread:9.2e} | {d12:9.2e} | {d13:9.2e} | {nsp:9.2e} | {d12/abs(S[1e-12][k]):9.2e}")
