# I1025-win/p4: P4 hybrid re-roots of four delta-table rows, the win laptop's share (P4 amendment 6, winb)

Machine: winb, Surface Laptop 4 (i7-1185G7, 4 cores, 8 threads), 31.8 GB, Windows 11, Git Bash. Written before the run starts (2026-11-20 18:55 UTC).

## Question

P4 (xfkappa's `p4_criteria.log` and amendment 6, raw `I1025-mac`) re-roots delta-table lambda records on their own states with the hybrid mode matrix: float64 for blocks 0 to 11, double-double for the horizon block 12, with multidouble 5.1.0's `dd_logdet` for the sign and ln|det|. On the Mac, Fb (k_c 55) at D 16 gave 2.244042809616683, against the float64 record 2.2426280. This laptop runs four rows of the batch; the coordinator decides what they mean.

| row | records | state |
|---|---|---|
| 1, the cross-check | `I1025-mac/out/l1kc55Fb1025.jsonl`, k_c 55, D 16 | `sol_l1kc55Fb1025_D16.0000.npy`: must give 2.244042809616683 to 1e-5, or the batch stops before any other row |
| 2 | `I1025-win2c/out/l1kc63Fz1025.jsonl`, k_c 63, D 15.5 | `sol_l1kc63Fz1025_D15.5000.npy` |
| 3 | `I1025-mac/out/l1kc55Fb1025.jsonl`, k_c 55, D 14.5 | `sol_l1kc55Fb1025_D14.5000.npy` |
| 4 | `I1025-win2b/out/l1kc63Fu1025.jsonl`, k_c 63, D 16.25 | `sol_l1kc63Fu1025_D16.2500.npy` |

## Inputs and code

| item | value |
|---|---|
| driver | raw `I1025-mac/p4_driver_w.sh`, blob dfdf706cd99effa3fcf88053a7e102690e2f4dbc, extracted by `git show` (LF, 0 CR bytes; `git hash-object --no-filters` equals the blob). The coordinator cited raw 4bdab1a4; on origin/main 6eb47eca the path's last commit is 79d3310b |
| p4_hybrid.py | raw `I1025-mac/p4_hybrid.py`, blob a402559b5d37661b49da50f07f877af21fd29b3a (the driver checks it) |
| WT | `C:/Users/nathan/Source/choptuik-i1025-lowd`, detached at 505d839940456a3d04321d75cf66cc3b5bc831c4 (wip/ell1-highD: dss_ell, ell_ddm, ddnp); idle since the low-D signtests |
| RAW | `C:/Users/nathan/Source/p4_1025/raw`: p4_hybrid.py and the driver's 7 INPUTS files, each by `git show origin/main:<path>` and checked with `git hash-object --no-filters` against its pinned blob (`prep_p4_inputs_1025.log`, 8 files, 154 KB). The driver checks them again by blob |
| PY | `C:/Users/nathan/Source/venv-md510/Scripts/python.exe`: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0 (pip direct_url commit 8c4360ac0be804d081faeea524e5c1c6e2fffaaa), planted dd_logdet check PASS (`I1058-winb`, raw 0cec38cc) |
| threads | THREADS=4 (BLAS and rayon), BelowNormal, per-row timeout 14400 s |

## Command

```
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe THREADS=4 bash p4_driver_w.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/p4_1025/raw <OUT>
```

OUT is a staging folder outside the push worktree, `C:/Users/nathan/Source/p4_1025/I1025-win/p4`, so that no worktree moves under the running job; its files are copied here for each push.

## Checks, fixed before the run (the driver's and the coordinator's)

- Row 1 must give lambda within 1e-5 of 2.244042809616683, else the driver stops (`STOP: cross-check FAILED`).
- A row PASSES if its record's system is rebuilt (|F| within 1% of the record's or 1e-13, and the same step count), the search has one sign change on its grid and one over all evaluations, the evaluations are noise robust, and the final bracket is at most 1e-7 wide. A timeout or crash counts toward the stop after two in a row.
- The driver has not run on Windows before: a refusal or crash on a path is reported at once.

## Launches (2026-11-20, UTC)

The driver was started three times. Only the third ran. No input, check or driver byte changed between them.

| launch | file | what happened |
|---|---|---|
| 1, about 18:56 | `start_p4_1025.cmd` | The driver refused at its input check. The refusal text went to a console window of the `start`ed bash and left no file |
| 2, 18:58 | `start_p4b_1025.cmd` | Same command with `bash -x` and output redirected to `driver_trace.log`. It shows the refusal: `refuse: .../I1025-win2c/out/l1kc63Fz1025.jsonl missing or not blob 1679d5b7...` and the same for `I1025-win2b/out/l1kc63Fu1025.jsonl` 10235f97 |
| 3, 18:58:54 | `start_p4c_1025.cmd` | `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` exported inside the launching `bash -c`. Inputs checked, rows started. Trace in `driver_trace2.log` |

