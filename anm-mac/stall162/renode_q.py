"""a chain state (four parts) re-noded to another layout (driver.renode: the new node beyond the last old one from the
horizon series), its parts 2-3 set to zero; saved with the new nodes for anm_run.py's base polish"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q, make_solver, renode, save_q
mp.mp.dps = 50
inp, out, nodes_new = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
z4, m = load_q(inp)
D = mp.mpf(m["D_str"])
s = make_solver(D, m["M"], nodes=list(m["nodes"]), kt=m["kt"], kc=m["kc"], ks=m["ks"], threads=4, kfreeze=m["kfreeze"])
zh, zl = renode(s, np.asarray(z4[0]), np.asarray(z4[1]), list(m["nodes"]), nodes_new, m["M"])
zh, zl = np.ascontiguousarray(zh), np.ascontiguousarray(zl)
print(f"re-noded {m['nodes']} -> {nodes_new}: length {len(z4[0])} -> {len(zh)}, Delta {zh[-1]!r} {zl[-1]:+.6e} "
      f"(was {float(z4[0][-1])!r} {float(z4[1][-1]):+.6e})")
save_q(out, (zh, zl, np.zeros_like(zh), np.zeros_like(zh)), dict(m, nodes=nodes_new, source=inp, renoded_from=list(m["nodes"])))
