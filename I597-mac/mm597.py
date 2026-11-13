#!/usr/bin/env python3
"""#597: dump modecount_cx's complex mode matrix and det on one build, and compare two dumps entry by entry.

    cd hp && python3 mm597.py dump OUT.npz STATE M KF|none RE,IM [RE,IM ...]    (the build on PYTHONPATH)
    python3 mm597.py compare A.npz B.npz [--rows=HORIZON_P]                       (no build needed)

dump: modecount_common.setup (threads 4, fmax 1e-15, as hp/modecount_smooth.py) and, at each lambda, CSolver.mode_matrix
(re_hi, re_lo, im_hi, im_lo) and CSolver.mode_det; also the module file it ran.
compare: per lambda, the entries whose four parts are not bit for bit equal, by (row block, column block) of 4M, the
largest |A - B| / max |A| and / |A| of the entry, and the dets' four floats side by side. --rows=HORIZON_P also counts
the differing entries outside the horizon block's p rows (rows 4MK .. 4MK + M), where the frozen rows sit.
"""
import os
import sys

import numpy as np


def dump(out, path, M, kf, lams):
    sys.path.insert(0, os.getcwd())
    from modecount_common import setup
    import modecount_cx
    st = setup(path, M=M, threads=4, kf=kf, fmax=1e-15, log=lambda *a: None)
    d = dict(M=st.M, K=st.K, kf=-1 if st.kf is None else st.kf, F=st.F, module=modecount_cx.__file__,
             lams=np.array(lams))
    for i, (re_, im_) in enumerate(lams):
        rh, rl, ih, il = (np.asarray(a) for a in st.c.mode_matrix(st.zh, st.zl, re_, im_))
        d[f"A{i}"] = np.stack([rh, rl, ih, il])
        d[f"det{i}"] = np.array(st.c.mode_det(st.zh, st.zl, re_, im_))
        print(f"lambda {re_}{im_:+}i: det {tuple(d[f'det{i}'])}", flush=True)
    np.savez(out, **d)
    print(f"{out}: M {st.M}, K {st.K}, kf {st.kf}, |F| {st.F:.1e}, module {modecount_cx.__file__}")


def compare(fa, fb, horizon_p):
    a, b = np.load(fa), np.load(fb)
    M, K = int(a["M"]), int(a["K"])
    blk = 4 * M
    print(f"A {fa} ({a['module']})\nB {fb} ({b['module']})\nM {M}, K {K}, kf {int(a['kf'])}")
    worst = 0
    for i, (re_, im_) in enumerate(a["lams"]):
        A, B = a[f"A{i}"], b[f"A{i}"]
        ne = np.any(A.view(np.uint64) != B.view(np.uint64), axis=0)
        n = ne.shape[0]
        va = (A[0] + A[1]) + 1j * (A[2] + A[3])
        dv = ((B[0] - A[0]) + (B[1] - A[1])) + 1j * ((B[2] - A[2]) + (B[3] - A[3]))
        top = np.abs(va).max()
        rel = np.abs(dv) / np.maximum(np.abs(va), 1e-300)
        print(f"lambda {re_}{im_:+}i: {int(ne.sum())} of {n * n} entries differ; max |dA| / max |A| "
              f"{np.abs(dv).max() / top:.2e}, max |dA| / |A| {rel[ne].max() if ne.any() else 0:.2e}")
        if ne.any():
            r, c = np.nonzero(ne)
            nb = (n + blk - 1) // blk
            joint = np.zeros((nb, nb), dtype=int)
            np.add.at(joint, (r // blk, c // blk), 1)
            for row in joint:
                print("    " + " ".join(f"{x:7d}" for x in row))
            if horizon_p:
                hp0 = blk * K
                out = int(np.sum((r < hp0) | (r >= hp0 + M)))
                print(f"  outside the horizon block's p rows ({hp0}..{hp0 + M - 1}): {out}")
                worst = max(worst, out)
        da, db = a[f"det{i}"], b[f"det{i}"]
        same = bool(np.all(da.view(np.uint64) == db.view(np.uint64)))
        print(f"  det A {tuple(float(x) for x in da)}\n  det B {tuple(float(x) for x in db)}  "
              f"{'bit for bit equal' if same else 'differ: d ln|det| %+.2e, d arg %+.2e' % (db[0] - da[0], np.angle(np.exp(1j * (db[1] - da[1]))))}")
        worst = max(worst, int(ne.sum()) if not horizon_p else 0, 0 if same or horizon_p else 1)
    return worst


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        out, path, M, kf = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
        lams = [tuple(float(x) for x in s.split(",")) for s in sys.argv[6:]]
        dump(out, path, M, None if kf == "none" else int(kf), lams)
    else:
        hp_rows = "--rows=HORIZON_P" in sys.argv
        files = [x for x in sys.argv[2:] if not x.startswith("--")]
        w = compare(files[0], files[1], hp_rows)
        # exit 1 if anything differs (or, with --rows=HORIZON_P, anything outside the frozen rows)
        sys.exit(1 if w else 0)
