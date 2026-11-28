| state | k_c | kappa | steps | \|F\| | weak below 1e-8 (s/s_max) | U_w^T F on them | weak above 1e-8 | U_w^T F on them | \|F\| weak part | full GN dDelta | GN \|dz\| | s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r0 | 127 | 0.7 | 4179 | 3.1940e-10 | idx 125 4.254e-11 | -1.0446e-10 | idx 126 2.690e-08, idx 127 2.691e-08 | -2.775e-13, +7.502e-14 | 1.045e-10 | **-1.9568e-02** | 2.7768e-02 | 510 |
| kc135 | 135 | 0.7 | 4441 | 3.1881e-10 | idx 134 4.031e-09, idx 135 4.032e-09 | +8.5432e-14, +1.1319e-15 | idx 136 9.135e-06 | +1.041e-15 | 8.545e-14 | **-9.1231e-12** | 4.1761e-08 | 737 |
| r2 | 127 | 0.35 | 8351 | 3.1233e-10 | idx 125 2.362e-11 | +9.6448e-11 | idx 126 1.511e-08, idx 127 1.512e-08 | +2.223e-12, -6.833e-13 | 9.648e-11 | **-1.8064e-02** | 2.5565e-02 | 1156 |

Field names as the report prints them (the unknown's part: d, c0, the node fields p m c q, mS aS qS, Delta). Weak vector composition (right: field shares and Delta's share, the two largest nodes, tau-harmonic bands [k 0], [1-3], [4-7], [8-15], [16-31], [32-] (HBANDS of i1101_weakdir.py), the three largest harmonics; left: the two largest blocks, fields, harmonics):

| state | idx | s/s_max | U_w^T F | right: fields (three largest), Delta share | right: nodes | right: tau-harmonic bands | right: top harmonics | left: blocks; fields; harmonics |
|---|---|---|---|---|---|---|---|---|
| r0 | 125 | 4.254e-11 | -1.0446e-10 | Delta 0.497, p 0.187, m 0.186; Delta 0.497 | x4 0.0587, x5 0.0585 | 0.0375 0.189 0.213 0.0493 0.0136 0.0005 | 5 0.13, 1 0.115, 7 0.0812 | 11 0.5, 12 0.5; q 0.655, p 0.165; k 1 0.981, 2 0.017 |
| r0 | 126 | 2.690e-08 | -2.7750e-13 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0687, 119 0.0334 | 11 0.344, 12 0.344; m 0.726, q 0.231; k 127 0.961, 125 0.0383 |
| r0 | 127 | 2.691e-08 | +7.5018e-14 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0686, 119 0.0332 | 11 0.344, 12 0.344; m 0.726, q 0.231; k 127 0.961, 125 0.0383 |
| kc135 | 134 | 4.031e-09 | +8.5432e-14 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 135 0.809, 133 0.0684, 127 0.0327 | 11 0.347, 12 0.347; m 0.72, q 0.23; k 135 0.962, 133 0.0363 |
| kc135 | 135 | 4.032e-09 | +1.1319e-15 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 135 0.809, 133 0.0683, 127 0.0326 | 11 0.347, 12 0.347; m 0.72, q 0.23; k 135 0.962, 133 0.0363 |
| kc135 | 136 | 9.135e-06 | +1.0414e-15 | d 0.424, p 0.237, m 0.216; Delta 0 | centre 0.436, x11 0.088 | 0.0032 0.478 0.0806 0.392 0.0435 0.0023 | 1 0.327, 3 0.146, 13 0.134 | 0 0.802, 1 0.126; q 0.971, a 0.0164; k 1 0.969, 6 0.0063 |
| r2 | 125 | 2.362e-11 | +9.6448e-11 | Delta 0.499, m 0.186, p 0.185; Delta 0.499 | x4 0.059, x5 0.0588 | 0.0367 0.186 0.215 0.0496 0.0137 0.0005 | 5 0.131, 1 0.111, 7 0.0816 | 11 0.5, 12 0.5; q 0.656, p 0.165; k 1 0.981, 2 0.0164 |
| r2 | 126 | 1.511e-08 | +2.2226e-12 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0687, 119 0.0334 | 11 0.339, 12 0.339; m 0.751, q 0.236; k 127 0.962, 125 0.0374 |
| r2 | 127 | 1.512e-08 | -6.8328e-13 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0686, 119 0.0332 | 11 0.339, 12 0.339; m 0.751, q 0.236; k 127 0.962, 125 0.0374 |

Controls (the check passes when its value is small; a control must read >= 1e-3, else it did not fire):
- r0: tau generator 2.249e-10, tau control 2.758e-03 (fired); cos(0 w tau) 2.252e-10; cos(2 w tau) 3.999e-07; sin(2 w tau) 4.798e-07; cos(0 w tau) control 1.150e-04 (DID NOT FIRE)
- kc135: tau generator 1.658e-11, tau control 4.806e-04 (DID NOT FIRE); cos(0 w tau) 1.677e-11; cos(2 w tau) 4.231e-08; sin(2 w tau) 4.764e-08; cos(0 w tau) control 2.003e-05 (DID NOT FIRE)
- r2: tau generator 1.245e-10, tau control 1.527e-03 (fired); cos(0 w tau) 1.245e-10; cos(2 w tau) 2.214e-07; sin(2 w tau) 2.656e-07; cos(0 w tau) control 6.366e-05 (DID NOT FIRE)
