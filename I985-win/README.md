# I985-win: the deep directions of the RT Jacobian at D 40.02 counted from the rough x (T1), and the null direction against D at 35 and 20 (T2), rt_sigma --save_x and rt_xcount (#985, from #983)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/985 (coordinator's plan, P7 stage 1, commands from #983 comment 6995620189). Status: **done** 2026-11-19 03:26:12 UTC, T1 reads **(H4) with k = 3/2 as well**, T2 reads **(H4)** by the rules below (result at the end of this file).

## Question

#983 (xfchecks) excluded (HP), (HN) and (HC) from the stored chords, leaving (H4), the scalar's horizon branch at its lowest harmonic k = 1/2 (one complex amplitude, two real directions, or four with k = 3/2), and (H2), lambda_2's branch as the second chord.
T1 counts the deep directions directly: `rt_sigma.py --save_x` stores each rough start's x, `rt_xcount.py` takes the SVD of the x block and gives d, the gap, and the chords' shares. T2 checks that a null direction appears where T0d puts the k = 1/2 branch below the floor (D 34.99) and is absent where it is above (D 20.04).

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i985`, detached at main `c6c1ee6a` (rt_sigma --save_x, rt_xcount). origin/main is `c80355df`, `solver/rt` has no change between the two |
| S_c (T1) | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| chords (T1) | A = `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (a6b9a729), B = `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (b048df8c) |
| S_35 (T2) | `I145-mac/fol/fol_32x121_D34.9933_32x121.npz` (D 34.993266, K 0, sha256 prefix 5c5523af, max abs F 6.38e-31 from the comment) |
| S_20 (T2) | `I105-mac/controls/res_32x121_D20.0437_D20.0437_32x121.npz` (D 20.043653, K 0, sha256 prefix 93a7d6b2, max abs F 9.76e-31 from the comment) |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I969-win/` for rt_sigma, `python -I` for rt_xcount and rt_perturb |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12 [--save_x X.npz]`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each |

The T2 roots are single stored states, so T2's moves are #963's seeded random move (rt_perturb seed 977), 1e-20 of max|z| at D 34.99 and 1e-26 at D 20.04 (at D 40 a 1e-20 move lifted the bound to 5.5e-24, above the gain (H4) predicts at D 20).

## Readings (the issue's, fixed before the first run)

m is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #972), m0 the unmoved root's.

- **Control:** T1's 12 `start i:` lines equal #951's first 12 (`I951-win/logs/K0c_D40_rough.log`) in every character. This also shows `--save_x` leaves the output unchanged. I compare the 12 `start i, x / max|x|:` lines the same way and report both. A mismatch stops the work before T2.
- **T1 (D 40.02), d is the number of singular values within 1e-4 of the top, the gap s_(d+1)/s_d is clean at 1e-3 or below:**
  - d = 1 with a clean gap reads (H2). d = 2 reads (H4) at k = 1/2. d = 4 reads (H4) with k = 3/2 as well.
  - d = 3, d at least 5, or no clean gap reads "none fits".
  - For d at least 2 the chords a - c and b - c must lie in span(p_1 .. p_d) with share at least 0.99 (the smaller of the two is used). Below 0.9 the deep directions are not the root set's. Between 0.9 and 0.99 the issue gives no rule and I report it as "between".
- **T2 at D 34.993266:** (H4) predicts d at least 2 (from T2_35's own rough starts) and a null direction at the root, m(1e-20) at least 100 m0.
- **T2 at D 20.043653:** (H4) predicts no null direction, m(1e-26) / m0 in [1/3, 3], and the best bound in [1e-32, 2e-22]. The issue does not say whose best bound. I apply it to the unmoved root's run (T2_20) and print the moved run's too, and if they fall on different sides of the interval I say so and do not choose.
- T2 reads (H4) if both T2 conditions hold. A run that does not print all 12 bounds (cap) cannot be read and is reported as incomplete.

Reported per run: d, the gap, the shares, m, products per start, cap hits (products at the `--max_products` default 250), best bound, printed max|F|, start 0's mu share of x.

## Commands, in order

```
python -I rt_xcount.py --selftest                                  # exit 0
python -I rt_xcount.py --selftest --mutate=transpose               # exit 1
rt_launch.py rt_sigma.py --planted --deep 2 --save_x planted\p2.npz  # exit 0
python -I rt_xcount.py planted\p2.npz --expect 2                   # exit 0
rt_launch.py rt_sigma.py --planted --deep 4 --save_x planted\p4.npz  # exit 0
python -I rt_xcount.py planted\p4.npz --expect 4                   # exit 0
python -I rt_xcount.py planted\p2.npz --expect 4                   # exit 1 (the control)
rt_launch.py rt_sigma.py S_c --rough --starts 12 --save_x x\T1_c.npz          # T1, about 40 min
python -I rt_xcount.py x\T1_c.npz --root S_c --chords A,B --out x\T1_c.json
python -I rt_perturb.py S_35 states\m35_d1e-20.npz --delta 1e-20              # seed 977, as #963
rt_launch.py rt_sigma.py S_35 --rough --starts 12 --save_x x\T2_35.npz        # T2, about 40 min each
rt_launch.py rt_sigma.py states\m35_d1e-20.npz --rough --starts 12
python -I rt_xcount.py x\T2_35.npz --out x\T2_35.json
python -I rt_perturb.py S_20 states\m20_d1e-26.npz --delta 1e-26
rt_launch.py rt_sigma.py S_20 --rough --starts 12 --save_x x\T2_20.npz
rt_launch.py rt_sigma.py states\m20_d1e-26.npz --rough --starts 12
python -I rt_xcount.py x\T2_20.npz --out x\T2_20.json
```
`run_985.py` runs these in this order (a failed check or an unexpected exit stops with 7, a control mismatch with 8, a cap kills one run and the next still starts), `table_985.py` reads the logs and the `.json` files.

## Files

| file | content |
|---|---|
| `run_985.py` | the sequential driver, 18 steps in the order of #983's commands (checks block, T1, the control, T2), `--selftest` |
| `table_985.py`, `table_985.txt` | tables and the readings by the rules above, `--selftest` with planted logs (every branch of T1, T2 at 35 and 20, mutated bars, the control against a perturbed log) |
| `start_985.cmd` | detached BelowNormal launcher |
| `states/m35_d1e-20.npz`, `states/m20_d1e-26.npz` | the two moved states (rt_perturb, seed 977) |
| `x/T1_c.npz`, `x/T2_35.npz`, `x/T2_20.npz` | `--save_x` output (5.25 MB each), `x/*.json` the rt_xcount results |
| `planted/p2.npz`, `planted/p4.npz` | the checks block's planted x files |
| `logs/` | one `.log` and `.exit` per step, `run_985.log`, `run_985.exit`, `selftests.log`, `sha256.txt` (the five input states) |

## Result

Started 2026-11-19 00:58:36 UTC (`start_985.cmd`), all 18 steps ended as wanted, driver exit 0 at 03:26:12 UTC (2 h 28 min: T1 2362 s, T2_35 2102 s, m35_d1e-20 1932 s, T2_20 1171 s, m20_d1e-26 1171 s). Nothing else of mine ran.
The old session's waiters did not report here after a relaunch, so the end was read from `logs/run_985.log`, `logs/run_985.exit` and the process list (nothing running).

**Checks block (#983's), every exit as wanted:** `rt_xcount --selftest` 0, `--mutate=transpose` 1 (the chords' share 0.053 and 0.082), planted `--deep 2` and `--expect 2` 0 and 0, `--deep 4` and `--expect 4` 0 and 0, `p2 --expect 4` 1 (the control).
**Control:** T1's 12 `start i:` lines and its 12 `start i, x / max|x|:` lines equal #951's first 12 (`I951-win/logs/K0c_D40_rough.log`) in every character, so `--save_x` leaves the output unchanged here.

| run | state | printed max abs F | m (median of 12) | best bound | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|
| T1_c | D 40.020065, sample c, K 0 | 6.91e-31 | 1.4800e-35 | 4.997e-36 | 67 (one start 73) | 0 of 12 | +1.00 |
| T2_35 | D 34.993266, root | 6.38e-31 | 5.8511e-34 | 1.963e-34 | 61 | 0 of 12 | +1.00 |
| m35_d1e-20 | the root moved by 1e-20 | 2.52e-18 | 7.5647e-23 | 3.022e-23 | 56 | 0 of 12 | +0.0036 |
| T2_20 | D 20.043653, root | 9.76e-31 | 6.3315e-24 | 2.594e-24 | 34 | 0 of 12 | +0.469 |
| m20_d1e-26 | the root moved by 1e-26 | 2.24e-24 | 6.3280e-24 | 2.591e-24 | 34 | 0 of 12 | +0.470 |

The 12 bounds of each run are in `table_985.txt`. Their best-to-worst spread is a factor 105.5, 11.6, 7.6, 6.1 and 6.1. The worst max|J x - v| is 8.6e-16, 1.6e-19, 4.9e-31, 9.3e-31 and 9.1e-31.

| x file | d | gap s_(d+1)/s_d | chord shares in span(p_1..p_d) | s_j / s_1, j = 1 to 6 |
|---|---|---|---|---|
| T1_c | 4 | 1.88e-04 (clean) | a - c 1.000000, b - c 1.000000 | 1.0, 9.5e-04, 2.9e-04, 1.0e-04, 2.0e-08, 1.0e-08 |
| T2_35 | 2 | 4.52e-04 (clean) | none (single root) | 1.0, 7.0e-02, 3.2e-05, 1.2e-05, 3.6e-09, 1.9e-09 |
| T2_20 | 2 | 1.22e-04 (clean) | none (single root) | 1.0, 3.8e-01, 4.6e-05, 2.1e-05, 5.4e-08, 2.9e-08 |

**Readings by the pre-set rules:**

| reading | measured | rule | result |
|---|---|---|---|
| T1 (D 40.02) | d = 4, gap 1.88e-04, smaller chord share 1.0000 | d = 4 clean reads (H4) with k = 3/2 as well; chords in span at 0.99 | **(H4) with k = 3/2 as well** |
| T2 at D 34.993266, d | 2 | at least 2 | holds |
| T2 at D 34.993266, null direction | m(1e-20) / m0 = 7.5647e-23 / 5.8511e-34 = 1.293e+11 | at least 100 | holds |
| T2 at D 20.043653, m(1e-26) / m0 | 6.3280e-24 / 6.3315e-24 = 0.9994 | in [1/3, 3] | holds |
| T2 at D 20.043653, best bound | root 2.594e-24, moved 2.591e-24 | in [1e-32, 2e-22] | holds for both, so no split |
| T2 as a whole | both conditions hold | | **reads (H4)** |

Observations beyond the rules:
- T1's fourth singular value is 1.04e-4 of the top, 4% above the 1e-4 cutoff of the count, and the clean gap (5.3e3) is between the fourth and fifth. A cutoff above 1.04e-4 would give d = 3 with the gap s_4 / s_3 = 0.36, not clean, which the rule reads as "none fits". The count d = 4 therefore rests on the cutoff, while the 5.3e3 drop from the fourth to the fifth does not depend on it. The chord shares are 1.000000 to six digits for d = 4 of 13665 dimensions.
- d = 2 holds at D 20.04 as well (gap 1.2e-4, s_2 / s_1 = 0.38), and at D 34.99 (s_2 / s_1 = 0.070). The count does not tell the two apart. The issue's rule at D 20 uses the moved to unmoved ratio and the best bound, not d, and the null direction is what differs: the 1e-20 move at D 35 lifts the median 1.3e11 times, the 1e-26 move at D 20 by 0.06%, the 12 bounds equal to three or four digits start by start (6.560e-24 against 6.556e-24 at start 0).
- m0 at D 40.02, 34.99 and 20.04 is 1.48e-35, 5.85e-34 and 6.33e-24. The 1e-20 move at D 35 reads 7.6e-23 against #963's 5.46e-24 at D 40 (printed max|F| 2.52e-18 against 3.36e-18).
- rt_xcount's gain estimates of the deep directions are 7.7e-38 (T1 direction 1), 4.0e-36 (T2_35) and 2.8e-26 (T2_20), which is 65, 49 and 93 times below each run's best max-norm bound. They are 2-norm estimates good to a factor of a few by design, and a factor like sqrt(13665) = 117 between the norms would give this, I did not check it further. The exact bounds are rt_sigma's.
- The D 20 moved run's printed max|F| is 2.24e-24 and the unmoved bound's median 6.3e-24: at this size the move and the bound are of the same order in F, and the bound did not move.

