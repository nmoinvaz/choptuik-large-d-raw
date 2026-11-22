# I1025-dh370/kc79_d195: win2's k_c 71 D 19.5 state regridded to k_c 79, then a hybrid sign scan (lambda 1.30 to 1.50)

Written before the run (the regrid started 2026-11-22 18:37:34 UTC by the clock). Machine `dh370-fedora` (Fedora, i7-8700, 12 threads, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator t5 (hc, 2026-11-22, received before 18:36 UTC).

## Order

The k_c 79 line of lambda_1, after `../kc79_d19125/` (raw c58e5052: one root in 1.44 to 1.58, lambda_1 1.505784).

1. Regrid win2's k_c 71 D 19.5 state (leg 2 of the k_c 71 leap, tag `l1kc71Lw1025b`) to k_c 79 exactly as at D 19.125: win2's `kc71_syscheck.py` on the source first, `ell_refine.py`, accepted only by `kc79_syscheck_1025.py` and its two controls. 6 threads, nice 10, a systemd unit (`i1025k795`).
2. Scan the accepted state with `d18_hybsign.py` (e089207a, unmodified), on 4 processes of 1 thread (the D 19.125 scan measured 3813 to 3897 s per point with 6 processes and 2021 to 2081 s with 4: six are memory-bound here), read with dh170's `read_lower.py`. **Split (t5's change, after the regrid was accepted and pushed):** this folder scans lambda 1.30 to 1.40 at 0.01 (11 values) plus a repeat of 1.35; dh610 scans 1.41 to 1.50 plus a repeat of 1.45 on the same state (after a Linux-to-Linux control on the D 19.125 k_c 79 point). I read my half with `read_lower.py`; t5 reads the joined window 1.30 to 1.50. A change between 1.40 and 1.41 straddles the halves: I report the edge sign at 1.40 and the reading of my half only. (The first launch, on the full window 1.30 to 1.50, was stopped 1 min after its start with no point done; `scan_attempt1_full_window_stopped/`, `steps.txt`.)
3. Report every robust change with its det-linear estimate and range, the edge signs, any ln|det| minimum without a change; they are k_c 79 roots. Stop and report on a refusal, a failed control or a regrid that does not converge. Report each step's verdict with the raw commit; post on #1025.

Estimate (t5): regrid about 45 min, scan 6 rounds of about 35 min for the full window; 3 rounds (4, 4, 4 evaluations) for this half.

## Prediction (information, not a pass rule)

lambda_1's straight line through k_c 79's D 19 value 1.539658 (winb, `I1025-win/kc79_d19/read_kc79_D19.log`: the change in (1.53, 1.54), + to - in that state) and D 19.125 value 1.505784 (`../kc79_d19125/read_lower.txt`) has slope -0.2709 per unit D and reaches about 1.4041 at D 19.5 (t5: near 1.405), inside the window. win2's k_c 71 scan of D 19.5 (raw `I1025-win2/kc71_leap/scan_D19.5_P*.jsonl`) was still running at 18:36 UTC (6 of 21 points); I report beside it when its reading is posted. k_c 79 at D 19.125 has no lower root in 1.44 to 1.58 (dh170 scans 1.10 to 1.44 on that state, raw `I1025-dh170/kc79_d19125low`).

