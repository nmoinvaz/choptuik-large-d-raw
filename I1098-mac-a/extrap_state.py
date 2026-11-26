"""A guess at a new D from two form-S states of the same layout (#1098 continuation in D): every unknown, Delta
included, linear in 1/n (n = D - 2) through the two states, at 160 digits from all eight parts; the meta (nodes, Taylor
plan, kt, kc, mob) is the second state's, with D and ks set (--ks; default the second state's ks + (D' - D_B)).

    python3 extrap_state.py STATE_A STATE_B D_NEW OUT [--ks KS]
"""
import sys

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from octo_corrector import load_o, save_o  # noqa: E402

a_path, b_path, dnew, out = sys.argv[1:5]
opt = dict(zip(sys.argv[5::2], sys.argv[6::2]))
za, ma = load_o(a_path)
zb, mb = load_o(b_path)
assert len(za[0]) == len(zb[0]) and ma["nodes"] == mb["nodes"] and int(ma["M"]) == int(mb["M"])
with mp.workdps(160):
    na, nb, nn = mp.mpf(ma["D_str"]) - 2, mp.mpf(mb["D_str"]) - 2, mp.mpf(dnew) - 2
    w = (1 / nn - 1 / na) / (1 / nb - 1 / na)
    L = len(za[0])
    parts = [np.zeros(L) for _ in range(8)]
    for i in range(L):
        va = mp.fsum(mp.mpf(float(za[q][i])) for q in range(8))
        vb = mp.fsum(mp.mpf(float(zb[q][i])) for q in range(8))
        v = va + w * (vb - va)
        for q in range(8):
            parts[q][i] = float(v)
            v -= mp.mpf(parts[q][i])
ks = int(opt.get("--ks", int(mb["ks"]) + int(round(float(mp.mpf(dnew)) - float(mp.mpf(mb["D_str"]))))))
meta = dict(mb, D=float(mp.mpf(dnew)), D_str=str(dnew), ks=ks, guess=f"linear in 1/n from D {ma['D_str']} and {mb['D_str']} "
            f"(weight {mp.nstr(w, 6)})")
save_o(out, parts, meta)
print(f"guess at D {dnew} (ks {ks}) from D {ma['D_str']} and {mb['D_str']}, weight {mp.nstr(w, 6)}, Delta "
      f"{mp.nstr(mp.mpf(float(parts[0][-1])) + mp.mpf(float(parts[1][-1])), 20)}; saved {out}", flush=True)
