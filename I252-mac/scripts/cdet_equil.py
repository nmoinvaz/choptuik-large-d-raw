"""Does exact power-of-two equilibration make the complex LU's det M orientation-independent? (#252 diagnosis; criteria
written here before the runs.)

    python cdet_equil.py HP_DIR STATE.npz KF LAM_PHYS OUT.json

At the same point as cdet_sensitivity.py (z = lam_phys + 0.2 e^{2 pi i / 20}), the complex mode matrix M is scaled
S = R M C with R, C diagonal powers of two (exact in double-double): three alternating sweeps, each row then each
column divided by the power of two nearest its largest modulus. ln det M = ln det S - sum ln R - sum ln C exactly.
modecount_cx.cdet (the LU of mode_det) on: M, M^T (as in cdet_sensitivity), S, S^T, and S with the entries' lo parts
moved by a random relative 1e-30 (two draws). Reported: |ln det| differences against M's. Reading, fixed before the
run: equilibration fixes the LU if S and S^T agree to 1e-8 in ln det (complex, arg wrapped) and S's perturbed draws
move it by at most 1e-8; then ln det S is the value to trust. Control: the same scaling of a random complex matrix
must change ln det by at most 1e-10 (the f64 summation of ln|u_kk| in clu_logdet gives about 1e-11 at n = 1536). Exit
0 when the control passes.
"""
import json
import sys
import time

import numpy as np

hp_dir, path, kf, lam, out = sys.argv[1:6]
sys.path.insert(0, hp_dir)
sys.path.insert(0, hp_dir + "/modecount_cx/build")
import modecount_common as mc  # noqa: E402
import modecount_cx  # noqa: E402

kf = None if kf == "none" else int(kf)
lam = float(lam)
st = mc.setup(path, M=None, kf=kf, fmax=1e-15)
z = lam + 0.2 * np.exp(2j * np.pi / 20)
t = time.time()
A = tuple(np.ascontiguousarray(np.asarray(a)) for a in st.c.mode_matrix(st.zh, st.zl, float(z.real), float(z.imag)))
print(f"D {st.D} M {st.M} ks {st.ks}: matrix {A[0].shape} at {z} ({time.time() - t:.0f} s)", flush=True)
rng = np.random.default_rng(2520)


def cdet(a):
    la, arg, pmin, pmax = modecount_cx.cdet(*(np.ascontiguousarray(x) for x in a))
    return complex(la, arg), pmin, pmax


def equil(a, sweeps=3):
    """S = R a C, R and C powers of two; returns S and the log of det(R) det(C)"""
    h1, l1, h2, l2 = (x.copy() for x in a)
    logs = 0.0
    for _ in range(sweeps):
        for axis in (1, 0):
            mod = np.hypot(h1, h2).max(axis=axis)
            e = -np.round(np.log2(np.where(mod > 0, mod, 1.0)))
            s = np.exp2(e)
            sh = s[:, None] if axis == 1 else s[None, :]
            h1, l1, h2, l2 = h1 * sh, l1 * sh, h2 * sh, l2 * sh
            logs += float(np.sum(e)) * np.log(2.0)
    return (h1, l1, h2, l2), logs


def perturbed(a, rel):
    h1, l1, h2, l2 = a
    return (h1, l1 + rel * np.abs(h1) * rng.standard_normal(h1.shape), h2,
            l2 + rel * np.abs(h2) * rng.standard_normal(h2.shape))


def d(x, y):
    return abs(complex(x.real - y.real, np.angle(np.exp(1j * (x.imag - y.imag)))))


def run(a, tag):
    m0 = cdet(a)
    mt = cdet(tuple(x.T for x in a))
    s, logs = equil(a)
    s0 = cdet(s)
    st_ = cdet(tuple(x.T for x in s))
    sp = [cdet(perturbed(s, 1e-30)) for _ in range(2)]
    val = s0[0] - logs
    r = dict(M=[m0[0].real, m0[0].imag, m0[1], m0[2]], MT=[mt[0].real, mt[0].imag, mt[1], mt[2]],
             S=[val.real, val.imag, s0[1], s0[2]], ST=[(st_[0] - logs).real, (st_[0] - logs).imag, st_[1], st_[2]],
             d_M_MT=d(mt[0], m0[0]), d_S_M=d(val, m0[0]), d_S_ST=d(st_[0], s0[0]),
             d_S_perturbed=[d(p[0], s0[0]) for p in sp], logscale=logs)
    print(f"  {tag}: ln det M {m0[0]:.10f} (pivots {m0[1]:.1e}..{m0[2]:.1e}); M^T off by {r['d_M_MT']:.2e}; "
          f"equilibrated S gives {val:.10f} (pivots {s0[1]:.1e}..{s0[2]:.1e}), off M by {r['d_S_M']:.2e}; S^T off S by "
          f"{r['d_S_ST']:.2e} (pivots {st_[1]:.1e}..{st_[2]:.1e}); S perturbed 1e-30: "
          f"{', '.join(f'{x:.2e}' for x in r['d_S_perturbed'])}", flush=True)
    return r


n = A[0].shape[0]
G = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
G[:, : n // 2] *= 1e6                         # badly scaled columns, so the scaling has work to do
ctl = run((G.real.copy(), np.zeros((n, n)), G.imag.copy(), np.zeros((n, n))), "control")
mode = run(A, "mode")
ok = ctl["d_S_M"] <= 1e-10
fixes = mode["d_S_ST"] <= 1e-8 and max(mode["d_S_perturbed"]) <= 1e-8
json.dump(dict(state=path, D=st.D, M=st.M, ks=st.ks, z=[z.real, z.imag], control=ctl, mode=mode,
               control_passed=bool(ok), equilibration_fixes=bool(fixes)), open(out, "w"), indent=1)
print(f"control {'passed' if ok else 'FAILED: not read'} ({ctl['d_S_M']:.1e}); equilibration "
      f"{'fixes' if fixes else 'does not fix'} the LU here", flush=True)
sys.exit(0 if ok else 1)
