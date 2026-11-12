# I501-mac: near_null's first Newton step at D 242.3642, its planted check and control, at the 0.3-0.7 and 0.3-0.8 starts

Machine: the M5 Mac (subagent), 2 threads under nice 10, interpreter venv-314 (its installed `hpkernel`).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/501 (depends on #493 and #488).

Code: choptuik-large-d `hp/near_null.py`. The runs used commits 2edb152 (the planted start moved to z - w) and 9e21ed8
(the planted residual as an offset at the state), both kept on the branch `wip/i501-subagent-runs`. The branch
`feat/i501-near-null-step` is the same code rebased onto main 53d8b78 (af82d98, 549c80f), with main's
`near_null.subspace`; on a mock solver its output equals 9e21ed8's on the default, planted, control, sigma and
scale_p1 paths.

## Runs

`run_i501.sh <worktree>/hp RAW RUN...` and `run_main.sh <worktree>/hp RAW`; exits and walls in `exits.txt`.

| run | state | options | commit | exit | log, json |
|---|---|---|---|---|---|
| planted (moved start) | `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (0.3-0.7, L 769) | `--planted=1` | 2edb152 | 1 | `near_null_planted_moved_2edb152.*` |
| planted | the same | `--planted=1` | 9e21ed8 | 0 | `near_null_planted.*` |
| control | the same | `--planted=1 --mutate=scale_block` | 9e21ed8 | 1 | `near_null_control.log`, `near_null_planted_ctl_scale_block.json` |
| s08 | `I489-mac/renode_L1_horizon_D242.3642.npz` (0.3-0.8, L 897) | defaults | 9e21ed8 | 0 | `near_null_s08.*` |
| s08_keep | the same | `--keep_plan=1` | 9e21ed8 | 0 | `near_null_s08_keep.*` |
| s07_keep | crawlJ's state | `--keep_plan=1` | 9e21ed8 | 0 | `near_null_s07_keep.*` |
| s08_main | the 0.3-0.8 start | main's near_null (53d8b78) | main | 0 | `near_null_s08_main.log` |

The planted run's first part is the default run at crawlJ's state (its lines before the planted ones).

## Planted check

At 9e21ed8 the offset c = F(z) + J w leaves the residual -J w at the state, so the Newton step from the same LU is w
(|w| 9.85e-21, w = (v_1 + g) / sqrt 2, g a random unit vector, seed 2). The printed step equals w to 0.0 in every
block, its Delta component and V^T dz (f64; the octo-double solve's error is far below half an ulp of w). The control,
the m_h block of every printed step times 1.01, gives m_h 1.0e-2 and V^T 1.2e-3, and the check fails (exit 1).

The moved start of 2edb152 (z - w, |w| 9.85e-31, its step newton_o(z - w).dz + J^-1 F(z)) failed. Its step was 4.4e8,
4e38 times |w| off w, mostly in the c blocks. The cause is the horizon rows' curvature, not the report path
(`probes/`).

## Default lines

The existing lines of `near_null_s08.log` (the step lines dropped, times masked) equal main's near_null on the same
start on this machine (`near_null_s08_main.log`) line for line. Against #493's run on macm3
(`I493-macm3/near_null_L1.log`) one digit differs, sigma_4's convergence (1e-16 here, 4e-16 there), which main's code
on this machine also prints as 1e-16: a machine difference at f64 epsilon. The planted run's default part equals the
2edb152 run's, and its sigma equal #488's (2.55e-27, 2.53e-27, 4.39e-26, 7.93e-26).

Comparison files:

- `cmp_old_lines.sh NEW.log REF.log`: a near_null log's existing lines (step lines dropped, times masked) against a
  reference. `cmp_s08_vs_main.txt` (identical), `cmp_s08_vs_I493.txt` (the sigma_4 convergence above).
- `mock/`: `mock_cmp.sh` runs near_null on a numpy mock solver (M 4, one node) with 9e21ed8's file and with the
  rebased branch's (549c80f). `mock_cmp_549c80f_vs_9e21ed8.txt`: identical output on the default, planted, control,
  sigma and scale_p1 paths.

## The first step (`tables_i501.md`, from `table_i501.py`)

"step" is newton_o's dz (the kernel's frozen rows drive p1's held harmonics to zero). "pinned step" is dz + J^-1 c
with the held offset at the state's own coefficients, the base polish's step. "new" is near_null's plan made again
at the state, "stored" the state's own plan (`--keep_plan=1`), the polish's.

| state, plan | step | max\|dz\| | \|dz\| | Delta | share on span(V) | V^T dz (v_1..v_4) |
|---|---|---|---|---|---|---|
| 0.7, new | step | 8.09e-04 | 5.27e-03 | -1.03e-05 | 0.037 | -1.1e-04, +1.6e-04, -2.6e-05, -7.5e-06 |
| 0.7, new | pinned | 1.25e-15 | 9.38e-15 | +9.23e-17 | 1.000 | -6.6e-15, -6.7e-15, +3.9e-16, +6.8e-16 |
| 0.7, stored | pinned | 8.12e-38 | 5.05e-37 | +9.97e-40 | 0.036 | +1.0e-38, -1.5e-38, +2.5e-39, +6.9e-40 |
| 0.8, new | step | 1.69e-01 | 1.73 | +7.61e-02 | 1.000 | -2.7e-02, -6.8e-02, -1.2e-02, +1.72 |
| 0.8, new | pinned | 1.68e-01 | 1.73 | +7.62e-02 | 1.000 | -2.7e-02, -6.8e-02, -1.2e-02, +1.72 |
| 0.8, stored | pinned | 1.68e-01 | 1.73 | +7.62e-02 | 1.000 | -2.7e-02, -6.8e-02, -1.2e-02, +1.72 |

The kernel step does not depend on the plan at either state (to the printed digits). At 0.7 it is 5.3e-3, mostly
held harmonic 5 of p and m. At 0.8 the polish's first step is order 1, 1.72 on v_4 (sigma_4 1.77e-34, harmonic 1 of p
and m at every node, Delta share 7.8e-4), the start's horizon residual (1.6e-34, p harmonics k <= 3) over sigma_4.
At 0.7 on its own plan the state is converged (5e-37); near_null's plan adds 5.6e-34 in n0>n1 and a step of 9.4e-15
on the harmonic-3 pair.

## Probes (`probes/`, run from the worktree's hp at 9e21ed8, 2 threads)

- `probe_F.py`: max|F| of each state under near_null's system (plan made again, no held offset), with the held offset,
  and on the stored plan. `probe_F_s07.txt`, `probe_F_s08.txt`.
- `probe_G.py`: G(t) = F(z - t g) - F(z) for a random unit g, and its nonlinearity |G(2t) - 2 G(t)| / |G(2t)|, at
  t 1e-20 to 1e-70 (`probe_G_s07.txt`). Only the horizon rows respond, with a quadratic term about 1e30 t of the
  linear one (7.7e-6 at 1e-35, 7.7e-11 at 1e-40, 8.4e-16 at 1e-45).
- `probe_blocks.py`: the same at t 1e-35 with g inside one block of z (`probe_blocks_s07_t1e-35.txt`). The centre and
  node unknowns are linear (0 nonlinearity, max|G| below 1e-35). The curvature is in a_h (3.3e-5), m_h (3.7e-8) and
  Delta (1.7e-10).
