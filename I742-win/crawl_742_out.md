
### own test (`--od_accept own`, the default), a = 1 from D 117, stopped at Newton step 9

| Newton step | max abs F before | the iterate's abs dz | trials: lam, trial max abs F, the trial's own correction abs dz_t, outcome | accepted lam | max abs F after |
|---|---|---|---|---|---|
| 0 | 1.49e-29 | 1.95e-07 | (none, lam 1 accepted at once) | 1 | 1.39e-15 |
| 1 | 1.39e-15 | 1.68e-15 | 1: 1.39e-28, 2.977e-15 (abs dz 1.68e-15), refused | 0.5 | 6.94e-16 |
| 2 | 6.94e-16 | 8.42e-16 | 1: 3.48e-29, 2.977e-15 (abs dz 8.42e-16), refused | 0.5 | 3.47e-16 |
| 3 | 3.47e-16 | 4.21e-16 | 1: 8.71e-30, 2.977e-15 (abs dz 4.21e-16), refused | 0.5 | 1.74e-16 |
| 4 | 1.74e-16 | 2.10e-16 | 1: 2.18e-30, 2.977e-15 (abs dz 2.10e-16), refused | 0.5 | 8.68e-17 |
| 5 | 8.68e-17 | 1.05e-16 | 1: 5.44e-31, 2.977e-15 (abs dz 1.05e-16), refused | 0.5 | 4.34e-17 |
| 6 | 4.34e-17 | 5.26e-17 | 1: 1.36e-31, 2.977e-15 (abs dz 5.26e-17), refused | 0.5 | 2.17e-17 |
| 7 | 2.17e-17 | 2.63e-17 | 1: 3.40e-32, 2.977e-15 (abs dz 2.63e-17), refused | 0.5 | 1.08e-17 |
| 8 | 1.08e-17 | 1.31e-17 | 1: 8.50e-33, 2.976e-15 (abs dz 1.31e-17), refused | 0.5 | 5.42e-18 |
| 9 |  |  | 1: 2.13e-33, 2.976e-15, refused |  | (running) |

### `--od_accept natural`, a = 1 from D 117, stopped after four crawling steps

| Newton step | max abs F before | the iterate's abs dz | trials: lam, trial max abs F, simplified correction (ratio x abs dz), outcome | accepted lam | max abs F after |
|---|---|---|---|---|---|
| 0 | 1.49e-29 | 1.95e-07 | 1: 1.39e-15, 1.979e-01 (1015000.0000 x 1.95e-07), refused<br>0.5: 3.47e-16, 2.475e-02 (126900.0000 x 1.95e-07), refused<br>0.25: 8.68e-17, 3.093e-03 (15860.0000 x 1.95e-07), refused<br>0.125: 2.17e-17, 3.865e-04 (1982.0000 x 1.95e-07), refused<br>0.0625: 5.42e-18, 4.822e-05 (247.3000 x 1.95e-07), refused<br>0.03125: 1.36e-18, 5.926e-06 (30.3900 x 1.95e-07), refused<br>0.015625: 3.39e-19, 6.369e-07 (3.2660 x 1.95e-07), refused<br>0.0078125: 8.47e-20, 1.353e-07 (0.6938 x 1.95e-07), accepted | 0.0078125 | 8.47e-20 |
| 1 | 8.47e-20 | 2.45e-09 | 1: 2.18e-19, 2.355e-09 (0.9612 x 2.45e-09), refused<br>0.5: 9.55e-20, 1.229e-09 (0.5018 x 2.45e-09), accepted | 0.5 | 9.55e-20 |
| 2 | 9.55e-20 | 2.47e-09 | 1: 2.20e-19, 2.435e-09 (0.9857 x 2.47e-09), refused<br>0.5: 1.03e-19, 1.235e-09 (0.5001 x 2.47e-09), accepted | 0.5 | 1.03e-19 |
| 3 | 1.03e-19 | 2.46e-09 | 1: 2.18e-19, 2.475e-09 (1.0060 x 2.46e-09), refused<br>0.5: 1.06e-19, 1.225e-09 (0.4978 x 2.46e-09), accepted | 0.5 | 1.06e-19 |
