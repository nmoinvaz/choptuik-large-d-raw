# I1032-dh370: runner checks of the cheaper octo-double projections (draft PR #1038, branch perf/elim-projections)

Machine: dh370-fedora (Fedora, 10 threads), chain `ks_chain3b` of #966 paused (kill -STOP) for the duration.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1032, commands from the coordinator's comment 7017967838.
Code: worktree `~/Source/choptuik-large-d-1032` at origin/perf/elim-projections, run with the python of the 40f4b4a5 build
(`~/Source/choptuik-large-d-961/.venv`, read-only).

Round 1 (head 76582864, `run1032.sh` as posted): mock, floor, time, bits, bits_ulp, accuracy (exit 1: the 1e-24 plant lay outside
the projection's basin), acc_sign and acc_nobar (stopped by pid at the coordinator's order), then `step_new/` (old head, a data point
only; `step_old` was not run at that head).

Round 2 (head 68c0a09f, worktree `~/Source/choptuik-large-d-1032b`, `run1032b.sh` as posted in comment 7021253688): `accuracy2.log`
(exit 0), `acc_sign2.log` and `acc_nobar2.log` (exit 1, the controls), `time2.log` (exit 0), then the chain A/B on leg 6's first step
(D 251.2845 to 251.8782, a 0.5938): `step_new2/` + `step_new2.log` (--proj_start pred --reseed_o_stop 1 --proj_o 1) and
`step_old2/` + `step_old2.log` (the same-session control, flags as the chain). `step_old2`'s saved state and prediction are bit
for bit the chain's own. `old_script_check.txt`, `step_new_ended.txt`: the hand-over from round 1's `run1032.sh` (its frozen bash was
killed so that the old head's `step_old` could never start).

- `<check>.log`: one log per check, last line `exit N`.
- The chain `ks_chain3b` of #966 was paused (kill -STOP) from 2026-11-19 18:19:55 UTC to 2026-11-20 00:16:04 UTC for these runs.
