import numpy as np
from hpkernel.driver import load_q, make_solver, predict_q, block_norms
R = "/Users/nathan/Source/raw-T81/"
za, ma = load_q(R + "conv_pin7_D72.8000_D72.800000.npz"); zb, mb = load_q(R + "conv_pin5_D73.0000_D73.000000.npz")
M = ma["M"]
mk = lambda Dx: make_solver(Dx, M, nodes=list(ma["nodes"]), kt=ma["kt"], kc=ma["kc"], ks=ma["ks"], threads=4, kfreeze=13)
s0 = mk(73.0); segs = s0.plan(zb[0], zb[1], 1e-32, 0.05)
for D in (72.9, 73.001, 73.01, 73.05):
    zp = predict_q([(72.8, za), (73.0, zb)], D)
    s = mk(D); s.set_segs(segs)
    F = s.residual_q(*zp)
    print(f"D {D}: linear predictor |F| by block " + " ".join(f"{v:.1e}" for v in block_norms(s, F[0], F[1])), flush=True)
