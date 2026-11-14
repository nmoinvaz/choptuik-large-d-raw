root (X2c): 1.745150028164499252944352893640343550633
offsets against the root: A1 on its own plan +2.9709e-26, X2 on its own plan -1.6580e-25

| node | segs index | cont3's value | shift of A1's plan | shift of X2's plan | effect at +1e-3 (Delta - root) |
|---|---|---|---|---|---|
| A | [0][1] | 0.3344860466 | +3.873e-04 | +7.751e-04 | +3.1390e-48 |
| B | [0][2] | 0.3727168239 | +5.370e-04 | +7.499e-04 | -4.4833e-44 |
| C | [1][1] | 0.4440903534 | +9.382e-05 | -1.211e-04 | +1.4433e-39 |
| D | [1][2] | 0.4720451767 | +4.691e-05 | -6.057e-05 | -5.3726e-36 |
| E | [2][1] | 0.5500000000 | +0.000e+00 | +0.000e+00 | -1.4729e-32 |
| F | [3][2] | 0.6742907959 | +4.703e-05 | +4.744e-04 | -3.4642e-26 |
| S3 | [3][1] | 0.6485815917 | +9.406e-05 | +9.489e-04 | +2.5804e-27 |

largest single-node effect so far: node F (3, 2), -3.4642e-26

literal test (c): the sum of the effects at 1e-3 against each plan's offset

| sum | value | against A1's offset (ratio, within a factor 2) | against X2's offset (ratio, within a factor 2) |
|---|---|---|---|
| six nodes | -3.4642e-26 | -1.166, NO | +0.209, NO |
| seven nodes (with S3) | -3.2061e-26 | -1.079, NO | +0.193, NO |

extra (an assumption of linearity, which #741 did not support for segs[3][1]): each effect scaled by the plan's actual node shift / 1e-3

| plan | scaled sum over the seven nodes | offset | ratio |
|---|---|---|---|
| A1 | -1.3866e-27 | +2.9709e-26 | -0.047 |
| X2 | -1.3987e-26 | -1.6580e-25 | +0.084 |

(b) repeat of node F from A1's arrays: Delta(R_F) - Delta(NF) = +1.6334e-56; bar 1e-40: met
