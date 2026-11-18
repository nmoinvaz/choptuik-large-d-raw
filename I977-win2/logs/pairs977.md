| zero | A | w/w_inf | estimate | centre solves | centre noise |
|---|---|---|---|---|---|
| Z13e #975 rtol 1e-13, end-state repeats | 2.719240421 | 1.000025476 | 4.08e-06 | 2 | 0.016 |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | 2.719242554 | 1.000025865 | 4.59e-06 | 2 | 0.016 |
| Z14a #976 rtol 1e-14, seed 976 | 2.719232205 | 1.000022996 | 7.71e-06 | 2 | 0.028 |
| Z14b run 1 alone: rtol 1e-14, seed 977 | 2.719237695 | 1.000026145 | 5.60e-06 | 2 | 0.020 |
| Z14c #976 + run 1 centres (3 distinct), run 1 offsets | 2.719234224 | 1.000024742 | 9.12e-06 | 3 | 0.032 |
| Z14c' same centres, #976 offsets | 2.719234100 | 1.000024630 | 9.03e-06 | 3 | 0.032 |
| Z14c+dup same with the duplicate solve counted twice | 2.719235107 | 1.000024650 | 9.18e-06 | 4 | 0.032 |
| rpi5 #965 rtol 1e-13 (printed values only) | 2.719236000 | 1.000028000 | 5.80e-06 | 2 | 0.021 |

| zero i | zero j | dA | dw | distance | in est i | in est j | in est i + est j | within the sum |
|---|---|---|---|---|---|---|---|---|
| Z13e #975 rtol 1e-13, end-state repeats | Z13p run 2: rtol 1e-13, perturbed seed 976 | -2.13e-06 | -3.89e-07 | 2.17e-06 | 0.53 | 0.47 | 0.25 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | Z14a #976 rtol 1e-14, seed 976 | +8.22e-06 | +2.48e-06 | 8.58e-06 | 2.10 | 1.11 | 0.73 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | Z14b run 1 alone: rtol 1e-14, seed 977 | +2.73e-06 | -6.69e-07 | 2.81e-06 | 0.69 | 0.50 | 0.29 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | Z14c #976 + run 1 centres (3 distinct), run 1 offsets | +6.20e-06 | +7.34e-07 | 6.24e-06 | 1.53 | 0.68 | 0.47 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | Z14c' same centres, #976 offsets | +6.32e-06 | +8.46e-07 | 6.38e-06 | 1.56 | 0.71 | 0.49 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | Z14c+dup same with the duplicate solve counted twice | +5.31e-06 | +8.26e-07 | 5.38e-06 | 1.32 | 0.59 | 0.41 | yes |
| Z13e #975 rtol 1e-13, end-state repeats | rpi5 #965 rtol 1e-13 (printed values only) | +4.42e-06 | -2.52e-06 | 5.09e-06 | 1.25 | 0.88 | 0.52 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | Z14a #976 rtol 1e-14, seed 976 | +1.03e-05 | +2.87e-06 | 1.07e-05 | 2.34 | 1.39 | 0.87 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | Z14b run 1 alone: rtol 1e-14, seed 977 | +4.86e-06 | -2.80e-07 | 4.87e-06 | 1.06 | 0.87 | 0.48 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | Z14c #976 + run 1 centres (3 distinct), run 1 offsets | +8.33e-06 | +1.12e-06 | 8.41e-06 | 1.83 | 0.92 | 0.61 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | Z14c' same centres, #976 offsets | +8.45e-06 | +1.23e-06 | 8.54e-06 | 1.86 | 0.95 | 0.63 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | Z14c+dup same with the duplicate solve counted twice | +7.45e-06 | +1.21e-06 | 7.55e-06 | 1.65 | 0.82 | 0.55 | yes |
| Z13p run 2: rtol 1e-13, perturbed seed 976 | rpi5 #965 rtol 1e-13 (printed values only) | +6.55e-06 | -2.14e-06 | 6.89e-06 | 1.50 | 1.19 | 0.66 | yes |
| Z14a #976 rtol 1e-14, seed 976 | Z14b run 1 alone: rtol 1e-14, seed 977 | -5.49e-06 | -3.15e-06 | 6.33e-06 | 0.82 | 1.13 | 0.48 | yes |
| Z14a #976 rtol 1e-14, seed 976 | Z14c #976 + run 1 centres (3 distinct), run 1 offsets | -2.02e-06 | -1.75e-06 | 2.67e-06 | 0.35 | 0.29 | 0.16 | yes |
| Z14a #976 rtol 1e-14, seed 976 | Z14c' same centres, #976 offsets | -1.89e-06 | -1.63e-06 | 2.50e-06 | 0.32 | 0.28 | 0.15 | yes |
| Z14a #976 rtol 1e-14, seed 976 | Z14c+dup same with the duplicate solve counted twice | -2.90e-06 | -1.65e-06 | 3.34e-06 | 0.43 | 0.36 | 0.20 | yes |
| Z14a #976 rtol 1e-14, seed 976 | rpi5 #965 rtol 1e-13 (printed values only) | -3.79e-06 | -5.00e-06 | 6.28e-06 | 0.81 | 1.08 | 0.46 | yes |
| Z14b run 1 alone: rtol 1e-14, seed 977 | Z14c #976 + run 1 centres (3 distinct), run 1 offsets | +3.47e-06 | +1.40e-06 | 3.74e-06 | 0.67 | 0.41 | 0.25 | yes |
| Z14b run 1 alone: rtol 1e-14, seed 977 | Z14c' same centres, #976 offsets | +3.60e-06 | +1.51e-06 | 3.90e-06 | 0.70 | 0.43 | 0.27 | yes |
| Z14b run 1 alone: rtol 1e-14, seed 977 | Z14c+dup same with the duplicate solve counted twice | +2.59e-06 | +1.49e-06 | 2.99e-06 | 0.53 | 0.33 | 0.20 | yes |
| Z14b run 1 alone: rtol 1e-14, seed 977 | rpi5 #965 rtol 1e-13 (printed values only) | +1.70e-06 | -1.86e-06 | 2.51e-06 | 0.45 | 0.43 | 0.22 | yes |
| Z14c #976 + run 1 centres (3 distinct), run 1 offsets | Z14c' same centres, #976 offsets | +1.24e-07 | +1.11e-07 | 1.67e-07 | 0.02 | 0.02 | 0.01 | yes |
| Z14c #976 + run 1 centres (3 distinct), run 1 offsets | Z14c+dup same with the duplicate solve counted twice | -8.83e-07 | +9.14e-08 | 8.87e-07 | 0.10 | 0.10 | 0.05 | yes |
| Z14c #976 + run 1 centres (3 distinct), run 1 offsets | rpi5 #965 rtol 1e-13 (printed values only) | -1.78e-06 | -3.26e-06 | 3.71e-06 | 0.41 | 0.64 | 0.25 | yes |
| Z14c' same centres, #976 offsets | Z14c+dup same with the duplicate solve counted twice | -1.01e-06 | -2.01e-08 | 1.01e-06 | 0.11 | 0.11 | 0.06 | yes |
| Z14c' same centres, #976 offsets | rpi5 #965 rtol 1e-13 (printed values only) | -1.90e-06 | -3.37e-06 | 3.87e-06 | 0.43 | 0.67 | 0.26 | yes |
| Z14c+dup same with the duplicate solve counted twice | rpi5 #965 rtol 1e-13 (printed values only) | -8.93e-07 | -3.35e-06 | 3.47e-06 | 0.38 | 0.60 | 0.23 | yes |
