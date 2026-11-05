"""The order-1 equation of the jet continuation at a stored base, link by link, against quad-double central differences,
with the Richardson combination formed exactly (4 r(e/2) - r(e) compared with 3 x), and with anm_run --probe 2's float64
weights 4/3, -1/3 (each 2^-54 below its value) for the reproduction. Then the quad-double model's order-1 residual of z_1
solved in two arithmetic forms of the same model, horizon_alpha 0 (the chain's) and 1. Read-only; one thread.
    python exp_order1.py [STATE]"""
import glob, json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q
from multidouble import dd_add, dd_scale
from pinning import qd_axpy, band_coeffs, band_field

mp.mp.dps = 50
RAW = "/Users/nathan/Source/choptuik-large-d-raw"
state = sys.argv[1] if len(sys.argv) > 1 else "anm-mac/run_trend_pin3_qd6/anm_pin3_D82.1642.npz"
zq, m = load_q(os.path.join(RAW, state))
zq = tuple(np.ascontiguousarray(p) for p in zq)
zh, zl = zq[0].copy(), zq[1].copy()
D, M, nodes = mp.mpf(m["D_str"]), int(m["M"]), list(m["nodes"])
kt, kc, ks, kf = m["kt"], m["kc"], m["ks"], 3
mk = lambda Dx, al=0: make_solver(Dx, M, nodes=nodes, kt=kt, kc=kc, ks=ks, threads=1, kfreeze=kf, horizon_alpha=al)
c4 = lambda v: tuple(np.ascontiguousarray(np.asarray(p)) for p in v)
A = lambda p: (np.asarray(p[0]), np.asarray(p[1]))
val = lambda p: np.asarray(p[0]) + np.asarray(p[1])
sub = lambda a, b: dd_add(np.asarray(a[0]), np.asarray(a[1]), -np.asarray(b[0]), -np.asarray(b[1]))
s0 = mk(D)
segs = s0.plan(zh, zl, 1e-32, 0.05); s0.set_segs(segs)
K = len(nodes); L = len(zh); hb = K * 4 * M
rows = slice(hb, hb + M)
# the held harmonics' trend (anm_run --trend T75), for the order-1 right-hand side on the held rows
ks_held = [k for k in range(kf + 1, 14) if k % 2 == 1]
base_coeffs = band_coeffs(zh[:M], zl[:M], M, ks_held)
slopes = [[0.0, 0.0] for _ in ks_held]
ns, vals = [], []
for f in sorted(glob.glob(os.path.join(RAW, "T75", "pin*_D*.npz")))[::4]:
    dd = np.load(f); mm = json.loads(str(dd["meta"]))
    if int(mm["M"]) != M:
        continue
    ns.append(float(mm["D"]) - 2.0); vals.append(band_coeffs(dd["zh"][:M], dd["zl"][:M], M, ks_held))
ns = np.array(ns)
for i, k in enumerate(ks_held):
    for j in (0, 1):
        v = np.array([c[i][j] for c in vals])
        if len(v) >= 6 and (np.all(v > 0) or np.all(v < 0)):
            sl, c0 = np.polyfit(np.log(ns), np.log(np.abs(v)), 1)
            if float(np.max(np.abs(np.log(np.abs(v)) - (c0 + sl * np.log(ns))))) < 0.05:
                slopes[i][j] = float(sl)
n0 = float(D) - 2.0
held1 = band_field([(a * sa / n0, b * sb / n0) for (a, b), (sa, sb) in zip(base_coeffs, slopes)], ks_held, M)
print(f"base {state}: D {mp.nstr(D, 12)}, M {M}, L {L}; trend exponents {slopes}", flush=True)

def fd(along, e, al=0):
    """r(e) = (F_q(z + e v, D + e t) - F_q(z - e v, D - e t)) / (2 e) in double-double; along = (v or None, t)"""
    v, tD = along
    Ks = []
    for sg in (1.0, -1.0):
        sx = mk(D + sg * tD * mp.mpf(e), al); sx.set_segs(segs)
        zz = c4(qd_axpy(sg * e, v[0], v[1], np.zeros(L), np.zeros(L), *zq)) if v is not None else zq
        Ks.append(sx.residual_q(*zz))
    d = qd_axpy(-1.0, *c4(Ks[1]), *c4(Ks[0]))
    return dd_scale(np.asarray(d[0]), np.asarray(d[1]), 0.5 / e)

def rich_exact(along, e, al=0):
    """4 r(e/2) - r(e): three times the Richardson value, every operation exact or double-double"""
    r1, r2 = fd(along, e, al), fd(along, e / 2, al)
    return dd_add(*dd_scale(r2[0], r2[1], 4.0), -np.asarray(r1[0]), -np.asarray(r1[1])), (r1, r2)

def err_vs(x, R3):
    """x - R3 / 3 as 3 x - R3 (double-double), divided by 3 in float64 (an error, so f64 suffices)"""
    return val(sub(dd_scale(np.asarray(x[0]), np.asarray(x[1]), 3.0), R3)) / 3.0

