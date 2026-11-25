"""The horizon sum's sensitivity to m_h against the point x where it is summed (#1088): t2v's float64 FormS.horizon
(a 8, exact products) summed at x for several x at a state or a fitted guess (NAME:DEG:GLOBS), the complex-step
derivative of (p, m, c) at x along m_h's direction |m_h| times random signs (default_rng(1)), and the order where the
coefficients fall for good below 1e-50 and 1e-70 (ks's need at that x). If the gain falls steeply with x, nodes between
0.7 and the horizon bound the shadow's growth per segment and a jump's basin widens.

    python3 gain_x.py T2V_DIR D KS X1,X2,... SPEC ...
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
xs = [float(x) for x in sys.argv[4].split(",")]
for spec in sys.argv[5:]:
    zs, m, D = state_of(spec, Dv)
    M, K = m["M"], len(m["nodes"])
    mh = zs[2 * M + 3 * M * K:2 * M + 3 * M * K + M]
    om = 2 * np.pi / zs[-1]
    dirn = np.abs(mh) * np.random.default_rng(1).choice([-1, 1], M)
    for x in xs:
        fs = FormS(D, M, a=8.0, kb=None, zK=x * x, ks=ks)
        with np.errstate(all="ignore"):
            ho = fs.horizon(2.0 * mh, om, keep=True)
            h = 1e-30
            hz = fs.horizon(2.0 * mh + 1j * h * 2.0 * dirn, om + 0j)
        g = max(np.abs(0.5 * (hz["U"].imag + x * hz["V"].imag) / h).max(),
                np.abs(0.5 * (hz["U"].imag - x * hz["V"].imag) / h).max(), np.abs(hz["c"].imag / h).max())
        mag = np.max([np.abs(ho["series"][nm]).max(axis=1) for nm in ("U", "V", "c")], axis=0)
        lv = []
        for lev in (1e-50, 1e-70):
            above = np.nonzero(mag >= lev)[0]
            lv.append(int(above[-1] + 1) if len(above) else 0)
        print(f"  {spec.split(':')[0] if ':' in spec else spec.split('/')[-1]} D {D:g}, x {x}: gain from m_h {g:.3e}; "
              f"max |p| {np.abs(0.5 * (ho['U'] + x * ho['V'])).max():.3e}; coefficients last above 1e-50 at k {lv[0]} "
              f"({lv[0] / (D - 2):.2f} n), 1e-70 at k {lv[1]}; largest past n/2 {mag[int((D - 2) / 2):].max():.1e}",
              flush=True)
