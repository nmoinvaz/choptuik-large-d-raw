# I1025-dh610/kc79_d205_fine: dh170's k_c 79 D 20.5 state on this build, scanned at lambda 1.060 to 1.090 by 0.005 (the fine grid), against this machine's k_c 87 root 1.077872 and dh170's coarse 1.087574

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 16:17 UTC, before any run of this folder. The k_c 79 and k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after `../kc87_d205`, raw 2514221e), in part
"D 20.5 k_c 87 accepted as read (raw 2514221e): 1.077872, and your post-hoc reading is right: the 0.0097 compares a 0.03 grid with a 0.005 one. Go on your proposal: dh170's k_c 79 D 20.5 state (30a92b78, record 5406e21c) on your build, kc79 check first (controls exit 1), d18_hybsign at 1.060-1.090 by 0.005 (7 evals, 5 procs; 1.060 and 1.090 again too, as repeats of dh170's on another build), read_lower. Written before (README): the k_c 79 root on the fine grid lies within 0.002 of 1.077872 (k_c 87), and the coarse two-point estimate is 0.010 high for this state, as you found. Raw I1025-dh610/kc79_d205_fine/."
Memory alerts only (standing rule). "7 evals" is read as the seven grid values 1.060, 1.065, ..., 1.090; 1.060 and 1.090 are the two lambdas dh170 evaluated on this state (`in/ref_dh170_k79_scan_D20.5.jsonl`: both noise-robust, signs - and +, ln|det| -2388.144894 and -2390.575506), so they are the repeats of his rows on this build. If t5 meant seven more evaluations beside those two, say so and I add them.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 79 D 20.5 state `sol_l1kc79dh170d205_D20.5000.npy` and record `l1kc79dh170d205.jsonl` (`I1025-dh170/kc79_d205`, raw 9535a78a; the same files as `../kc87_d205/in`) | 30a92b78, 5406e21c |
| `kc79_syscheck_1025.py` | 29dce7ea |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| dh170's final k_c 79 reading and rows (`dh170_k79_read_lower.txt`, `ref_dh170_k79_scan_D20.5.jsonl`, raw 249571b8) | 317b8f61, b68c0f6d |
| this machine's k_c 87 reading and rows of `../kc87_d205` (raw 2514221e) | 493c7401, c96a65da |
| `rows_check.py` (mine: this machine's rows at 1.060 and 1.090 against dh170's, sign equal and ln|det| within 1e-9 relative, the bar of `../kc79_d195/in/control_check.py`; selftest exit 0, `--mutate` exit 1; run on the k_c 87 rows against dh170's k_c 79 rows it fails, as it must) | b26817b5 |
| `fine_read.py` (mine: the scan's change beside the k_c 87 root 1.077872 by position, bar 0.002, and beside dh170's 1.087574; selftest exit 0, `--mutate` exit 1) | 4fd1fd24 |
Code: `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; the k_c 79 check reads the worktree `~/Source/choptuik-large-d-1025g` at 48c36355; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2).

## Commands (`lane_kc79_d205_fine.sh` via `start_kc79_d205_fine.sh` = systemd user unit i1025ai under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails; `notify_kc79_fine.sh` sends the coordinator an hc line at the source check and the end)
1. Pins and the tools' controls: selftests of `kc79_syscheck_1025.py` (exit 0), `read_lower.py` and its two mutations (0 1 1), `fine_read.py` (0, `--mutate` 1), `rows_check.py` (0, `--mutate` 1).
2. The source: `kc79_syscheck_1025.py` on dh170's record and state at D 20.5 accepts it (exit 0; `--mutate=F` and `--mutate=steps` exit 1). It already did so on 23 Nov at 13:39 UTC (`../kc87_d205/regrid/source_kc79_syscheck*.txt`); this folder runs it again as ordered.
3. The scan: `d18_hybsign.py` at 1.060 to 1.090 by 0.005 (7 evaluations), 5 processes of 1 thread, nice 10: p0 1.060, 1.085; p1 1.090, 1.065; p2 1.070; p3 1.075; p4 1.080 (1.060 and 1.090 in round 1). Each process prints the record system first (exit 3 if not). Refuses to start with less than 5 x 2.5 GB + 4 GB free.
4. The reading: `read_lower.py scan 1.060 1.090`, `fine_read.py`, and `rows_check.py` (1.060 and 1.090 against dh170's rows).
Threads: 5 beside the #1076 recount's up to 12 (`../../I1021-dh610/fu022mp_m3mp`), 17 at most, all at nice 10.

## Acceptance (fixed before the run)
- The k_c 79 check accepts the state with both controls exit 1; every scan process prints the record system; `rows_check.py` passes at 1.060 and 1.090 (a failing control stops the work and I report it; no bar is loosened).
- Reported: every robust change by position with bracket, orientation as printed, det-linear and range, beside this machine's k_c 87 root (1.077872) and dh170's 1.087574; the edge signs; ln|det| minima without a sign change; the rows at 1.060 and 1.090 beside dh170's (bit-identical or not); the coarse two-point estimate from this build's rows at 1.060 and 1.090.
- The coordinator's reading: the k_c 79 root on the fine grid lies within 0.002 of 1.077872 (k_c 87), and the coarse two-point estimate is 0.010 high for this state.

## Predictions, registered before the run (mine, information)
- The k_c 79 check accepts the state with both controls exit 1 (97%); all five processes exit 0 with the record system (92%).
- The rows at 1.060 and 1.090 have the same sign as dh170's (98%) and ln|det| within 1e-9 relative (90%), bit-identical (85%); the coarse two-point estimate from them is 1.087574 to 1e-6 (88%).
- Exactly one robust change in 1.060 to 1.090 (92%; the edge signs - and + differ); it lies within 0.002 of 1.077872 (55%, the coordinator's reading), within 0.001 (35%), within 0.005 (80%). The k_c 79 root minus the k_c 87 one is between -0.002 and +0.003 (60%). The coarse estimate minus the fine k_c 79 root is 0.010 +- 0.002 (55%).
- Each scan point takes 800 to 1700 s (65%; k_c 79 at D 20.25 took 699 to 1800 s); the lane ends 17:10 to 17:50 UTC (two rounds on p0 and p1).

## Status
- 2026-11-23 16:17 UTC: folder, inputs, lane and the reading prepared before any run; dry run of the lane passed (16:16:41 UTC; pins, selftests 0 0 1 1 0 1 0 1).
