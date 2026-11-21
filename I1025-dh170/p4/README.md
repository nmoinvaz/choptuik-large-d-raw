# I1025-dh170/p4: #1025 P4 hybrid re-roots, k_c 55 at D 15, 15.5, 17

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM + 8 GB zram). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025
(P4 amendment 9; the coordinator's hc 23:2x UTC 2026-11-20). Raw inputs at raw-repository commit 791f8a9f (origin/main when fetched, 23:32 UTC).

## What this is
A share of the #1025 P4 batch: double-double re-roots (float64 blocks 0-11, dd block 12; `I1025-mac/p4_hybrid.py`) of the delta-table records
of k_c 55 on their own states, at D 15, 15.5 and 17, run by `p4_driver_rows.sh` after its built-in cross-check row (Fb, k_c 55, D 16).
Winb and win2b ran the same driver today (cross-checks within 1.05e-7 and 3.16e-7 of the Mac's; raw I1025-win/p4, I1025-win2b/p4).

## Pass criteria (written before the run)
- The driver's own input checks pass: `p4_driver_rows.sh` blob e004c9ec, `p4_hybrid.py` blob a402559b, row list `I1025-mac/p4_rows_dh170.txt` blob
  31ce2b58, every record and state blob named in the row list, WT at 505d839940456a3d04321d75cf66cc3b5bc831c4. A refusal stops the batch.
- Cross-check row (Fb, D 16, k_c 55; built-in, default timeout 14400 s): the hybrid root must match the Mac's 2.244042809616683 to 1e-5, or the batch
  stops before any listed row (this is the check that can fail; it is reported at once either way).
- Each listed row PASS: exit 0, and the last JSONL record has the right D, `record_system`, one sign change on the grid, one change in all, `noise_robust`,
  and `bracket_width` <= 1e-7. A row over its 21600 s timeout is TIMEOUT, a nonzero exit is CRASH; two in a row stop the batch.
- Results (lam per row, the cross-check's difference from the Mac's) are quoted from `p4_w.log` and `ell_p4_hybrid_1025_w.jsonl`, nothing else.

## Command
```
cd I1025-dh170/p4   # in the raw-input tree ~/Source/choptuik-large-d-raw-p4 (git archive of I1025-mac at 791f8a9f + this folder; not a git worktree)
PY=$HOME/Source/choptuik-large-d-1058b/.venv/bin/python THREADS=4 nice -n 10 bash p4_driver_rows.sh \
  ~/Source/choptuik-large-d-1025p4 ~/Source/choptuik-large-d-raw-p4 ~/Source/choptuik-large-d-raw-p4/I1025-dh170/p4 \
  ~/Source/choptuik-large-d-raw-p4/I1025-mac/p4_rows_dh170.txt 31ce2b5810e88e14328217e79c0be2ccb649fda5
```
- WT `~/Source/choptuik-large-d-1025p4` is a new worktree at 505d8399 (detached). PY is the #1058 venv at hp 8179068d (multidouble Python package 8c4360ac,
  numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0).
- The live raw clone is not touched: the inputs are `git archive` copies of `I1025-mac` at 791f8a9f in `~/Source/choptuik-large-d-raw-p4`; this folder
  is pushed from there with `~/Source/push_raw_p4_dh170.sh` (a copy of `push_raw_dh170.sh` with its LIVE root changed).
- Beside the #1057 lane (2 threads, nice 10, keeps its priority). Memory is sampled every 60 s into `p4_mem.log` (alert-only, stops nothing).

## Log
- 2026-11-20 23:34 UTC: folder, worktree and inputs prepared; blobs checked by hand: driver e004c9ec, p4_hybrid.py a402559b, row list 31ce2b58.
- 2026-11-20 23:34:16 UTC: batch started (`p4_run.out`): driver bash pid 979737 (timeout 979775, python 979776), THREADS=4, nice 10; memory sampler pid 979786 (`p4_mem.sh`, alert-only). Input checks passed (4 rows, the cross-check first). Cross-check row (D 16) running.
- 2026-11-21 00:41:31 UTC: **cross-check row PASS** (`p4_w.log`): row 1, Fb, k_c 55, D 16: hybrid root lam 2.2440431522619795 against the Mac's 2.244042809616683, difference +3.43e-07 (bar 1e-5), one sign change on the grid, one over all 13 evaluations, bracket width 3.8933017698639105e-08, noise-robust True, 4032 s (started 23:34:16). Row 2 (D 15, timeout 21600 s) started 00:41:31.
- 01:06 UTC: I found the result at 01:05:49, 25 minutes after it was logged: my P4 monitor ended its pipe in `cut`, which holds a pipe's output until it exits, so the PASS line never reached me (and the monitor before it had the same fault). The monitor was replaced at 01:06 by one with `grep --line-buffered` as its last stage (no `cut`). No row result or stop was missed: the only line logged between 00:37 and 01:05 was this PASS and row 2's start. Nothing in the batch itself changed.
