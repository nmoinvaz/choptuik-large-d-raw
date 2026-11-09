"""How much the double-double complex LU's rounding moves ln det M (#252 diagnosis; criteria written here before the runs).

    python cdet_sensitivity.py HP_DIR STATE.npz KF LAM_PHYS OUT.json

The complex mode matrix M at z = lam_phys + 0.2 e^{2 pi i / 20} (the lambda_phys circle's second base point) from
modecount_cx's mode_matrix, and modecount_cx.cdet (multidouble's clu_logdet, the LU that mode_det uses) on:
  M itself; its transpose (the same determinant, other rounding); M with every entry's lo part moved by a random
  relative 1e-30 (three draws, below the matrix's own double-double accuracy).
The spread of ln det over these is the LU's rounding noise at this point. Control: a random complex matrix of the same
size with entries of order one (well conditioned), whose transpose and perturbations must agree to 1e-20 in ln det; if
they do not, the test is not read. Exit 0 when the control passes (the measurement is the output, not a pass/fail).
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
rh, rl, ih, il = (np.ascontiguousarray(np.asarray(a)) for a in st.c.mode_matrix(st.zh, st.zl, float(z.real), float(z.imag)))
print(f"D {st.D} M {st.M} ks {st.ks}: matrix {rh.shape} at {z} ({time.time() - t:.0f} s)", flush=True)
rng = np.random.default_rng(252)


def cdet(a, label):
    t = time.time()
    la, arg, pmin, pmax = modecount_cx.cdet(*(np.ascontiguousarray(x) for x in a))
    print(f"  {label:>22s}: ln|det| {la!r} arg {arg!r} pivots {pmin:.2e}..{pmax:.2e} ({time.time() - t:.0f} s)",
          flush=True)
    return complex(la, arg), pmin, pmax


def perturbed(a, rel):
    h1, l1, h2, l2 = a
    return (h1, l1 + rel * np.abs(h1) * rng.standard_normal(h1.shape), h2,
            l2 + rel * np.abs(h2) * rng.standard_normal(h2.shape))


def spread(a, tag):
    base = cdet(a, f"{tag} M")
    vals = [base, cdet(tuple(x.T for x in a), f"{tag} M^T")]
    vals += [cdet(perturbed(a, 1e-30), f"{tag} M + 1e-30 draw {i}") for i in range(3)]
    d = [abs(complex(v[0].real - base[0].real, np.angle(np.exp(1j * (v[0].imag - base[0].imag))))) for v in vals[1:]]
    return base, vals, d


n = rh.shape[0]
G = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
ctl = (G.real.copy(), np.zeros((n, n)), G.imag.copy(), np.zeros((n, n)))
_, _, dctl = spread(ctl, "control")
_, vals, dm = spread((rh, rl, ih, il), "mode")
ok = max(dctl) < 1e-20
rec = dict(state=path, D=st.D, M=st.M, ks=st.ks, z=[z.real, z.imag], n=n, control_spread=dctl, mode_spread=dm,
           mode_values=[[v[0].real, v[0].imag, v[1], v[2]] for v in vals], control_passed=bool(ok))
json.dump(rec, open(out, "w"), indent=1)
print(f"control spread {max(dctl):.1e} ({'passed' if ok else 'FAILED: not read'}); mode matrix: |ln det(M^T) - ln det(M)| "
      f"{dm[0]:.2e}, perturbed draws {', '.join(f'{x:.2e}' for x in dm[1:])}", flush=True)
sys.exit(0 if ok else 1)
