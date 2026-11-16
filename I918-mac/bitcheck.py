# #918: the new build against the build of #652 at rate zero: the residual and the Newton step of a state, as a hash
import hashlib, sys, numpy as np
sys.path.insert(0, "matter/sigma_ms")
import smdriver as sd
z, meta = sd.load(sys.argv[1])
zh, zl = np.ascontiguousarray(z[0], float), np.ascontiguousarray(z[1], float)
s = sd.solver_of(meta, 2)
F = s.residual([zh, zl])
dz, F2, pmin, pmax = s.newton([zh, zl])
h = hashlib.sha256()
for a in list(F) + list(dz) + list(F2):
    h.update(np.ascontiguousarray(a).tobytes())
print(h.hexdigest()[:16], f"|F| {sd.fnorm(F):.3e} |dz| {float(np.max(np.abs(np.asarray(dz[0])))):.3e} pivots {pmin:.3e} {pmax:.3e}")
