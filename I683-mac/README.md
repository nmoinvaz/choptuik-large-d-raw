# I683-mac: precision of the real S₁ inputs to the Padé and twin scripts, with reruns at full precision

Machine: mac (the coordinator's Apple M5 Mac), one process at a time under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/683

Code: `solver/inner_amp/sigma_load.py` (the shared loader, its check and the `53bit` control) and
`solver/inner_amp/pade_precision.py` (plants, comparisons and the strings' floor) on the branch `wip/i683-subagent`
of nmoinvaz/choptuik-large-d. Results: `notes/PADE_FAR_END.md` section 10. Every exit is the last line of its log or
stdout.

- `check.log`, `check_mutate_53bit.log`: `sigma_load.py --check` through each caller's entry point at mpmath's
  default precision (every component within 1e-100 of its string), and its control, which must exit 1.
- `rounding.json`, `rounding.log`: `sigma_load.py --rounding`, the strings' rounding per order against the measured
  errors.
- `plants_c.*`: `pade_precision.py plants`, the plants' c_m and σ₀–σ₃₀ with the real template read at 53 bits, 60
  and 100 digits against 300 digits.
- Reruns at full precision with the stage's own script, each against its stored record (`compare/<name>.log` and
  `.json`, from `pade_precision.py compare`; `*_below_n` leave out the rows at M = n, whose χ is rounding noise):
  - `twins_plants.*`, `twins_real.*`: `pade_twin_size.py twins` and `twins_real`, against `I672-mac/`.
  - `real.json`, `farend_real.stdout`: `pade_farend.py real`, against `I547-mac/real.json`.
  - `diag_post_freeze.json`, `farend_diag.stdout`: `pade_farend_diag.py`, against `I547-mac/`.
  - `geometry/*.json`, `geometry_*.stdout`: `pade_geometry.py plants` and `real`, frozen and `--noise=measured`,
    against `I541-mac/`. Their exit 1 is the frozen verdict, as in #541.
- `floor.*`, `floor_mutate_corner.*`: `pade_precision.py floor`, the first-order shift of the Padé and DA2 statistics
  over the box of the strings' rounding, with its corner control and the mutation that must fail it.
- `floor_twins.*`, `floor_twins_mutate_proj.*`: `pade_precision.py floor_twins`, the same for the twins' residuals at
  22 terms, its controls and their mutation, and the twin scans with err_k widened to the rounding.
- `reruns.log`: start and end times and exits of the reruns.
