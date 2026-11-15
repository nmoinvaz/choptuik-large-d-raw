"""diagnostic (#821, plants only): the near-amplitude fit's floor and recovery without the regular part and with the
fit from higher orders"""
import json, sys
import mpmath as mp
import numpy as np
sys.path.insert(0, ".")
sys.argv = [sys.argv[0], "x"]
import near_amp as NA
import lam_singularity as LS
mp.mp.dps = 200
co = {float(k): v for k, v in json.load(open("data/fold_cancel_coeffs.json")).items()}
bl = [float(np.median([v["lam"][i] for v in co.values()])) for i in range(3)]
for D0 in (259.49278398857086, 259.6306324762619, 259.7436, 259.8184):
    D0 = min(co, key=lambda x: abs(x - D0))
    with mp.workdps(60):
        reg = LS.regular(D0, 24)
    zero = [mp.mpf(0)] * 24
    for label, rg, ks in (("no regular, k 4-24", zero, range(4, 25)), ("regular, k 4-24", reg, range(4, 25)),
                          ("regular, k 8-24", reg, range(8, 25)), ("regular, k 12-24", reg, range(12, 25))):
        NA.KS = ks
        cells = []
        for a in (0.0, 0.003, 0.01, 0.03, 0.3):
            f = NA.fit(NA.plant(D0, bl, a, rg, 821), D0)
            cells.append("%.3g/%.3g" % (f["a2"], f["a3"]))
        print("D0 %.4f %-18s a2/a3 at a = 0, .003, .01, .03, .3: %s" % (D0, label, "  ".join(cells)))
