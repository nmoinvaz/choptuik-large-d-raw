"""Non-smooth error in the entries of the complex mode matrix (#252 diagnosis; criteria written here before the runs).

    python matrix_noise.py HP_DIR STATE.npz KF LAM_PHYS OUT.json [--ks=N]

--ks=N builds the solvers with horizon order N instead of the state's (the state is not re-converged: this measures
only how the entries' error depends on ks; same reading as below).

At z = lam_phys + 0.2 e^{2 pi i / 20} (the lambda_phys circle's second base point) the complex mode matrix (modecount_cx
mode_matrix, double-double) at z, z + d, z + 2d for d = 2^-40 (9.1e-13) and d = 2^-46 (1.4e-14), steps that are exact in f64 at Re z in [2, 4) (ulp
2^-51), so the points are equally spaced. The second difference
D2 = M(z + 2d) - 2 M(z + d) + M(z), formed in double-double, is d^2 M'' (smooth, falls 4096 times from the first d to the
second) plus the entries' non-smooth error (does not fall). Reported per row block (centre, segments, horizon): max
|D2| / max |M| for both d, and the ratio of the two. Reading, fixed before the run: a block whose relative D2 is the same
at both d (ratio below 10) and above 1e-30 carries non-smooth error above double-double rounding (2^-106 = 1.2e-32), of
that size. Run at D 61 M 64 and, as the reference, D 61 M 48 (whose circles located lambda_phys to 5.5e-7).
"""
import json
import sys
import time

import numpy as np

hp_dir, path, kf, lam, out = sys.argv[1:6]
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

kf = None if kf == "none" else int(kf)
lam = float(lam)
ks_opt = next((int(a.split("=")[1]) for a in sys.argv[6:] if a.startswith("--ks=")), None)
if ks_opt is None:
    st = mc.setup(path, M=None, kf=kf, fmax=1e-15)
else:
    from hpkernel.driver import load
    zh0, zl0, meta0 = load(path)
    meta0 = dict(meta0, ks=ks_opt)

    class St:
        pass
    st = St()
    st.s, st.c = mc.build_pair(meta0, zh0, zl0, meta0["M"], kf)
    st.zh, st.zl = np.ascontiguousarray(zh0), np.ascontiguousarray(zl0)
    st.M, st.K, st.D, st.ks = meta0["M"], len(meta0["nodes"]), meta0["D"], ks_opt
    print(f"ks {ks_opt} instead of the state's; |F| in this layout {mc.resid(st.s, st.zh, st.zl):.1e}", flush=True)
M, K = st.M, st.K
z = lam + 0.2 * np.exp(2j * np.pi / 20)


def mat(w):
    t = time.time()
    a = tuple(np.asarray(x) for x in st.c.mode_matrix(st.zh, st.zl, float(w.real), float(w.imag)))
    print(f"  matrix at {w!r} ({time.time() - t:.0f} s)", flush=True)
    return a


def d2(a0, a1, a2):
    """second difference in double-double: hi parts by exact differences, then the lo parts"""
    re = ((a2[0] - a1[0]) - (a1[0] - a0[0])) + ((a2[1] - a1[1]) - (a1[1] - a0[1]))
    im = ((a2[2] - a1[2]) - (a1[2] - a0[2])) + ((a2[3] - a1[3]) - (a1[3] - a0[3]))
    return np.hypot(re, im)


m0 = mat(z)
res = {}
D1, D2_ = 2.0 ** -40, 2.0 ** -46
assert 2 <= z.real < 4
for d in (D1, D2_):
    res[d] = d2(m0, mat(z + d), mat(z + 2 * d))
mag = np.hypot(m0[0], m0[2])
n = mag.shape[0]
blk = 4 * M
names = ["centre"] + [f"seg {b}" for b in range(1, K)] + ["horizon"]
rows = []
print(f"D {st.D} M {M} ks {st.ks} at {z}", flush=True)
for b in range((n + blk - 1) // blk):
    r0, r1 = b * blk, min((b + 1) * blk, n)
    big = float(mag[r0:r1].max())
    rel = {d: float(res[d][r0:r1].max()) / big for d in res}
    rel[1e-12], rel[1e-14] = rel[D1], rel[D2_]
    rows.append(dict(block=names[b] if b < len(names) else f"block {b}", max_abs=big, rel_d12=rel[1e-12],
                     rel_d14=rel[1e-14], ratio=rel[1e-12] / max(rel[1e-14], 1e-300)))
    print(f"  {rows[-1]['block']:>8s}: max |M| {big:.2e}; max |D2| / max |M|: d 2^-40 {rel[1e-12]:.2e}, d 2^-46 "
          f"{rel[1e-14]:.2e} (ratio {rows[-1]['ratio']:.1f})", flush=True)
json.dump(dict(state=path, D=st.D, M=M, ks=st.ks, z=[z.real, z.imag], rows=rows), open(out, "w"), indent=1)
