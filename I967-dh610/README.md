# I967-dh610: main's hp build on the low-memory recipe, thread-count bits at ks 240 and ks 291, and #842's predictor test at step 61

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/967

Worktree `~/Source/choptuik-large-d-967` at origin/main d96a09a1 (detached), fresh venv (uv, Python 3.14).
Inputs are extracted from origin/main of the raw repository into `~/scratch967/raw` with `git show`, so the live clone is not pulled.

Files are added as the items run:

| file | what |
|---|---|
| `common967.sh` | paths and inputs, sourced by the scripts |
| `memlog967.sh` | alert-only memory log (writes a line only when available memory or swap crosses a threshold, kills nothing) |
| `build967.sh` | item 1, `hp/build.sh` on the low-memory recipe at nice 10 under `/usr/bin/time -v` |
| `withmem967.sh` | runs a script with the memory log watching it (systemd turns `$$` in a unit's command line into `$`, so the pid is taken here) |
| `build.log`, `build_time.txt`, `memlog.log` | item 1's log, its `/usr/bin/time -v` output and the memory log (the build's first minute is not in it, see its second line) |
| `checks967.sh`, `summary_item2.txt`, `jbo_*` | item 2 |
| `step61_967.py`, `run_item3_967.sh`, `i3_*` | item 3 |

A memory log run through `withmem967.sh` has no "end" line: systemd kills it with the unit when the script ends. A log with no ALERT line means no alert while the script ran.
