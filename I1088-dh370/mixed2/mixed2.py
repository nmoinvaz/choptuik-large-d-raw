"""Newton on form S's held system (#1088) with the Jacobian in double-double, refreshed at every step, and the residual
in octo-double: z -= J_dd(z)^-1 F_od(z), J from jacobian_s at the state's leading two parts, solved by multidouble's
dd_solve (LU with partial pivoting in double-double) or, with SOLVE=f64, by scipy's f64 LU of J's leading part.
From the rescaled guess at the state's D (mixed.py's fit, the same 50 states and degree), so the held values and the
solution are the octo-double jump's; the end state's Delta is compared with that stored solution's.

    python3 mixed2.py STATE.npz THREADS RAW DMAX DEG SOLVE SCALE STEPS TOL [JPREC] [CHORD]

SOLVE: dd or f64. SCALE multiplies J (the control: 1.01 must turn quadratic convergence into linear at about 1e-2).
JPREC: the Jacobian's precision, dd (2 parts, the default), qd (4) or od (8), its leading two parts used by the solve.
CHORD 1: the Jacobian of the first step reused at every step (one Jacobian in all).
"""
import glob, sys, time
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-1088a/hp")
import numpy as np
import mpmath as mp
import scipy.linalg as sl
import jump
from form_s import make_solver_s, HeldS, held_field, a_to_s
from octo_corrector import load_o, o8, delta_digits
from multidouble import od_axpy, dd_solve

path, thr, raw, dmax, deg = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
solve, scale, steps, tol = sys.argv[6], float(sys.argv[7]), int(sys.argv[8]), float(sys.argv[9])
jprec = sys.argv[10] if len(sys.argv) > 10 else "dd"
chord = int(sys.argv[11]) if len(sys.argv) > 11 else 0
nparts = {"dd": 2, "qd": 4, "od": 8}[jprec]
z8s, meta = load_o(path)
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
kw = dict(kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, segs=meta["segs"])
s3 = make_solver_s(D, M, nodes, kfreeze=3, **kw)
L = s3.size_s
print(f"D {meta['D']}: form S, L {L}, ks {meta['ks']}, kc {meta['kc']}, {thr} threads; J in {jprec} "
      f"{'once (chord)' if chord else 'at every step'}, solve {solve}, J scaled by {scale}", flush=True)
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
F = sh.residual_s(list(g))
nF = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
print(f"  guess from {len(rows)} states (degree {deg}); step 0: max |F| {nF:.3e}", flush=True)
zero = np.zeros(L)
t_all = time.time()
for it in range(1, steps + 1):
    if nF <= tol:
        break
    t0 = time.time()
    if not (chord and it > 1):
        Jd = s3.jacobian_s([np.ascontiguousarray(g[q]) for q in range(nparts)])
        Jh, Jl = np.asarray(Jd[0]) * scale, np.asarray(Jd[1]) * scale
    tj = time.time() - t0
    t0 = time.time()
    Fh, Fl = np.asarray(F[0]), np.asarray(F[1])
    if solve == "dd":
        dh, dl = dd_solve(np.ascontiguousarray(Jh), np.ascontiguousarray(Jl), np.ascontiguousarray(-Fh), np.ascontiguousarray(-Fl))
        dh, dl = np.asarray(dh), np.asarray(dl)
    else:
        dh, dl = sl.lu_solve(sl.lu_factor(Jh), -(Fh + Fl)), zero
    ts = time.time() - t0
    t0 = time.time()
    g = o8(od_axpy(1.0, np.ascontiguousarray(dh), np.ascontiguousarray(dl), *([zero] * 6), *g))
    F = sh.residual_s(list(g))
    nF1 = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
    tr = time.time() - t0
    print(f"  step {it}: max |F| {nF1:.3e}, digits gained {np.log10(nF / nF1) if nF1 > 0 else float('inf'):.2f}, "
          f"|dz| {np.abs(dh).max():.2e}; J {tj:.1f} s, solve {ts:.1f} s, residual {tr:.1f} s", flush=True)
    nF = nF1
print(f"  end: max |F| {nF:.3e} after {time.time() - t_all:.0f} s; Delta {delta_digits(g, 40)}", flush=True)
dD = [np.asarray(a)[-1] for a in g]
dS = [np.asarray(a)[-1] for a in z8s]
with mp.workdps(140):
    diff = sum(mp.mpf(float(x)) for x in dD) - sum(mp.mpf(float(x)) for x in dS)
    zdiff = max(abs(float(sum(mp.mpf(float(np.asarray(a)[i])) for a in g) - sum(mp.mpf(float(np.asarray(b)[i])) for b in z8s)))
                for i in range(0, L, max(1, L // 64)))
print(f"  against the octo-double jump's stored solution: Delta difference {mp.nstr(diff, 3)}, max |z difference| "
      f"over 64 sampled entries {zdiff:.2e}", flush=True)
