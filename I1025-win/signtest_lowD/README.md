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

## Status

Started 17:33:36 UTC: the driver's input checks passed (all 25 inputs, `signtest.py` blob, WT commit; numpy 2.5.4, scipy 1.18.1) and the planted control printed agree, agree, DISAGREE (`signtest_lowD_planted.log`). Row D 14.5 started at 17:33:39 UTC. Results follow in `signtest_lowD.log`, `signtest_lowD.jsonl`, `signtest_lowD_planted.log` and `signtest_lowD_rows/`.
