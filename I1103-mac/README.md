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
