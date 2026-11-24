"""scratch: |r_5| (and r_3, r_1) over a (B5, C5) grid at fixed (A, w, B3, C3), float64 inner_nb, several radii"""
import sys, os, json, time
import numpy as np
WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, "solver", "inner_stokes"))
import inner_nb
inner_nb.install()
import hier as H
from multiprocessing import get_context

A, wf, B3, C3 = [float(t) for t in sys.argv[2].split(",")]
lo, hi, n = float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
radii = [float(t) for t in sys.argv[6].split(",")]
out = sys.argv[7]


def one(bc):
    b5, c5 = bc
    x = np.array([A, wf, B3, C3, b5, c5])
    try:
        R = H.demixed_multi(x, 5, radii)
        return b5, c5, {str(r): R[r].tolist() for r in radii}
    except Exception as e:
        return b5, c5, repr(e)


if __name__ == "__main__":
    g = np.linspace(lo, hi, n)
    pts = [(b, c) for b in g for c in g]
    t0 = time.time()
    with get_context("spawn").Pool(int(os.environ.get("NPROC", 4))) as pool, open(out, "w") as fh:
        for b5, c5, R in pool.imap(one, pts, chunksize=8):
            fh.write(json.dumps(dict(B5=b5, C5=c5, R=R)) + "\n")
    print(f"{len(pts)} points, {time.time() - t0:.0f} s")
