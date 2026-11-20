# I1025-win/signtest_lowD: signtests of seven low-D rows of #1025's delta table (winb, win laptop)

Machine: Surface Laptop 4 (i7-1185G7, 4 cores, 8 threads), 32 GB, Windows 11, Git Bash. Written before the run starts (2026-11-20 17:33 UTC).

## Question

#1025's delta table has rows at D 4 to 14.5 (k_c 31 to 55) that never had a signtest. The coordinator's rule: a row counts only with a passing signtest, no exemption. This lane runs seven of those rows, taken off rpi5's batch so that no row runs twice: k_c 47 at D 10.5, 11, 11.5, 12, 13.5 and 14, and k_c 55 at D 14.5. Order: D 14.5, 14, 13.5, 12, 11.5, 11, 10.5.

## Inputs and code

| item | value |
|---|---|
| driver | raw `I1025-mac/signtest_lowD_driver_v2.sh` at 0596f58f, blob c4f92d36043f2b72299dd8cd9a59377fad564e7e, extracted by `git show` (LF, no CR; `git hash-object --no-filters` equals the blob) |
| signtest.py | raw `I1025-mac/signtest.py`, blob 179ea09681b0a75f7cefdff98984b48051b3f085 (the driver checks it) |
| WT | choptuik-large-d worktree `C:/Users/nathan/Source/choptuik-i1025-lowd`, detached at 505d839940456a3d04321d75cf66cc3b5bc831c4 (wip/ell1-highD) |
| RAW | `C:/Users/nathan/Source/signtest_lowD_1025/raw`: the 21 raw files of the driver's INPUTS list and `I1025-mac/signtest.py`, each taken by `git show origin/main:<path>` and checked by `git hash-object --no-filters` against its pinned blob (log `prep_raw_inputs_1025.log`, 22 files, 406 KB). The driver checks all 25 inputs itself |
| PY | `C:/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe` (Python 3.14.10) |
| threads | `BLAS_THREADS=4`, BelowNormal priority, row timeout the driver's default 7200 s |

Each row runs `signtest.py STATE D kc around=RECORD:D:0.02` with the record's own `--u0 --Ks --kappa --rk`. It first checks that these rebuild the record's discrete system (|F| within 1% of the record's or 1e-13, same step count) and exits 3 without signs if not.

## Command

```
PY=C:/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe ROWS_D=14.5,14,13.5,12,11.5,11,10.5 BLAS_THREADS=4 \
  bash signtest_lowD_driver_v2.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/signtest_lowD_1025/raw <OUT>
```

OUT is a staging folder outside the push worktree, `C:/Users/nathan/Source/signtest_lowD_1025/I1025-win/signtest_lowD`, so that no worktree moves under the running job; its files are copied here for each push.

## Checks, fixed before the run

- The planted control (`signtest.py planted`) must print agree, agree, DISAGREE, else the driver stops at once.
- A row PASSES if both lambda - 0.02 and lambda + 0.02 have agree true and opposite signs. Exit 3 is SYSTEM MISMATCH (no signs); a timeout or crash counts toward the driver's stop rule (two in a row).
- The driver has not been run on Windows before: a refusal or crash on a path is reported at once.

## Result (driver finished 2026-11-20 18:17:16 UTC, written 2026-11-20 18:17 UTC)

All seven rows PASS. Run from 17:33:36 to 18:17:16 UTC: inputs checked (all 25, `signtest.py` blob, WT commit; numpy 2.5.4, scipy 1.18.1), the planted control printed agree, agree, DISAGREE (`signtest_lowD_planted.log`), then the rows in the order D 14.5, 14, 13.5, 12, 11.5, 11, 10.5. Every row's system check had the same step count as its record and |F| within the record's (`same: true`), so each signtest ran on the record's own discrete system. A row passes if both lambda -+ 0.02 have agree true and opposite signs.

| D | k_c | system check (F, record F, steps) | lam - 0.02 | signs | lam + 0.02 | signs | agree | below 1e-12 / 1e-15 | s | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 14.5 | 55 | F 2.241e-10, record 2.240e-10, 2786 = 2786 steps, same true | 2.4760793 | -1, -1, -1, -1 | 2.5160793 | 1, 1, 1, 1 | true, true | 40 / 10 ; 40 / 10 | 276, 268 | PASS |
| 14 | 47 | F 2.369e-10, record 2.369e-10, 2434 = 2434 steps, same true | 2.5456420 | -1, -1, -1, -1 | 2.5856420 | 1, 1, 1, 1 | true, true | 28 / 4 ; 28 / 4 | 172, 169 | PASS |
| 13.5 | 47 | F 2.497e-10, record 2.496e-10, 2479 = 2479 steps, same true | 2.6084136 | -1, -1, -1, -1 | 2.6484136 | 1, 1, 1, 1 | true, true | 24 / 2 ; 24 / 2 | 162, 157 | PASS |
| 12 | 47 | F 3.070e-11, record 3.070e-11, 2584 = 2584 steps, same true | 2.7523124 | -1, -1, -1, -1 | 2.7923124 | 1, 1, 1, 1 | true, true | 6 / 0 ; 6 / 0 | 170, 165 | PASS |
| 11.5 | 47 | F 2.275e-11, record 2.272e-11, 2605 = 2605 steps, same true | 2.7829219 | -1, -1, -1, -1 | 2.8229219 | 1, 1, 1, 1 | true, true | 2 / 0 ; 2 / 0 | 171, 168 | PASS |
| 11 | 47 | F 1.637e-11, record 1.635e-11, 2626 = 2626 steps, same true | 2.8160397 | -1, -1, -1, -1 | 2.8560397 | 1, 1, 1, 1 | true, true | 0 / 0 ; 0 / 0 | 181, 171 | PASS |
| 10.5 | 47 | F 3.776e-12, record 3.774e-12, 2650 = 2650 steps, same true | 2.8529585 | -1, -1, -1, -1 | 2.8929585 | 1, 1, 1, 1 | true, true | 0 / 0 ; 0 / 0 | 190, 181 | PASS |

Row wall times (4 BLAS threads, BelowNormal): D 14.5 9.1 min, D 14 5.7, D 13.5 5.4, D 12 5.6, D 11.5 5.7, D 11 5.9, D 10.5 6.2; 43.6 min for the seven rows. The counts of singular values of Q M below 1e-12 and 1e-15 fall from 40 and 10 at D 14.5 to 0 at D 11 and 10.5. The log's summary: seven lines `D <D> k_c <kc>: PASS`. A passing signtest checks the rounding of the determinant, not the accuracy of M's construction. The reading of the rows stays with #1025.

## Files

| file | what |
|---|---|
| `README.md` | this file (written before the run; the status and result sections updated) |
| `signtest_lowD_driver_v2.sh` | the driver, byte-identical to raw `I1025-mac/signtest_lowD_driver_v2.sh` (blob c4f92d36) |
| `signtest_lowD.log`, `signtest_lowD.jsonl`, `signtest_lowD_planted.log`, `signtest_lowD_rows/D*.log` | the driver's log, its 21 JSON lines (7 system checks and 14 signtest lines), the control and each row's full output |
| `prep_raw_inputs_1025.sh`, `prep_raw_inputs_1025.log` | how the RAW input folder was made from pinned blobs by `git show` (22 files) |
| `start_lowD_1025.cmd`, `publish_lowD_1025.sh`, `table_lowD_1025.py`, `fix_readme_lowD_1025.py` | the detached launcher, the copy-and-push script, the table and README patch scripts |
