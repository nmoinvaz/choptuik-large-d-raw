# I934-dh610: hp on multidouble 4.8.2 (octo-double renormalization repaired), bit-identity checks

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB, at 5 CPUs (two chains use the rest).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/934
Code: branch `hp/multidouble-4.8.2` at cdb5a6bc, worktree `/home/nathan/Source/choptuik-large-d-934` with its own
venv. The 4.8.0 reference is #923's worktree `/home/nathan/Source/choptuik-large-d-923` and its venv.

Scripts, in order, each started as `systemd-run --user --scope bash <script>` from this folder: `build.sh`, `tests.sh`,
`checks.sh`, `jac.sh`, `states.sh` (with `state_dump.py`).
