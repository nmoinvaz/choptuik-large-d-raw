# I684-mac: the real S₁ twins with the far end moved past κ⋆ or the end exponent shifted, with the controls

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/684

Code: `solver/inner_amp/pade_twin_end.py` on the branch `wip/i684-subagent` of nmoinvaz/choptuik-large-d. Method and
frozen criteria: `notes/PADE_FAR_END.md` section 11.

- `selftest*.log`: the exact moved-end, shifted-exponent moments against the plants' quadrature, and the mutations
  `endmom` and `upoly` (each must fail).
- `control.*`: K0 (the far ends reproduce #541), K1 (#547's far-end-1.85 plant), C0 (every variant basis against the
  plant of its own class), and the context scans (sensitivity, resolution).
- `control_mutate_farend.*`, `control_mutate_exshift.*`: the control mutations (each must fail as frozen).
- `real.*`: the twins of the real σ₀–σ₂₂ (J1250) per variant, class and node, with the widened errors and J1500 as
  context.
- `real_mutate_c1dup.*`: the amended C1 with a degenerate 250-digit basis (must fire on every scan with M_min = n).
- `diag.*`, `diag2.*`, `diag3.*`: post-freeze diagnostics at ω/ω∞ = 1.00, chord class, judged by nothing: far ends and
  near ends on grids by χ at 22 terms (`diag`; its minimum is a tuned zero, see `diag2`), the far end by l2 at 20 terms
  on a grid and minimised (`diag2`, `diag3`), and the far end and exponent tuned together (`diag3`).

`control.log` holds two runs: the first stopped with a KeyError after K0 and K1 at ω/ω∞ = 0.99 (code 40c370ab), the
second is the complete run (37d9cbc4). `control.stdout` is the second run's.
