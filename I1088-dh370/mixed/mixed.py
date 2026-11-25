"""Speed probes of form S at a converged held state (#1088).

tangents: the octo-double Jacobian (jacobian_s at eight parts) with 1 and 2 columns per evaluation (form_s.rs
    jacobian_s_o has those two; 4 and 8 are not wired for form S), its time and whether the two agree bit for bit.
mixed: from the rescaled guess at the state's D (form_s.py jump's fit), the iteration z -= J^-1 F with F the
    octo-double residual of the held system (form_s.HeldS) and J the leading part of the double-double Jacobian of form
    S (jacobian_s at two parts, rounded to f64), factored once in f64 (scipy lu_factor); --scale 1.01 multiplies J by
    1.01 (the control, which must contract visibly worse). Prints max |F| and the digits gained per step, and the times.

    python3 mixed.py tangents STATE.npz THREADS
    python3 mixed.py mixed STATE.npz THREADS RAW DMAX DEG [SCALE] [STEPS]
"""
import glob, sys, time
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-1088a/hp")
import numpy as np
import mpmath as mp
import scipy.linalg as sl
import jump
from form_s import make_solver_s, HeldS, held_field, a_to_s
from hpkernel.driver import make_solver
from octo_corrector import load_o, o8
from multidouble import od_axpy

cmd, path, thr = sys.argv[1], sys.argv[2], int(sys.argv[3])
z8, meta = load_o(path)
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, segs=meta["segs"])
s3 = make_solver_s(D, M, nodes, kfreeze=3, **kw)
L = s3.size_s
print(f"D {meta['D']}: form S, L {L} (form A {4 * M * (K + 1) + 1}), ks {meta['ks']}, kc {meta['kc']}, "
      f"{sum(len(g) - 1 for g in meta['segs'])} Taylor steps, {thr} threads", flush=True)
z = [np.ascontiguousarray(p) for p in z8]
if cmd == "tangents":
    out = {}
    for tan in (1, 2):
        t0 = time.time()
        J = s3.jacobian_s(z, tangents=tan)
        out[tan] = [np.asarray(p) for p in J]
        print(f"  octo-double Jacobian, {tan} tangent(s) per evaluation: {time.time() - t0:.1f} s", flush=True)
    same = all(np.array_equal(a, b) for a, b in zip(out[1], out[2]))
    print(f"  1 and 2 tangents: {'the same bits' if same else 'DIFFERENT bits'}", flush=True)
    t0 = time.time()
    s3.jacobian_s(z[:2])
    print(f"  double-double Jacobian: {time.time() - t0:.1f} s", flush=True)
    t0 = time.time()
    s3.residual_s(z)
    print(f"  octo-double residual: {time.time() - t0:.1f} s", flush=True)
    sys.exit(0)
# mixed
raw, dmax, deg = sys.argv[4], float(sys.argv[5]), int(sys.argv[6])
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
steps = int(sys.argv[8]) if len(sys.argv) > 8 else 8
paths = sorted(glob.glob(raw + "/I903-macm3/chain_k135/anm_pin3_D*.npz") + glob.glob(raw + "/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz"))
rows = []
for p in paths:
    zz, m = load_o(p)
    if 226 <= m["D"] <= dmax:
        rows.append((m["D"], zz))
rows.sort(key=lambda r: r[0])
Ds = np.array([r[0] for r in rows])
Y = np.array([jump.scale(sum(np.asarray(p) for p in r[1][:2]), r[0], M, K) for r in rows])
c = np.polyfit(1.0 / (Ds - 2.0), Y, deg)
y = np.array([np.polyval(c[:, j], 1.0 / (float(D) - 2.0)) for j in range(Y.shape[1])])
zA = jump.unscale(y, float(D), M, K)
g = [a_to_s([zA], M, K)[0]] + [np.zeros(L) for _ in range(7)]
sd = jump.series_delta(meta["D_str"]) or jump.series_delta(str(int(round(float(D)))))
with mp.workdps(60):
    v = mp.mpf(sd[0])
    for q in range(8):
        f = float(v)
        g[q][-1] = f
        v -= mp.mpf(f)
g = o8(g)
sh = HeldS(s3, M, K, held_field(g, M))
t0 = time.time()
Jd = s3.jacobian_s([np.ascontiguousarray(g[0]), np.ascontiguousarray(g[1])])
J = np.asarray(Jd[0]) * scale
tj = time.time() - t0
t0 = time.time()
lu = sl.lu_factor(J)
tf = time.time() - t0
print(f"  guess from {len(rows)} states (degree {deg}); double-double Jacobian at the guess {tj:.1f} s, its f64 LU "
      f"{tf:.2f} s; J scaled by {scale}", flush=True)
F = sh.residual_s(list(g))
nF = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
print(f"  step 0: max |F| {nF:.3e}", flush=True)
zero = np.zeros(L)
for it in range(1, steps + 1):
    t0 = time.time()
    Fv = np.asarray(F[0]) + np.asarray(F[1])
    dz = sl.lu_solve(lu, -Fv)
    g = o8(od_axpy(1.0, np.ascontiguousarray(dz), *([zero] * 7), *g))
    F = sh.residual_s(list(g))
    nF1 = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
    print(f"  step {it}: max |F| {nF1:.3e}, digits gained {np.log10(nF / nF1) if nF1 > 0 else float('inf'):.2f}, "
          f"|dz| {np.abs(dz).max():.2e}, {time.time() - t0:.1f} s", flush=True)
    nF = nF1
