"""#966 diagnostic, outside the fixed protocol: why the square-root two-term fit of Delta's c_k at 262.3756 misfits.
Fits over k K0..31 with (a) the pair P1 and the real point, (b) adding the pair P2 = 258.3606 +- 2.2688i, all as
square roots; prints the relative misfit and |A2|/|A1|, and the plain Dlog on a plant with that ratio."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp, numpy as np
from jet_singularity import load_jet, row_series
import singularity_type as st
import subdom as sd
mp.mp.dps = 60
Z, m = load_jet(sys.argv[2]); D0 = m["D"]
c = np.array([float(x) for x in row_series(Z, "delta")[0]])
s1, s2, s3 = complex(262.0810 - D0, 0.9729), 265.0788 - D0, complex(258.3606 - D0, 2.2688)
K = np.arange(1, 32)
bk = np.array([float(sd.b(0.5, int(k))) for k in K])
for K0 in (1, 10, 16, 21):
    for with3 in (False, True):
        sel = K >= K0
        u, v, x = bk / s1 ** K, bk / s2 ** K, bk / s3 ** K
        cols = [2 * u.real, -2 * u.imag, v] + ([2 * x.real, -2 * x.imag] if with3 else [])
        X = np.column_stack(cols)[sel] / np.abs(c[sel])[:, None]
        coef, *_ = np.linalg.lstsq(X, c[sel] / np.abs(c[sel]), rcond=None)
        fit = np.column_stack(cols)[sel] @ coef
        rel = np.abs(fit - c[sel]) / np.abs(c[sel])
        A1 = complex(coef[0], coef[1]); A2 = coef[2]
        e = None
        if not with3:
            pc = sd.plant(A1, A2, sd.S1, sd.S2)
            e = st.dlog_fit(pc)
        print(f"k {K0}..31, {'P1 + real + P2' if with3 else 'P1 + real'}: misfit median {np.median(rel):.2e}, max {rel.max():.2e}; "
              f"|A2|/|A1| {abs(A2) / abs(A1):.3e}" + (f"; plain Dlog on that plant: {sd.fmt(e)}" if e is not None or not with3 else ""))
