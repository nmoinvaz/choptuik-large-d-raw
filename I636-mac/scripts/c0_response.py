"""How far the free fits' c0 moves for a smooth error in lam_g along the chain (#636, a scale for the measured terms):
lam_g + eps g(D) on the chain's backbone (D >= 73), g a ramp from 0 at D 73 to 1 at D 245, or the measured
M 48 - M 32 differences scaled up. Prints the free c0 median and range for each eps."""
import sys

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a85c4feb2fd2f0829/hp")
import mpmath as mp
import lam_gauge_fit as LF

mp.mp.dps = 40
pts = LF.backbone()
for eps in (0, 1e-12, -1e-12):
    p = [(D, y + (mp.mpf(eps) * (D - 73) / (245 - 73) if D >= 73 else 0)) for D, y in pts]
    med, lo, hi = LF.summary(LF.fits(p), 0)
    print(f"ramp eps {eps:+.0e}: free c0 {mp.nstr(med, 13)} [{mp.nstr(lo, 13)}, {mp.nstr(hi, 13)}], 1 - max {mp.nstr(1 - hi, 3)}",
          flush=True)
