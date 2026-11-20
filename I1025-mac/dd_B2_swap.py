import sys, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
import ell_ddm
from scipy.optimize import brentq
S, z = ell_ddm._setup("/Users/nathan/Source/choptuik-1025/solver/matter/data/sol_l1kc31L1025_D13.0000.npy", 13.0, 31)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk
cache = {}
def sl(lam):
    if lam not in cache:
        with np.errstate(all="ignore"):
            Mf = S.mode_matrix(z, lam)
        Md = E.mode_matrix(z, lam, only=[12])
        Mf[r0:r0 + blk, c0:c0 + nf] = Md.h[r0:r0 + blk, c0:c0 + nf] + Md.l[r0:r0 + blk, c0:c0 + nf]
        cache[lam] = np.linalg.slogdet(Mf)
        print(f"  lambda {lam!r}: swapped sign {cache[lam][0]:+.0f}, ln|det| {cache[lam][1]:.10f}", flush=True)
    return cache[lam]
lo, hi = 2.6641484641099442, 2.7041484641099442
ref = 0.5 * (sl(lo)[1] + sl(hi)[1])
root = brentq(lambda l: sl(l)[0] * np.exp(sl(l)[1] - ref), lo, hi, xtol=1e-11, rtol=1e-15)
dd_root, rec = 2.684148132800803, 2.6841484641099442
v = "CONFIRMED" if abs(root - dd_root) <= 1e-8 else ("NOT block 12" if abs(root - rec) <= 1e-8 else "UNEXPLAINED")
print(f"swapped root {root!r}: minus the dd root {root - dd_root:+.2e}, minus the float64 record {root - rec:+.2e} -> {v}")
open("/Users/nathan/Source/choptuik-1025/solver/matter/data/ell_ddm_checks_1025.jsonl", "a").write(json.dumps(dict(
    test="B2 swap block 12", D=13.0, kc=31, root=root, minus_dd=root - dd_root, minus_record=root - rec, verdict=v, n_eval=len(cache))) + "\n")
