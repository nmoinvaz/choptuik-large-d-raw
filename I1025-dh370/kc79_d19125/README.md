# I1025-dh370/kc79_d19125: win2's k_c 71 D 19.125 state regridded to k_c 79, then a hybrid sign scan (lambda 1.44 to 1.58)

Written before the run, 2026-11-22 about 15:03 UTC. Machine `dh370-fedora` (Fedora, i7-8700, 12 threads, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator t5 (hc, 2026-11-22 about 15:00 UTC).

## Order

Question: at D 19.125 k_c 63 shows no change in 1.505 to 1.545 (dh610, raw fedc68ff) while k_c 71 has two (dh610, raw ee09203f). Does the lower root's meeting with lambda_1 settle as k_c grows? A third k_c at D 19.125 measures it.

1. Regrid win2's k_c 71 D 19.125 state to k_c 79 with `ell_refine.py`, the way winb did at D 19 (raw `I1025-win/kc79_d19`, f712f94c). Adapt only paths, D and the source. Accept it only by winb's check (`kc79_syscheck_1025.py`, controls included). 6 threads, nice 10, a systemd unit, outside the terminal.
2. Scan the k_c 79 state at D 19.125 with `d18_hybsign.py` (e089207a, unmodified), lambda 1.44 to 1.58 at 0.01 (15 values) plus a repeat of 1.50, 6 processes of 1 thread, read with dh170's `read_lower.py`.
3. Stop and report on a refusal, a failed control or a regrid that does not converge. Report each step's verdict with the raw commit; post on #1025.

Estimate (t5): regrid 1 to 1.5 h, scan about 1 h. Information, not a pass rule: win2's k_c 71 leap at D 19.125 and dh610's k_c 71 scan of it (below).

## Inputs (raw origin/main, pinned by `git hash-object --no-filters`; `run_regrid.sh` refuses any other blob and copies them to `in/`)

| item | raw path | blob |
|---|---|---|
| k_c 71 D 19.125 state (win2's leap) | `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.125000.npy` | 42a4e4cc |
| its record (leap points to D 19.125; the D 19.125 line is used) | `I1025-win2/kc71_leap/states/l1kc71Lw1025.jsonl` at raw fedc68ff (dh610's pin) | 18542c4c |
| win2's source check | `I1025-win2/kc71_leap/kc71_syscheck.py` | 4cd86cd4 |
| winb's result check | `I1025-win/kc79_d19/kc79_syscheck_1025.py` | 29dce7ea |
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a |
| reader (dh170's) | `I1025-dh170/lower_root/read_lower.py` | 89309d3c |
| reader's change finder | `I1025-mac/d18/d185_scan_read.py` | 7c9d400f |

The current raw file (blob c5fc14a9, 12 lines) appends D 19.1875 and 19.25 to that one; its D 19.125 line is identical (checked), so the older pinned blob is used, as in dh610's scan. Attempt 1 of `run_regrid.sh` stopped at this pin (`steps.txt`, `VERDICT_attempt1_refused.txt`) before any computation.

The k_c 71 source record at D 19.125: |F| 2.8422e-10, 2651 steps, constraint 1.784e-3, Delta 1.0707594252027368 (the leap step's 3028 s).
Code: worktree `~/Source/choptuik-large-d-1025` at 48c36355; `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's (winb's pin), `ell_refine.py` blob 631e5801 and `ell_delta.py` are 48c36355's. Python `~/Source/choptuik-large-d-1058b/.venv` (3.14, multidouble 5.1.0, hpkernel avx2). The state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025_D19.1250.npy`, the name `ell_refine.py` reads (`D:.4f`), and checked by blob.

## Commands

Regrid (winb's D 19 command with D, tag and lambda_0 changed; `--no-gamma` does not use the lambda_0 argument; lambda_0(19.125) = 2.1150338480 from `ell_delta.lam0_at(D, *ell_delta.lam0_table())`, which here reproduces winb's 2.1181259879 at D 18.5 and 2.1156378446 at D 19):

    cd ~/Source/choptuik-large-d-1025/solver/matter && nice -n 10 timeout 21600 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 \
      ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py l1kc71Lw1025 71 l1kc79dh370 79 1 19.125 2.1150338480 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

`run_regrid.sh` (unit `i1025k79`, under `systemd-inhibit`) runs, in this order, stopping at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the two selftests, the source check, the regrid, the result check.

## Acceptance (fixed before the run; winb's two steps)

1. **Source.** win2's `kc71_syscheck.py` accepts the k_c 71 D 19.125 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, |F| within 1%) and both controls (`--mutate=F`, `--mutate=steps`) exit 1. Otherwise no regrid.
2. **Result.** `kc79_syscheck_1025.py` accepts the regridded record and state (k_c 79 at D 19.125, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, and both controls exit 1. A regrid that exits non-zero, or hits the 21600 s cap, is a stop.

The scan (step 2 of the order) starts only after the verdict is ACCEPTED. Each scan process first checks the state against its record (`d18_hybsign.py` prints `the record system`); a process that prints anything else is a stop.

## k_c 71 changes beside which I report (information, not a pass rule)

dh610's k_c 71 scan of D 19.125 (raw ee09203f, `I1025-dh610/kc71_d19125/read_lower.txt`): hybrid signs + at 1.44 to 1.48, - at 1.49 to 1.51, + at 1.52 to 1.58; robust changes + to - at 1.488137 (range [1.486996, 1.488137]) and - to + at 1.511209 (range [1.511209, 1.511571]); no ln|det| minimum without a change; the repeat of 1.50 agrees. k_c 63 at D 19.125 (dh610, raw fedc68ff): no change in 1.505 to 1.545.

## Cost, written before the run

winb's regrid at D 19: 5595 s on 4 threads (cpu about 1.8 cores), 2976 steps, peak private 2.5 to 3 GB. Here 6 threads, alone on the machine after the k_c 63 leap ends at 15:06 UTC: expect 1 to 1.5 h. The scan's points take about 1900 s each at k_c 63 on 1 thread (and 1650 s with 5 processes); k_c 79 is larger, so expect longer; the first point's time is reported.

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check (win2's `kc71_syscheck.py`) | accepted, both controls exit 1, selftests 0 | state |F| 2.8443e-10, 2651 steps = record's | 15:08 |
| regrid (`ell_refine.py`, exit 0) | accepted by `kc79_syscheck_1025.py`, both controls exit 1 | |F| 2.9245e-10, 2949 steps, constraint 8.306e-4, Delta 1.0707569213 (k_c 71: 2.8422e-10, 2651, 1.784e-3, 1.0707594252) | 15:08 to 15:51 (2576 s, peak RSS 1.47 GB) |
| scan (`run_scan.sh`, unit i1025s79) | done, 16 evaluations, all six processes exit 0 and printed the record system | one robust change, - to + in (1.50, 1.51), det-linear 1.505784, range [1.505586, 1.505784]; none elsewhere in 1.44 to 1.58; repeat of 1.50 bit-identical | 15:52 to 18:34 (3813 to 3897 s per point with 6 processes, 2021 to 2081 s with 4) |
| reader (`read_lower.py` 89309d3c) | selftest exit 0, mutations shift and round2 exit 1 | `read_lower.txt` | 18:34 |

Beside (information): k_c 71 at D 19.125 has + to - at 1.488137 and - to + at 1.511209 (dh610, raw ee09203f); k_c 63 has none in 1.505 to 1.545 (dh610, raw fedc68ff). The lower root has no counterpart at k_c 79 in 1.44 to 1.58.
Float64 sign: - at all points, differs from the hybrid at 1.51 to 1.58; not used.
