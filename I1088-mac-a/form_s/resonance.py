"""The horizon series' near-resonance (#1088): at a form-S state, L_k = omega D_odd + diag((k + 1)(1 - G_0) - n/2),
G_0 = -(n - 1) X_0/(1 + X_0) with (omega D_e - (n - 1) - 2 m_h^2) X_0 = 2 m_h^2 (form_s.rs horizon_mob's P_k operator,
the u series' too), and its smallest singular value over k = 0..ks, with the k where it is smallest; a guess at D is
form_s.py jump's fit (guess_probe.py's) when given as NAME:DEG:GLOBS. float64.

    python3 resonance.py D KS STATE.npz|FIT ...
"""
import glob, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
from octo_corrector import load_o
from form_s import scale_s, unscale_s, dmat_even
from hpkernel.driver import dmat_odd


def state_of(spec, Dv):
    if ":" not in spec:
        z, m = load_o(spec)
        return sum(np.asarray(q) for q in z[:2]), m
    name, deg, globs = spec.split(":", 2)
    rows = []
    for g in globs.split(","):
        for p in sorted(glob.glob(g)):
            z, m = load_o(p)
            rows.append((m["D"], sum(np.asarray(q) for q in z[:2]), m))
    rows.sort(key=lambda r: r[0])
    M, K = rows[-1][2]["M"], len(rows[-1][2]["nodes"])
    Ds = np.array([r[0] for r in rows])
    Y = np.array([scale_s(r[1], r[0], M, K) for r in rows])
    c = np.polyfit(1.0 / (Ds - 2.0), Y, int(deg))
    y = np.array([np.polyval(c[:, j], 1.0 / (Dv - 2.0)) for j in range(Y.shape[1])])
    return unscale_s(y, Dv, M, K), dict(rows[-1][2], D=Dv)


Dv, ks = float(sys.argv[1]), int(sys.argv[2])
for spec in sys.argv[3:]:
    zs, m = state_of(spec, Dv)
    D = float(m["D"]) if ":" not in spec else Dv
    n = D - 2.0
    M, K = m["M"], len(m["nodes"])
    mh = zs[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
    om = 2 * np.pi / zs[-1]
    De = dmat_even(M)[0]
    Do = dmat_odd(M)[0]
    X0 = np.linalg.solve(om * De - np.diag((n - 1) + 2 * mh * mh), 2 * mh * mh)
    G0 = -(n - 1) * X0 / (1 + X0)
    sig = np.array([np.linalg.svd(om * Do + np.diag((k + 1) * (1 - G0) - n / 2), compute_uv=False)[-1] for k in range(ks + 1)])
    k0 = int(sig.argmin())
    sR = (n / 2 - 1 + G0) / (1 - G0)
    print(f"  {spec.split(':')[0] if ':' in spec else spec.split('/')[-1]} at D {D:g}: smallest singular value of L_k "
          f"{sig[k0]:.3e} at k {k0}; sigma_R(theta) {sR.min():.4f} .. {sR.max():.4f}; next smallest "
          f"{np.sort(sig)[1]:.3e}", flush=True)