Cause of the refusal: the driver checks each input with plain `git hash-object <file>`. Git for Windows sets `core.autocrlf=true` in its system config, so that command converts CRLF to LF before hashing. Those two input files are CRLF blobs in raw (written by a Windows runner), so their hash differed from the pinned blob. The prep step had already shown both files equal to the pinned blobs under `git hash-object --no-filters` (`prep_p4_inputs_1025.log`). The two environment variables switch the conversion off for the driver's own git calls, so it hashes the bytes as stored. The coordinator was told and accepted the change.

Priority: the driver runs each row under `nice -n 10`, which Git for Windows maps to Windows Idle priority. Another session on this laptop runs at BelowNormal, so the row would have been starved. `prio_p4_1025.ps1` (started 18:59, log `prio_p4_1025.log`) lifts each row's python from Idle to BelowNormal every 20 s until the driver logs `p4_driver_w.sh done`. It touches no input or output.

The driver's header line prints `multidouble ?` because the package has no `__version__`. The package is 5.1.0 (venv-md510, direct_url commit 8c4360ac0be804d081faeea524e5c1c6e2fffaaa, `I1058-winb`).

## Status

Progress push at 2026-11-21 03:31 UTC (the coordinator asked for progress): rows 1 to 3 are done and PASS, row 4 is running (7 evaluations, 1.61e-03 bracket). `p4_w.log` and `ell_p4_hybrid_1025_w.jsonl` hold rows 1 to 3; `p4_rows/D16.25.log` is the live log of row 4 (partial). The Result section is written at the last push.

### Rows so far (UTC; 4 threads, BelowNormal)

| row | D, k_c | lambda (hybrid) | minus float64 record | evaluations | final bracket | noise robust | time | verdict |
|---|---|---|---|---|---|---|---|---|
| 1, cross-check | 16, 55 | 2.2440427049579905 | +1.4147e-03 | 13 | 2.77e-08 | True | 6722 s, 18:58:54 to 20:51:01 | PASS |
| 2 | 15.5, 63 | 2.3361355728260387 | +4.5299e-04 | 12 | 3.22e-08 | True | 10953 s, 20:51:02 to 23:53:40 (beside the #1058 hp build) | PASS |
| 3 | 14.5, 55 | 2.4960783095120362 | -9.922e-07 | 15 | 2.49e-08 | True | 8057 s, 23:53:40 to 02:08:03 | PASS |
| 4 | 16.25, 63 | running | | 7 at 03:27:09 (3 grid + 4 Brent) | [2.195797442666, 2.197411200000] = 1.61e-03 | so far True | started 02:08:04 | running |

Row 4 so far: record system true (abs(F) 1.8842488019e-10 against 1.8839637548e-10, 2890 steps against 2890); grid 2.153463 (-1), 2.197411 (+1), 2.241359 (+1), one sign change; the float64 record 2.196430918 lies inside the bracket. Rows 1 to 3 needed 5, 3 and 5 more evaluations after the bracket first fell under 2e-03, so row 4 needs 3 to 5 more. Time per evaluation (setup included): 517 s (row 1), 913 s (row 2, with the build), 537 s (row 3), 678 s (row 4 so far). ETA 04:01 to 04:23 UTC, about 04:12; the row timeout is 06:08:04 UTC.

### Cross-check, row 1: PASS

| quantity | value |
|---|---|
| lambda (hybrid) | 2.2440427049579905 |
| the Mac's root | 2.244042809616683 |
| difference | -1.05e-07 (bar 1e-5) |
| float64 record | 2.2426280416106374 (hybrid minus record 0.0014146633) |
| record system | true: abs(F) 1.7849625462e-10 against 1.7853243545e-10, 2565 steps against 2565 |
| grid changes, changes over all 13 evaluations | 1, 1 |
| final bracket | [2.2440427049579905, 2.2440427326553025], width 2.77e-08, noise robust True |
| time | 6722 s (1.87 h, 4 threads, BelowNormal) |

The Mac's root lies 7.7e-08 above the bracket's upper edge, which is 2.8 bracket widths. The bar is 1e-5, so the driver counts the row as a pass. The coordinator decides what the gap means.

Results follow in `p4_w.log`, `ell_p4_hybrid_1025_w.jsonl` and `p4_rows/`.
