"""Schur complement of the full system on the held coefficients at a pinned state (exploration)."""
import sys, os, json, time
HP = '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp'
sys.path.insert(0, HP)
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q, qmax, qd_axpy
from pinning import band_coeffs, band_field
mp.mp.dps = 80
raw = '/Users/nathan/Source/choptuik-large-d-raw/'
KS = [5, 7, 9, 11, 13]
st = sys.argv[1]
z, m = load_q(raw + st)
z = tuple(np.ascontiguousarray(np.asarray(p)) for p in z)
D = mp.mpf(m['D_str']) if 'D_str' in m else mp.mpf(repr(float(m['D'])))
M = int(m['M'])
mk = lambda kf: make_solver(D, M, nodes=list(m['nodes']), kt=m.get('kt', 36), kc=m.get('kc', 146), ks=m.get('ks', 130), threads=2, kfreeze=kf)
sp, sf = mk(3), mk(13)
segs = sp.plan(z[0], z[1], 1e-32, 0.05)
sp.set_segs(segs); sf.set_segs(segs)
L = len(z[0]); K = (L - 1) // (4 * M) - 1; r0 = K * 4 * M
zero = np.zeros(L)
th = [mp.pi * j / M for j in range(M)]


def proj(parts, rows):
    """band coefficients (a_k, b_k), k in KS, of the field in rows from four-part arrays, in mpmath"""
    f = [sum(mp.mpf(float(np.asarray(p)[r])) for p in parts) for r in rows]
    out = []
    for k in KS:
        a = sum(f[j] * mp.cos(k * th[j]) for j in range(M)) * 2 / M
        b = sum(f[j] * mp.sin(k * th[j]) for j in range(M)) * 2 / M
        out += [a, b]
    return out


rows = list(range(r0, r0 + M))
t0 = time.time()
out = sp.newton_q(*z)
print(f'{st}: D {mp.nstr(D, 10)}, pinned newton_q {time.time() - t0:.1f} s, piv {out[6]:.1e}..{out[7]:.1e}', flush=True)
Ff = sf.residual_q(*z)
g0 = proj(Ff, rows)
print('full residual: max', qmax(Ff[:2]), ' outside the horizon p rows', float(np.max(np.abs(np.delete(np.asarray(Ff[0]) + np.asarray(Ff[1]), rows)))))
print('g0 =', ' '.join(mp.nstr(v, 4) for v in g0))
h0 = proj(z, list(range(M)))
S = mp.matrix(10, 10)
sens = []
for i, k in enumerate(KS):
    for j, ab in enumerate([(1.0, 0.0), (0.0, 1.0)]):
        col = 2 * i + j
        fh, fl = band_field([ab], [k], M)
        ch = zero.copy(); cl = zero.copy()
        ch[r0:r0 + M] = fh; cl[r0:r0 + M] = fl
        x = sp.qlu_solve(ch, cl, zero, zero)
        x = tuple(np.ascontiguousarray(np.asarray(p)) for p in x)
        sens.append(sum(mp.mpf(float(p[-1])) for p in x))
        eps = 2.0 ** -40 / float(np.max(np.abs(x[0])))
        Fp = sf.residual_q(*qd_axpy(eps, *x, *z))
        Fm = sf.residual_q(*qd_axpy(-eps, *x, *z))
        gp, gm = proj(Fp, rows), proj(Fm, rows)
        for r in range(10):
            S[r, col] = (gp[r] - gm[r]) / (2 * mp.mpf(eps))
        # second difference: curvature check
        g2 = [(gp[r] + gm[r] - 2 * g0[r]) / mp.mpf(eps) ** 2 for r in range(10)]
        print(f'  col {k}{"ab"[j]}: eps {eps:.2e}, |dDelta/dh| {mp.nstr(sens[-1], 5)}, S col max {mp.nstr(max(abs(S[r, col]) for r in range(10)), 4)}, '
              f'2nd diff max {mp.nstr(max(abs(v) for v in g2), 3)}', flush=True)
U, sig, V = mp.svd_r(S)
print('singular values of S:', ' '.join(mp.nstr(v, 4) for v in sig))
lab = [f'{k}{c}' for k in KS for c in 'ab']
for i in range(10):
    vi = [V[i, c] for c in range(10)]
    big = sorted(range(10), key=lambda c: -abs(vi[c]))[:3]
    sv = sum(sens[c] * vi[c] for c in range(10))
    ug = sum(U[r, i] * g0[r] for r in range(10))
    print(f'  sigma {mp.nstr(sig[i], 4)}: v ~ ' + ', '.join(f'{lab[c]} {mp.nstr(vi[c], 3)}' for c in big)
          + f'; dDelta/dt along v {mp.nstr(sv, 4)}; u.g0 {mp.nstr(ug, 4)}; full step along v {mp.nstr(-ug / sig[i], 4)}, its dDelta {mp.nstr(-ug / sig[i] * sv, 4)}', flush=True)
dh = mp.lu_solve(S, mp.matrix(g0)) * -1
print('full Newton step in h:', ' '.join(mp.nstr(dh[c], 4) for c in range(10)))
print('its dDelta:', mp.nstr(sum(sens[c] * dh[c] for c in range(10)), 6))
for tau in (1e-3, 1e-6, 1e-9, 1e-12, 1e-15):
    dt = [mp.mpf(0)] * 10
    for i in range(10):
        if sig[i] > tau * sig[0]:
            ug = sum(U[r, i] * g0[r] for r in range(10))
            for c in range(10):
                dt[c] -= V[i, c] * ug / sig[i]
    print(f'  truncated at sigma > {tau:.0e} sigma_max: dDelta {mp.nstr(sum(sens[c] * dt[c] for c in range(10)), 6)}, max |dh| {mp.nstr(max(abs(v) for v in dt), 3)}')
json.dump(dict(state=st, D=str(D), S=[[str(S[r, c]) for c in range(10)] for r in range(10)], g0=[str(v) for v in g0], sens=[str(v) for v in sens],
               h0=[str(v) for v in h0]), open(f'/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/schur_{mp.nstr(D, 8)}.json', 'w'))
