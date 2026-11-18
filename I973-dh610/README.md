# I973-dh610: base polishes from ks_chain2's D 237.7132 state at ks 297, 301, 303 and 307, then ks 293 again (the mod-4 test)

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/973

Build, state and flags as I971-dh610 (worktree `~/Source/choptuik-large-d-967` at origin/main d96a09a1, run903e.sh's flags, `--steps 0 --keep_plan 0 --save_base 1 --ks K`),
each capped at 1 h (`timeout -s TERM 3600`), nice 10. ks 297, 301, 303 and 307 side by side at `--threads 5` (20 threads) beside #967's item 3, which was
reniced to 19 when they started so that the polishes keep the cpu; then ks 293 alone after them at `--threads 6` as in #971.

Predictions, fixed before the runs (the issue): 303 and 307 converge, 297 and 301 fail; ks 293 fails at chord 0 max|F| 1.53e-06 as in #971.

| file | what |
|---|---|
| `run973.sh` | the four polishes, then ks 293 |
| `gate973.py` | the verdict of one rung's log |
| `table973.py`, `table973.md` | the table of every polish from this state (291, 293, 295, 299, 304 and these) |
| `ks<K>.log`, `ks<K>/`, `ks293_rerun.log`, `ks293_rerun/` | a rung's stdout and output directory |
| `exits_973.txt`, `summary_973.txt` | exits and verdicts |
