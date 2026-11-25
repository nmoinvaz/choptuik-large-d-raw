"""The horizon sum's gain from m_h and its coefficient profile (t2v's float64 FormS.horizon, a 8, exact products) at a
state or a fitted guess (NAME:DEG:GLOBS as in resonance.py): the complex-step derivative of (p, m, c) at the last node
along m_h's direction |m_h| times random signs (default_rng(1)), the largest coefficient below and above sigma_R and
where it sits, and the mismatch with the last node.

    python3 gain_f64.py T2V_DIR D KS SPEC ...
"""
import glob, sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
sys.path.insert(0, sys.argv[1])
import numpy as np
from mobius_s import FormS
from octo_corrector import load_o
from form_s import scale_s, unscale_s


def state_of(spec, Dv):
    if ":" not in spec:
        z, m = load_o(spec)
        return sum(np.asarray(q) for q in z[:2]), m, float(m["D"])
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
    return unscale_s(y, Dv, M, K), rows[-1][2], Dv


Dv, ks = float(sys.argv[2]), int(sys.argv[3])
for spec in sys.argv[4:]:
    zs, m, D = state_of(spec, Dv)
    M, nodes = m["M"], m["nodes"]
    K = len(nodes)
    xl = float(nodes[-1])
    on = 2 * M + 3 * M * (K - 1)
    N = zs[on:on + 3 * M]
    mh = zs[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
    om = 2 * np.pi / zs[-1]
    fs = FormS(D, M, a=8.0, kb=None, zK=xl * xl, ks=ks)
    with np.errstate(all="ignore"):
        ho = fs.horizon(2.0 * mh, om, keep=True)
        T = np.concatenate([0.5 * (ho["U"] + xl * ho["V"]), 0.5 * (ho["U"] - xl * ho["V"]), ho["c"]])
        dirn = np.abs(mh) * np.random.default_rng(1).choice([-1, 1], M)
        h = 1e-30
        hz = fs.horizon(2.0 * mh + 1j * h * 2.0 * dirn, om + 0j)
    g = max(np.abs(0.5 * (hz["U"].imag + xl * hz["V"].imag) / h).max(),
            np.abs(0.5 * (hz["U"].imag - xl * hz["V"].imag) / h).max(), np.abs(hz["c"].imag / h).max())
    mag = np.max([np.abs(ho["series"][nm]).max(axis=1) for nm in ("U", "V", "c")], axis=0)
    sR = int(round((D - 2) / 2))
    lo, hi = mag[1:sR], mag[sR:]
    print(f"  {spec.split(':')[0] if ':' in spec else spec.split('/')[-1]} at D {D:g}: mismatch {np.abs(T - N).max():.3e}; "
          f"gain from m_h {g:.3e}; largest coefficient below sigma_R ~{sR} {lo.max():.2e} at k {1 + lo.argmax()}, above "
          f"{hi.max():.2e} at k {sR + hi.argmax()}; tail {mag[-1]:.1e}", flush=True)
