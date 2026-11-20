# I1040-dh610: #1040's step_timing_check at main 9980cd93, after #1034's build

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1040 (the check is the coordinator's order of 20 Nov 2026, 06:30 UTC, run once after the #1034 build).
From `hp/` of `~/Source/choptuik-large-d-1034` (detached at 9980cd93, venv `~/Source/venv-i1034`, hpkernel built there by `hp/build.sh`, driver `--driver=checkout`), `nice -n 10`:

1. `python3 step_timing_check.py --reps=3 --threads=4` (expect exit 0),
2. `python3 step_timing_check.py --reps=2 --threads=4 --mutate=drop` (expect exit 1, check 1 FAIL).

Both exits are posted on #1040. The machine is loaded (#1033 run 5, #1021's jobs), and the check's wall-clock arithmetic is meant to tolerate that (the script's own note). Logs: `step_timing_ok.log`, `step_timing_mutate_drop.log`, `exits_1040.txt`.

## Files

| file | what |
|---|---|
| `step_timing_ok.log`, `step_timing_mutate_drop.log`, `exits_1040.txt` | the two runs (written by `../I1034-dh610/run1034.sh`) |

## Result, 20 Nov 08:20 UTC (`step_timing_ok.log`, `step_timing_mutate_drop.log`, `exits_1040.txt`)

Build `hp/build.sh` at main 9980cd93 (venv `~/Source/venv-i1034`): exit 0 in 3554 s; hpkernel avx2, multidouble 4.9.1, multishoot 3.3.0 (`../I1034-dh610/hpkernel_import.log`). Then, from `hp/`, `nice -n 10`:

1. `step_timing_check.py --reps=3 --threads=4`: **exit 1 (expected 0)**, checks 2 and 4 FAIL (block closure +12.98% against the bar 5%, the median over block calls of +22.8%, +13.0%, -66.6%; check 4 -12.02%); checks 1, 3 and 5 PASS.
2. `step_timing_check.py --reps=2 --threads=4 --mutate=drop`: **exit 1 (expected 1)**, but checks 1, 2 and 4 FAIL (check 1 FAIL as the control requires, the dense entries miss up to 9.46% of a call; 2 and 4 fail as in run 1); 3 and 5 PASS.

The machine was loaded (#1033 run 5 with 8 threads, #1021's recount with 3 workers, the 4 threads of the check). The block calls' wall seconds of run 1 were 1.92, 2.04 and 7.73 s with process CPU seconds 6.82, 7.54 and 26.71, and the dense calls' 1.81, 2.55 and 4.09 s with 6.17, 9.29 and 15.29: CPU seconds rose with wall seconds by up to 3.9 times between repetitions, so the script's premise that load lengthens a call's wall time "but hardly its CPU time" does not hold here, and its median over so few calls follows the outlier. Not fixed (the check is #1040's).
