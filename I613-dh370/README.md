# I613-dh370: #580's layout ladders again with the covariant Curtis-Reid floor (e929849), dh370 (Fedora Linux 45)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/613 (follows #580, I580-dh370/)
Code: choptuik-large-d main at e929849ff21aeb7588177f8d05ba7633fe0a91be, worktree `choptuik-large-d-604`. The kernel is the
build of I604-dh370/ (main e835d94): hp/src, hp/Cargo.* and the pyprojects are unchanged between e835d94 and e929849, so
only Python differs. `cr_floor_check.py` passes (cr_floor_check.log).
Runs: `python near_null_eq.py RAW STATE --plant=7 --cr_floor=F --threads=4 --json=OUT` from `hp/`, three at a time, nice 10,
at the four layouts of I580-dh370/README.md and F = 1e-14, 1e-12, 1e-10 and the controls at F = 0.
