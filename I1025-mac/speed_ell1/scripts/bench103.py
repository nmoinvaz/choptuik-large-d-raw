import sys, time, cProfile, pstats, numpy as np
sys.path.insert(0, sys.argv[5] if len(sys.argv) > 5 else "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm as fm
S, z, rec, same, msg = fm.load_system(sys.argv[1], sys.argv[2], float(sys.argv[3]))
print(msg, flush=True)
only = [int(v) for v in sys.argv[4].split(",")]
lam = 0.4875
pr = cProfile.Profile(); pr.enable()
t0 = time.time()
with np.errstate(all="ignore"):
    Mf = fm.mode_matrix_fast(S, z, lam, only=only, log=lambda s: print("fast" + s, flush=True))
tf = time.time() - t0
pr.disable(); pstats.Stats(pr).sort_stats("tottime").print_stats(8)
t0 = time.time()
with np.errstate(all="ignore"):
    Mc = fm.mode_matrix_cs(S, z, lam, only=only, log=lambda s: print("cs  " + s, flush=True))
tc = time.time() - t0
print(f"fast {tf:.1f} s, cs {tc:.1f} s, ratio {tc / tf:.2f}", flush=True)
fm.compare(S, Mf, Mc, only)
