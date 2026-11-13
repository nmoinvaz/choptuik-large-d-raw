# I547-mac: far end of S₁'s Borel singular support, differential-approximant estimator calibrated on plants

Machine: mac (the coordinator's Apple M5), one core under `nice -n 10`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/547

Made by `solver/inner_amp/pade_farend.py` of the code repository (branch `wip/i547-subagent`), from the σ₀–σ₂₂ of
`solver/inner_amp/scan45J1250` and `scan45J1500`. Method and frozen criteria: `notes/PADE_FAR_END.md` there.

| file | what |
|---|---|
| `selftest.log` | the script's selftest and its mutations |
| `plants.json`, `plants.log` | calibration on the planted functions, with the verdict of C1–C3 and B1 |
| `real.json`, `real.log` | the real series at the three nodes and J 1500 |
| `real_mutate_*.json`, `.log` | mutation controls on the real series |
| `diag_post_freeze.json`, `.log` | post-freeze diagnostics (`pade_farend_diag.py`): every Q₂ zero past \|t\| = 1.65 per member |
