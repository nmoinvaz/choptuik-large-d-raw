"""Smoke test of the fitted M = 64 layout in the count's determinant: setup (loads the saved state), then det M at two
real lambda on either side of lam_phys with hpkernel's mode_det and with modecount_cx's complex mode_det."""
import sys, time
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a92db8e6b268598e4/hp"
sys.path.insert(0, WT)
import modecount_common as mc
path, M, kf = sys.argv[1], int(sys.argv[2]), (None if sys.argv[3] == "none" else int(sys.argv[3]))
lams = [float(v) for v in sys.argv[4].split(",")]
st = mc.setup(path, M=M, kf=kf, fmax=1e-15)
print(f"D {st.D} M {st.M} K {st.K} nodes {st.meta['nodes']} |F| {st.F:.1e} lam_g {st.lam_g:.10f}", flush=True)
for lam in lams:
    t = time.time()
    r = st.det_real(lam)
    t1 = time.time() - t
    t = time.time()
    c = st.det(lam, 0.0)
    t2 = time.time() - t
    print(f"  lam {lam}: hpkernel mode_det {r}  ({t1:.0f} s)\n            modecount_cx mode_det {c}  ({t2:.0f} s)", flush=True)
