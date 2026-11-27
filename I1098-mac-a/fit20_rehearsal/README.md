# I1098-mac-a/fit20_rehearsal: the 20-point ladder's planted calibration and leave-one-out check, before its data

Coordinator (t5), Mac, 2026-11-27 19:47 UTC. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098.
Code as I1098-mac-a/fit15 (ladder_fit.py of wip/twenty-digits b85787c0 beside main's export_delta_all.py). The ladder:
the 15 records' D and err_sum ratios plus D 3214 (sigma 1e-25, its larger pendings), 4628, 5555, 6666 and 8000
(6.5e-26 each, the recent points' err_sum), `ladder20_args.txt`.
- `planted20.log`: `planted --ladders=X <args> --sigmas=1e-25 --seeds=20`, exit 0: F = 3.78.
- `loo20.log`: `loocheck --ladders=X --D=<the 20> --sigmas=1e-25 --Fs=X:3.78`, exit 0.
