"""step 0a: the quad-double residual's own error at a stored converged state. python step0_res.py RAW PLAN_TOL STATE...
For each state: the pinned residual in quad-double (residual_q, its horizon solves refined QD_REFINE = 2 steps, and
with mutate 8 = QD_MUT_REFINE4) and in octo-double (residual_o at the state's four parts promoted to eight, OD_REFINE
steps, and mutate 8: eight steps), on the segment plan at PLAN_TOL. The differences are the quad-double residual's
error at that point (the octo-double one is the reference), which bounds below what quad-double Newton can reach."""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp")
import numpy as np, mpmath as mp
mp.mp.dps = 50
from hpkernel.driver import load_q, make_solver
from multidouble import od_axpy, od_add_dd
from pinning import PinnedSolver, band_coeffs, band_field

raw, plan_tol = sys.argv[1], float(sys.argv[2])


def o8(z):
    return tuple(np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z)


def lift(z4):
    zero = np.zeros(len(z4[0]))
    return o8(tuple(z4) + (zero,) * 4)


def omax(F):
    return float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())


for p in sys.argv[3:]:
    z4, meta = load_q(os.path.join(raw, p))
    z4 = o8(z4)
    D = mp.mpf(meta["D_str"])
    M = int(meta["M"])
    s = make_solver(D, M, nodes=meta["nodes"], kt=meta.get("kt", 36), kc=meta.get("kc", 146), ks=meta.get("ks", 130),
                    threads=3, kfreeze=meta["kfreeze"])
    segs = s.plan(z4[0], z4[1], plan_tol, 0.05)
    s.set_segs(segs)
    ks_held = [k for k in range(int(meta["kfreeze"]) + 1, 14) if k % 2 == 1]
    hh, hl = band_field(band_coeffs(z4[0][:M], z4[1][:M], M, ks_held), ks_held, M)
    sp = PinnedSolver(s, M, hh, hl)
    ch, cl = sp.ch, sp.cl
    t0 = time.time()
    Fq = {mu: lift(s.residual_q(*z4, mutate=mu)) for mu in (0, 8)}
    Fo = {mu: o8(s.residual_o(list(lift(z4)), mutate=mu)) for mu in (0, 8)}
    pin = lambda F: o8(od_add_dd(*F, -ch, -cl))  # noqa: E731
    dif = lambda A, B: omax(o8(od_axpy(-1.0, *B, *A)))  # noqa: E731
    nsteps = sum(len(sg) - 1 for sg in segs)
    print(f"{float(D):.4f} plan {plan_tol:.0e} ({nsteps} Taylor steps): pinned max|F| qd {omax(pin(Fq[0])):.2e} qd-refine4 {omax(pin(Fq[8])):.2e} "
          f"od {omax(pin(Fo[0])):.2e} od-refine8 {omax(pin(Fo[8])):.2e}; |F_qd - F_od| {dif(Fq[0], Fo[0]):.2e}, "
          f"|F_qd4 - F_od| {dif(Fq[8], Fo[0]):.2e}, |F_od - F_od8| {dif(Fo[0], Fo[8]):.2e}; {time.time() - t0:.0f} s", flush=True)
