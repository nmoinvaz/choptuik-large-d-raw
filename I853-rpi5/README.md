# I853-rpi5: lemma 6b1(5), the covering behind Theorem A(M = 5), reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/853. Script (the coordinator's): `run853.sh`, #121's commands
(`I121-win2/run_i121.sh`) on p̂ ± 1e-18 from `solver/proof/` of the worktree `~/Source/choptuik-large-d-853`: the C1 ray
run, the 18 rows in four processes, `check`, `check --drop=9,5` (must fail) and `mutate --j=0` (must certify no disc).
Exits and wall times in `exits_853.txt`; versions in `env.txt`.

- `lemma6b1_runs_M5_rpi5/`: the run directory, every row computed here (tag `_rpi5`).
- `lemma6b1_check_M5_rpi5.json`: the covering check C1-C8.
