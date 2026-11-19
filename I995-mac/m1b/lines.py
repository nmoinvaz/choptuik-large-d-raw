"""Smoothness of R_1 along lines in wf, for several arc radii r1; also max |Y| on the path."""
import sys, json, time
import numpy as np
from multiprocessing import get_context
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-995/solver/inner_stokes")

def ev(arg):
    A, wf, r1 = arg
    import lateral_np as LN
    from scipy.integrate import solve_ivp
    w = LN.W0 * wf; Fh = LN.Fharm(A); M = 1; r0 = 0.1; phi0 = 3 * np.pi / 8
    Y0, jt, err = LN.series_data(Fh, w, M, r0 * np.exp(1j * phi0), True)
    nm = LN.NP(M, w, True)
    u = np.exp(1j * phi0)
    s1 = solve_ivp(lambda t, Z: nm.rhs(t * u, Z) * u, (r0, r1), Y0, method="DOP853", rtol=1e-12, atol=1e-15)
    s2 = solve_ivp(lambda t, Z: nm.rhs(r1 * np.exp(1j * t), Z) * 1j * r1 * np.exp(1j * t), (phi0, 0.0), s1.y[:, -1],
                   method="DOP853", rtol=1e-12, atol=1e-15)
    Y = s2.y[:, -1]
    mx = max(np.abs(s1.y).max(), np.abs(s2.y).max())
    no = nm.no; D = Y[:no]; idx = {mu: k for k, mu in enumerate(nm.odd)}
    JD = D[idx[1]] - np.conj(D[idx[-1]])
    s = 1j * w
    R = JD / (2j * np.pi * LN.Kp(s) * LN.fast_lin(s, r1) * (2 * Fh[1])) * r1 ** (-A * A)
    return dict(A=A, wf=wf, r1=r1, re=R.real, im=R.imag, mx=float(mx), nst=len(s1.t) + len(s2.t), Y0=float(np.abs(Y0).max()))

if __name__ == "__main__":
    out = sys.argv[1]; As = [float(a) for a in sys.argv[2].split(",")]; r1s = [float(r) for r in sys.argv[3].split(",")]
    N = int(sys.argv[4]); wfs = np.linspace(0.2, 3.0, N) + 0.00654321
    args = [(A, float(wf), r1) for A in As for r1 in r1s for wf in wfs]
    t0 = time.time()
    with get_context("spawn").Pool(2) as P, open(out, "w") as f:
        for r in P.imap(ev, args, chunksize=4):
            f.write(json.dumps(r) + "\n"); f.flush()
    print("done", len(args), round(time.time() - t0), "s")
