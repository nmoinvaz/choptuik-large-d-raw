"""plants only (#822): the free-D* fit's residual on a lam_g plant with a fourth fold term b7 (in units of b1)"""
import sys
import mpmath as mp
sys.path.insert(0, ".")
sys.argv = [sys.argv[0], "x"]
import fold_separation as FS
import lam_singularity as LS
mp.mp.dps = 200
bases, bl, bd = FS.medians()
for D0 in (bases[0], bases[7], bases[15]):
    with mp.workdps(60):
        reg = LS.regular(D0, 24)
    for b7 in (0.0, 0.01, 0.1, 1.0):
        Dl, f = FS.free_fit(FS.series_plant(D0, bl, FS.D0STAR + 1e-6, reg, 1, b7=b7 * bl[0]), D0)
        print("D0 %.4f b7 %-5g D* - planted %+.2e res %.1e" % (D0, b7, Dl - float(FS.D0STAR + 1e-6), f["res"]))
