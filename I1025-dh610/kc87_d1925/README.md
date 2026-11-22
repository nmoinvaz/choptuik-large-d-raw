# I1025-dh610/kc87_d1925: macm3's k_c 79 D 19.25 state regridded to k_c 87, then a hybrid sign scan at lambda_1 1.42 to 1.52

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc87_d195/` (raw 94e9ebc6): k_c 87 at D 19.25, the same regrid and scan as there at a smaller D.

## Order (the coordinator's)

1. **Regrid** macm3's accepted k_c 79 D 19.25 state (raw `I1025-macm3/kc79_d1925/`, 5dd45fae or later: `sol_l1kc79macm3_D19.2500.npy` and `l1kc79macm3.jsonl`, pinned by blob below; a macOS state is a fine source, the k_c 87 state is then this machine's) to k_c 87 exactly as the D 19.5 regrid (`../kc87_d195/`): `kc79_syscheck_1025.py` on the source first (must accept, both controls refuse), the kc87 check with both controls on the result, and the k_c 79 check must refuse the result. 8 threads, nice 10.
2. **Scan** the accepted state: lambda 1.42 to 1.52 at 0.01 (11 values) plus a repeat of 1.47, 4 processes of 1 thread (the order cites my D 19.5 measurement: 4 processes cost about 1630 s a point against about 2200 s with 6), `read_lower.py`.
3. Read roots by position. Post on #1025, send the coordinator each step's verdict with the raw commit.

Beside which I report (information, not a pass rule; the coordinator's numbers): k_c 79 at D 19.25 has lambda_1 at 1.469975 and no other root in 1.42 to 1.52 (macm3, raw cc30e59c); the reading predicts that k_c 87's rising root crosses lambda_1 only after D 19.31, so it should not be in this window either. At D 19.5 the k_c 87 root near lambda_1's line is 1.399169 (`../kc87_d195/`) against k_c 79's 1.397565.

## Setup

- Regrid: unit `i1025r` (`lane_kc87_d1925_regrid.sh`, started by `start_kc87_d1925_regrid.sh`), `OMP`, `OPENBLAS`, `MKL` = 8, nice 10, cap 21600 s, under `systemd-inhibit` with the alert-only memory log; steps and verdicts in `regrid/steps.txt` and `regrid/VERDICT.txt`. The lane is `../kc87_d195/lane_kc87_regrid.sh` with the D, the tags, the source blobs and lambda_0 changed; nothing else.
- Code (as at D 19.5): worktree `~/Source/choptuik-large-d-1025g` at 48c36355 for `ell_refine.py` (blob 631e5801; `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's) and worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean) for the scan; Python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2). The lanes refuse on any other pin.
- lambda_0(19.25) = 2.1144367878 from `ell_delta.lam0_at(19.25, *ell_delta.lam0_table())` (macm3's value; the lane recomputes it with worktree 48c36355's `ell_delta.py` and refuses if it differs; `--no-gamma` does not use it).
- Inputs (copied to `in/`, pinned by `git hash-object --no-filters`, `in_blobs.txt`): macm3's `sol_l1kc79macm3_D19.2500.npy` 0bc41565 and `l1kc79macm3.jsonl` 75855f71 (the same blobs at raw 5dd45fae, cc30e59c and 94e9ebc6; the record is k_c 79, D 19.25, |F| 3.066078749798487e-10, 2925 steps, constraint 9.574e-04, Delta 1.0737660558, macOS NEON build, 578 s); `kc79_syscheck_1025.py` 29dce7ea (winb's); `kc87_syscheck_1025.py` 6df5d960 (the k_c 79 check with three lines changed, `kc87_syscheck_1025.diff`, as at D 19.5); `d18_hybsign.py` e089207a (xfkappa's, unmodified), `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited).

## Commands

Regrid (cwd `~/Source/choptuik-large-d-1025g/solver/matter`; the source state is copied to `data/sol_l1kc79macm3_D19.2500.npy` and checked by blob):

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 \
      ~/Source/venv-i1058/bin/python -u ell_refine.py l1kc79macm3 79 l1kc87dh610d1925 87 1 19.25 2.1144367878 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

Scan (`lane_kc87_d1925_scan.sh`, unit `i1025s`, written from `../kc87_d195/lane_kc87_scan.sh` with the D, the tags, the process count and the lambda list changed): `d18_hybsign.py in/l1kc87dh610d1925.jsonl in/sol_l1kc87dh610d1925_D19.2500.npy 19.25 <lambdas> scan/scan_D19.25_p<p>.jsonl` in 4 processes of 1 thread, nice 10; the list is 1.42 to 1.52 then the repeat 1.47, value i to process i mod 4 (macm3's splitting at k_c 79): p0 1.42, 1.46, 1.50; p1 1.43, 1.47, 1.51; p2 1.44, 1.48, 1.52; p3 1.45, 1.49 and the repeat 1.47, so the repeat runs on a different process than its original. Then `read_lower.py scan 1.42 1.52` and `repeat_check.py` (`read_lower.txt`), after the reader's selftest and its mutations `shift` and `round2` (exits wanted 0 1 1 0 with `repeat_check.py selftest`).

## Acceptance (fixed before the run, as at D 19.5)

1. **Source.** `kc79_syscheck_1025.py` accepts macm3's k_c 79 D 19.25 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, 2925, and |F| within 1% of the record's), `--mutate=F` and `--mutate=steps` exit 1, both selftests exit 0, and the k_c 87 check refuses the k_c 79 source. Otherwise no regrid. (The dry run of the lane, `regrid/source_syscheck*.txt`, has done this: the state's |F| is 3.0762761295e-10 against the record's 3.0660787498e-10, steps 2925 = 2925, controls exit 1.)
2. **Result.** `kc87_syscheck_1025.py` accepts the regridded record and state (k_c 87 at D 19.25, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1, and `kc79_syscheck_1025.py` on the k_c 87 result exits 1. A regrid that exits non-zero, hits the 21600 s cap or cannot be built is a stop, and I report; no code is changed.
3. **Scan.** Starts only after the verdict ACCEPTED. Each process first prints `the record system`; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.47 agrees (`repeat_check.py`). No other machine holds this state, so there is no cross-machine control for the k_c 87 scan: the system check and the repeat are the controls, as at D 19.5.

## Reading (fixed before the run)

Every robust change (bracket, orientation as printed by the reader, det-linear estimate, estimator range); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. A root is named by position (the root near lambda_1's line, the rising root), its orientation printed only as the reader prints it and never compared across D. Roots are called k_c 87 roots, not yet physical.

## Predictions (written before the run; information)

The regrid exits 0 and is accepted (85%), in 3200 to 3600 s with about 3220 steps (D 19.5: 3215 s, 3171 steps from a 2879-step source; here the source has 2925); the scan shows one robust change in 1.42 to 1.52 (70%), within 0.005 of macm3's k_c 79 value 1.469975 (70% given one), and no second (80%); a point takes about 1600 s with 4 processes (the scan about 1.4 to 1.6 h).

## Status (22 Nov)

- 22:25:14 UTC the dry run of the regrid lane passed the pins, the selftests and the source check (see Acceptance 1); nothing started yet.
- 22:26:29 UTC the regrid started (unit `i1025r`, 8 threads; the source check of the real run passed again: exit 0, controls exit 1, 1; the k_c 87 check refuses the k_c 79 source). 23:21:27 UTC ACCEPTED (below). 23:22:11 UTC the scan lane's dry run passed (pins, selftests 0 1 1 0).

## Regrid result (22 Nov, 22:26:29 to 23:21:27 UTC): ACCEPTED

`ell_refine.py` (8 threads, nice 10, unit `i1025r`) exited 0 after 3293 s (the record's own 3291 s); peak sampled RSS 2.27 GB, 773 to 777% CPU; no size or array error (`regrid/regrid.log`, `regrid/regrid_samples.csv`, `regrid/steps.txt`). Its log carries 21 numpy RuntimeWarnings (overflow, invalid value) from `dss_ell.py` lines 88, 211 to 219, 325 and 334 in the solver's trial evaluations (the D 19.5 regrid's log had 25 of the same kind at the same lines); the acceptance is the check below, not the log.
- Record `l1kc87dh610d1925.jsonl` (blob fb0c7e77) and state `sol_l1kc87dh610d1925_D19.2500.npy` (blob 1dd46e46, copied to `in/`; `in_blobs_regrid.txt`): k_c 87 at D 19.25, |F| 3.1106067183e-10, F_start 3.943e-06, 3222 steps, constraint 5.413e-04, Delta 1.0737644588 (macm3's k_c 79 source: |F| 3.0661e-10, 2925 steps, constraint 9.574e-04, Delta 1.0737660558; k_c 87's Delta is 1.597e-06 below). The prediction was about 3220 steps and 3200 to 3600 s: 3222 steps and 3293 s.
- **Acceptance:** `kc87_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3222 steps = the record's); `--mutate=F` exit 1 (the state's |F| is not within 1% of 1.5 times the record's), `--mutate=steps` exit 1 (`freeze_from` gives 3222, the record 3223); extra control: `kc79_syscheck_1025.py` on the k_c 87 result exit 1 ("the record is not k_c 79 at D 19.25 (kc 87, D 19.25)"). Verdict `regrid/VERDICT.txt`: ACCEPTED 23:21:27 UTC.
