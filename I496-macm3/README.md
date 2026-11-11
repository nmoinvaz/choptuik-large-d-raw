# I496-macm3: the kf 27 lambda_phys control on R 0.06 and R 0.03 circles at D 61.03, M 48

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/496.

State: modecount_state_D61.0264_M48_kf27.npz (the kf 27 state of I280-macm3/hp_data_after, sha256 in ../I472-macm3/state_sha256.txt, 1fd892fc...), in hp/data so the setup loads it with no refit. The cache `data/` is a copy of I472-macm3/kf27/data (it holds the R 0.2 control and the circles of #472), so the R 0.06 and R 0.03 circles below are new determinants.
Command (control.cmd), #472's settings with the two circles, one thread, nice 10, caffeinate -is.

Written before the run (the issue's). Each circle winds +1 with its zero within 1e-6 of lambda_phys 2.043532530673195. If R 0.03 still misses, that is reported as it stands. #472's miss at R 0.2 was 3.25e-5.

## Results

control exit 0 at 17:02:19 UTC on 2026-11-11 (started 16:23:42, 38 min, 1 thread, 59 new determinants). Both circles wind +1 with 28 points (+2 for beta), 0 verification mismatches, 0 alias bisections:

| R | zero | miss from lambda_phys 2.043532530673195 | estimate | largest step |
|---|---|---|---|---|
| 0.2 (#472, kf 27) | 2.043503 - 0.000013i | 3.25e-5 | | |
| 0.06 | 2.043522 - 0.0000039i | 1.16e-5 | 1.8e-6 | 0.354 |
| 0.03 | 2.0435338 - 0.0000025i | 2.84e-6 | 1.8e-6 | 0.353 |

Neither circle is within 1e-6, so the acceptance fails at both radii, reported as it stands.
