"""Is the D 1000 guess's horizon gain (hprobe.py: 4e14 from m_h) the u variable's, or the map's own? (#1088, #1090)

At a form-S state z (a converged state, or form_s.py jump's guess at D), hp's horizon sum at the last node x_l is the
last node's (p, m, c) plus the horizon block of the residual (S = N + F_h; N - F_h is printed too). t2v's float64
recurrence in the Moebius variable t = (1 - z)/(1 + a z), z = x^2 (wip/large-d-inner, solver/inner_large_d/mobius_s.py,
FormS.horizon with zK = x_l^2, exact Cauchy products, kb None) gives U, V, c at x_l from Q0 = 2 m_h, so p = (U + x V)/2,
m = (U - x V)/2. Printed per a: the largest difference from hp's sum, and the complex-step derivative of (p, m, c) at
x_l along hprobe's first direction (m_h moved by |m_h| times random signs, default_rng(1)), which is hprobe's gain.
If the Moebius gain at a = 8 is near hp's, the gain is the map's own and no change of variable removes it.

    python3 mobius_gain.py T2V_DIR state STATE.npz THREADS A1,A2,..
    python3 mobius_gain.py T2V_DIR guess RAW D DEG DMAX KS THREADS A1,A2,..
"""
import glob, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
sys.path.insert(0, sys.argv[1])
import numpy as np
import mpmath as mp
import jump
from form_s import make_solver_s, a_to_s, blocks_s
from hpkernel.driver import make_solver
from octo_corrector import load_o, o8
from mobius_s import FormS

mode = sys.argv[2]
if mode == "state":
    z8, meta = load_o(sys.argv[3])
    thr, As = int(sys.argv[4]), [float(a) for a in sys.argv[5].split(",")]
    M, nodes, Dv = meta["M"], meta["nodes"], meta["D_str"]
    with mp.workdps(60):
        Dt = mp.mpf(Dv)
    s = make_solver_s(Dt, M, nodes, kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, segs=meta["segs"])
    ks = meta["ks"]
else:
    raw, Dv, deg, dmax, ks, thr = sys.argv[3], sys.argv[4], int(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
    As = [float(a) for a in sys.argv[9].split(",")]
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
    c = np.polyfit(1.0 / (Ds - 2.0), Y, deg)
    y = np.array([np.polyval(c[:, j], 1.0 / (float(Dt) - 2.0)) for j in range(Y.shape[1])])
    zA = jump.unscale(y, float(Dt), M, K)
    sa = make_solver(Dt, M, nodes=nodes, kt=36, kc=200, ks=ks, threads=thr)
    segs = sa.plan(np.ascontiguousarray(zA), np.zeros(len(zA)), 1e-40, 0.05)
    zs = a_to_s([zA], M, K)[0]
    z8 = o8([zs] + [np.zeros(len(zs))] * 7)
    s = make_solver_s(Dt, M, nodes, kt=36, kc=200, ks=ks, threads=thr, segs=segs)
K = len(nodes)
xl = float(nodes[-1])
t0 = time.time()
F = s.residual_s(list(z8))
Fv = np.asarray(F[0]) + np.asarray(F[1])
zv = np.asarray(z8[0]) + np.asarray(z8[1])
b = blocks_s(F, M, K)
print(f"D {Dv}: M {M}, K {K}, x_l {xl}, hp ks {ks}; hp's max |F| per block " + " ".join(f"{v:.2e}" for v in b)
      + f" ({time.time() - t0:.0f} s)", flush=True)
on = 2 * M + 3 * M * (K - 1)
N = zv[on:on + 3 * M]
Fh = Fv[K * 3 * M:(K + 1) * 3 * M]
mh = zv[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
Delta = zv[-1]
om = 2 * np.pi / Delta
dirn = np.abs(mh) * np.random.default_rng(1).choice([-1, 1], M)
for sgn, nm in ((1, "N + F_h"), (-1, "N - F_h")):
    S = N + sgn * Fh
    print(f"  hp's sum as {nm}: max |p| {np.abs(S[:M]).max():.4e}, |m| {np.abs(S[M:2 * M]).max():.4e}, "
          f"|c - 1| {np.abs(S[2 * M:] - 1).max():.4e}", flush=True)
for a in As:
    fs = FormS(float(Dt), M, a=a, kb=None, zK=xl * xl, ks=int(float(Dt) - 2 + 14 * np.sqrt(float(Dt) - 2) + 80))
    t0 = time.time()
    ho = fs.horizon(2.0 * mh, om)
    pv, mv = 0.5 * (ho["U"] + xl * ho["V"]), 0.5 * (ho["U"] - xl * ho["V"])
    T = np.concatenate([pv, mv, ho["c"]])
    d1, d2 = np.abs(T - (N + Fh)).max(), np.abs(T - (N - Fh)).max()
    hc = 1e-30
    hz = fs.horizon(2.0 * mh + 1j * hc * 2.0 * dirn, om + 0j)
    dp = 0.5 * (hz["U"].imag + xl * hz["V"].imag) / hc
    dm = 0.5 * (hz["U"].imag - xl * hz["V"].imag) / hc
    dc = hz["c"].imag / hc
    g = max(np.abs(dp).max(), np.abs(dm).max(), np.abs(dc).max())
    print(f"  a {a:g} (ks {fs.ks}, tail {ho['tail']:.1e}): max |p| {np.abs(pv).max():.4e}, |m| {np.abs(mv).max():.4e}, "
          f"|c - 1| {np.abs(ho['c'] - 1).max():.4e}; differs from the last node by {np.abs(T - N).max():.2e} "
          f"(p {np.abs(T - N)[:M].max():.2e}, m {np.abs(T - N)[M:2 * M].max():.2e}, c {np.abs(T - N)[2 * M:].max():.2e}), "
          f"from hp's N + F_h by {d1:.2e}, N - F_h by {d2:.2e}; "
          f"gain from m_h {g:.3e} ({time.time() - t0:.0f} s)", flush=True)
