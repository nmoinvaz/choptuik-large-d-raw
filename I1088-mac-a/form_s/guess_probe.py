"""The horizon mismatch of jump guesses at D (#1088): form_s.py jump's fit in form S's layout (scale_s, polyfit in 1/n)
from given form-S states (and optionally the chain's form-A states), and t2v's float64 Moebius sum (mobius_s.py,
exact products) at the last node against the guess's last node, for several fits. No hp kernel. Each fit is NAME:DEG:
GLOB[,GLOB...] with form-S state files; CHAIN adds the 50 chain states D 226-252.5 from RAW.

    python3 guess_probe.py T2V_DIR RAW D KS A FIT1 FIT2 ...
"""
import glob, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
sys.path.insert(0, sys.argv[1])
import numpy as np
from octo_corrector import load_o
from form_s import a_to_s, scale_s, unscale_s
from mobius_s import FormS

raw, Dv, ks, a = sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
chain = sorted(glob.glob(raw + "/I903-macm3/chain_k135/anm_pin3_D*.npz") + glob.glob(raw + "/I966-dh370/ks_chain3b/*/anm_pin3_D*.npz"))
for spec in sys.argv[6:]:
    name, deg, globs = spec.split(":", 2)
    rows = []
    for g in globs.split(","):
        if g == "CHAIN":
            for p in chain:
                z, m = load_o(p)
                if 226 <= m["D"] <= 252.5:
                    rows.append((m["D"], a_to_s([sum(np.asarray(q) for q in z[:2])], m["M"], len(m["nodes"]))[0], m))
        else:
            for p in sorted(glob.glob(g)):
                z, m = load_o(p)
                rows.append((m["D"], sum(np.asarray(q) for q in z[:2]), m))
    rows.sort(key=lambda r: r[0])
    M, nodes = rows[-1][2]["M"], rows[-1][2]["nodes"]
    K = len(nodes)
    Ds = np.array([r[0] for r in rows])
    Y = np.array([scale_s(r[1], r[0], M, K) for r in rows])
    c = np.polyfit(1.0 / (Ds - 2.0), Y, int(deg))
    y = np.array([np.polyval(c[:, j], 1.0 / (Dv - 2.0)) for j in range(Y.shape[1])])
    zs = unscale_s(y, Dv, M, K)
    on = 2 * M + 3 * M * (K - 1)
    N = zs[on:on + 3 * M]
    mh = zs[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
    xl = float(nodes[-1])
    fs = FormS(Dv, M, a=a, kb=None, zK=xl * xl, ks=ks)
    with np.errstate(all="ignore"):
        ho = fs.horizon(2.0 * mh, 2 * np.pi / zs[-1])
    T = np.concatenate([0.5 * (ho["U"] + xl * ho["V"]), 0.5 * (ho["U"] - xl * ho["V"]), ho["c"]])
    print(f"  {name}: {len(rows)} states D {Ds[0]:g} .. {Ds[-1]:g}, degree {deg}: horizon mismatch {np.abs(T - N).max():.3e}, "
          f"the fit's Delta {zs[-1]:.12f}", flush=True)
