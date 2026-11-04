"""Two-stage jump. Stage 'pin': the pinned quad-double Newton (kfreeze K, p1's harmonics above K up to 13 held at
the guess's values; pinning.PinnedQ as hp/full_release.py builds it) from the guess. Stage 'release': the full
system (kfreeze 13) newton_qd from a four-part state. Both report the distance to the truth state if one exists.
Usage: b_pinned.py pin D GUESS.npz K [it]  |  b_pinned.py release D STATE.npz [it]"""
import sys, time, json
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/hp')
import numpy as np
from hpkernel.driver import make_solver, newton_qd, load_q, qmax, qd_axpy, qparts
from pinning import PinnedQ, PinnedSolver, band_coeffs, band_field
from b_lib import TRUTH, T, LABELS
mode, Dt, gp = sys.argv[1], float(sys.argv[2]), sys.argv[3]
M = 32
truth = load_q(TRUTH[Dt]) if Dt in TRUTH else None
Dv = (truth[1].get('D_str') or float(truth[1]['D'])) if truth else Dt
G = np.load(gp)
z = qparts(G['g'], np.zeros(769)) if 'g' in G else tuple(np.ascontiguousarray(G[k]) for k in ('zh', 'zl', 'z2', 'z3'))
if 'Delta_series' in sys.argv:
    import mpmath as mp
    mp.mp.dps = 80
    v = mp.mpf(json.load(open('series.json'))['fits']['1/D 20'][str(Dt)])
    z = tuple(np.array(a, dtype=float) for a in z)
    for i in range(4):
        p = float(v); z[i][-1] = p; v -= p
    z = tuple(np.ascontiguousarray(a) for a in z)
def dist(z):
    if truth is None:
        return float('nan'), float('nan'), float('nan')
    d = qd_axpy(-1.0, *truth[0], *z); dv = np.asarray(d[0]) + np.asarray(d[1])
    return np.abs(dv[:-1]).max(), np.abs(dv[704:768]).max(), dv[-1]
t0 = time.time()
if mode == 'pin':
    K = int(sys.argv[4]); it = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5].isdigit() else 8
    s = make_solver(Dv, M, nodes=[0.3, 0.4, 0.5, 0.6, 0.7], kt=36, kc=146, ks=130, threads=1, kfreeze=K)
    s.set_segs(s.plan(np.asarray(z[0]), np.asarray(z[1]), 1e-32, 0.05))
    ks_held = [k for k in range(K + 2, 14, 2)]
    hh, hl = band_field(band_coeffs(np.asarray(z[0])[:M], np.asarray(z[1])[:M], M, ks_held), ks_held, M)
    ps = PinnedSolver(s, M, hh, hl); sq = PinnedQ(s, ps.ch, ps.cl)
    tol = 1e-40
else:
    it = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 8
    sq = make_solver(Dv, M, nodes=[0.3, 0.4, 0.5, 0.6, 0.7], kt=36, kc=146, ks=130, threads=1, kfreeze=13)
    sq.set_segs(sq.plan(np.asarray(z[0]), np.asarray(z[1]), 1e-32, 0.05))
    tol = 1e-40
e = dist(z)
print(f'{mode} D {Dt} from {gp}: |F| {qmax(sq.residual_q(*z)):.2e}; start - truth: max {e[0]:.2e}, horizon data {e[1]:.2e}, Delta {e[2]:+.2e}', flush=True)
zn, hist, conv = newton_qd(sq, z, tol=tol, it_max=it, max_halvings=3, verbose=True)
e = dist(zn)
print(f'  {mode}: {"converged" if conv else "NOT converged"} in {len(hist)} records, {time.time()-t0:.0f} s; first step |dz| {hist[0]["dz"]:.2e}; '
      f'end - truth: max {e[0]:.2e}, horizon data {e[1]:.2e}, Delta {e[2]:+.2e}', flush=True)
out = gp.replace('.npz', f'_{mode}{sys.argv[4] if mode == "pin" else ""}{"_sD" if "Delta_series" in sys.argv else ""}.npz')
np.savez(out, zh=zn[0], zl=zn[1], z2=zn[2], z3=zn[3], conv=conv)
print('  saved', out, flush=True)
