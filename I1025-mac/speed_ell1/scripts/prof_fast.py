import sys, cProfile, pstats, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm as fm
S, z, rec, same, msg = fm.load_system(sys.argv[1], sys.argv[2], float(sys.argv[3]))
print(msg)
only = [int(v) for v in sys.argv[5].split(",")]
pr = cProfile.Profile(); pr.enable()
with np.errstate(all="ignore"):
    fm.mode_matrix_fast(S, z, float(sys.argv[4]), only=only, log=print)
pr.disable(); pstats.Stats(pr).sort_stats("tottime").print_stats(15)
