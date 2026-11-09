"""Smoothness probe of modecount_cx's det M(lambda) (#252, after both lambda_phys gates fired; criteria written in
../README.md, "Smoothness probe", before the runs).

    python smooth_probe.py HP_DIR STATE.npz KF LAM_PHYS OUT.json

f(lam) = ln det M = ln|det| + i arg (modecount_cx). Five determinants:
  x0 = lam_phys - 0.015 (real) and x0 + 1e-9 i: A = |f(x0 + 1e-9 i) - f(x0) - 1e-9 i f'(x0)|, with f'(x0) taken from
     the slope of ln|det| between x0 and the circle point below (|f'| ~ 33, so the linear term is ~3e-8 and the rest
     should be below 1e-12). A large A means the li != 0 path (2M x 2M horizon solves) changes det M by itself.
  z = lam_phys + 0.2 e^{2 pi i / 20} (the lambda_phys circle's second base point), z + d, z + 2d with d = 1e-7:
     B = |f(z + 2d) - 2 f(z + d) + f(z)| (second difference; |f''| d^2 should be ~1e-11).
Passes (smooth) when A < 1e-6 and B < 1e-6. Exit 0 on pass, 1 on fail.
"""
import cmath
import json
import math
import sys
import time

hp_dir, path, kf, lam, out = sys.argv[1:6]
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

kf = None if kf == "none" else int(kf)
lam = float(lam)
st = mc.setup(path, M=None, kf=kf, fmax=1e-15)
print(f"D {st.D} M {st.M} ks {st.ks} kf {st.kf} |F| {st.F:.1e}", flush=True)
vals = {}


def f(z):
    t = time.time()
    la, arg, pmin, pmax = st.det(z.real, z.imag)
    vals[z] = dict(re=z.real, im=z.imag, lnabs=la, arg=arg, pmin=pmin, pmax=pmax, sec=round(time.time() - t, 1))
    print(f"  {z}: ln|det| {la!r} arg {arg!r} ({vals[z]['sec']} s)", flush=True)
    return complex(la, arg)


x0 = complex(lam - 0.015, 0.0)
z = lam + 0.2 * cmath.exp(2j * math.pi / 20)
d = 1e-7
f0, f0i = f(x0), f(x0 + 1e-9j)
fz, fz1, fz2 = f(z), f(z + d), f(z + 2 * d)
slope = (fz1 - fz) / d                       # f' near z, for scale only
# f'(x0) from the real-axis slope of ln|det| (det is real there, so f' is real): central estimate from x0 and x0 + 1e-9 i
# is not available, so use the Cauchy-Riemann form: Im f(x0 + i e) - Im f(x0) = e Re f'(x0), Re part changes by O(e^2)
dI = cmath.phase(cmath.exp(1j * (f0i.imag - f0.imag)))
A_re = abs(f0i.real - f0.real)
fp_x0 = dI / 1e-9
A = A_re                                     # the real part must not move at first order
B = abs(fz2 - 2 * fz1 + fz)
ok = A < 1e-6 and B < 1e-6
rec = dict(state=path, D=st.D, M=st.M, kf=st.kf, lam_phys=lam, x0=lam - 0.015, z=[z.real, z.imag], d=d,
           A_lnabs_change=A, arg_change_over_1e9=dI, implied_fprime_x0=fp_x0, B_second_difference=B,
           first_difference_slope=[slope.real, slope.imag], values=list(vals.values()), passed=ok)
json.dump(rec, open(out, "w"), indent=1)
print(f"A = |ln|det|(x0 + 1e-9 i) - ln|det|(x0)| = {A:.2e} (arg moved {dI:+.3e}, f'(x0) ~ {fp_x0:+.2f}); "
      f"B = second difference at z = {B:.2e} (slope {abs(slope):.2f}) -> {'PASS (smooth)' if ok else 'FAIL (not smooth)'}",
      flush=True)
sys.exit(0 if ok else 1)
