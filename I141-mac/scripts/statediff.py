import sys
import numpy as np
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a92db8e6b268598e4/hp"
sys.path.insert(0, WT)
from hpkernel.driver import load
a = load(sys.argv[1]); b = load(sys.argv[2])
M = a[2]["M"]; K = len(a[2]["nodes"])
za = np.asarray(a[0]) + np.asarray(a[1]); zb = np.asarray(b[0]) + np.asarray(b[1])
d = (np.asarray(a[0]) - np.asarray(b[0])) + (np.asarray(a[1]) - np.asarray(b[1]))
print(f"M {M} K {K}: F {a[2].get('F')} vs {b[2].get('F')}; Delta diff {d[-1]:.2e}; max |dz| {np.abs(d[:-1]).max():.2e} at {np.abs(d[:-1]).argmax()}")
names = ["p1", "c0"] + [f"n{i}.{f}" for i in range(K) for f in "pmac"] + ["m_h", "a_h"]
par = [True, False] + [p for i in range(K) for p in (True, True, False, False)] + [True, False]
for j, (nm, odd) in enumerate(zip(names, par)):
    f = d[j * M:(j + 1) * M]
    full = np.r_[f, -f] if odd else np.r_[f, f]
    H = np.abs(np.fft.rfft(full)) / (2 * M)
    ks = np.arange(1, M, 2) if odd else np.arange(0, M + 1, 2)
    top = ks[np.argsort(-H[ks])[:3]]
    fa = za[j * M:(j + 1) * M]
    fulla = np.r_[fa, -fa] if odd else np.r_[fa, fa]
    Ha = np.abs(np.fft.rfft(fulla)) / (2 * M)
    print(f"  {nm:6s} max|d| {np.abs(f).max():.1e}  harmonics of d: " + " ".join(f"k{k}:{H[k]:.1e}" for k in top)
          + f"   state's own |a_k| at those: " + " ".join(f"{Ha[k]:.1e}" for k in top))
