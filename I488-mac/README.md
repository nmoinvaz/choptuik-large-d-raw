# I488-mac: the weakest directions of the chain's pinned Newton system at D 237.13 and 242.36 (hp/near_null.py)

Machine: mac (Apple M5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/488

| file | state | options | check |
|---|---|---|---|
| D237.log, D242.log | crawlI D 237.1312, crawlJ D 242.3642 | first version, check by a central difference of the residual | FAIL: f64 vectors cannot resolve sigma near 1e-27 when J is near 1e34 (the check was wrong, the singular values stand) |
| D237_v2 | crawlI D 237.1312 | exact Jacobian at 140 digits | pass (0.9992) |
| D242_kf3 | crawlJ D 242.3642 | the same | pass (0.9994) |
| D242_kf1 | the same | --kfreeze=1 (harmonic 3 held) | pass (1.0000) |
| D242_ctl | the same | --mutate=scale_row (one row x 1.01) | passes: this control does not fire |
| D242_ctl_scale_p1 | the same | --mutate=scale_p1 (p1 rows x 1.05) | passes (1.0058): does not fire |
| D242_ctl_sigma | the same | --mutate=sigma (sigma reported x 1.05) | FAIL (0.952), as it must |
