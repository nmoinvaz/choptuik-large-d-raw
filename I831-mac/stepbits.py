"""#831: Real's stored-step check and the bits of its re-solved step, for comparing runs (not judged)"""
import hashlib, os, sys, time
sys.path.insert(0, os.getcwd())
import numpy as np
first = len(sys.argv) > 5 and sys.argv[5] == "reseed_first"
import reduced_cubic as rc
if first:
    import reseed               # noqa: F401  (after reduced_cubic, before Real, as #828's probe did)
raw, dzf, base, thr = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
t0 = time.time()
sysm = rc.Real(raw, dzf, base, thr, lambda s: None, fast=True)
F = sysm.F()
x = sysm.s.olu_solve(list(sysm.parts8(F)), False)
hx = hashlib.sha256(b"".join(np.ascontiguousarray(p, dtype=float).tobytes() for p in x)).hexdigest()[:16]
hF = hashlib.sha256(b"".join(np.ascontiguousarray(p, dtype=float).tobytes() for p in sysm.so.residual_o(sysm.z0))).hexdigest()[:16]
st = sysm.s.newton_o(list(sysm.z0))
hd = hashlib.sha256(b"".join(np.ascontiguousarray(p, dtype=float).tobytes() for p in st[0])).hexdigest()[:16]
import mpmath
print(f"STEPBITS dps={mpmath.mp.dps} reseed_first={first} hp={os.getcwd()} openblas={os.environ.get('OPENBLAS_NUM_THREADS', 'unset')} threads={thr} dz0_re={float(sysm.dz0_re):.3e} "
      f"F={hF} solve={hx} newton_o_again={hd} pivots={st[3]:.6e} ({time.time() - t0:.0f} s)", flush=True)
