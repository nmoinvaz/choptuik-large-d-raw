# rerun_ff08351: #613's ladder on main ff08351, the Curtis-Reid floor weighted from a covariant star

Machine: dh370 (Fedora Linux 45, i7-8700, 12 threads, AVX2 and FMA, 31 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/613
Code: choptuik-large-d main at ff083514f64327c74271a5440e92caad8f4b2940, worktree `choptuik-large-d-604`, the kernel of I604-dh370/
(hp/src, the Cargo files and the pyprojects are unchanged since e835d94). `cr_floor_check.log`: exit 0.
Runs: `python near_null_eq.py RAW STATE --plant=7 --cr_sets --cr_floor=F --threads=4 --json=OUT` from `hp/`, three at a time, nice 10,
no memory guard (Nathan's rule), at the four layouts of I580-dh370/README.md with F = 1e-14, 1e-12, 1e-10, and at 0.80 also F = 5e-13
and 2e-12. The F = 0 controls are not rerun (the code does not change them).

## Files

| file | what |
|---|---|
| cr_floor_check.log | `python cr_floor_check.py` at ff08351 before the runs: three `pass` lines, exit 0 |
| eq_LAY_FF.json, eq_LAY_FF.log | one run, layout LAY (070, 080, 092, 0975) and floor FF; the log ends with `wall`, `maxrss` and `exit`; the json holds `cr_sets` (entries below full weight in J and J S, entries full in one only, largest weight difference) |
| rerun.sh | the driver of the 14 runs (all exit 0) |
| ladder_table.py, ladder_table.txt | the tables of the issue's summary, from these json files and those of ../ (e929849), ../../I580-dh370/ (raw-max floor) |
