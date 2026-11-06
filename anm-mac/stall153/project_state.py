"""project a stored state (Reseeder.project: its horizon data re-inverted from its last node, then the quad-double
polish), and save it beside, for a restart test"""
import json, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q, save_q
from reseed import Reseeder
z4, m = load_q(sys.argv[1])
rs = Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
zp, how = rs.project(z4)
o = rs.off; M = rs.M; sl_ = slice(o["mh"], o["mh"] + 2 * M)
dm = float(np.max(np.abs((np.asarray(zp[0]) - np.asarray(z4[0]))[sl_] + (np.asarray(zp[1]) - np.asarray(z4[1]))[sl_])))
rest = float(np.max(np.abs(np.delete(np.asarray(zp[0]) - np.asarray(z4[0]), np.r_[sl_]))))
print(f"projection: {how}; horizon data moved {dm:.3e}; the rest moved {rest:.1e}")
save_q(sys.argv[2], zp, dict(m, source=m.get("source"), projected_from=sys.argv[1]))
