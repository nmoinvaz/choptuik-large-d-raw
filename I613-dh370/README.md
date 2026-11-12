# I613-dh370: #580's layout ladders again with the covariant Curtis-Reid floor (e929849), dh370 (Fedora Linux 45)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/613 (follows #580, I580-dh370/)
Code: choptuik-large-d main at e929849ff21aeb7588177f8d05ba7633fe0a91be, worktree `choptuik-large-d-604`. The kernel is the
build of I604-dh370/ (main e835d94): hp/src, hp/Cargo.* and the pyprojects are unchanged between e835d94 and e929849, so
only Python differs. `cr_floor_check.py` passes (cr_floor_check.log).
Runs: `python near_null_eq.py RAW STATE --plant=7 --cr_floor=F --threads=4 --json=OUT` from `hp/`, three at a time, nice 10,
at the four layouts of I580-dh370/README.md and F = 1e-14, 1e-12, 1e-10 and the controls at F = 0.

## Files

| file | what |
|---|---|
| cr_floor_check.log | `python cr_floor_check.py` at e929849 before the runs, exit 0 |
| eq_LAY_FF.json, eq_LAY_FF.log | one `near_null_eq.py` run, layout LAY (070, 080, 092, 0975) and floor FF (1e-14, 1e-12, 1e-10, or 0 for the control); the log ends with `wall`, `maxrss` and `exit` |
| ladders613.sh | the 16 runs, three at a time (exit 0 at all but 0.80 with F = 1e-12, which failed the planted check) |
| diag_080_F1e-12_rerun, diag_080_F5e-13, diag_080_F2e-12 (.json, .log), diag613.sh | the diagnosis of that one failure: the same run again, and the neighbouring floors |
| rerun_54c9fcb/ | the rerun of the 0.80 bracket on main 54c9fcb with `--cr_sets=1` (its own README.md) |
| ladder_table.py, ladder_table.txt | the tables of the issue's summary, from the json files of this folder and of I580-dh370/ |

The F = 0 controls give sigma_1..4 identical to I580-dh370/'s, bit for bit.
