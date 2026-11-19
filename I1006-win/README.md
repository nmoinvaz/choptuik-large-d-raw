# I1006-win: the deep-direction count (rt_sigma --save_x, rt_xcount) at D 40.02 at samples a and b with 12 rough starts and at sample c with 24 (#1006, from #985)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1006 (coordinator's plan, P7 stage 1, follows #985). Status: **done** 2026-11-19 09:09 UTC, (H4) at k = 1/2 and 3/2 holds (d = 4 at all three samples).

## Question

#985 counted d = 4 deep directions at sample c with a clean gap (5.3e3 after the fourth singular value), the reading (H4) at k = 1/2 and 3/2. The fourth singular value is 1.04e-4 of the first, 4% above the count's 1e-4 cutoff.
If d is a property of the root set it must come out the same at the other samples and with more starts. T1 at sample a, at sample b (12 starts each) and at sample c with 24 starts.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i985` (made for #985), detached at main `c6c1ee6a` (rt_sigma --save_x, rt_xcount). origin/main is `92a6c284` now, `solver/rt` has no change between the two (`git diff --stat c6c1ee6a origin/main -- solver/rt` is empty), so the worktree is not moved |
| A | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (sample a, K 0, D 40.020065, 32 x 121), sha256 prefix a6b9a729 |
| B | `I701-win/solves/k0b_D40_mutnorows_D40.0201_32x121.npz` (sample b, K 0), sha256 prefix b048df8c |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0), sha256 prefix 0c8f3de8 |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I985-win/` for rt_sigma, `python -I` for rt_xcount |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts N --save_x X.npz`, N = 12 at a and b, 24 at c, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each |

The rough right-hand sides are the same for every state (default_rng(163), as #943, #701, #951, #985), so the first 12 starts of c are #985's and #951's.
Expected run time: about 39 min for 12 starts, so about 79 min for 24, and about 2 h 40 min in all.

## Acceptance (the issue's, fixed before the first run)

d is the number of singular values of the x block within 1e-4 of the top (rt_xcount), the gap is s_(d+1) / s_d, clean at 1e-3 or below.

- **(H4) at k = 1/2 and 3/2 holds** if all three runs give d = 4 with a clean gap (s_5 / s_4 at most 1e-3) and chord shares at least 0.99 (for each run the smaller of its two chords, the two other samples minus the root).
- **Reopened** if any of the three gives d = 3 or d at least 5.
- Anything else (d = 4 with a gap above 1e-3 or a share below 0.99, or d of 1 or 2) does not hold the reading. The issue gives no word for it and I report it as "does not hold".
- A run that does not print its N bounds (cap) cannot be read and is reported as incomplete.

Reported per run: d, the gap, the singular values s_1 to s_6 (and to s_8) relative to s_1, with s_4 / s_1 and s_5 / s_1 against the 1e-4 cutoff so its margin is visible, the chord shares, printed max|F|, m (median of the bounds, geometric mean of the two middle ones for an even count), the best bound, products, cap hits, start 0's mu share of x.
Informational, not part of the acceptance: the first 12 (24 at c) `start i:` lines and `start i, x / max|x|:` lines against the stored rough logs of the same state (`I943-win/logs/K0_D40_rough.log` for a, `I701-win/logs/K0b_D40_rough.log` for b, `I951-win/logs/K0c_D40_rough.log` for c), once in every character and once on max|x|, the bound and the products only (the residual column can depend on the BLAS threads).

## Commands, in order

```
python -I rt_xcount.py --selftest                                  # exit 0
python -I rt_xcount.py --selftest --mutate=transpose               # exit 1
rt_launch.py rt_sigma.py A --rough --starts 12 --save_x x\T1_a.npz
python -I rt_xcount.py x\T1_a.npz --root A --chords B,C --out x\T1_a.json
rt_launch.py rt_sigma.py B --rough --starts 12 --save_x x\T1_b.npz
python -I rt_xcount.py x\T1_b.npz --root B --chords A,C --out x\T1_b.json
rt_launch.py rt_sigma.py C --rough --starts 24 --save_x x\T1_c24.npz
python -I rt_xcount.py x\T1_c24.npz --root C --chords A,B --out x\T1_c24.json
```
`run_1006.py` runs these in this order (an unexpected exit stops with 7, a cap kills one run and the next still starts, driver exit 5), `table_1006.py` reads the logs and the `.json` files.

## Files

| file | content |
|---|---|
| `run_1006.py` | the sequential driver, 8 steps in the order above, `--selftest` |
| `table_1006.py`, `table_1006.txt` | tables and the reading by the acceptance above, `--selftest` (mutated bars for the gap, the shares, d = 4 and the reopen conditions, the control comparison) |
| `start_1006.cmd`, `rt_launch.py`, `resource.py` | detached BelowNormal launcher, the multidouble and fma shim, the `resource` shim (copied from `I985-win/`) |
| `x/T1_a.npz`, `x/T1_b.npz`, `x/T1_c24.npz` | `--save_x` output (5.25, 5.25 and 10.5 MB), `x/*.json` the rt_xcount results |
| `logs/` | one `.log` and `.exit` per step, `run_1006.log`, `run_1006.exit`, `selftests.log`, `sha256.txt` (the three input states) |

## Result

Started 2026-11-19 06:34:43 UTC (`start_1006.cmd`), all 8 steps ended as wanted, driver exit 0 at 09:09:21 UTC (2 h 35 min: T1_a 2322 s, T1_b 2332 s, T1_c24 4573 s, each rt_xcount 10 s). Nothing else of mine ran.

**Reading by the pre-set acceptance: (H4) at k = 1/2 and 3/2 holds.** All three give d = 4 with a clean gap and chord shares of 1.000000.

| run | sample | starts | d | gap s_5 / s_4 (at most 1e-3) | smaller chord share (at least 0.99) | result |
|---|---|---|---|---|---|---|
| T1_a | a, D 40.020065 | 12 | 4 | 1.95e-04 | 1.000000 | holds |
| T1_b | b | 12 | 4 | 1.98e-04 | 1.000000 | holds |
| T1_c24 | c | 24 | 4 | 1.56e-04 | 1.000000 | holds |

Singular values of the x block relative to s_1 (the cutoff is 1e-4 s_1, so the last two columns are the margin):

| run | s_2 | s_3 | s_4 | s_5 | s_6 | s_4 / 1e-4 | s_5 / 1e-4 |
|---|---|---|---|---|---|---|---|
| T1_a | 2.32e-02 | 3.47e-03 | 1.28e-03 | 2.50e-07 | 1.28e-07 | 12.8 | 2.5e-03 |
| T1_b | 4.87e-01 | 6.72e-02 | 2.33e-02 | 4.62e-06 | 2.37e-06 | 233 | 4.6e-02 |
| T1_c24 | 1.11e-03 | 2.95e-04 | 1.54e-04 | 2.41e-08 | 1.63e-08 | 1.54 | 2.4e-04 |
| T1_c, 12 starts (#985) | 9.5e-04 | 2.9e-04 | 1.04e-04 | 2.0e-08 | 1.0e-08 | 1.04 | 2.0e-04 |

Chord shares in span(p_1..p_4): a gives b - a and c - a 1.000000 and 1.000000, b gives a - b and c - b 1.000000 and 1.000000, c gives a - c and b - c 1.000000 and 1.000000.

| run | printed max abs F | m (median of the bounds) | best bound | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|
| T1_a | 4.39e-31 | 2.4630e-34 | 9.136e-35 | 67 | 0 of 12 | +1.00 |
| T1_b | 5.12e-31 | 2.4165e-33 | 8.570e-34 | 67 | 0 of 12 | +1.00 |
| T1_c24 | 6.91e-31 | 1.7063e-35 | 4.997e-36 | 67 (one 73) | 0 of 24 | +1.00 |

The bounds of each start are in `table_1006.txt`. Their best-to-worst spread is a factor 15.5, 6.9 and 105.5. The worst max|J x - v| is 2.5e-18, 4.4e-19 and 8.6e-16.

**Informational control:** the 12 (a, b) and 24 (c) `start i:` lines and `start i, x / max|x|:` lines equal the stored rough logs of the same state in every character (I943-win K0_D40_rough.log for a, I701-win K0b_D40_rough.log for b, I951-win K0c_D40_rough.log for c). So `--save_x` and the 2-thread BelowNormal setup leave the output unchanged here, and c's first 12 are #985's.

Observations beyond the acceptance:
- The fourth singular value sits 12.8 times above the cutoff at a, 233 times at b and 1.54 times at c with 24 starts (1.04 times with 12). At c the margin is still thin. A cutoff above s_4 would give d = 3 with s_4 / s_3 = 0.37 (a), 0.35 (b) and 0.52 (c), not clean, which the rule reads as "none fits".
- The drop from s_4 to s_5 does not depend on the cutoff. It is 5.1e3, 5.0e3 and 6.4e3, and it is the largest ratio s_j / s_(j+1) among j = 1 to 10 in all three. The next largest is s_6 / s_7 = 500 (a, b) and 772 (c).
- 24 starts at c do not add a fifth direction. s_5 / s_1 is 2.4e-8 against 2.0e-8 with 12, and s_7 to s_24 fall from 2.1e-11 to 5.2e-18 without a step.
- The deep directions' weights differ by sample (s_2 / s_1 is 0.023, 0.49 and 0.0011), but rt_xcount's gain estimates for directions 2 to 6 agree between the samples to a factor of 2.2: 4.2e-35, 2.8e-34, 7.7e-34, 3.9e-30, 7.6e-30 (a), 3.7e-35, 2.7e-34, 7.8e-34, 3.9e-30, 7.6e-30 (b), 8.1e-35, 3.0e-34, 5.8e-34, 3.7e-30, 5.5e-30 (c). Direction 1 differs: 9.8e-37, 1.8e-35, 8.9e-38.
- The ratios s_j / s_(j+1) for j = 5 to 10 are equal to three digits at a and b (1.95, 500, 1.72, 23.2, 2.8, 5.5), so the tail of the x block outside the deep span is the same at the two samples up to one scale (s_5 / s_1 differs by 18.5). I did not investigate it. The rough right-hand sides are the same for every state, which would give this if the Jacobians' non-deep parts agree.
- rt_xcount's gain estimate of direction 1 is 93, 48 and 56 times below each run's best max-norm bound (9.8e-37 against 9.136e-35, 1.8e-35 against 8.570e-34, 8.9e-38 against 4.997e-36), as in #985 (49 to 93). They are 2-norm estimates good to a factor of a few by design, and I did not check the norm factor further.
- d is a count at one D (40.02). #985's T2 gave d = 2 at D 35 and at D 20.
