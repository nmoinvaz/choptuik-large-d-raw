"""python qd_floor.py RAW STATE.npz ...: the pinned quad-double Newton (newton_qd, plain, as the chain's corrector below
ElimQ's switch) from each converged chain state with tol 1e-45: the residual it reaches (its floor) against D and the
Jacobian's pivot range (the gain)."""
import os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import mpmath as mp
from hpkernel.driver import load_q, newton_qd
from reseed import pinned
raw = sys.argv[1]
for p in sys.argv[2:]:
    z4, meta = load_q(os.path.join(raw, p))
    D = mp.mpf(meta["D_str"])
    t0 = time.time()
    _, _, sq = pinned(meta, D, z4, threads=4)
    z, hist, conv = newton_qd(sq, z4, tol=1e-45, it_max=5, verbose=False)
    Fs = [h["F"] for h in hist]
    piv = hist[0].get("piv", [float("nan")] * 2)
    print(f"{float(D):.4f} start {Fs[0]:.2e} min {min(Fs):.2e} last {Fs[-1]:.2e} steps {len(hist)} piv {piv[0]:.1e}..{piv[1]:.1e} "
          f"dDelta {float(z[0][-1] - z4[0][-1]) + float(z[1][-1] - z4[1][-1]):+.1e} {time.time() - t0:.0f} s", flush=True)
