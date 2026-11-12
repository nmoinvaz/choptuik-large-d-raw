# I541-mac: Borel-Padé pole tables of S₁ and of the planted two-branch-point and arc functions

Machine: Apple M5 Mac (mac), subagent. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/541

Written by `solver/inner_amp/pade_geometry.py` (branch `wip/i541-subagent` of choptuik-large-d):

- `plants.json`, `plants.log`: the plants (chord2, arcjump and the context plants), their [k/k] poles for k = 6–11,
  R_k, noise spreads, and checks T1–T4.
- `real.json`, `real.log`: the real σ₀–σ₂₂ (`scan45J1250`, and `scan45J1500` at wf 1.00), the same tables and the
  verdict.
- `*_mutate_sigma7.*`: the same with σ₇ scaled by 1.01.
