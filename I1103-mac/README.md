# I1103-mac: why the l = 1 multiplet needs k_c above 120 at D 23, and formulations that would need fewer harmonics

Machine: mac (Apple laptop, the coordinator's machine), files only, no solves. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1103. Code: branch `wip/i1103-kc-math` of choptuik-large-d (based on
wip/ell1-speed 92b9bf53), copies of the scripts beside their outputs here. Python: ~/venv-314 (3.14), nice 10.

## Inputs (read by git show from raw main 6f5483eb5, not copied here)
| file | source | blob |
|---|---|---|
| `sol_l1kc135win2d23_D23.0000.npy` | raw `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy` | cd134e2c |
| `sol_l1kc127wind23_D23.0000.npy` | raw `I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy` | 7a1b150c |
| `sol_l1kc119macm3d23_D23.0000.npy` | raw `I1025-dh170/kc119_d23_wide/sol_l1kc119macm3d23_D23.0000.npy` | 2771cf87 |
| `sol_l1kc111dh170j_D23.0000.npy` | raw `I1025-dh170/kc111_d23/sol_l1kc111dh170j_D23.0000.npy` | c0edd3c1 |
| `sol_l1kc103macm3d23_D23.0000.npy` | raw `I1025-dh170/kc111_d23/in/sol_l1kc103macm3d23_D23.0000.npy` | 845e92a5 |
| `sol_l1kc95win2d23_D23.0000.npy` | raw `I1025-win2/kc95_d23/sol_l1kc95win2d23_D23.0000.npy` | 096f1cc0 |
| `sol_l1kc87Lmacm3c2_D23.0000.npy` | raw `I1025-macm3/kc87_leg2/c2/sol_l1kc87Lmacm3c2_D23.0000.npy` | bb32ff05 |
| `sol_l1kc143macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc143_d230625/in/sol_l1kc143macm3d230625_D23.0625.npy` | a62d6f77 |
| `sol_l1kc135macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc143_d230625/in/sol_l1kc135macm3d230625_D23.0625.npy` | a6253940 |
| `sol_l1kc127macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc127_d230625/in/sol_l1kc127macm3d230625_D23.0625.npy` | 7aae10c6 |
| `sol_l1kc119macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc127_d230625/in/sol_l1kc119macm3d230625_D23.0625.npy` | 57f67269 |
| `sol_l1kc39r1025_D10.5000.npy` | raw `I1025-mac/out/sol_l1kc39r1025_D10.5000.npy` | 11d96af6 |
| `sol_l1kc39r1025_D12.0000.npy` | raw `I1025-mac/out/sol_l1kc39r1025_D12.0000.npy` | 3fbf18e5 |
| `sol_l1kc39L1025_D14.0000.npy` | raw `I1025-mac/out/sol_l1kc39L1025_D14.0000.npy` | e2f744cc |
| `sol_l1kc47F1025_D15.0000.npy` | raw `I1025-mac/out/sol_l1kc47F1025_D15.0000.npy` | abfc6128 |
| `sol_l1kc47F1025_D16.0000.npy` | raw `I1025-mac/out/sol_l1kc47F1025_D16.0000.npy` | b7059fab |
| `sol_l1kc47F1025_D17.0000.npy` | raw `I1025-mac/out/sol_l1kc47F1025_D17.0000.npy` | 69a64bd5 |
| `sol_l1kc55F1025_D18.0000.npy` | raw `I1025-mac/out/sol_l1kc55F1025_D18.0000.npy` | b2c3c302 |
| `sol_l1kc55F1025_D19.0000.npy` | raw `I1025-mac/out/sol_l1kc55F1025_D19.0000.npy` | 7117e443 |
| `sol_l1kc87dh170d1975_D19.7500.npy` | raw `I1025-dh170/kc87_d1975/sol_l1kc87dh170d1975_D19.7500.npy` | 352107a8 |
| `sol_l1kc111dh170h_D21.1250.npy` | raw `I1025-dh170/kc111_d21125/sol_l1kc111dh170h_D21.1250.npy` | edbb419e |
| `sol_l1kc103dh370d2225_D22.2500.npy` | raw `I1025-dh370/kc103_d2225/sol_l1kc103dh370d2225_D22.2500.npy` | 9b920bad |
| `sol_l1kc127dh370d22875_D22.8750.npy` | raw `I1025-dh370/kc127_d22875/sol_l1kc127dh370d22875_D22.8750.npy` | 43bbf313 |
| `sol_l1_D4_kc47_D4.0000.npy` | choptuik-large-d `solver/matter/data/sol_l1_D4_kc47_D4.0000.npy` at 92b9bf53 | 9c6d051a |
| `sol_l1_kc23r_D6.0000.npy` | choptuik-large-d `solver/matter/data/sol_l1_kc23r_D6.0000.npy` at 92b9bf53 | 5589c981 |
| `sol_l1_kc23r_D8.0000.npy` | choptuik-large-d `solver/matter/data/sol_l1_kc23r_D8.0000.npy` at 92b9bf53 | e16e79b8 |
| `sol_l1_kc23m_D9.0000.npy` | choptuik-large-d `solver/matter/data/sol_l1_kc23m_D9.0000.npy` at 92b9bf53 | 0be5e4f2 |

