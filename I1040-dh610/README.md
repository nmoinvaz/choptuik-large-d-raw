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
