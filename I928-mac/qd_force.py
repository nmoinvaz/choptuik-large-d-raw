# #928, a diagnostic and not a counted point: the quad-double Newton from a state, with full steps taken whether
# or not max |F| falls, to see what follows a first step that raises it (qd_protocol.md's rule stops there)
import sys
import mpmath as mp
import numpy as np
sys.path.insert(0, "matter/sigma_ms")
import smdriver as sd
mp.mp.dps = 70
z, meta = sd.load(sys.argv[1])
z = [np.ascontiguousarray(p, float) for p in sd.qparts(z[0], z[1])]
s = sd.solver_of(meta, 2)
print(f"{sys.argv[1].split('/')[-1]}: D {meta['D']}, eta {meta['eta']}, forced quad-double Newton", flush=True)
for it in range(int(sys.argv[3]) if len(sys.argv) > 3 else 4):
    dz, F, _, _ = s.newton(z)
    nF = sd.fnorm(F)
    step = float(np.max(np.abs(dz[0] + dz[1])))
    D = sum(mp.mpf(float(p[-1])) for p in z)
    print(f"  step {it}: max |F| {nF:.2e} at its start, max |dz| {step:.2e}, dDelta {float(dz[0][-1] + dz[1][-1]):+.2e}, "
          f"Delta {mp.nstr(D, 32)}", flush=True)
    if nF < 1e-55:
        break
    z = [np.ascontiguousarray(p, float) for p in sd.qd_axpy(1.0, *dz, *z)]
fq = sd.fnorm(s.residual(z))
fd = sd.fnorm(s.residual(z[:2]))
print(f"  final: max |F| in quad-double {fq:.2e}, double-double residual of the first two parts {fd:.2e}, "
      f"Delta {mp.nstr(sum(mp.mpf(float(p[-1])) for p in z), 50)}", flush=True)
if len(sys.argv) > 2 and sys.argv[2] != "-":
    sd.save(sys.argv[2], z[0], z[1], dict(meta, tag=str(meta.get("tag", "")) + "_forced"), z[2], z[3])
