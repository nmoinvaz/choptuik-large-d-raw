# I668-rpi5: an error-weighted far-end estimator recalibrated on #547's plants

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores), one process at `nice -n 10`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/668

Made by `solver/inner_amp/pade_farend_w.py` (branch `wip/i668`) from the σ₀–σ₂₂ of `solver/inner_amp/scan45J1250` and
`scan45J1500`. Design, frozen criteria and amendments: `notes/PADE_FAR_END.md` §19.

| file | what |
|---|---|
| `selftest.log`, `selftest_mutate_*.log` | the selftest and its five mutations |
