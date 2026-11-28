| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\|det\| | b12 | seconds |
|---|---|---|---|---|---|---|---|---|
| 0.045 | +1 | True | True | 1.54e-05 | -1 | -3902.5303054577 | rust | 1521 |
| 0.050 | -1 | True | True | 2.50e-06 | -1 | -3901.1035170558 | rust | 1515 |

- PASS: signs + then -: +1, -1
- PASS: both robust: True, True
- PASS: on the Rust block 12 (b12 field): rust, rust
- PASS: ln|det| at 0.045 within 0.0001 of dh370's: -3902.5303054577 - (-3902.5303054577) = +4.093e-12
- PASS: ln|det| at 0.05 within 0.0001 of dh370's: -3901.1035170558 - (-3901.1035170558) = -4.820e-11
- PASS: det-linear root within 1e-05 of 0.045967998: 0.045967998, difference -9.150e-11
