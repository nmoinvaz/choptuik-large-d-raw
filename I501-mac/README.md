# I501-mac: near_null's first Newton step at D 242.3642, its planted check and control, at the 0.3-0.7 and 0.3-0.8 starts

Machine: the M5 Mac (subagent), 2 threads under nice 10, interpreter venv-314 (its installed `hpkernel`).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/501 (depends on #493 and #488).

Code: choptuik-large-d branch `feat/i501-near-null-step` (`hp/near_null.py`), the commit named in `exits.txt` for each
run (2edb152: the planted start moved to z - w; 9e21ed8: the planted residual as an offset at the state).

## Runs

`run_i501.sh <worktree>/hp RAW RUN...`, exits and walls in `exits.txt`.

| run | state | options | commit | exit | log, json |
|---|---|---|---|---|---|
| planted (moved start) | `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (0.3-0.7) | `--planted=1` | 2edb152 | 1 | `near_null_planted_moved_2edb152.*` |
| planted | the same | `--planted=1` | 9e21ed8 | 0 | `near_null_planted.*` |
| control | the same | `--planted=1 --mutate=scale_block` | 9e21ed8 | 1 | `near_null_control.log`, `near_null_planted_ctl_scale_block.json` |
| s08 | `I489-mac/renode_L1_horizon_D242.3642.npz` (0.3-0.8) | defaults | 9e21ed8 | | `near_null_s08.*` |
| s08_keep | the same | `--keep_plan=1` | 9e21ed8 | | `near_null_s08_keep.*` |
| s07_keep | crawlJ's state | `--keep_plan=1` | 9e21ed8 | | `near_null_s07_keep.*` |

## Planted check

At 9e21ed8 the offset c = F(z) + J w leaves the residual -J w at the state, so the Newton step from the same LU is w
(|w| 9.85e-21, w = (v_1 + g) / sqrt 2, g a random unit vector, seed 2). The printed step equals w to 0.0 in every
block, its Delta component and V^T dz (f64; the octo-double solve's error is far below half an ulp of w). The control,
the m_h block of every printed step times 1.01, gives m_h 1.0e-2 and V^T 1.2e-3, and the check fails (exit 1).

The moved start of 2edb152 (z - w, |w| 9.85e-31, its step newton_o(z - w).dz + J^-1 F(z)) failed. Its step was 4.4e8,
4e38 times |w| off w, mostly in the c blocks. The cause is the horizon rows' curvature, not the report path
(`probes/`).

## Probes (`probes/`, run from the worktree's hp at 9e21ed8, 2 threads)

- `probe_F.py`: max|F| of each state under near_null's system (plan made again, no held offset), with the held offset,
  and on the stored plan. `probe_F_s07.txt`, `probe_F_s08.txt`.
- `probe_G.py`: G(t) = F(z - t g) - F(z) for a random unit g, and its nonlinearity |G(2t) - 2 G(t)| / |G(2t)|, at
  t 1e-20 to 1e-70 (`probe_G_s07.txt`). Only the horizon rows respond, with a quadratic term about 1e30 t of the
  linear one (7.7e-6 at 1e-35, 7.7e-11 at 1e-40, 8.4e-16 at 1e-45).
- `probe_blocks.py`: the same at t 1e-35 with g inside one block of z (`probe_blocks_s07_t1e-35.txt`). The centre and
  node unknowns are linear (0 nonlinearity, max|G| below 1e-35). The curvature is in a_h (3.3e-5), m_h (3.7e-8) and
  Delta (1.7e-10).
