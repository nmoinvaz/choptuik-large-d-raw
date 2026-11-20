# I1025-rpi5: signtests of the 16 delta-table rows at D <= 14.5 (D 4 to 14.5, l = 1 multiplet) on rpi5, by xfkappa's driver

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task named by the coordinator by message, 2026-11-20 (a second job beside #1013's recount3, which runs in `I1013-rpi5-cap/recount3/` and is not touched).

## What it does
`I1025-mac/signtest_lowD_driver.sh` (raw 5955fbdc, blob 8be8d1cd9540b702567764bb0ab0022c5d9c5025, the driver's own header documents the rest) checks every input by git blob (it refuses on a mismatch) and the code worktree's HEAD, then:
1. the planted control (`signtest.py planted`): it must print agree, agree, DISAGREE, or the batch stops;
2. one row at a time, nice 10, 2 BLAS threads, a 7200 s timeout per row: `signtest.py STATE D kc around=RECORDS:D:0.02 --u0 --Ks --kappa --rk` of the record's own settings. `signtest.py` first checks that these rebuild the record's discrete system (|F| within 1% of the record's or 1e-13, the same step count) and exits 3 without signs if not.
3. A row PASSES if both lambda - 0.02 and + 0.02 have agree true and opposite signs; exit 3 is SYSTEM MISMATCH, exit 124 TIMEOUT, other nonzero CRASH. The batch stops after 2 consecutive timeouts or crashes.
The 16 rows: D 4 (k_c 47), 5 (39), 6 (31), 7 to 10 (39), 10.5 to 12 (47), 12.5 and 13 (39), 13.5 and 14 (47), 14.5 (55).

## Setup
- Code: worktree `~/Source/choptuik-1025st`, detached at `wip/ell1-highD` 505d839940456a3d04321d75cf66cc3b5bc831c4 (the driver refuses any other HEAD). Python 3.13.7, numpy 2.5.4, scipy 1.18.1 (venv-choptuik; the driver prints them).
- Inputs: this raw clone is a full checkout, not sparse, so RAW for the driver is the push worktree `~/Source/choptuik-large-d-raw-964` at raw 26164229 (read only; the live clone `~/Source/choptuik-large-d-raw` is not pulled while jobs write). All 24 input blobs are checked by the driver.
- Output: this folder, in the live clone; pushed from the push worktree after the control and at the end.
- Command, from `~/Source/choptuik-large-d`:
  `PY=~/Source/venv-choptuik/bin/python nice -n 10 bash ~/Source/choptuik-large-d-raw-964/I1025-mac/signtest_lowD_driver.sh ~/Source/choptuik-1025st ~/Source/choptuik-large-d-raw-964 ~/Source/choptuik-large-d-raw/I1025-rpi5`
- Beside it, #1013's recount3 runs 4 processes at nice 10 on the same 4 cores, so both jobs are slower than alone; the row timeout (7200 s) is wall time.

## Criteria (the driver's, fixed before the run)
1. Planted control prints agree, agree, DISAGREE.
2. Each row's verdict is the driver's (PASS, FAIL, SYSTEM MISMATCH, TIMEOUT, CRASH); a row counts only with PASS (coordinator's rule). A mismatch or a crash is reported as it is, not retried or repaired by me.
3. The result table (D, k_c, verdict) is posted on #1025. The driver's log and jsonl are the raw record (`signtest_lowD.log`, `signtest_lowD.jsonl`, `signtest_lowD_rows/D<D>.log`, `signtest_lowD_planted.log`).

## Split with winb (coordinator, 2026-11-20, message at about 17:30 UTC)
The low-D batch is split so that winb takes 7 of the 16 rows (k_c 47 at D 10.5, 11, 11.5, 12, 13.5 and 14, and k_c 55 at D 14.5) and no row runs twice. This machine keeps 9 rows: D 4 (k_c 47), 5 (39), 6 (31), 7, 8, 9, 10, 12.5 and 13 (all 39). The result table posted on #1025 covers these 9 rows only.
1. After the next verdict line in `signtest_lowD.log` (D 8's), the v1 driver (`signtest_lowD_driver.sh`) and the signtest it had just started (D 9's) are stopped, by pid (the driver first, so that it cannot write a verdict for the killed row; no `pkill -f`). D 9 then has no verdict in the log and runs again under v2. recount3's processes are not touched. The kill times and pids are under Runs.
2. v2 resumes in this folder: `git show origin/main:I1025-mac/signtest_lowD_driver_v2.sh` (raw 0596f58f, blob c4f92d36043f2b72299dd8cd9a59377fad564e7e; a copy sits here as `signtest_lowD_driver_v2.sh`), `PY=~/Source/venv-choptuik/bin/python RESUME=1 ROWS_D=4,5,6,7,8,9,10,12.5,13 BLAS_THREADS=2 nice -n 10 bash signtest_lowD_driver_v2.sh ~/Source/choptuik-1025st ~/Source/choptuik-large-d-raw-964 ~/Source/choptuik-large-d-raw/I1025-rpi5`. Rows whose verdict is in the log are skipped. v2 checks the same inputs and HEAD, runs the planted control again (its lines are appended to `signtest_lowD.log`; it overwrites `signtest_lowD_planted.log`, so v1's copy is kept as `signtest_lowD_planted_v1.log`) and writes each row's output to `signtest_lowD_rows/D<D>.log` (D 9's partial v1 file is kept as `signtest_lowD_rows/D9.v1_killed.log`).

## Runs
All times UTC, 2026-11-20 (clock `date -u`).
- 15:41:47 v1 driver started. Planted control: agree, agree, DISAGREE (raw aa769031). Verdicts: D 4 (k_c 47) PASS 31.4 min, D 5 (39) PASS 23.5 min, D 6 (31) PASS 8.4 min, D 7 (39) PASS 24.5 min, D 8 (39) PASS 27.4 min (verdict 17:37:06). Each row's system check was `same: true` (steps and |F| as in the record).
- 17:37:07 after D 8's verdict: v1 driver stopped by pid (960854, `driver exit 143` in `driver.start`; killed first so it could not write a verdict). 17:37:07 to 17:37:08: D 9's signtest stopped by pid (975689 `timeout`, 975690 `python`). `ps` afterwards showed only recount3's 949245 and 949246 (its worker processes were not listed and kept running). D 9's partial v1 output (its first line) is `signtest_lowD_rows/D9.v1_killed.log`; D 9 has no verdict from v1.
- 17:37:20 v2 started (the command above; `v2 start` in `driver.start`). Planted control again: agree, agree, DISAGREE. D 4 to 8 skipped (verdict already in the log). D 9 started again at 17:37:23.
- 18:41:21 v2 done, exit 0 (`v2 exit` in `driver.start`): D 9, 10, 12.5 and 13 all PASS. The 9 rows of this machine are done; the other 7 rows are winb's.

## Result (this machine's 9 rows; verdict is the driver's)
| D | k_c | verdict | signs at lambda - 0.02 / + 0.02 | singular values below 1e-12 | smallest singular value printed (at - 0.02, + 0.02) | row time |
|---|---|---|---|---|---|---|
| 4 | 47 | PASS | -1 / +1, all 4 Q agree | 0 | 2.0e-8, 1.9e-8 | 31.4 min |
| 5 | 39 | PASS | -1 / +1, agree | 0 | 2.5e-6, 2.4e-6 | 23.5 min |
| 6 | 31 | PASS | -1 / +1, agree | 0 | 1.2e-5, 1.2e-5 | 8.4 min |
| 7 | 39 | PASS | -1 / +1, agree | 0 | 5.0e-6, 5.3e-6 | 24.5 min |
| 8 | 39 | PASS | -1 / +1, agree | 0 | 3.0e-7, 3.4e-7 | 27.4 min |
| 9 | 39 | PASS | -1 / +1, agree | 0 | 9.4e-9, 1.1e-8 | 41.0 min (v2; v1's stopped start discarded) |
| 10 | 39 | PASS | -1 / +1, agree | 0 | 1.1e-10, 1.5e-10 | 10.8 min |
| 12.5 | 39 | PASS | -1 / +1, agree | 6 | 9.2e-14, 1.1e-13 | 6.1 min |
| 13 | 39 | PASS | -1 / +1, agree | 10 | 1.8e-14, 2.0e-14 | 6.1 min |
Every row's system check printed `same: true` (the record's step count and |F| within 1% of the record's or 1e-13). No SYSTEM MISMATCH, TIMEOUT or CRASH. Row times differ with the load: recount3 shares the 4 cores and each row has 2 BLAS threads.

Observation, not a failure: D 12.5 and D 13 have 6 and 10 singular values below 1e-12 (the driver's counter; none below 1e-15 in any row), and the 4 random orthogonal Q still agree on the sign. The planted control has 40 singular values at 1e-13 (agree) and 40 at 1e-19 (DISAGREE), but its matrix is scaled to a largest value of about 1 and these are not, so I do not read the control as a margin for D 13.

## Criteria met
1. Planted control agree, agree, DISAGREE: met, by v1 (15:41:48) and again by v2 (17:37:20).
2. Verdict per row, counted only with PASS: all 9 PASS; nothing was retried or repaired.
3. The result table is posted on #1025 (comment 7047740827, 2026-11-20 about 18:50 UTC). The raw record: `signtest_lowD.log`, `signtest_lowD.jsonl`, `signtest_lowD_rows/D<D>.log`, `signtest_lowD_planted.log` (v2's) and `signtest_lowD_planted_v1.log`.

## Second job: more random Q at D 12.5 and 13 (coordinator, 2026-11-20, message about 18:50 UTC; written before the runs)
Why: D 12.5 and D 13 PASS with 6 and 10 singular values below 1e-12 (smallest printed 9.2e-14 and 1.8e-14), and I suggested more random Q as margin. xfkappa's `I1025-mac/signtest_q.py` (raw 50a478fc, blob 0b7c6caf21df007292b8b0a6b9ac37e16275743c) is `signtest.py` (blob 179ea096) plus `--nq=N` (default 3, the same seed, so the first 3 Q are the same at any N). Criteria are xfkappa's `I1025-mac/signtest_moreq_criteria.log` (read before the run):
1. The check that can fail: at `--nq=12` the first 4 signs (the LU's and the first 3 Q's) and `logabs` at each lambda equal this folder's nq=3 lines in `signtest_lowD.jsonl` (same machine, same inputs).
2. The margin passes if all 13 signs agree at each lambda and the two lambda have opposite signs. A disagreement among the extra Q is reported; it does not undo the PASS by itself, the coordinator rules.
Runs: k_c 39, lambda - 0.02 and + 0.02 of the record `l1kc39L1025` at D 12.5 and at D 13, with the record's u0 0.04, Ks 30, kappa 0.7, rk 1 (signtest_q.py's defaults). Command as the coordinator gave it, from `~/Source/choptuik-1025st/solver/matter` (worktree at 505d8399), RAW = `~/Source/choptuik-large-d-raw-964` (raw f99b8df9):
`for D in 12.5 13; do OPENBLAS_NUM_THREADS=2 nice -n 10 ~/Source/venv-choptuik/bin/python -u $RAW/I1025-mac/signtest_q.py $RAW/I1025-mac/out/sol_l1kc39L1025_D$(printf %.4f $D).npy $D 39 around=$RAW/I1025-mac/out/l1kc39L1025.jsonl:$D:0.02 --nq=12 > signtest_moreq_D$D.log 2>&1; done`
Output: `signtest_moreq_D12.5.log`, `signtest_moreq_D13.log`; `moreq.start` has the start and exit times. Beside it recount3 runs 4 processes at nice 10 (#1013), so the times are for a shared machine.

### Result of the second job (2026-11-20, run 18:49:51 to 19:16:28 UTC, `moreq.start`; both rows exit 0)
| D | lambda - 0.02, + 0.02 | signs (13 each) | first 4 signs and logabs vs the nq=3 lines | singular values below 1e-12 | time |
|---|---|---|---|---|---|
| 12.5 | 2.7123751, 2.7523751 | all -1, all +1 | equal, logabs bit-equal (diff 0) | 6 (nq=3: 6) | 12.9 min (380 s, 393 s per lambda) |
| 13 | 2.6641825, 2.7041825 | all -1, all +1 | equal, logabs bit-equal (diff 0) | 10 (nq=3: 10) | 13.7 min (413 s, 407 s per lambda) |
`moreq_check.py` prints this and exits 0; its three controls (`--mutate=signs`, `logabs`, `nq`) each exit 1. Both system checks printed `same: true`. Criteria met: (1) the first 4 signs and logabs equal the nq=3 lines at all four lambda; (2) all 13 signs agree at each lambda and the two lambda have opposite signs. No disagreement among the extra Q. The coordinator rules on what this does to the D 12.5 and D 13 rows (the PASS is not changed by this job).
