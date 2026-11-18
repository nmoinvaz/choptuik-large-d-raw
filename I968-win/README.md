# I968-win: sample c's K = 0 root at D 40.02 moved along the line to sample a by 1e-20, 1e-19 and 1e-18, and 12 rough rt_sigma starts at each (#968, does the bound stay at the root's level along the line?)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/968 (coordinator's plan, follows #963). Status: **done** 2026-11-18 20:48:28 UTC, verdict **ALONG A FAMILY** by the criteria below (result at the end of this file).

## Question

#963 found the mu-led weak direction null at the root: sample c moved by a random delta = 1e-20 of max|z| reads a median bound of 5.46e-24 against 1.48e-35 at the root. Yet samples a and c are
1.7e-20 of max|z| apart (2.189e-21 in max-norm, `I951-win/README.md`) and both read 1e-35 to 1e-34. If the solves land on a family of roots, their difference lies along it, and a move along that line stays
near the root's level. Test: move c along the line through a, `rt_perturb.py --along`, and read the rough bounds.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i968`, detached at main `d96a09a1` (rt_perturb: --along). `solver/rt` differs from #963's `f88adb20` only in `rt_perturb.py` |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| A | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` (sample a, K 0), sha256 prefix a6b9a729, the live raw clone's copy equals the push worktree's |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I963-win/` |
| rt_perturb | run in `venv-t151` (`python -I`), not the system python3 |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each |

The move (rt_perturb --along): z' = z + delta max|z| r in double-double, r = (z_A - z_C) formed in double-double and scaled to max|r| = 1. delta = 1.7e-20 would land on a itself, so 1e-20 lies between the two
samples and 1e-19 and 1e-18 run past a along the same line.

## Pass criteria (the issue's, fixed before the first run)

m(delta) is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #963). m_rand(delta) is #963's at the same delta: 5.46e-24 (1e-20), 2.68e-22 (1e-19), 4.06e-21 (1e-18)
(`I963-win/README.md`, precisely 5.4593e-24, 2.6809e-22, 4.0592e-21).

- **Along a family** if m(1e-20) and m(1e-19) are both at most 1e-3 m_rand at the same delta.
- **Not along a family** if m(delta) / m_rand(delta) lies in [0.1, 10] at both (1e-20 and 1e-19).
- **Undecided** otherwise. m(1e-18) and its ratio are reported as well (a curved family would let the bound grow past a).
- An incomplete run (fewer than 12 bounds, a cap) cannot be decided by these criteria and is reported as incomplete.

