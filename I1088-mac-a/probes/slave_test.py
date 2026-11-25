"""Lead (a) of #1089 slice 3 on the jump: a_h slaved to m_h by the momentum constraint (jump.slave_ah).
(1) On a converged state: the slaved a_h against the stored one, max|diff| / max|a_h - 1|; with --mutate=sign the
    sign of omega is flipped, and the two must then differ by O(1).
(2) On a guess (or any eight-part file): a_h replaced by the slaved one, the u0 rung's |R| with the guess's own m_h,
    then the u0 rung's Newton (OLadder.rung, octo-double block LU) from those data, no inner rungs.

    python3 slave_test.py STATE.npz GUESS.npz [--mutate=sign]
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
import jump
from jump import OLadder, D_mp, slave_ah
from octo_corrector import load_o, o8

mut = any(a == "--mutate=sign" for a in sys.argv)
files = [a for a in sys.argv[1:] if not a.startswith("--")]
for k, path in enumerate(files):
    z, meta = load_o(path)
    D = D_mp(meta)
    M, K = meta["M"], len(meta["nodes"])
    o = 2 * M + 4 * M * K
    zz = [np.array(p) for p in z]
    if mut:
        for p in zz:
            p[-1] = -p[-1]
    t = time.time()
    ah = slave_ah(zz, M, K, D)
    with mp.workdps(60):
        diff = max(abs(mp.fsum(mp.mpf(float(a[j])) for a in ah) - mp.fsum(mp.mpf(float(np.asarray(p)[o + M + j])) for p in z))
                   for j in range(M))
        am1 = max(abs(mp.fsum(mp.mpf(float(np.asarray(p)[o + M + j])) for p in z) - 1) for j in range(M))
    print(f"{path.split('/')[-1]}: D {meta['D']:.4f}, slaved a_h against its own: max|diff| {mp.nstr(diff, 3)}, "
          f"/ max|a_h - 1| = {mp.nstr(diff / am1, 3)}{' (omega sign flipped)' if mut else ''} ({time.time() - t:.1f} s)", flush=True)
    if k == 0 or mut:
        continue
    lad = OLadder(meta, D, threads=2)
    nk = lad.rs.off["node"](K - 1)
    sl_ = slice(lad.rs.off["mh"], lad.rs.off["mh"] + 2 * M)
    zs = [np.array(p) for p in z]
    for q in range(8):
        zs[q][o + M:o + 2 * M] = ah[q]
    target = [np.array(np.asarray(p)[nk:nk + 4 * M]) for p in zs]
    d0 = [np.ascontiguousarray(np.array(p[sl_])) for p in zs]
    dz = [np.ascontiguousarray(np.array(np.asarray(p)[sl_])) for p in z]
    for name, d in (("own a_h", dz), ("slaved a_h", d0)):
        t = time.time()
        dn, h, ok = lad.rung(lad.us[-1], zs, target, d)
        print(f"  u0 rung from the guess's m_h and {name}: |R| " + " -> ".join(f"{x:.2e}" for x in h) +
              f" ({'converged' if ok else 'not converged'}, {time.time() - t:.0f} s)", flush=True)
