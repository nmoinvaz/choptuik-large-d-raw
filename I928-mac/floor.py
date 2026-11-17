# #928: the double-double residual's rounding floor at a state: the residual evaluated in double-double against the
# same state's residual evaluated in quad-double (the state's two parts with two zero parts)
import sys
import numpy as np
sys.path.insert(0, "matter/sigma_ms")
import smdriver as sd
for path in sys.argv[1:]:
    z, meta = sd.load(path)
    zh, zl = np.ascontiguousarray(z[0], float), np.ascontiguousarray(z[1], float)
    s = sd.solver_of(meta, 1)
    Fd = s.residual([zh, zl])
    Fq = s.residual(sd.qparts(zh, zl))
    fd = np.asarray(Fd[0]) + np.asarray(Fd[1])
    fq = sum(np.asarray(p) for p in Fq)
    print(f"{path.split('/')[-1]:38s} D {meta['D']:<10} max|F| in dd {np.max(np.abs(fd)):.2e}, in qd {np.max(np.abs(fq)):.2e}, "
          f"max |F_dd - F_qd| {np.max(np.abs(fd - fq)):.2e}", flush=True)
