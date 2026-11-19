# I1022-win: how far the out-of-plane tangency extends, sample c's K = 0 root at D 40.02 moved along q0 and q1 and along a random direction by 1e-18 and 1e-17, 12 rough rt_sigma starts at each (#1022, from #1018)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, Windows 11). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1022 (coordinator's plan, P7, follows #1018). Status: **done**, 2026-11-19 12:04 to 15:43 UTC. Reading: **TANGENT at both sizes** (m / m_rand 6e-12 to 1.2e-11 at 1e-18 and 1e-17, bar 1e-3), so q0 and q1 stay tangent out to 1e-17 of max|z|, 370 times the longer chord.

## Question

#1018 found the two deep directions q0, q1 out of the samples' plane tangent at c at 1e-20 and 1e-19 of max|z| (m / m_rand 1.3e-12 to 3.9e-10), so with a - c and b - c all four deep directions are tangent. The printed max|F| along q1 grew linearly in delta (2.34e-29, 2.34e-28), 20 to 77 times the in-plane moves'.
If the root set curves away from its tangent space, a larger move should show it. The same two rows `rt_perturb.py --dir` (rows of `I1018-win/Q_c24.npz`) at 1e-18 and 1e-17, and a random move (seed 977) at each size as that size's own m_rand reference (#963's random medians cover 1e-20, 1e-19 and 1e-18 only), six runs, each read with `rt_sigma.py --rough --starts 12`.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1018` (made for #1018), detached at main `7745882e` (rt_angles --complement, rt_perturb --dir). `git diff --stat 7745882e origin/main -- solver/rt` is empty (origin/main `065b50dc`), so the worktree is not moved |
| C | `I951-win/solves/k0c_D40_mutnorows_D40.0201_32x121.npz` (sample c, K 0, D 40.020065, 32 x 121), sha256 prefix 0c8f3de8 |
| Q | `I1018-win/Q_c24.npz` (`rt_angles.py --complement` of `I1006-win/x/T1_c24.npz` at C with chords a - c and b - c), sha256 prefix 54e91230, copied here unchanged |
| interpreter | `venv-t151` (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0, multidouble 0.1.0), `rt_launch.py` and `resource.py` copied from `I1018-win/` for rt_sigma, `python -I` for rt_perturb |
| rt_sigma | `rt_launch.py <worktree>/solver/rt/rt_sigma.py STATE --rough --starts 12`, cwd `<worktree>/solver/rt`, 2 BLAS threads, BelowNormal, one run at a time, cap 2 h each |

The 12 rough right-hand sides are the same for every state (default_rng(163)). The chords' sizes (max-norm over max|z_C| 0.1291061) are a - c 1.6958e-20 and b - c 2.7086e-20, so 1e-18 is 37 times and 1e-17 is 370 times the longer chord.
#963 already holds a random run at 1e-18 (c_d1e-18, m = 4.0592e-21, 12 of 12 bounds, 58 products). The state made here at 1e-18 with seed 977 is that run's, bit for bit (`check_1022.py`), so the random run at 1e-18 repeats it. It stays in as the issue words it (six runs) and as a control, and the readings use this task's own medians.

## Readings (the issue's, fixed before the first run)

m(row, delta) is a run's median of 12 bounds (geometric mean of the two middle bounds, the convention of #701 to #1018). Per size delta, m_rand(delta) is this task's random-move median at that size, and r = m(row k, delta) / m_rand(delta) for k = 0, 1.

- r at most 1e-3 reads **tangent** at that size.
- r in [0.1, 10] reads **leaving the set**.
- Any other r reads **undecided**.
- A run that does not print all 12 bounds (cap) cannot be decided by these criteria and is reported as incomplete.

The issue gives each rule per ratio. For a whole size I read it as tangent when both rows are tangent, leaving when either row is leaving (which I fixed before the runs), undecided otherwise. The overall line is "tangent at both sizes" when both sizes are tangent.
Reported per run: printed max|F| beside each median, the 12 bounds, m, products per start, cap hits (products at the `--max_products` default 250), start 0's mu share of x.
Checks of the moves themselves from the stored states (read-only, `check_1022.py`, not part of the readings): each directional move's realised size, its parallelism to its row of Q, its part in the plane of a - c and b - c, its part outside the deep span, two control families that must fail, and the random 1e-18 state against #963's.

## Commands, in order

```
python -I rt_perturb.py --selftest --dir                          # exit 0, PASS (first; plain --selftest 0 and --selftest --mutate 1 follow, logs/selftests.log)
python -I rt_perturb.py C states/c_q${k}_d${d}.npz --delta $d --dir Q_c24.npz --dir_k $k      # k = 0 1, d = 1e-18 1e-17 (logs/perturb.log)
python -I rt_perturb.py C states/c_rand_d${d}.npz --delta $d --seed 977                         # d = 1e-18 1e-17
python -I check_1022.py                                           # the moves against the plane, the span and the controls (logs/check.log)
python run_1022.py                                                # the six runs, one at a time, via start_1022.cmd (q0, q1, random at 1e-18, then at 1e-17)
python table_1022.py                                              # tables and the reading
```

## Files

| file | content |
|---|---|
| `README.md` | this file |
| `run_1022.py`, `start_1022.cmd`, `rt_launch.py`, `resource.py` | the driver (six runs one at a time, 2 h cap each), its detached launcher, the launcher of rt_sigma and the `resource` shim for Windows |
| `check_1022.py` | read-only check of the moved states (realised size, parallelism to Q's row, part in the plane of a - c, b - c, part outside the deep span, controls that must fail, random 1e-18 state against #963's) |
| `table_1022.py`, `table_1022.txt` (`table_1022.err` is empty) | the tables below and the readings, from `logs/c_*.log` |
| `Q_c24.npz` | copy of `I1018-win/Q_c24.npz` (sha256 54e91230...) |
| `states/c_{q0,q1,rand}_d{1e-18,1e-17}.npz` | the six moved states (zh, zl) |
| `logs/` | `selftests.log`, `perturb.log`, `check.log`, `sha256.txt`, `run_1022.log` and `.exit`, per run `c_*.log` (rt_sigma output) and `c_*.exit` |

## Result

**TANGENT at both sizes.** At 1e-18 and 1e-17 of max|z| (37 and 370 times the longer chord b - c) both out-of-plane deep directions give m / m_rand between 1.5e-12 and 1.2e-11, eight orders below the 1e-3 bar, and no run is near the leaving band [0.1, 10].

Checks (all passed before the runs, logs in `logs/`):

| check | result |
|---|---|
| `rt_perturb.py --selftest --dir` (first), plain `--selftest`, `--selftest --mutate` | exit 0 (cosine 1.000000000000000), 0, 1 (the mutant fails as it must) |
| `check_1022.py --selftest`, `table_1022.py --selftest`, `run_1022.py --selftest` | all passed |
| the four directional moves, `check_1022.py` | realised size exactly 1e-18 and 1e-17 of max|z|; parallel to their row of Q to 1.0e-14 at most; part in the plane of a - c, b - c at most 1.4e-15; part outside the deep span at most 3.3e-15 |
| controls, same check | #972's sum moves (in the plane) and this task's two random moves (outside the span) fail, as they must |
| random 1e-18 state against `I963-win/states/c_d1e-18.npz` | zh and zl equal bit for bit; the run's 12 bounds, 12 product counts and median 4.0592e-21 equal #963's in every printed digit |
| the six runs | all exit 0, 12 of 12 bounds each, no start at the 250-product cap, 1912 to 2332 s each |

Per run (the 12 bounds of each run are in `table_1022.txt`):

| run | printed max abs F | m (median of 12) | m_rand at this delta | m / m_rand | reading | products per start |
|---|---|---|---|---|---|---|
| q0, 1e-18 | 5.33e-29 | 2.4545e-32 | 4.0592e-21 | 6.05e-12 | TANGENT | 67 |
| q1, 1e-18 | 2.34e-27 | 5.9709e-33 | 4.0592e-21 | 1.47e-12 | TANGENT | 67 |
| random, 1e-18 | 3.36e-16 | 4.0592e-21 | (itself) | | reference (repeats #963) | 58 |
| q0, 1e-17 | 5.33e-28 | 1.3885e-31 | 1.1883e-20 | 1.17e-11 | TANGENT | 66 |
| q1, 1e-17 | 2.34e-26 | 4.8811e-32 | 1.1883e-20 | 4.11e-12 | TANGENT | 66 |
| random, 1e-17 | 3.36e-15 | 1.1883e-20 | (itself) | | reference | 56 |

The extent series (1e-20 and 1e-19 from #963 and #1018's logs, 1e-18 and 1e-17 from this task):

| delta | m_rand | m along q0 | m along q1 | q0 / m_rand | q1 / m_rand | printed max abs F, q0 | printed max abs F, q1 |
|---|---|---|---|---|---|---|---|
| 1e-20 | 5.4593e-24 | 7.3744e-34 | 2.1019e-33 | 1.35e-10 | 3.85e-10 | 1.39e-30 | 2.34e-29 |
| 1e-19 | 2.6809e-22 | 3.9858e-33 | 3.4795e-34 | 1.49e-11 | 1.30e-12 | 5.33e-30 | 2.34e-28 |
| 1e-18 | 4.0592e-21 | 2.4545e-32 | 5.9709e-33 | 6.05e-12 | 1.47e-12 | 5.33e-29 | 2.34e-27 |
| 1e-17 | 1.1883e-20 | 1.3885e-31 | 4.8811e-32 | 1.17e-11 | 4.11e-12 | 5.33e-28 | 2.34e-26 |

Per size, by the rule fixed before the runs (tangent when both rows are): 1e-18 TANGENT (6.05e-12, 1.47e-12), 1e-17 TANGENT (1.17e-11, 4.11e-12). Overall: TANGENT at both sizes.

Observations:
- r stays between 1.3e-12 and 3.9e-10 over four decades of delta (1e-20 to 1e-17), with no upward trend toward the bar. The four-dimensional root set shows no curvature away from its tangent space along q0 and q1 out to 1e-17 of max|z|, 370 times the longer chord.
- m along each direction grows with delta, q0 by 188 and q1 by 23 from 1e-20 to 1e-17 (q0 about 5.4, 6.2, 5.7 per decade, q1 0.17, 17, 8.2). The random move's m grows 2177 times over the same range (49, 15, 2.9 per decade), flattening. So r is nearly constant because the random reference flattens while the directional m keeps rising slowly. The q1 dip at 1e-19 (0.78 decade below 1e-20, noted in #1018) is not a trend: 1e-18 and 1e-17 are above it.
- The printed max abs F is linear in delta: q1 2.34e-29, 2.34e-28, 2.34e-27, 2.34e-26 over the four sizes (exactly 10 per decade), q0 5.33e-30, 5.33e-29, 5.33e-28 from 1e-19 on (its 1e-20 value 1.39e-30 sits above the line, a floor). No quadratic term shows in three digits to 1e-17. These residuals are 1.6e-13 (q0) and 7.0e-12 (q1) of the random move's (3.36e-16 at 1e-18, 3.36e-15 at 1e-17).
- The random move at 1e-17 uses the same seed, hence the same direction as at 1e-18, 10 times longer. m_rand at 1e-17 (1.1883e-20) is 2.9 times that at 1e-18.
- The random 1e-18 run repeats #963's `c_d1e-18` exactly (same state bit for bit, same bounds), so it adds no information beyond a reproducibility control (the issue's six runs counted it).

Limits:
- One ray per direction (q0, q1), at sample c only. Combinations of q0 and q1, and of q0 or q1 with the in-plane chords, were not moved.
- The bounds are upper bounds on the smallest gain from 12 rough right-hand sides, not the gain itself. The reading rests on the ratio to the random reference, as the issue fixed it.
- The largest move is 1e-17 of max|z|. Curvature beyond that size, or at a different sample, is not excluded.
- The two sizes use one `m_rand` each (one random ray, seed 977, the same as #963's).

## Commands, as run

See the list above. The driver ran from 12:04:17 to 15:42:57 UTC (run_1022.log: q0 2332 s, q1 2322 s, random 1992 s at 1e-18, then q0 2272 s, q1 2292 s, random 1912 s at 1e-17). Code worktree `C:\Users\nathan\Source\choptuik-i1018` at main 7745882e; origin/main is 80811009 at the end (`solver/rt` unchanged since 7745882e).
