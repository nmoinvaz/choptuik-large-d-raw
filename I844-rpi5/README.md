# I844-rpi5: Theorem A(M = 3)'s certificate and its M = 1 path reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/844. Script (the coordinator's): `run844.sh`, the commands of
proof/A_M.md section 8 (without the numerical refine and plan steps) and the first checks of proof/A_lemmas_M.md, from
`solver/proof/` of the worktree `~/Source/choptuik-large-d-844`. Each command has its log here and its exit code and
wall time in `exits_844.txt`; the lines marked ctrl are the controls that must fail. `env.txt` records the commit and
the versions.

- `A_M_box_M3_1e-10.json`, `.log`: this machine's rigorous M = 3 box run. The coordinator cross-loads it on the Mac.
- `krawczyk3_stored.log`: the test on the stored x86 box (`data/A_M_box_M3_1e-10.json`), the cross-load the other way.
- `A_M_point_M1.json`, `A_M_box_M1_1e-9.json`, `A_M_m1.log`: the M = 1 point and box runs that `m1 --rerun` made here.
