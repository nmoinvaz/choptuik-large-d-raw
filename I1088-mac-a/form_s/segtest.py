"""The Taylor-step plan's truncation in form S (#1088): two held D 300 solutions on different plans (both at
plan_tol 1e-40, both converged to 1e-44) differ in Delta by 3.8e-18. Here a converged state's held residual on its own
plan and on that plan with every step halved (a midpoint inserted), whose blocks are the plan's truncation as seen by
form S, and the first-order Delta change on the halved plan, -e_Delta^T J^-1 F from the quad-double Jacobian.

    python3 segtest.py STATE.npz THREADS
"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
from form_s import make_solver_s, HeldS, held_field, blocks_s
from octo_corrector import load_o
from multidouble import dd_solve

z8, meta = load_o(sys.argv[1])
thr = int(sys.argv[2])
M, nodes = meta["M"], meta["nodes"]
K = len(nodes)
with mp.workdps(60):
    D = mp.mpf(meta["D_str"])
h8 = held_field(z8, M)
fine = [[g[0]] + [v for a, b in zip(g[:-1], g[1:]) for v in (0.5 * (a + b), b)] for g in meta["segs"]]
for nm, segs in (("own plan", meta["segs"]), ("every step halved", fine)):
    s = make_solver_s(D, M, nodes, kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=thr, segs=segs, kfreeze=3,
                      mob=meta.get("hmob", 0.0))
    t0 = time.time()
    F = HeldS(s, M, K, h8).residual_s(list(z8))
    b = blocks_s(F, M, K)
    line = f"  {nm} ({sum(len(g) - 1 for g in segs)} steps): max |F| per block " + " ".join(f"{x:.2e}" for x in b)
    if nm != "own plan":
        J = s.jacobian_s([np.ascontiguousarray(z8[q]) for q in range(4)])
        L = s.size_s
        eD = np.zeros(L)
        eD[-1] = 1.0
        g = np.asarray(dd_solve(np.ascontiguousarray(np.asarray(J[0]).T), np.ascontiguousarray(np.asarray(J[1]).T), eD,
                                np.zeros(L))[0])
        Fv = np.asarray(F[0]) + np.asarray(F[1])
        line += f"; first-order dDelta {-(g @ Fv):+.3e} (gain {np.abs(g).sum():.2e})"
    print(line + f" ({time.time() - t0:.0f} s)", flush=True)
