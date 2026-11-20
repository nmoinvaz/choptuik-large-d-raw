"""dump_ctx.py's file (model.rs ctxfile) from a state with a stored plan, without the compiled kernel: the driver's
dmat_odd and phase_weights are imported with a stub _hpkernel. n = D - 2 from D_str when the state has it."""
import importlib.util
import json
import sys
import types

import mpmath as mp
import numpy as np

drv_path, state, out = sys.argv[1], sys.argv[2], sys.argv[3]
pkg = types.ModuleType("hpkernel")
pkg.__path__ = []
stub = types.ModuleType("hpkernel._hpkernel")
stub.Solver = object
sys.modules["hpkernel"] = pkg
sys.modules["hpkernel._hpkernel"] = stub
spec = importlib.util.spec_from_file_location("hpkernel.driver", drv_path)
drv = importlib.util.module_from_spec(spec)
sys.modules["hpkernel.driver"] = drv
spec.loader.exec_module(drv)

d = np.load(state, allow_pickle=False)
m = json.loads(str(d["meta"]))
zh, zl = np.asarray(d["zh"], float), np.asarray(d["zl"], float)
M = int(m["M"])
segs = m.get("segs")
if not segs:
    # no stored plan: one step per segment (ctxfile needs a plan; the planner tests replan anyway)
    nodes = m["nodes"]
    segs = [[nodes[b], nodes[b + 1]] for b in range(len(nodes) - 1)]
with mp.workdps(60):
    Dm = mp.mpf(m["D_str"]) if "D_str" in m else mp.mpf(float(m["D"]))
    nh, nl = drv.dd_from_mp([Dm - 2])
dh, dl = drv.dmat_odd(M)
ph, pl = drv.phase_weights(M)
v = [M, float(nh[0]), float(nl[0]), m["kt"], m["kc"], m["ks"], len(m["nodes"])] + list(m["nodes"])
for g in segs:
    v += [len(g)] + list(g)
v += list(dh.ravel()) + list(dl.ravel()) + list(ph) + list(pl) + [len(zh)] + list(zh) + list(zl)
np.asarray(v, dtype="<f8").tofile(out)
print(f"{out}: M {M}, L {len(zh)}, {sum(len(g) - 1 for g in segs)} Taylor steps, kt {m['kt']}")
