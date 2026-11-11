# I500-macm3: the kf 27 lambda_phys control on R 0.015 and R 0.0075 circles at D 61.03, M 48

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118 (the hp build is the older one, no rebuild). Started 2026-11-11 17:07 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/500.

State: modecount_state_D61.0264_M48_kf27.npz (the kf 27 state of I280-macm3/hp_data_after, sha256 1fd892fc..., no refit). The cache `data/` is a copy of I496-macm3/data, so both circles are new determinants. Command (control.cmd): #496's with the two radii, one thread, nice 10, caffeinate -is.

Written before the run (the issue's). Each circle winds +1 and its miss from lambda_phys 2.043532530673195 is reported. The miss falls below 1e-6 at R 0.0075, or the floor it stops at is named. Earlier misses: 3.25e-5 (R 0.2), 1.16e-5 (R 0.06), 2.84e-6 (R 0.03).

## Results

control exit 0 at 17:59:40 UTC on 2026-11-11 (started 17:07:38, 52 min, 1 thread, 58 new determinants). Both circles wind +1 with 28 points (+2 for beta), largest step 0.353, 0 verification mismatches, 0 alias bisections:

| R | zero inside | miss from lambda_phys 2.043532530673195 | Re, Im of the offset | estimate |
|---|---|---|---|---|
| 0.2 (#472) | 2.043503 - 0.000013i | 3.25e-5 | | |
| 0.06 (#496) | 2.0435216 - 0.0000039i | 1.16e-5 | | 1.8e-6 |
| 0.03 (#496) | 2.0435338 - 0.0000025i | 2.84e-6 | | 1.8e-6 |
| 0.015 | 2.0435333 + 0.0000022i | 2.37e-6 | +7.8e-7, +2.2e-6 | 1.4e-6 |
| 0.0075 | 2.0435315 - 0.00000076i | 1.27e-6 | -1.0e-6, -7.6e-7 | 1.9e-7 |

The miss at R 0.0075 is 1.27e-6, not below 1e-6: the acceptance fails by 27%, reported as it stands. The last three misses (2.84e-6, 2.37e-6, 1.27e-6) fall slower than R^2 (it would be 7e-7 at 0.015 and 1.8e-7 at 0.0075); the offset's imaginary part changes sign between R 0.015 and 0.0075 and its real part too, which looks like scatter of about 1 to 2e-6 and not a fixed displacement (my reading, three radii only).
