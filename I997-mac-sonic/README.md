# I997-mac-sonic: the low-D critical solution marched on warped curves through the sonic valley (planted checks, D 3.045 to 3.04)

Machine: mac (Nathan's Mac, shared). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/997 (experiment (b)).

Code: `solver/lowd_sonic/` of branch `wip/lowd-sonic` of the code repository (band.py: the warped equations and the
integrator; hybrid.py: hp's multiple shooting with the band segment replaced; segment.py: one segment against hp's next
node; ecker_gap.py: the Vienna group's data). Note: notes/LOW_D_SONIC.md on that branch. Kernel: hpkernel built for
#1043 (multidouble 4.9.1, multishoot 3.3.0), from the session scratchpad `i1043/site`.

- `ecker_gap.log`: `python3 -I ecker_gap.py <clone>` on github.com/EckerChristian/CriticalSpacetimeCrystal at
  f002d0af (read only): min (f - x) in their exported fields, their lowest D and step counts.
- `planted/p1.jsonl`: check P1 (`segment.py`, hp's D 3.7 M 256 state, band 0.01 -> 0.02): test warp, its control
  `--mutate nowarp`, and phi = 0.
- `planted/p2*.{jsonl,log}`: check P2 (`hybrid.py`, D 3.7 M 128): test warp (`p2.log`), phi = 0 (`p2_none.log`), the
  control (`p2_nowarp.log`); `p2_jac_hp.*`: the first try, the chord with hp's own band rows in the Jacobian, which
  diverges along the top harmonics.
- `planted/p3*.{jsonl,log}`: check P3 (D 4 M 96, nodes 0.8 and 0.9 added); `p3_lastnode0.7*`: the stored state's own
  nodes, whose horizon block (last node 0.7) is hypersensitive, so the chord step fails there for a reason outside the
  band; `p3_transLU.log`: the same check after the LU was changed to factor in place.
- `planted/jachp_*`: the chord with hp's Jacobian (any M) at D 3.7 M 128 for test warps A 1.5e-4, 5e-4 (plain) and
  5e-4, 1.5e-3 with Anderson mixing (`--aa_m 8`).
- `planted/wood_*`, `planted/rejac_*`: the Woodbury form of the Newton matrix at D 3.7, M 128 (test warp, control,
  replanning, split plans), and the per-D and per-iteration Jacobians at D 3.7 -> 3.69 on a state resampled to M 128.
- `real/`: the test at M 320 from hp's D 3.045 state (raw `T82-win/states/lowDhm_x0.000157-0.975_D3.0450_M320.npz`, with
  hp's M 320 states at 3.04375, 3.04355, 3.04335, 3.04315 from `T105-win2/`, `I343-win2/`, `I945-win2/` as history).
  `run_real.sh` is the last attempt's command; attempts 1-6 are `real_attempt<k>_*.log/jsonl` (1: dense Jacobian
  refused at M 320; 2: hp's Jacobian with Anderson mixing, diverged at 3.045; 3: Woodbury, D 3.045 passed, non-finite at
  3.04375; 4: replanned, diverged; 5: plan split after the Jacobian, diverged; 6: plan split before the Jacobian, D 3.045
  passed, chord stalled at 3.04375 near |F| 1e-8). `states/`: the D 3.045 solution (attempt 3), the warp phi and the
  band Jacobian at 3.045. `plancheck.py/.log`: hp's residual blocks at that solution on the stored and split plans.
