# I858-dh610: the octo-double corrector through a quad-double LU against the octo-double LU, at #608's D 253.3382

Machine: dh610, Fedora Linux 45, Intel i7-12700 (20 threads, AVX2), 62 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/858
Code: branch `hp/mixed-corrector` at cf7bd594, worktree `/home/nathan/Source/choptuik-large-d-858`, run with #855's
venv (`/home/nathan/Source/choptuik-large-d-855/.venv`, main's kernel). Input: `I608-dh610/restart4_d6/pred_pin3_D253.3382.npz`.

`mixed.sh` (started as `systemd-run --user --scope bash mixed.sh` from this folder, after #855) runs
`octo_corrector.py wall` with `--lu od` and `--lu qd` at 6 threads each, concurrently, then `--lu qd --mutate 10`,
then `compare.py` on the results (`compare.log`).
