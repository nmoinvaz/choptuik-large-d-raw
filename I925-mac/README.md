# I925-mac: the stall rule of the low-D Newton solves, its checks and its replay on stored logs

Machine mac (Apple M5, shared, load 20-36 during the runs), subagent of the coordinator, 2026-11-16. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/925. Code on branch `wip/sa-925` of choptuik-large-d (3d6f393f).

## The rule

`driver.newton_solve(stall=3, stall_factor=0.5, prior=hist)`: after an accepted step, when the last 3 accepted steps
together did not bring max |F| to at most 1/2 of its value before the first of them, the solve ends with a record
`failed="stall"`. A step that brings |F| below tol is never a stall, since the next iteration converges. The option is
off by default, so every other caller of `newton_solve` is unchanged.

`lowD_dd.solve_point` passes it with the solve's earlier records (`prior`, since it takes one iteration per call). With
an hpkernel whose `newton_solve` has no `stall` parameter (`inspect.signature`, as `anm_run.tangent_kw`), it applies the
same test itself after each accepted step, from one extra residual evaluation at the accepted point, and logs one
notice per process. `lowD_highM.py --stall 3 --stall_factor 0.5` are the defaults (`--stall 0` turns it off). A failed
solve's record in the points file now carries `failed` ("stall" or "line search").

## Checks (hp/test_stall.py)

Two drivers: "new" is an overlay package (this branch's `driver.py` beside the installed `_hpkernel` of 2026-10-28,
on `PYTHONPATH`), "old" is the installed hpkernel, whose `newton_solve` predates the option. With the new driver every
solve runs on two paths, the driver deciding and solve_point deciding (a `newton_solve` with the old signature).

| Case | What | Driver | Result | Log |
|---|---|---|---|---|
| 1 | toy, step turned by acos(0.26), lam 1/2 each step | new, old | stall after 3 accepted steps, off: 8 steps | `test_case1_*.log` |
| 2 | M 48 at D 4, steps scaled by 0.05 | new | stall after 3 steps, \|F\| 2.6713e-7 to 2.2903e-7; off: 5 steps; paths bit-identical | `test_cases23_new.log` |
| 3 | M 80, D 3.4 to 3.39, last-state start | new | converged in 7 steps, history, record and state bit-identical on/off and across paths | `test_cases23_new.log` |
| 4 | planted leg, M 80/96 from D 3.4, target 3.35 | old | stall after 3 steps (\|F\| 1.38e-1 to 1.18e-1), D 3.375 inserted, 1 notice | `test_case4_old.log` |
| 4 | the same | new | the same, 0 notices | `test_case4_new.log` |

Cases 2 and 3 were not run on the old driver (the Mac's load reached 150). Their script path ran on the new driver,
with a `newton_solve` of the old signature, and case 4 ran the script-level rule on the old driver itself.

Controls, each expected to exit 1: `control_case1_nostall_new.log`, `control_case2_nostall_new.log` (the rule off where
it must fire), `control_case3_eager_new.log` (stall_factor 1e-12: the converging solve fails after 3 steps, so the
bit-identity check fires). The first three exit 1. The leg control, `control_case4_nostall_old.log` (`--cases 4
--mutate nostall`, the leg's solve runs to `--it_max 5`), has not completed. Its first run lost its output (a rebase of
this clone replaced its log file while it ran), and the second was stopped after 45 min with 5 CPU-minutes at load
100-150. Case 4 itself, 3 steps, took 5 min here at load 30 (`test_case4_old.log`), so the control's 5 steps take
about 8.

## Replay on stored logs

`replay_logs.py ROOT W F` reads every solve_point log under ROOT (a header `D .. M ..: L .., steps .., start |F|`, its
Newton lines, its end line) and applies the rule with window W and factor F to max |F| before each accepted step and
after it (the next line's |F|, or the end line's). Checked by hand on #343's D 3.04315 and T39's D 3.425.

| Logs | Solves | Converged | Fires (w 3) | of them converged | Fires (w 4) | of them converged |
|---|---|---|---|---|---|---|
| raw repository, 36 logs (f4bfaec8) | 155 | 113 | 11 | 3 | 7 | 1 |
| main `hp/data`, 39 logs (7e077e5b) | 224 | 186 | 10 | 0 | 5 | 0 |

The converged solves on which window 3 fires (`replay_raw_w3.txt`):

- T105-win2 `down25f.log`, D 3.04375 M 384: at the residual floor, after the last step (|F| 1.05e-27 to 5.70e-28),
  where the floor rule stops it too. Its |F| is below `--accept` (1e-27), so solve_point still counts it converged.
- T39-win `local_t41.log`, D 3.425 M 96: |F| 9.7e-6, 3.2e-6, 2.5e-6, 2.7e-6, 2.7e-6, 1.4e-6, then quadratic to
  3.1e-30 in 9 steps. The rule fails it after its fourth step (3.25e-6 to 2.71e-6 over steps 2-4). In a leg this costs a halved step.
- T39-win `local_t41.log`, D 3.4 M 128: 30 steps, beyond lowD_highM's `--it_max` 14, so it fails there either way.

With window 4 only the 30-step solve remains. #343's D 3.04315 (I343-win2 `leg2.log`) fires with window 3 after its
third step (2.71e-2 to 1.41e-2, ratio 0.52); its log stops during the fourth step, so window 4 cannot be replayed.

## Files

- `test_*.log`, `control_*.log`: `hp/test_stall.py` runs, the command in each first line.
- `replay_logs.py`, `replay_{raw,main}_w{3,4}.txt`: the replay and its output.
