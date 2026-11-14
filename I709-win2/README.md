# I709-win2: newton_od's natural test with the full step's drop, the planted check and an A/B on chain_nsr

Machine win2 (desktop-pc, 20 cores), issue https://github.com/nmoinvaz/choptuik-large-d/issues/709.

Code: main 0da740e1 or later in the worktree D:/choptuik-i709, with venv-i600 (#603's own build, after #523's exact freeze projector) (`newton_od(..., full_drop)`, `anm_run.py --od_full_drop`, `octo_corrector.py --full_drop`; its toy
check `newton_od_toy.py` passes and its control `--mutate=drop` fails). Scripts (written by the coordinator; the win laptop's, moved to win2 since its build predates #523, #774): `run_709.sh` (8 threads, it reruns the toy and its control first)
and `compare_709.py` (its selftest passes).

Criteria, written before the run (#709): the planted check at D 200 with `--accept natural --full_drop 1e-20` reaches
REF200's Delta to 1e-40; on chain_nsr's attempts 4 and 5, one step each from the same base without (A) and with (B) the
option, both are accepted at the same D_str, their states agree in every unknown to 1e-55, and B's corrector time is
below A's. The issue's control with the floor at 1 on a class A start is not run here; the toy's `--mutate=drop` is its
stand-in.
