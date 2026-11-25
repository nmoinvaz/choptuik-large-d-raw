"""Which horizon sum is off at the D 400 held state, u or Moebius? (mobcheck's check 1 read 6.1e-27 against 1e-30)
The held system's horizon block (max |F|) at the state with the u series (the state's ks) and the Moebius series at
a = 4, 6, 8 and two ks, each with 1/k rounded to double-double (exact_recip 0, the default) and to the lane's precision
(set_exact_recip(1, 0)), and the largest difference of the horizon block's rows between the variants. If the Moebius
variants agree among themselves far below 6e-27 and differ from u by it, the u sum carries the error.

    python3 mobsplit.py STATE.npz THREADS
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
from form_s import make_solver_s, HeldS, held_field, blocks_s, ks_mob
from octo_corrector import load_o

z8, meta = load_o(sys.argv[1])
thr = int(sys.argv[2])
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
h8 = held_field(z8, M)
kw = dict(kt=meta["kt"], kc=meta["kc"], threads=thr, segs=meta["segs"], kfreeze=3)
r0 = K * 3 * M
rows = {}
km = ks_mob(float(D))
for nm, mob, ks, er in (("u", 0, meta["ks"], 0), ("u exact 1/k", 0, meta["ks"], 1), ("a 8", 8, km, 0),
                        ("a 8 exact 1/k", 8, km, 1), ("a 8 ks+200", 8, km + 200, 0), ("a 6", 6, km, 0),
                        ("a 4", 4, km, 0)):
    s = make_solver_s(D, M, nodes, ks=ks, mob=mob, **kw)
    if er:
        s.set_exact_recip(1, 0)
    t0 = time.time()
    F = HeldS(s, M, K, h8).residual_s(list(z8))
    rows[nm] = [np.asarray(p)[r0:r0 + 3 * M] for p in F]
    print(f"  {nm} (ks {ks}): horizon block {blocks_s(F, M, K)[K]:.3e} ({time.time() - t0:.0f} s)", flush=True)


def diff(a, b):
    with mp.workdps(140):
        return max(abs(float(sum(mp.mpf(float(p[i])) for p in rows[a]) - sum(mp.mpf(float(p[i])) for p in rows[b])))
                   for i in range(3 * M))


for a, b in (("u", "a 8"), ("u", "u exact 1/k"), ("a 8", "a 8 exact 1/k"), ("a 8", "a 8 ks+200"), ("a 8", "a 6"),
             ("a 8", "a 4"), ("u exact 1/k", "a 8 exact 1/k")):
    print(f"  horizon rows, {a} against {b}: {diff(a, b):.3e}", flush=True)
