"""#966 diagnostic, not one of the criteria: the signs of Delta's c_1..c_N and the root test |c_k|^(-1/k) at k = N-4..N."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from jet_singularity import load_jet, row_series
mp.mp.dps = 60
for f in sys.argv[2:]:
    Z, m = load_jet(f)
    c, _ = row_series(Z, "delta")
    N = len(c)
    sg = "".join("+" if x > 0 else "-" if x < 0 else "0" for x in c)
    rt = [float(abs(c[k - 1]) ** (-mp.mpf(1) / k)) for k in range(N - 4, N + 1)]
    print(f"D0 {m['D']:.4f} N {N} signs {sg}  root test k {N-4}..{N}: " + " ".join(f"{r:.3f}" for r in rt))