Update (t5's hc, about 20:00 UTC; information, not a pass rule): roots are identified by position, not by sign orientation, across D as well as across k_c, and posts call them "the root near lambda_1's line" and "the rising root". macm3's k_c 79 scan at D 19.25 (raw cc30e59c, `I1025-macm3/kc79_d1925/read_lower.txt`) has one robust change, det-linear 1.469975, the root near lambda_1's line there; the line through it and D 19.125's 1.505784 has slope -0.2865 per unit D and reaches about 1.3984 at D 19.5 (t5: about 1.398). t5 reads k_c 71's roots near k_c 79's lambda_1 as 1.5365, 1.5112, 1.4907, 1.4750 at D 19, 19.125, 19.1875, 19.25, and its rising root as 1.296, 1.488, about 1.58, 1.661, crossing lambda_1's line between D 19.125 and 19.1875. A rising root at D 19.5 lies well above 1.50, outside this folder's window 1.30 to 1.40 and dh610's 1.41 to 1.50.

## Inputs (raw origin/main, pinned by `git hash-object --no-filters`; `run_regrid.sh` refuses any other blob and copies them to `in/`)

| item | raw path | blob |
|---|---|---|
| k_c 71 D 19.5 state (win2's leg 2) | `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.500000.npy` (the `_D19.5000.npy` copy has the same blob) | 6b65c531 |
| its record (leg 2 points to D 19.5; the D 19.5 line is used) | `I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl` at raw b343a4da | 464fe2f2 |
| win2's source check | `I1025-win2/kc71_leap/kc71_syscheck.py` | 4cd86cd4 |
| winb's result check | `I1025-win/kc79_d19/kc79_syscheck_1025.py` | 29dce7ea |
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a |
| reader (dh170's) | `I1025-dh170/lower_root/read_lower.py` | 89309d3c |
| reader's change finder | `I1025-mac/d18/d185_scan_read.py` | 7c9d400f |

The current raw record file (blob c6dc4397, 4 lines) appends D 19.5625 to that one; its D 19.5 line is identical (checked), so the blob of b343a4da is used, as at D 19.125. The k_c 71 source record at D 19.5: |F| 3.5028e-10, 2587 steps, constraint 2.467e-3, Delta 1.0798467018887798 (the leap step's 2527 s; |F| is above the 2.8e-10 of D 19.125 and below the 1e-9 bar).
Code: worktree `~/Source/choptuik-large-d-1025` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` blob 631e5801), python `~/Source/choptuik-large-d-1058b/.venv` (3.14, multidouble 5.1.0, avx2): the same as `../kc79_d19125/`. The state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025b_D19.5000.npy`, the name `ell_refine.py` reads.

## Commands

Regrid (the D 19.125 command with D, source tag, output tag and lambda_0 changed; `--no-gamma` does not use the lambda_0 argument; lambda_0(19.5) = 2.1132623525 from `ell_delta.lam0_at(D, *ell_delta.lam0_table())`, error 6.2e-7):

    cd ~/Source/choptuik-large-d-1025/solver/matter && nice -n 10 timeout 21600 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 \
      ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py l1kc71Lw1025b 71 l1kc79dh370d195 79 1 19.5 2.1132623525 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

`run_regrid.sh` (unit `i1025k795`, under `systemd-inhibit`) is `../kc79_d19125/run_regrid.sh` with only D, the tags, the source pins and the record's origin changed (`diff_regrid_vs_d19125.txt`); it stops at the first failure (`VERDICT.txt`, `steps.txt`). `run_scan.sh` (unit `i1025s795`) is the D 19.125 scan driver with D, tag, the window (1.30 to 1.50 and the repeat of 1.40, the repeat on another process than the first 1.40) and 4 processes (`diff_scan_vs_d19125.txt`); it runs the reader's selftest and both mutations after the scan.

## Acceptance (fixed before the run, as at D 19.125)

1. **Source.** win2's `kc71_syscheck.py` accepts the k_c 71 D 19.5 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, |F| within 1%), both controls (`--mutate=F`, `--mutate=steps`) exit 1, and both selftests exit 0. Otherwise no regrid.
2. **Result.** `kc79_syscheck_1025.py` accepts the regridded record and state (k_c 79 at D 19.5, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), and both controls exit 1. A regrid that exits non-zero, or hits the 21600 s cap, is a stop.

The scan starts only after the verdict is ACCEPTED; each scan process first prints `the record system` (`d18_hybsign.py`'s check of the state against its record), and anything else is a stop.

## Cost, written before the run

The D 19.125 regrid: 2576 s on 6 threads, 2949 steps, peak RSS 1.47 GB. Expect the same, 45 min. The scan: 12 evaluations on 4 processes are 3 rounds (4, 4, 4); at about 2050 s per point that is about 1.8 h.

## Status

- 18:37:38 UTC source check accepted (|F| 3.5040e-10 against the record's 3.5028e-10, 2587 steps; both controls exit 1); regrid started.
- 19:16:51 to 20:58:04 UTC scan of lambda 1.30 to 1.40 (12 evaluations, 4 processes, all exit 0, each printed the record system; 1971 to 2068 s per point, mean 2016 s). Reader `read_lower.py` (89309d3c, unedited; `read_lower.txt`): selftest exit 0, mutations shift and round2 exit 1. **One robust change in (1.39, 1.40), + to - as printed, det-linear 1.397565, range [1.396781, 1.397565]: the root near lambda_1's line (k_c 79); edge signs + at 1.30, - at 1.40; no ln|det| minimum without a change.** The repeat of 1.35 is bit-identical (ln|det| -2499.0985930399347, signs and noise signs equal). Float64 sign -1 at 1.30 to 1.39 and +1 at 1.40: opposite to the hybrid everywhere, not used.
- Beside (information; by position, t5's rule): the line through macm3's D 19.25 (1.469975) and D 19.125 (1.505784) gives about 1.3984 (found: 1.397565, -0.0008). win2's k_c 71 scan of D 19.5 (raw f502bf52, `I1025-win2/kc71_leap/read_D19.5.txt`, lambda 1.20 to 1.60) has two robust changes: + to - at 1.371531 (range [1.370956, 1.371531]) and - to + at 1.449187 (range [1.449089, 1.449187]), none else. k_c 71's root nearest the line is 1.371531, 0.026 below k_c 79's 1.397565; its other root, 1.449187, is in dh610's half (1.41 to 1.50) for k_c 79.
- 19:14:58 UTC regrid exit 0 in 2240 s (peak RSS 1.20 GB); 19:15:02 `kc79_syscheck_1025.py` ACCEPTED (|F| 3.5123e-10, 2879 steps, constraint 1.273e-3, Delta 1.0798406632; k_c 71: 3.5028e-10, 2587, 2.467e-3, 1.0798467019), both controls exit 1. State and record pushed at raw f40a4556.
