# I963-win: sample c's K = 0 root at D 40.02 moved by a planted 1e-20, 1e-19 and 1e-18, and 12 rough rt_sigma starts at each (#963, is the mu-led weak direction null at the root?)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/963 (coordinator's plan). Status: **done** 2026-11-18 17:35:00 UTC, verdict **NULL AT THE ROOT** by the criteria below (result at the end of this file).

## Question

#951 found the K = 0 rough bounds spread by more than 50 times over three floor-level samples of one root, with residuals within a factor 1.6 and in no common order with the medians.
In every start x is led by mu. If that direction is null at the exact root, its bound measures the distance of a sample from the root along it. Test: move sample c's K = 0 root by a planted, seeded
perturbation of size delta (`solver/rt/rt_perturb.py`, double-double) and read the rough bounds there.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i963`, detached at main `f88adb20` (rt_perturb: an RT state moved off its root by a planted perturbation), `solver/rt` as of that commit |
| S | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (D 40.020065, 32 x 121, K 0), sha256 prefix 0c8f3de8 |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` (adds `multidouble._dd_dot` and `math.fma`, copied from `I951-win/`), `resource.py` (the #701/#951 shim, copied from `I951-win/`, not needed by `rt_sigma.py`) |
| rt_perturb | run in `venv-t151` (`python -I`), not the system python3 |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads (`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=2`), BelowNormal, one run at a time, cap 2 h each |

The perturbation (rt_perturb): z' = z + delta max|z| r in double-double, r independent normal entries from `default_rng(977)` scaled to max|r| = 1, every entry the scalar mu included.

## Pass criteria (the issue's, fixed before the first run)

m(delta) is the median of a run's 12 bounds and m0 the control's. Median of an even count: the geometric mean of the two middle bounds (the convention of #701 to #951, `table_701.median`).

- **Control:** the delta = 0 run's 12 bounds equal #951's first 12 (`I951-win/logs/K0c_D40_rough.log`) in every printed digit. Checked by `run_963.py` on the 12 `start` lines as text, a miss stops the work.
- **Null at the root** if m rises at each step of delta and m(1e-18) >= 100 m0. "Each step" is read as the chain m0 < m(1e-20) < m(1e-19) < m(1e-18); the chain over the three nonzero delta alone is printed too, and a difference between the two readings is flagged.
- **Not null** (an intrinsic small gain) if m(delta) / m0 lies in [1/3, 3] at all three delta.
- **Undecided** otherwise. A run that does not print all 12 bounds (cap) cannot be decided by these criteria and is reported as incomplete.

Reported per run: printed max|F|, the 12 bounds, m, the products per start, the cap hits (products at the `--max_products` default 250), start 0's mu share of x (the `mu` entry of the `start 0, x / max|x|` line).

## Commands, in order

```
python -I solver/rt/rt_perturb.py --selftest                 # exit 0, PASS
python -I solver/rt/rt_perturb.py --selftest --mutate        # exit 1, FAIL (the control)
python -I solver/rt/rt_perturb.py S states/c_d$d.npz --delta $d      # d = 1e-20 1e-19 1e-18   (logs/perturb.log)
python run_963.py                                            # c_d0 (control), then c_d1e-20, c_d1e-19, c_d1e-18, via start_963.cmd
python table_963.py                                          # tables and verdict
```

## Files

| file | content |
|---|---|
| `run_963.py` | the sequential driver (cap, control compare, STOP_963), `--selftest` |
| `table_963.py` | tables and the verdict by the criteria above, `--selftest` with planted logs |
| `start_963.cmd` | detached BelowNormal launcher |
| `states/c_d*.npz` | the three moved states |
| `table_963.txt` | the output of `table_963.py` |
| `logs/` | `perturb.log`, `sha256.txt`, `c_d*.log` and `.exit`, `control.exit`, `run_963.log`, `run_963.exit` |

## Result

Started 2026-11-18 15:14:13 UTC (`start_963.cmd`), all four runs exit 0, driver exit 0 at 17:35:00 UTC (3 h 21 min: control 2362 s, then 2062 s, 2032 s, 1991 s). Nothing else of mine ran, the laptop was otherwise quiet.
`rt_perturb.py --selftest` exit 0, `--selftest --mutate` exit 1, the three moved states realised 1.000000e-20, 1.000000e-19, 1.000000e-18 of max|z| 0.1291061 (`logs/perturb.log`).

**Control: PASS.** The delta 0 run's 12 `start` lines equal #951's first 12 in every printed character, and its printed max|F| is 6.91e-31 as #951's.

**Verdict: NULL AT THE ROOT.** m rises at every step (m0 < m(1e-20) < m(1e-19) < m(1e-18), and over the three nonzero delta alone, so the two readings of "each step" agree) and m(1e-18) / m0 = 2.7e14 >= 100.

| run | delta | printed max abs F | m, median of the 12 bounds | m / m0 | m / delta | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|---|
| c_d0 | 0 | 6.91e-31 | 1.4800e-35 | 1 | - | 67 to 73 (median 67) | 0 of 12 | +1.00e+00 |
| c_d1e-20 | 1e-20 | 3.36e-18 | 5.4593e-24 | 3.689e+11 | 5.5e-04 | 60 (all 12) | 0 of 12 | +2.46e-03 |
| c_d1e-19 | 1e-19 | 3.36e-17 | 2.6809e-22 | 1.811e+13 | 2.7e-03 | 59 (all 12) | 0 of 12 | -1.23e-04 |
| c_d1e-18 | 1e-18 | 3.36e-16 | 4.0592e-21 | 2.743e+14 | 4.1e-03 | 58 (all 12) | 0 of 12 | +2.30e-03 |

The 12 bounds of each run are in `table_963.txt`. Their spread (best to worst, from each log) is a factor 105.5 at delta 0, 181.2 at 1e-20, 13.0 at 1e-19 and 10.7 at 1e-18. The worst max|J x - v| is 8.6e-16 (control) and at most 9.8e-30 in the moved runs.

Observations beyond the criteria:
- At the root x is led by mu in every start (start 0's share +1.00). At every moved state start 0's mu share is 1e-4 to 2e-3, so the mu-led weak direction is no longer the one the solve finds.
- m grows 1.69 decades per decade of delta from 1e-20 to 1e-19 and 1.18 from 1e-19 to 1e-18, so faster than linear at first. The printed max|F| of the moved states is linear in delta (336 delta).
- A flag for the reading, not tested: #951's K 0 roots of a, b and c are 2.1e-21 to 3.5e-21 apart in max-norm (`I951-win/README.md`), yet their bounds sit at 1.5e-35 to 2.6e-33, while a planted random move of 1e-20 already reads 5.5e-24 (m / delta at least 5.5e-04). The differences between the three samples therefore do not act like a random move of that size on the bound; they lie mostly along directions that do not lift the weak direction.
