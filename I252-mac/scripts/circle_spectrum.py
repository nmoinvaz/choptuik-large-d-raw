"""Fourier spectrum of ln h on a recorded circle (#252, the D 55 lambda_phys gate), from the cache only.

    python circle_spectrum.py HP_DIR CACHE.jsonl RE,IM,R [--n0=20]

Replays hp/modecount_circle.circle with a determinant that reads the cache (a point missing from it raises), so the
record is the circle's own. Then, with h = det M exp(-beta (lam - c)) / (lam - c)^W and ln h continued around the
circle, prints the Fourier coefficients a_k of ln h on the n0 base points (ln h = sum a_k e^{i k t}). For k < 0 they
carry the zeros inside (a_-1 = -(sum z_j - c) to aliasing), for k > 0 the singularities of ln h outside: a zero or pole
of det M at distance d from c in direction phi gives |a_k| ~ (R/d)^k / k with arg a_k ~ -k phi + const. The aliasing error
of a_-1, hence of the position, is about |a_(n0-1)|. Prints the fitted ratio R/d and phi from a_2 ... a_8.
"""
import json
import math
import sys

import numpy as np

hp_dir, cache_path, spec = sys.argv[1:4]
n0 = int(next((a.split("=")[1] for a in sys.argv[4:] if a.startswith("--n0=")), 20))
sys.path.insert(0, hp_dir)
from modecount_circle import circle  # noqa: E402
from modecount_wind import wrap  # noqa: E402

cache = {}
for line in open(cache_path):
    r = json.loads(line)
    cache[(r["re"], r["im"])] = (r["lnabs"], r["arg"])


def det(lam):
    return cache[(float(lam.real), float(lam.imag))]


cr, ci, R = (float(v) for v in spec.split(","))
c = complex(cr, ci)
rec = circle(det, c, R, n0=n0)
W = int(round(rec["winding"]))
beta = complex(*rec["beta"])
pt = lambda s: c + R * complex(math.cos(2 * math.pi * s), math.sin(2 * math.pi * s))
# every cached point on the circle, by its parameter t (the base points at exactly i / n0), to continue the phase as
# circle() does
base = [i / n0 for i in range(n0)]
bkeys = {(float(pt(t).real), float(pt(t).imag)): t for t in base}
vals = {}
for k in cache:
    if abs(abs(complex(*k) - c) - R) < 1e-9:
        t = bkeys.get(k, (math.atan2(k[1] - ci, k[0] - cr) / (2 * math.pi)) % 1.0)
        la, arg = cache[k]
        v = complex(la, arg) - beta * (complex(*k) - c)
        vals[t] = (v.real, wrap(v.imag))
assert all(t in vals for t in base)
allt = sorted(vals)
phase, cont = vals[allt[0]][1], {allt[0]: vals[allt[0]][1]}
for a, b in zip(allt[:-1], allt[1:]):
    phase += wrap(vals[b][1] - vals[a][1])
    cont[b] = phase
lnh = np.array([complex(vals[t][0], cont[t]) - W * complex(math.log(R), 2 * math.pi * t) for t in base])
a = np.fft.fft(lnh) / n0      # ln h(t_j) = sum_k a_k e^{i k t_j}, t_j = 2 pi j / n0, so a_k = a[k mod n0]
coef = {k: a[k % n0] for k in range(-(n0 // 2) + 1, n0 // 2 + 1)}
print(f"circle {c} R {R}: winding {rec['winding']:+.6f}, zeros {rec.get('zeros')}, estimate {rec.get('zeros_est')}")
print(" k   |a_k|       arg a_k")
for k in sorted(coef):
    print(f"{k:+3d}  {abs(coef[k]):.3e}  {np.angle(coef[k]):+.3f}")
ks = np.arange(2, 9)
mag = np.array([abs(coef[k]) * k for k in ks])
slope = np.polyfit(ks, np.log(mag), 1)[0]
ratio = math.exp(slope)
ph = np.unwrap([np.angle(coef[k]) for k in ks])
phi = -np.polyfit(ks, ph, 1)[0]
print(f"fit over k = 2..8: R/d = {ratio:.3f} (d = {R / ratio:.3f}), direction phi = {phi:+.3f} rad -> singularity near "
      f"{c + (R / ratio) * complex(math.cos(phi), math.sin(phi)):.4f}; aliasing of a_-1 ~ (R/d)^{n0 - 1} = "
      f"{ratio ** (n0 - 1):.1e}, times R: {R * ratio ** (n0 - 1):.1e}")
