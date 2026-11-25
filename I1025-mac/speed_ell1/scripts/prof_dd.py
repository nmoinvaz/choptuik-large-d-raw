import sys, cProfile, pstats, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm, ell_ddm, ell_fastdd
S, z, rec, same, msg = ell_fastm.load_system(sys.argv[1], sys.argv[2], float(sys.argv[3]))
E = ell_ddm.DDEll(S); J = ell_fastdd.DDJac(E)
pr = cProfile.Profile(); pr.enable(); t0 = time.time()
with np.errstate(all="ignore"):
    J.mode_matrix(z, float(sys.argv[4]))
print("fast dd", time.time() - t0)
pr.disable(); pstats.Stats(pr).sort_stats("tottime").print_stats(14)
