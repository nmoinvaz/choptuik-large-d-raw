# I1025-dh610/kc87_d195: dh370's k_c 79 D 19.5 state regridded to k_c 87, then a hybrid sign scan at lambda_1 1.36 to 1.44

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc79_d195/` (raw cc372303): k_c 87 at D 19.5, so that lambda_1 has a third k_c there.

## Order (the coordinator's)

1. **Regrid** dh370's accepted k_c 79 D 19.5 state (raw `I1025-dh370/kc79_d195/sol_l1kc79dh370d195_D19.5000.npy`, record `l1kc79dh370d195.jsonl`, f40a4556; blobs pinned) to k_c 87 with `ell_refine.py` as dh370 ran its k_c 79 regrids (its `kc79_d195` README: the command, lambda_0 from `ell_delta.lam0_at(19.5)`, `--no-gamma`), source k_c 79, target k_c 87. First `kc79_syscheck_1025.py` on the source (must accept, both controls refuse). Accept the k_c 87 state only by a kc87 check made from `kc79_syscheck_1025.py` by changing the k_c 79 test to k_c 87 and nothing else (the diff is in this folder), with its selftest and both controls (they must refuse). 8 threads, nice 10, a systemd unit.
2. **Scan** the accepted state: lambda 1.36 to 1.44 at 0.01 (9 values) plus a repeat of 1.40, 6 processes of 1 thread, `read_lower.py`.
3. If `ell_refine.py` cannot reach k_c 87 (a size or array limit), stop and report; change no code. Read roots by position. Report each step's verdict with the raw commit; post on #1025. Estimate: regrid about 1 h (unknown at k_c 87), scan about 2 rounds.

Beside which I report (information, not a pass rule): k_c 79's line of lambda_1 near 1.398 at D 19.5 (the coordinator's line; `../kc79_d195/` found no k_c 79 root in 1.41 to 1.50, sign - at 1.41, and dh370 reads 1.30 to 1.40); k_c 71 has two roots near the line at D 19.5, 1.3715 and 1.4492 (the coordinator's numbers).

## Setup

- Regrid: unit `i1025p` (`lane_kc87_regrid.sh`, started by `start_kc87_regrid.sh`), `OMP`, `OPENBLAS`, `MKL` = 8, nice 10, cap 21600 s, under `systemd-inhibit` with the alert-only memory log; steps and verdicts in `regrid/steps.txt` and `regrid/VERDICT.txt`.
- Code: worktree `~/Source/choptuik-large-d-1025g` at 48c36355 (made for this task; the one dh370 ran its regrids in): `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's (the scan's pin), `ell_refine.py` blob 631e5801, `ell_delta.py` blob fde699f5. Python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2); dh370 ran its regrids in `~/Source/choptuik-large-d-1058b/.venv` (3.14, multidouble 5.1.0, avx2). The lane refuses on any other pin.
- Inputs (copied to `in/`, pinned by `git hash-object --no-filters`, `in_blobs.txt`): dh370's `sol_l1kc79dh370d195_D19.5000.npy` 9528b355 and `l1kc79dh370d195.jsonl` 5777d2a2; `kc79_syscheck_1025.py` 29dce7ea (winb's, raw `I1025-win/kc79_d19/`); `kc87_syscheck_1025.py` 6df5d960 (below); `d18_hybsign.py` e089207a (xfkappa's, unmodified), `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited).
- The k_c 87 check, `in/kc87_syscheck_1025.py`: `kc79_syscheck_1025.py` with three lines changed, the k_c test and its message (`rec.get("kc") != 87`, "the record is not k_c 87 ...") and the selftest's planted record (`kc=87`); nothing else, not the docstring either (`kc87_syscheck_1025.diff`; the lane rebuilds the diff, requires that it equals this file and has three changed lines).

## Commands (regrid)

    cd ~/Source/choptuik-large-d-1025g/solver/matter && nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 \
      ~/Source/venv-i1058/bin/python -u ell_refine.py l1kc79dh370d195 79 l1kc87dh610d195 87 1 19.5 2.1132623525 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

dh370's command for k_c 79 at D 19.5 with the source tag, the target tag, k_c 79 and k_c 87 changed; lambda_0(19.5) = 2.1132623525 from `ell_delta.lam0_at(19.5, *ell_delta.lam0_table())` (the lane recomputes it and refuses if it differs; error 6.2e-7; `--no-gamma` does not use it). The lane runs, in this order and stopping at the first failure: the pins, the worktree checks, the two selftests, the source check with its controls, the regrid, the acceptance with its controls.

## Acceptance (fixed before the run, as dh370's, with k_c 87)

1. **Source.** `kc79_syscheck_1025.py` accepts dh370's k_c 79 D 19.5 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1, and both selftests exit 0. Extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1 (the k_c test fires). Otherwise no regrid.
2. **Result.** `kc87_syscheck_1025.py` accepts the regridded record and state (k_c 87 at D 19.5, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1. Extra control: `kc79_syscheck_1025.py` on the k_c 87 result exits 1. A regrid that exits non-zero, hits the 21600 s cap, or cannot be built at k_c 87 is a stop, and I report.

The scan lane is written after the verdict. Each scan process first prints `the record system` (`d18_hybsign.py`'s check of the state against its record), and anything else is a stop. The k_c 87 control of this machine against another machine's row does not exist (no other machine has this state); the record system check and the repeat are the controls of the scan.

Written as the run goes.

## Status (22 Nov)

- 20:22:44 UTC the source check passed (dh370's k_c 79 D 19.5 state: |F| 3.5136527614e-10 against the record's 3.5122938292e-10, steps 2879 = 2879; `--mutate=F` and `--mutate=steps` exit 1; selftests 0; the k_c 87 check refuses the k_c 79 source), the regrid started (unit `i1025p`, 8 threads; 313 MB RSS and 747% CPU at 1 min, no size or array error). The scan lane `lane_kc87_scan.sh` (unit `i1025q`, `start_kc87_scan.sh`) is written and waits for `regrid/VERDICT.txt` to read ACCEPTED and for `in_blobs_regrid.txt` (the blobs of the regridded state and record, written after the regrid): lambda 1.36 to 1.44 at 0.01 plus a repeat of 1.40, ten evaluations, the repeat on process 5 and its original on process 4, `read_lower.py scan 1.36 1.44` and `repeat_check.py` (`read_lower.txt`).
- 21:17:50 UTC the regrid was accepted (below) and the scan started (unit `i1025q`, `lane_kc87_scan.sh`): lambda 1.36, 1.37, 1.38, 1.39, 1.40 (original, process 4), 1.40 (repeat, process 5), 1.41, 1.42, 1.43, 1.44, ten evaluations on 6 processes of 1 thread, nice 10; it ended at 22:21:50 UTC, all six processes exit 0. Result below.

## Regrid result (22 Nov, 20:22:44 to 21:16:23 UTC): ACCEPTED

`ell_refine.py` (8 threads, nice 10, unit `i1025p`) exited 0 after 3215 s (the record's own 3213 s); peak sampled RSS 2.27 GB; no size or array error (`regrid/regrid.log`, `regrid/regrid_samples.csv`, `regrid/steps.txt`). Its log carries 25 numpy RuntimeWarnings (overflow, invalid value) from `dss_ell.py` lines 88, 211 to 219, 325 and 334 in the solver's trial evaluations; dh370's k_c 79 regrid log has 21 of the same kind at the same lines; the acceptance is the check below, not the log.
- Record `l1kc87dh610d195.jsonl` (blob 64b8db7c) and state `sol_l1kc87dh610d195_D19.5000.npy` (blob 57f8e2d3, copied to `in/`; `in_blobs_regrid.txt`): k_c 87 at D 19.5, |F| 3.5228509267e-10, F_start 5.096e-06, 3171 steps, constraint 7.311e-04, Delta 1.0798374906 (dh370's k_c 79 state: |F| 3.5123e-10, 2879 steps, constraint 1.273e-03, Delta 1.0798406632).
- **Acceptance:** `kc87_syscheck_1025.py` exit 0 (the state's |F| equals the record's, freeze_from gives 3171 steps = the record's); `--mutate=F` exit 1 (the state's |F| is not within 1% of 1.5 times the record's), `--mutate=steps` exit 1 (freeze_from gives 3171, the record 3172); extra control: `kc79_syscheck_1025.py` on the k_c 87 result exit 1 ("the record is not k_c 79 at D 19.5 (kc 87, D 19.5)"). Verdict `regrid/VERDICT.txt`: ACCEPTED 21:16:23 UTC.

## Scan result (22 Nov, 21:17:50 to 22:21:50 UTC): one robust change in 1.36 to 1.44, between 1.39 and 1.40; the repeat agrees

All six processes exit 0 (`exits_kc87_scan.txt`). Walls: 1:03:56 to 1:03:59 for processes 0 to 3 (two points each) and 36:38 (process 4) and 36:43 (process 5) for the one-point processes; peak RSS 2.70 to 2.79 GB for the two-point processes and 2.12 and 2.29 GB for the one-point ones (`scan/scan_p<p>.raw`, `/usr/bin/time -v`). Sampled every minute (`scan/sampler.log`): summed RSS at most 8.97 GB, MemAvailable at least 22.46 GB. The pre-run checks passed (`selftest_exits.txt`: read_lower 0, `--mutate=shift` 1, `--mutate=round2` 1, repeat_check 0). The system check printed "the record system" on all six: |F| 3.5200981508e-10 against the record's 3.5228509267e-10 (relative 7.8e-4, inside the 1e-2 bar; one thread prints the |F| a little off the 8-thread regrid's), steps 3171 = 3171. All ten evaluations are noise-robust. A point took 2195 to 2207 s in round 1 (six processes) and 1629 to 1637 s in round 2 (four processes). No other machine holds this state, so there is no cross-machine control; the system check and the repeat are the controls.

| lambda_1 | process | hybrid sign | ln\|det\| | noise_robust | float64 sign | point sec |
|---|---|---|---|---|---|---|
| 1.36 | 0 | +1 | -2823.9426546920 | True | +1 | 2207 |
| 1.37 | 1 | +1 | -2824.5773567326 | True | +1 | 2202 |
| 1.38 | 2 | +1 | -2825.3319293523 | True | +1 | 2200 |
| 1.39 | 3 | +1 | -2826.4073684168 | True | +1 | 2205 |
| 1.40 | 4 | -1 | -2828.8083845642 | True | +1 | 2195 |
| 1.40 (repeat) | 5 | -1 | -2828.8083845642 | True | +1 | 2200 |
| 1.41 | 0 | -1 | -2826.8065413728 | True | -1 | 1629 |
| 1.42 | 1 | -1 | -2826.4630742704 | True | +1 | 1631 |
| 1.43 | 2 | -1 | -2826.3660508021 | True | -1 | 1637 |
| 1.44 | 3 | -1 | -2826.3702619384 | True | -1 | 1632 |

Reading (`read_lower.txt`, `read_lower.py` dh170's, unedited; signs as the reader prints them):
- **Robust change:** one, between 1.39 and 1.40, `+ to -` as the reader prints it, det-linear estimate **1.399169**, estimator range [1.398747, 1.399169] (a spread over interpolation choices, not an enclosure). No change touches a non-robust point.
- **Edge signs:** + at 1.36, - at 1.44.
- **ln|det| minima without a sign change:** none. ln|det| is lowest at 1.40, the point beside the change (the deepest of the scan: 2.40 below its + neighbor at 1.39 and 2.00 below its - neighbor at 1.41); above it ln|det| rises to -2826.366 at 1.43 and is flat at 1.44 (-2826.370), a maximum, not a minimum.
- **Repeat of 1.40:** agrees, bit-identical (`repeat_check.py` PASS; ln -2828.80838456417 on process 4 and on process 5). Same machine, same build, so it tests the run's repeatability, not another machine.
- **Float64:** its sign differs from the hybrid at 1.40 and 1.42 (+ against -), as before; the hybrid is the reading.

Beside which I report (information, not a pass rule; the coordinator's numbers): k_c 79's line of lambda_1 near 1.398 at D 19.5; k_c 71's two roots near the line at D 19.5, 1.3715 and 1.4492.
- By position the k_c 87 root at 1.3992 is the root near lambda_1's line: 0.0012 above 1.398.
- It is 0.0277 above k_c 71's root at 1.3715 and 0.0500 below k_c 71's root at 1.4492. The scan stops at 1.44, so nothing is read at or above 1.4492: no statement about a second k_c 87 root there. In 1.36 to 1.39 the signs are all + and ln|det| falls monotonically, so no k_c 87 change at 1.3715 at this 0.01 spacing (two changes closer than 0.01 would not show).
- Nothing was scanned below 1.36 or above 1.44.

These are k_c 87 roots, not yet physical.