def z1_of(al):
    s = mk(D, al); s.set_segs(segs)
    t = time.time(); s.newton(zh, zl); tn = time.time() - t
    Hs, Ls = s.residual_jet([zh], [zl], 2, 0)
    bh, bl = -np.asarray(Hs[1]), -np.asarray(Ls[1])
    bh, bl = bh.copy(), bl.copy()
    bh[rows], bl[rows] = dd_add(bh[rows], bl[rows], np.asarray(held1[0]), np.asarray(held1[1]))
    xh, xl = A(s.lu_solve(bh, bl))
    jh, jl = A(s.jvp(zh, zl, xh, xl)[:2])
    r0 = dd_add(bh, bl, -jh, -jl)
    ch, cl = A(s.lu_solve(*r0))
    xh, xl = A(dd_add(xh, xl, ch, cl))
    jh, jl = A(s.jvp(zh, zl, xh, xl)[:2])
    r1 = val(dd_add(bh, bl, -jh, -jl))
    print(f"  alpha {al}: Jacobian and LU {tn:.0f} s; jet-model order-1 residual after one refinement: max {np.abs(r1).max():.3e}", flush=True)
    return s, (xh, xl), (np.asarray(Hs[1]), np.asarray(Ls[1]))

out = {}
s_a0, z1_a0, jetD_a0 = z1_of(0)
s_a1, z1_a1, jetD_a1 = z1_of(1)
# links at the chain's z_1 (alpha 0), in both forms
jvp_a0 = A(s_a0.jvp(zh, zl, *z1_a0)[:2])
jvp_a1 = A(s_a1.jvp(zh, zl, *z1_a0)[:2])
for e in (2.0 ** -42, 2.0 ** -45):
    RD, (rD1, rD2) = rich_exact((None, 1.0), e)
    RZ, (rZ1, rZ2) = rich_exact((z1_a0, 0.0), e)
    # the probe's combination, float64 weights
    pr = lambda r1, r2: dd_add(*dd_scale(r2[0], r2[1], 4.0 / 3.0), *dd_scale(r1[0], r1[1], -1.0 / 3.0))
    eD_probe = val(sub(jetD_a0, pr(rD1, rD2))); eZ_probe = val(sub(jvp_a0, pr(rZ1, rZ2)))
    eD0, eZ0 = err_vs(jetD_a0, RD), err_vs(jvp_a0, RZ)
    eD1, eZ1 = err_vs(jetD_a1, RD), err_vs(jvp_a1, RZ)
    vD, vZ = val(RD) / 3, val(RZ) / 3
    print(f"step {e:.3e}: |dF/dD| max {np.abs(vD).max():.4e}, |J z_1| max {np.abs(vZ).max():.4e}")
    print("  row  idx  dF/dD        probe: eD/val   eZ/val      exact, alpha0: eD/val  eZ/val      sum       alpha1: eD/val  eZ/val      sum")
    for i in list(range(hb + 6, hb + 18)) + [hb + 3 * M + 31]:
        print(f"  {i:4d} {(i - hb) % M:3d}  {vD[i]:+.4e}  {eD_probe[i] / vD[i]:+.3e} {eZ_probe[i] / vZ[i]:+.3e}   "
              f"{eD0[i] / vD[i]:+.3e} {eZ0[i] / vZ[i]:+.3e} {eD0[i] + eZ0[i]:+.3e}   {eD1[i] / vD[i]:+.3e} {eZ1[i] / vZ[i]:+.3e} {eD1[i] + eZ1[i]:+.3e}")
    for name, a, b in (("probe weights", eD_probe, eZ_probe), ("exact, alpha 0", eD0, eZ0), ("exact, alpha 1", eD1, eZ1)):
        print(f"  {name}: max |eD| {np.abs(a).max():.3e}, max |eZ| {np.abs(b).max():.3e}, max |eD + eZ| {np.abs(a + b).max():.3e} (row {int(np.argmax(np.abs(a + b)))})")
    out[e] = dict(eD_probe_max=float(np.abs(eD_probe).max()), eD0_max=float(np.abs(eD0).max()), eZ0_max=float(np.abs(eZ0).max()),
                  sum0_max=float(np.abs(eD0 + eZ0).max()), eD1_max=float(np.abs(eD1).max()), eZ1_max=float(np.abs(eZ1).max()),
                  sum1_max=float(np.abs(eD1 + eZ1).max()))
# the quad-double model's order-1 residual of each z_1 (what the prediction's |F| / h measures), held slope subtracted
for name, z1 in (("alpha 0 (chain)", z1_a0), ("alpha 1", z1_a1)):
    R3, _ = rich_exact((z1, 1.0), 2.0 ** -42)
    r = val(R3) / 3.0
    r[rows] -= val(held1)
    print(f"order-1 residual in the quad-double model of z_1 from {name}: max {np.abs(r).max():.4e}, 2-norm {np.sqrt(np.sum(r * r)):.4e}, "
          f"max outside the horizon block {np.abs(r[:hb]).max():.3e}", flush=True)
    out[name] = float(np.abs(r).max())
dz = val(sub(z1_a0, z1_a1))
print(f"|z_1(alpha 0) - z_1(alpha 1)| max {np.abs(dz).max():.3e}, |z_1| max {np.abs(val(z1_a0)).max():.3e}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp_order1_" + os.path.basename(state).replace(".npz", ".json")), "w"), indent=1)
