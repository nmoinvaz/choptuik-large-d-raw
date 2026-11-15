"""diagnostic (#819, plants only): which ingredient of the plant keeps the estimators from reading mu 3/2 in X"""
import json, sys
import mpmath as mp
import numpy as np
sys.path.insert(0, ".")
sys.argv = [sys.argv[0], "x", sys.argv[1]]
import fold_cancel as FC
mp.mp.dps = 200
raw = sys.argv[2]
co = {float(k): v for k, v in json.load(open("data/fold_cancel_coeffs.json")).items()}
med = lambda key, i: float(np.median([v[key][i] for v in co.values()]))
bl = [med("lam", i) for i in range(3)]; bd = [med("delta", i) for i in range(3)]
r = bl[0] / bd[0]
for D0 in (259.49278398857086, 259.6306324762619, 259.7436, 259.8184):
    D0 = min(co, key=lambda x: abs(x - D0))
    reg_l, reg_d = FC.low_orders(raw, D0, co[D0])
    zero = [mp.mpf(0)] * 24
    for label, cont, rl, rd in (("clean", 0.0, zero, zero), ("contamination only", 0.3, zero, zero),
                                ("regular only", 0.0, reg_l, reg_d), ("both", 0.3, reg_l, reg_d)):
        FC.CONT = cont
        pl, pd = FC.plant_pair(D0, bl, bd, rl, rd)
        v = FC.type_X(D0, pl, pd, r)
        print("D0 %.4f %-19s ratio D* %.4f mu %+.3f | dlog %s" % (D0, label, D0 + v["ratio"][0], v["ratio"][1],
              "D* %.4f mu %+.3f" % (D0 + v["dlog"][0], v["dlog"][1]) if v["dlog"] else "none"))