Reported per run: printed max|F|, the 12 bounds, m, products per start, cap hits (products at the `--max_products` default 250), start 0's mu share of x (the `mu` entry of the `start 0, x / max|x|` line).
No delta = 0 control run is part of the plan: the root's own rough bounds are #963's control (12 of 12 start lines equal #951's).

## Commands, in order

```
python -I solver/rt/rt_perturb.py --selftest --along            # exit 0, PASS
python -I solver/rt/rt_perturb.py --selftest --along --mutate   # exit 1, FAIL (the control)
python -I solver/rt/rt_perturb.py C states/c_along_d$d.npz --delta $d --along A      # d = 1e-20 1e-19 1e-18   (logs/perturb.log)
python run_968.py                                              # the three runs, one at a time, via start_968.cmd
python table_968.py                                            # tables and verdict
```

## Files

| file | content |
|---|---|
| `run_968.py` | the sequential driver (cap, STOP_968), `--selftest` |
| `table_968.py`, `table_968.txt` | tables and the verdict by the criteria above, `--selftest` with planted logs (every branch, a mutated bar, #963's medians re-read from `I963-win/logs`) |
| `landing_968.py`, `logs/landing.log` | a check of `--along` on the real samples: delta = the a - c distance lands on a |
| `collinear_968.py`, `logs/collinear.log` | read-only, no run: are the stored K 0 samples a, b, c collinear? (not part of the criteria) |
| `start_968.cmd` | detached BelowNormal launcher |
| `states/c_along_d*.npz` | the three moved states |
| `logs/` | `perturb.log`, `sha256.txt`, `c_along_d*.log` and `.exit`, `run_968.log`, `run_968.exit`, `landing.log`, `collinear.log` |

## Result

Started 2026-11-18 18:53:03 UTC (`start_968.cmd`), all three runs exit 0, driver exit 0 at 20:48:28 UTC (1 h 55 min: 2312 s, 2312 s, 2302 s). Nothing else of mine ran.
`rt_perturb.py --selftest --along` exit 0 (cosine with the planted difference 1.000000000), `--selftest --along --mutate` exit 1. The three moved states realised 1.000000e-20, 1.000000e-19, 1.000000e-18 of max|z| 0.1291061,
along C to A with max|A - C| / max|z| = 1.695756e-20 (the issue's 1.7e-20). `landing_968.py`: delta = that distance lands on A to 1.366e-37 of max|z| (8e-18 of the distance), and the cosine of each moved state's
shift with z_A - z_C is 1.000000000000.

**Verdict: ALONG A FAMILY.** m(1e-20) and m(1e-19) are 1.4e-10 and 1.8e-11 of m_rand at the same delta, the bar is 1e-3.

| run | delta | printed max abs F | m (median of 12) | m_rand (#963) | m / m_rand | products per start | starts at the 250 cap | start 0 mu share of x |
|---|---|---|---|---|---|---|---|---|
| c_along_d1e-20 | 1e-20 | 1.09e-30 | 7.6733e-34 | 5.4593e-24 | 1.406e-10 | 67 (all 12) | 0 of 12 | -1.00 |
| c_along_d1e-19 | 1e-19 | 5.20e-30 | 4.7540e-33 | 2.6809e-22 | 1.773e-11 | 67 (all 12) | 0 of 12 | +0.893 |
| c_along_d1e-18 | 1e-18 | 5.51e-29 | 1.6601e-32 | 4.0592e-21 | 4.09e-12 | 67 (all 12) | 0 of 12 | -0.259 |

The 12 bounds of each run are in `table_968.txt`. Their best-to-worst spread is a factor 10.8, 13.0 and 50.0. The worst max|J x - v| is 5.8e-19, 1.0e-20 and 2.1e-20. m_rand's constants are #963's medians, re-read from
`I963-win/logs/c_d*.log` by the table's selftest (equal to 5 digits).

The bound along the line, same 12 right-hand sides throughout (a's row is #943's first 12 bounds, `I943-win/logs/K0_D40_rough.log`, printed max|F| from its first line):

| point on the line | position (distance from c over the a - c distance) | printed max abs F | m |
|---|---|---|---|
| c | 0 | 6.91e-31 | 1.480e-35 |
| delta 1e-20 | 0.59 | 1.09e-30 | 7.673e-34 |
| a | 1 | 4.39e-31 | 2.463e-34 |
| delta 1e-19 | 5.9 | 5.20e-30 | 4.754e-33 |
| delta 1e-18 | 59 | 5.51e-29 | 1.660e-32 |

Observations beyond the criteria:
- The bound moves along the line but stays at 1e-35 to 1e-32, against 5e-24 to 4e-21 for the random move of the same size. It is not monotone between c and a (c 1.5e-35, delta 1e-20 7.7e-34, a 2.5e-34), and past a it grows 0.79 and 0.54 decades per decade of delta, which is m(1e-18) = 1.66e-32, 1.1e3 times c's. The spread of #951's three samples (a 2.7e-34, b 2.6e-33, c 1.5e-35) lies inside this range.
- The printed max|F| rises with delta past a, 5.2e-30 at 1e-19 and 5.5e-29 at 1e-18, about 5e-11 per unit delta (5.5e-11 at 1e-18), against 336 per unit delta for the random move (#963). Start 0's mu share of x is -1.00 at 1e-20 and 0.89 at 1e-19, so x stays mu-led there, and drops to -0.26 at 1e-18 where the bound has grown.
- `collinear_968.py` (read-only, stored states, no run): the K 0 samples are not collinear. max|a - c|, |b - c|, |a - b| are 1.70e-20, 2.71e-20, 1.62e-20 of max|z|, the cosine of (a - c) and (b - c) is 0.2337, and b - c = 1.107 (a - c) + a part that is 97% of b - c in 2-norm (61% in max-norm). So b does not lie on the line through c and a. Whether b lies on the same family (a surface, not a line) is not tested by this issue's runs.
