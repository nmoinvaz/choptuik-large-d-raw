# I847-rpi5: Theorem A(M = 5)'s second-order certificate reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/847. Script (the coordinator's): `run847.sh`, the commands of
proof/A_M2.md section 7 from `solver/proof/` of the worktree `~/Source/choptuik-large-d-847`, without the
finite-difference runs (d2check reads the stored fd files) and the pilot. Each command has its log here and its exit code
and wall time in `exits_847.txt`; the lines marked ctrl are the controls that must fail. `env.txt` records the commit and
the versions.

- `A_M2_box_M5_1e-10.json`, `.log`: this machine's rigorous M = 5 box run. The coordinator cross-loads it on the Mac.
- `A_M2_box_M1_1e-6.json`, `A_M2_box_M3_1e-8.json`: the M = 1 and M = 3 runs of the same code.
- `krawczyk5_stored.log`: the test on the stored x86 M = 5 box, the cross-load the other way.
