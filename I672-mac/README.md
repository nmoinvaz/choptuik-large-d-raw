# I672-mac: the real S₁ twins with C1 amended at M = n, and the smallest chord twin by peak density, with controls

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/672

Code: `solver/inner_amp/pade_twin_size.py` and `solver/inner_amp/pade_twin_peak.py` on the branch `wip/i672-subagent` of
nmoinvaz/choptuik-large-d. Method and frozen criteria: `notes/PADE_FAR_END.md` section 9.

- `twins_plants.*`: part 1 on the plants, rerun with the amended C1 (pade_twin_size.py `twins`).
- `twins_real.*`: part 1 on the real σ₀–σ₂₂ (J1250), with J1500 at ω/ω∞ = 1.00 as context (`twins_real`).
- `twins_real_mutate_c1dup.*`: the amended C1 with column n − 1 of the 250-digit bases replaced by column n − 2 (must
  fire on every scan with M_min = n).
- `twins_jdiag.*`: a post-freeze diagnostic at ω/ω∞ = 1.00, not judged: the real scans repeated with the J1250 file
  read at 150 digits (the stage above holds it at 53 bits), with err_k widened to the J1500 − J1250 difference, and the
  misfit at 22 terms per order.
- `peak_selftest*.log`: part 2's selftest (pade_twin_peak.py) on two planted minimax problems with closed-form
  answers and #670's planted 8-term chord density, and its mutations `radius`, `noproj` and `dual` (each must exit 1).
- `peak_plants.*`: part 2. The smallest chord twin by peak density on s = j/200 (M = 40) of chord2, arcjump and arc
  at n = 23 and 31 and every node, its bracket and its checks at 250 digits; the same on s = j/1000 and M = 50 at
  ω/ω∞ = 1.00 (context); the verdicts.
- `peak_plants_mutate_scale.*`: P0 with chord2's coefficients scaled by 0.75 (must fail).
- `peak_real.stdout`: the gated real stage, refused by its frozen rule (no separation at n = 23), exit 1.
- `*.stdout`: the console copies.

Part 1 code at 2f6e3d6d (the diagnostic at bc8bf51d), run 2026-11-13 10:51–10:57 UTC. Part 2 code at 15a53292, run
2026-11-13 11:18–11:47 UTC. Every exit is the last line of its stdout or selftest log. The errors of orders 23–30 are
#670's extrapolation, an estimate, not a measurement.