## spectrum/ (task 1)
`python i1103_spectrum.py <dir of the states above> spectrum.json` (planted tests run first; `--planted` runs only them;
controls `--mutate=swapfit`, `nowindow`, `nomap` each make a planted test fail, `spectrum/planted.log`).
- `spectrum.log`, `spectrum.json`: per state, the dips of c(tau, 0), |c_k| of q (the centre datum), c0, 1/c0 and of
  p, m, c, psi at x = 0.02, 0.05, 0.1, 0.23, 0.5, 0.9 and the horizon data; geometric, algebraic and mixed fits of
  the envelope; for k_c >= 87 the local bandwidth k_loc(theta) and the best arctan grid (Boyd's map) at three tolerances.

## strip/ (the strip-width question)
`python i1103_strip.py <k_c 87 leg dir> <high k_c dir> strip.json` (planted tests first; `--planted` alone; controls
`--mutate=flipD` and `--mutate=nowin` each fail a planted test, `strip/planted.log`). Code commit 753eac86 of
wip/i1103-kc-math. The window fits of spectrum/ moved with k_c (0.25-0.85 k_c); here the windows are fixed ([21, 61] on
the k_c 87 leg; [41, 81] and [61, 101] at k_c 127 and 135), and the closing point D0 of delta(D) = A (D0 - D)^nu is fitted.
Inputs:

| file | source | blob |
|---|---|---|
| `sol_l1kc87Lmacm3b_D21.562500.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.562500.npy` | 35b5dcae |
| `sol_l1kc87Lmacm3b_D21.625000.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.625000.npy` | 597d564d |
| `sol_l1kc87Lmacm3b_D21.687500.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.687500.npy` | daf6e538 |
| `sol_l1kc87Lmacm3b_D21.750000.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.750000.npy` | f99f513b |
| `sol_l1kc87Lmacm3b_D21.812500.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.812500.npy` | 12856df0 |
| `sol_l1kc87Lmacm3b_D21.843750.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.843750.npy` | 48c4dc82 |
| `sol_l1kc87Lmacm3b_D21.875000.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.875000.npy` | fabc792a |
| `sol_l1kc87Lmacm3b_D21.906250.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.906250.npy` | 9ff5f191 |
| `sol_l1kc87Lmacm3b_D21.937500.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.937500.npy` | a0c4ddb3 |
| `sol_l1kc87Lmacm3b_D21.968750.npy` | raw `I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.968750.npy` | 9174c559 |
| `sol_l1kc87Lmacm3b2_D22.000000.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.000000.npy` | 84bc8e08 |
| `sol_l1kc87Lmacm3b2_D22.031250.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.031250.npy` | d6ee0268 |
| `sol_l1kc87Lmacm3b2_D22.062500.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.062500.npy` | 4da7126e |
| `sol_l1kc87Lmacm3b2_D22.093750.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.093750.npy` | 50282f80 |
| `sol_l1kc87Lmacm3b2_D22.125000.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.125000.npy` | 9ff74e1f |
| `sol_l1kc87Lmacm3b2_D22.156250.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.156250.npy` | fbea9009 |
| `sol_l1kc87Lmacm3b2_D22.187500.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.187500.npy` | 8f56f515 |
| `sol_l1kc87Lmacm3b2_D22.218750.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.218750.npy` | f197a4ec |
| `sol_l1kc87Lmacm3b2_D22.250000.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.250000.npy` | 7caefe44 |
| `sol_l1kc87Lmacm3b2_D22.281250.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.281250.npy` | 3ce8bc2e |
| `sol_l1kc87Lmacm3b2_D22.312500.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.312500.npy` | 96b8990e |
| `sol_l1kc87Lmacm3b2_D22.343750.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.343750.npy` | 467e2690 |
| `sol_l1kc87Lmacm3b2_D22.375000.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.375000.npy` | d7bfdaa2 |
| `sol_l1kc87Lmacm3b2_D22.406250.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.406250.npy` | 01be5647 |
| `sol_l1kc87Lmacm3b2_D22.437500.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.437500.npy` | 53b470af |
| `sol_l1kc87Lmacm3b2_D22.468750.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.468750.npy` | 87920481 |
| `sol_l1kc87Lmacm3b2_D22.500000.npy` | raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.500000.npy` | 78956b39 |
| `sol_l1kc87Lmacm3c_D22.562500.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.562500.npy` | 59a086a6 |
| `sol_l1kc87Lmacm3c_D22.625000.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.625000.npy` | 5bdce8b0 |
| `sol_l1kc87Lmacm3c_D22.687500.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.687500.npy` | 53749cf7 |
| `sol_l1kc87Lmacm3c_D22.750000.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.750000.npy` | 4e60e44d |
| `sol_l1kc87Lmacm3c_D22.812500.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.812500.npy` | 75df3e97 |
| `sol_l1kc87Lmacm3c_D22.875000.npy` | raw `I1025-macm3/kc87_leg2/c/sol_l1kc87Lmacm3c_D22.875000.npy` | b1e4f8ca |
| `sol_l1kc87Lmacm3c2_D22.937500.npy` | raw `I1025-macm3/kc87_leg2/c2/sol_l1kc87Lmacm3c2_D22.937500.npy` | 5d759685 |
| `sol_l1kc87Lmacm3c2_D23.000000.npy` | raw `I1025-macm3/kc87_leg2/c2/sol_l1kc87Lmacm3c2_D23.000000.npy` | bb32ff05 |
| `sol_l1kc87Lmacm3ctl_D21.281250.npy` | raw `I1025-macm3/kc87_leg2/ctl/sol_l1kc87Lmacm3ctl_D21.281250.npy` | 31e8737c |
| `sol_l1kc87Lmacm3ctl_D21.312500.npy` | raw `I1025-macm3/kc87_leg2/ctl/sol_l1kc87Lmacm3ctl_D21.312500.npy` | 3cc59721 |
| `sol_l1kc87Lmacm3ctl_D21.343750.npy` | raw `I1025-macm3/kc87_leg2/ctl/sol_l1kc87Lmacm3ctl_D21.343750.npy` | 3acc7233 |
| `sol_l1kc87Lmacm3ctl_D21.375000.npy` | raw `I1025-macm3/kc87_leg2/ctl/sol_l1kc87Lmacm3ctl_D21.375000.npy` | 7f602409 |
| `sol_l1kc87Lmacm3_D21.312500.npy` | raw `I1025-macm3/kc87_leg2/sol_l1kc87Lmacm3_D21.312500.npy` | 2c47f756 |
| `sol_l1kc87Lmacm3_D21.375000.npy` | raw `I1025-macm3/kc87_leg2/sol_l1kc87Lmacm3_D21.375000.npy` | eb7d29d7 |
| `sol_l1kc87Lmacm3_D21.437500.npy` | raw `I1025-macm3/kc87_leg2/sol_l1kc87Lmacm3_D21.437500.npy` | 8477c297 |
| `sol_l1kc87Lmacm3_D21.500000.npy` | raw `I1025-macm3/kc87_leg2/sol_l1kc87Lmacm3_D21.500000.npy` | 99759238 |
| `sol_l1kc127dh370d22875_D22.8750.npy` | raw `I1025-dh370/kc127_d22875/sol_l1kc127dh370d22875_D22.8750.npy` | 43bbf313 |
| `sol_l1kc127wind23_D23.0000.npy` | raw `I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy` | 7a1b150c |
| `sol_l1kc127macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc127_d230625/in/sol_l1kc127macm3d230625_D23.0625.npy` | 7aae10c6 |
| `sol_l1kc127Lmacm3_D23.1250.npy` | raw `I1025-macm3/kc127_leg/states/sol_l1kc127Lmacm3_D23.1250.npy` | e1dccb3c |
| `sol_l1kc135win2d23_D23.0000.npy` | raw `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy` | cd134e2c |
| `sol_l1kc135macm3d230625_D23.0625.npy` | raw `I1025-macm3/kc143_d230625/in/sol_l1kc135macm3d230625_D23.0625.npy` | a6253940 |
| `sol_l1kc135macm3d23125_D23.1250.npy` | raw `I1025-macm3/kc135_d23125/in/sol_l1kc135macm3d23125_D23.1250.npy` | ac01e477 |
