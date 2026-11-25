import sys, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm as fm
S, z, rec, same, msg = fm.load_system(sys.argv[1], sys.argv[2], float(sys.argv[3]))
print(msg, flush=True)
only = [int(v) for v in sys.argv[4].split(",")]
lam = 0.4875
M = {}
T = {}
for kind in sys.argv[5].split(","):
    t0 = time.time()
    with np.errstate(all="ignore"):
        if kind == "cs":
            M[kind] = fm.mode_matrix_cs(S, z, lam, only=only, log=lambda s: print(kind + s, flush=True))
        else:
            M[kind] = fm.mode_matrix_fast(S, z, lam, only=only, log=lambda s: print(kind + s, flush=True), basis=kind)
    T[kind] = time.time() - t0
    print(f"{kind}: {T[kind]:.1f} s", flush=True)
for kind in M:
    if kind != "cs" and "cs" in M:
        print(f"{kind} against cs (time ratio {T['cs'] / T[kind]:.2f}):")
        fm.compare(S, M[kind], M["cs"], only)
