# I669-mac: twins both ways, twins of the real S₁ series, and the smallest chord twin by size, with controls

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/669

Code: `solver/inner_amp/pade_twin_size.py` on the branch `wip/i669-subagent` of nmoinvaz/choptuik-large-d. Method and
frozen criteria: `notes/PADE_FAR_END.md` section 8.

- `selftest*.log`: the selftest and its mutations `upoly` and `radius` (each must exit 1).
- `twins_plants.*`: part 1 on the plants. The same-class controls C0, and the twin scans (M = 6..23, one row per M with
  chi, l2, the largest |c_m|, the coefficient norm and the peak density) of the arc twin and the smooth-arc twin of
  chord2 and of the chord twin of arcjump, with M_min, M_lo and the precision rows.
- `twins_plants_mutate_*.*`: C0 with one basis column perturbed by 1e-8 (must fail for that basis).
- `twins_real.*`: part 1 on the real σ₀–σ₂₂ (J1250). Only its first scan ran, the chord twin at ω/ω∞ = 0.99: the
  precision control C1 fired there (at M = n = 23, χ is rounding noise at both precisions), and by the frozen rule the
  real stage stopped. No other real scan and no real size stage was run.
- `size_plants.*`: part 2. The smallest chord twin by coefficient norm (M = 40) of chord2, arcjump and arc at n = 23 and
  31, its bracket, the checks at 250 digits, the ridge route and M = 50 (context), and the verdicts.
- `size_plants_killed.*`: the first start of `size`, killed after two twins so that the gated real size stage could not
  follow it. Its numbers equal those of `size_plants.*`.
- `size_plants_mutate_scale.*`: S0 with chord2's coefficients scaled by 1.25 (must fail; S0 fails unmutated too).
- `*.stdout`: the console copies.

Code at f2926c0c (wip/i669-subagent). Run 2026-11-13 10:10–10:33 UTC. Every exit is the last line of its stdout or log
file. The errors of orders 23–30 are #670's extrapolation, an estimate, not a measurement.
