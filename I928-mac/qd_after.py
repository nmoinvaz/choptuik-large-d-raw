# #928: a quad-double state's residual in quad-double, the double-double residual of its first two parts, and its
# Delta against a double-double value given as hi,lo (or a second state's)
import sys
import mpmath as mp
import numpy as np
sys.path.insert(0, "matter/sigma_ms")
import smdriver as sd
mp.mp.dps = 70
z, meta = sd.load(sys.argv[1])
assert len(z) == 4, "not a quad-double state"
z = [np.ascontiguousarray(p, float) for p in z]
s = sd.solver_of(meta, 2)
fq = sd.fnorm(s.residual(z))
fd = sd.fnorm(s.residual(z[:2]))
Dq = sum(mp.mpf(float(p[-1])) for p in z)
print(f"{sys.argv[1].split('/')[-1]}: D {meta['D']}, max |F| in quad-double {fq:.2e}, double-double residual of its first "
      f"two parts {fd:.2e}, Delta {mp.nstr(Dq, 50)}")
if len(sys.argv) > 2:
    z2, _ = sd.load(sys.argv[2])
    Dd = mp.mpf(float(z2[0][-1])) + mp.mpf(float(z2[1][-1]))
    print(f"    minus the double-double Delta of {sys.argv[2].split('/')[-1]} ({mp.nstr(Dd, 30)}): {mp.nstr(Dq - Dd, 4)}")
