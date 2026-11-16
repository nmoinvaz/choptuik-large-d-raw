# I903-win2: the pilot of the D 150 chain with the horizon order tied to D (p130, p160, s160)

Machine win2 (win2b runner), worktree `D:/choptuik-i603r` at a515ab87 plus the cherry-picks of 614211ab and 1fc37c03 (`--ks`, #696), venv-i600.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/903

Start state `T138-win2/chain/anm_pin3_D150.0000.npz` (ks 130). p130 is the polish at the state's own ks 130 (the control), p160 the same at `--ks 160 --keep_plan 0`, s160 two steps from p160's polished state at `--ks 160`.
