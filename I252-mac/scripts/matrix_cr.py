"""Where the complex path of modecount_cx departs from analyticity (#252 diagnosis; README "Matrix check").

    python matrix_cr.py HP_DIR STATE.npz KF X0 OUT.json [--eps=1e-9]

Builds the complex mode matrix M (modecount_cx.CSolver.mode_matrix, double-double, no LU) at x0, x0 + eps and
x0 + i eps. Every entry is analytic in lambda, so dC = M(x0 + i eps) - M(x0) must equal i dR, dR = M(x0 + eps) - M(x0),
up to O(eps^2). Reports, per row block (centre series, segments, horizon) and field (p, m, a, c), the largest |dC - i dR|
against the largest |dR|, and the entries where the departure is largest (row, column). Passes (analytic to
eps * 1e-6) when max |dC - i dR| <= 1e-6 max |dR|. Exit 0 on pass, 1 on fail.
"""
import json
import sys
import time

import numpy as np

hp_dir, path, kf, x0, out = sys.argv[1:6]
eps = float(next((a.split("=")[1] for a in sys.argv[6:] if a.startswith("--eps=")), 1e-9))
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

kf = None if kf == "none" else int(kf)
x0 = float(x0)
st = mc.setup(path, M=None, kf=kf, fmax=1e-15)
M, K = st.M, st.K
print(f"D {st.D} M {M} K {K} ks {st.ks} kf {st.kf}", flush=True)


def mat(lr, li):
    t = time.time()
    rh, rl, ih, il = st.c.mode_matrix(st.zh, st.zl, lr, li)
    A = (np.asarray(rh) + np.asarray(rl)) + 1j * (np.asarray(ih) + np.asarray(il))
    # the lo parts matter at eps = 1e-9: keep the difference in two pieces
    print(f"  matrix at {lr} + {li}i: {A.shape} ({time.time() - t:.0f} s)", flush=True)
    return np.asarray(rh), np.asarray(rl), np.asarray(ih), np.asarray(il)


m0, mr, mi = mat(x0, 0.0), mat(x0 + eps, 0.0), mat(x0, eps)


def diff(a, b):
    """a - b for (rh, rl, ih, il) tuples, hi and lo differences summed after subtracting (exact enough here)"""
    return ((a[0] - b[0]) + (a[1] - b[1])) + 1j * ((a[2] - b[2]) + (a[3] - b[3]))


dR, dC = diff(mr, m0), diff(mi, m0)
E = np.abs(dC - 1j * dR)
scale = np.abs(dR).max()
n = E.shape[0]
blk = 4 * M
names = ["centre"] + [f"seg {b}" for b in range(1, K)] + ["horizon"]
rows = []
for b in range((n + blk - 1) // blk):
    for q in range(4):
        r0, r1 = b * blk + q * M, min(b * blk + (q + 1) * M, n)
        if r0 >= n:
            continue
        e = float(E[r0:r1].max())
        d = float(np.abs(dR[r0:r1]).max())
        rows.append(dict(block=names[b] if b < len(names) else f"block {b}", field="pmac"[q], max_dev=e, max_dR=d))
        print(f"  rows {names[b] if b < len(names) else b:>8s} {'pmac'[q]}: max |dC - i dR| {e:.2e}, max |dR| {d:.2e}",
              flush=True)
top = np.dstack(np.unravel_index(np.argsort(-E.ravel())[:12], E.shape))[0]
worst = [dict(row=int(i), col=int(j), dev=float(E[i, j]), dR=abs(complex(dR[i, j])), dC=abs(complex(dC[i, j])))
         for i, j in top]
for w in worst:
    print(f"  entry ({w['row']}, {w['col']}): |dC - i dR| {w['dev']:.2e}, |dR| {w['dR']:.2e}, |dC| {w['dC']:.2e}",
          flush=True)
ok = bool(float(E.max()) <= 1e-6 * float(scale))
json.dump(dict(state=path, D=st.D, M=M, K=K, ks=st.ks, x0=x0, eps=eps, n=n, max_dev=float(E.max()), max_dR=scale,
               rows=rows, worst=worst, passed=ok), open(out, "w"), indent=1)
print(f"max |dC - i dR| = {E.max():.2e} against max |dR| = {scale:.2e} -> {'PASS' if ok else 'FAIL'}", flush=True)
sys.exit(0 if ok else 1)
