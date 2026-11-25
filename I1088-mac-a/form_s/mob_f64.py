"""t2v's float64 Moebius horizon sum (wip/large-d-inner, mobius_s.py, FormS.horizon; exact products, kb None) at a
form-S state's m_h and Delta, against the state's last node: the horizon mismatch (p, m, c at x_l) for several a and
ks, with the sum's largest coefficient and tail. Separates a bad guess (every a and ks give the same large mismatch) from
a sum that fails (they disagree).

    python3 mob_f64.py T2V_DIR STATE.npz A1,A2,.. KS1,KS2,..
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
sys.path.insert(0, sys.argv[1])
import numpy as np
from octo_corrector import load_o
from mobius_s import FormS

z8, meta = load_o(sys.argv[2])
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
D = float(meta["D"])
zv = np.asarray(z8[0]) + np.asarray(z8[1])
on = 2 * M + 3 * M * (K - 1)
N = zv[on:on + 3 * M]
mh = zv[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
om = 2 * np.pi / zv[-1]
xl = float(nodes[-1])
print(f"D {D:g}, x_l {xl}, max |m_h| {np.abs(mh).max():.4e}, Delta {zv[-1]:.12f}", flush=True)
for a in [float(x) for x in sys.argv[3].split(",")]:
    for ks in [int(x) for x in sys.argv[4].split(",")]:
        t0 = time.time()
        fs = FormS(D, M, a=a, kb=None, zK=xl * xl, ks=ks)
        with np.errstate(all="ignore"):
            ho = fs.horizon(2.0 * mh, om, keep=True)
        pv, mv = 0.5 * (ho["U"] + xl * ho["V"]), 0.5 * (ho["U"] - xl * ho["V"])
        T = np.concatenate([pv, mv, ho["c"]])
        mag = np.max([np.abs(ho["series"][nm]).max(axis=1) for nm in ("U", "V", "c")], axis=0)
        print(f"  a {a:g} ks {ks}: mismatch with the last node {np.abs(T - N).max():.3e} (p {np.abs(T - N)[:M].max():.2e}, "
              f"m {np.abs(T - N)[M:2 * M].max():.2e}, c {np.abs(T - N)[2 * M:].max():.2e}); largest coefficient "
              f"{mag[1:].max():.2e} at k {1 + mag[1:].argmax()}, smallest {mag.min():.2e} at k {mag.argmin()}, tail "
              f"{ho['tail']:.1e} ({time.time() - t0:.0f} s)", flush=True)
