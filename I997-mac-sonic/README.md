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
