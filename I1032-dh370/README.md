# I1032-dh370: runner checks of the cheaper octo-double projections (draft PR #1038, branch perf/elim-projections)

Machine: dh370-fedora (Fedora, 10 threads), chain `ks_chain3b` of #966 paused (kill -STOP) for the duration.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1032, commands from the coordinator's comment 7017967838.
Code: worktree `~/Source/choptuik-large-d-1032` at origin/perf/elim-projections, run with the python of the 40f4b4a5 build
(`~/Source/choptuik-large-d-961/.venv`, read-only).

- `run1032.sh`: the commands as posted, unchanged.
- `<check>.log`: one log per check (mock, floor, time, bits, bits_ulp, accuracy, acc_sign, acc_nobar), last line `exit N`.
- `step_new/`, `step_new.log`, `step_old/`, `step_old.log`: the chain A/B, leg 6's first step with and without the new flags.
