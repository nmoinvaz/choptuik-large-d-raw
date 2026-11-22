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
