# I971-dh610: base polishes from ks_chain2's D 237.7132 state at ks 293, 295 and 299 on #967's main build

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/971

Build: worktree `~/Source/choptuik-large-d-967` at origin/main d96a09a1 and its `.venv` (hpkernel from #967's build, `I967-dh610/build.log`).
State: `I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz` (extracted from origin/main of the raw repository into `~/scratch967/raw`).
Flags: run903e.sh's (`I903-win2/run903e.sh`) with `--threads 6 --steps 0 --keep_plan 0 --save_base 1 --ks K`, K = 293, 295, 299 (+2, +4, +8),
side by side, each capped at 1 h (`timeout -s TERM 3600`), nice 10. A rung that fails (gate971.py: exit non-zero, no converged octo-double Newton line
at max|F| <= 1e-60, or no saved base) stops the larger rungs still running.

| file | what |
|---|---|
| `run971.sh` | the three polishes and the stop rule |
| `gate971.py` | the verdict of one rung's log |
| `ks<K>.log`, `ks<K>/` | a rung's stdout and its output directory (anm_run.jsonl, base_pin3_D237.7132.npz if saved) |
| `exits_971.txt`, `summary_971.txt` | exits and verdicts |

Result: ks 295 and ks 299 converged (4 steps), ks 293 failed (capped at 3600 s). Details in the issue's closing comment.
