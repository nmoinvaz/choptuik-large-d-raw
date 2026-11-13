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
- `*.stdout`: the console copies.

Part 1 code at 2f6e3d6d (the diagnostic at bc8bf51d), run 2026-11-13 10:51–10:57 UTC. Every exit is the last line of
its stdout file.
