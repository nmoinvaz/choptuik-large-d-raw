"""Why does form S's horizon block read 0.4 at the D 1000 guess? The guess of form_s.py jump (the same fit), its
horizon block's max |F| at several ks, and that block's response to m_h moved by eps (relative, random signs, seed 1),
whose ratio to eps is the block's gain from m_h: an O(1) gain says the 0.4 is the guess's own error, a gain far above
1 says the horizon series amplifies its data (the affine variable's recurrence, #1090).

    python3 hprobe.py RAW D DEG DMAX KS1,KS2,... EPS1,EPS2,...
"""
import glob, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
import jump
from form_s import make_solver_s, a_to_s, blocks_s
from hpkernel.driver import make_solver
from octo_corrector import load_o, o8
from multidouble import od_axpy

raw, Dv, deg, dmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
kss = [int(x) for x in sys.argv[5].split(",")]
epss = [float(x) for x in sys.argv[6].split(",")]
paths = sorted(glob.glob(raw + "/I903-macm3/chain_k135/anm_pin3_D*.npz") + glob.glob(raw + "/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz"))
rows = []
for p in paths:
    z, m = load_o(p)
    if 226 <= m["D"] <= dmax:
        rows.append((m["D"], z, m))
rows.sort(key=lambda r: r[0])
M, nodes = 32, rows[-1][2]["nodes"]
K = len(nodes)
Ds = np.array([r[0] for r in rows])
Y = np.array([jump.scale(sum(np.asarray(p) for p in r[1][:2]), r[0], M, K) for r in rows])
with mp.workdps(60):
    Dt = mp.mpf(Dv)
t = 1.0 / (Ds - 2.0)
c = np.polyfit(t, Y, deg)
y = np.array([np.polyval(c[:, j], 1.0 / (float(Dt) - 2.0)) for j in range(Y.shape[1])])
zA = jump.unscale(y, float(Dt), M, K)
sa = make_solver(Dt, M, nodes=nodes, kt=36, kc=200, ks=kss[0], threads=2)
segs = sa.plan(np.ascontiguousarray(zA), np.zeros(len(zA)), 1e-40, 0.05)
zs = a_to_s([zA], M, K)[0]
z8 = o8([zs] + [np.zeros(len(zs))] * 7)
print(f"D {Dv}: {len(rows)} states to {dmax}, degree {deg}, {sum(len(g) - 1 for g in segs)} Taylor steps", flush=True)
for ks in kss:
    s = make_solver_s(Dt, M, nodes, kt=36, kc=200, ks=ks, threads=2, segs=segs)
    t0 = time.time()
    F = s.residual_s(list(z8))
    b = blocks_s(F, M, K)
    print(f"  ks {ks}: max |F| per block " + " ".join(f"{x:.2e}" for x in b) + f" ({time.time() - t0:.1f} s)", flush=True)
    Fh = (np.asarray(F[0]) + np.asarray(F[1]))[K * 3 * M:(K + 1) * 3 * M]
    o = 2 * M + 3 * M * K
    rng = np.random.default_rng(1)
    for eps in epss:
        pert = np.zeros(len(zs))
        pert[o:o + M] = eps * np.abs(zs[o:o + M]) * rng.choice([-1, 1], M)
        zp = o8(od_axpy(1.0, pert, *([np.zeros(len(zs))] * 7), *z8))
        Fp = s.residual_s(list(zp))
        dF = (np.asarray(Fp[0]) + np.asarray(Fp[1]))[K * 3 * M:(K + 1) * 3 * M] - Fh
        print(f"    m_h moved by {eps:.0e}: the horizon block moves by {np.abs(dF).max():.2e}, gain {np.abs(dF).max() / eps:.2e}", flush=True)
