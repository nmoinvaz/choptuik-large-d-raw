# I1025-dh610/d19_k95: dh170's k_c 87 D 19 state regridded to k_c 95 on Linux (for dh170's d19_lower, which scans it after its k_c 87 scan)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 18:30 UTC, before the regrid of this folder (the dry run of the lane, which checks the source, ran at 18:30 UTC). The k_c 95 state is not yet physical.

## Order (coordinator t5, hc), in part
"Added task for your gaps, now, 8 threads at nice 10 beside the leg lane: the k_c 95 regrid at D 19 for dh170's d19_lower (#1025, comment of 17:25), from dh170's accepted k_c 87 state (raw I1025-dh170/d19_lower: state 08e92aca, record b18197d4, tag l1kc87dh170d19; pin by blob): ell_refine.py l1kc87dh170d19 87 l1kc95dh610d19 95 1 19.0 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, accepted by your kc95_syscheck_1025.py (both controls exit 1, kc87 check refusing). Push the state and record to raw I1025-dh610/d19_k95/ (README first) and report; dh170 scans it after its k_c 87 scan."
dh170's task (#1025 comment of "17:25"): "k_c 87 from winb's accepted k_c 79 D 19 state, then k_c 95 from that k_c 87 state, the same way, and the same two windows; written before: from k_c 87 to 95 on this build the lower root moving less than 0.002 means it converges, more than 0.004 a discretization root." Memory alerts only (standing rule).

## Inputs (copies in `in/`; `in_blobs.txt`; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 87 D 19 state `sol_l1kc87dh170d19_D19.0000.npy` and record `l1kc87dh170d19.jsonl` (raw I1025-dh170/d19_lower/k87 at commit 599dff20, "k_c 87 regrid ACCEPTED on Linux (4578 s, |F| 2.8978e-10, 3276 steps, Delta 1.067769696966)") | 08e92aca, b18197d4 |
| `kc87_syscheck_1025.py`, `kc95_syscheck_1025.py` (the k_c 87 check with its k_c test changed to 95, its message and the selftest's planted record, nothing else: `kc95_syscheck_1025.diff`, rebuilt by the lane) | 6df5d960, d487e628 |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2). lambda_0(19.0) = 2.1156378446 (`ell_delta.lam0_at`, checked by the lane as a number). The lane is `../kc95_d1975/lane_kc95_regrid.sh` (the same step at D 19.75) with the tag, D, lambda_0, state names and blobs changed.

## Commands (`lane_d19_k95.sh` via `start_d19_k95.sh` = systemd user unit i1025ak under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails)
1. Pins; the selftests of the two checks (exit 0); the source: `kc87_syscheck_1025.py` accepts it (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc95_syscheck_1025.py` refuses it (exit 1). (The dry run of 18:30:28 UTC passed this: exits 0, 1, 1, 1.)
2. The regrid: the order's `ell_refine.py` command, 8 threads, nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free.
3. Acceptance: `kc95_syscheck_1025.py` on the result (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc87_syscheck_1025.py` refusing it (exit 1). On ACCEPTED the state `sol_l1kc95dh610d19_D19.0000.npy` and record `l1kc95dh610d19.jsonl` are copied to this folder's root with their blobs (`in_blobs_regrid.txt`), the files dh170 pins.
Threads: 8 beside the leg lane (8 threads while a point is scanned) and the #1076 recount (nominal 12, two processes in use); nominal 28, real about 18; all at nice 10.

## Acceptance (fixed before the run)
- Source accepted by the k_c 87 check (controls exit 1) and refused by the k_c 95 check; the regrid exits 0 and is accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check. A failing control stops the work and I report it; no bar is loosened.
- Reported: |F|, steps, the constraint, Delta beside dh170's k_c 87 record (Delta 1.06776969696562, |F| 2.897762648832e-10, 3276 steps, constraint 3.9188e-4) and winb's Windows k_c 95 at D 19 (raw I1025-dh170/d19_lower/k87/in/ref_winb_kc95_d19_regrid_summary.txt: |F| 2.930751034295e-10, 3575 steps, constraint 1.39786e-4, Delta 1.06776937015196, 10230 s), wall.

## Predictions, registered before the run (mine, information)
- Regrid exits 0 (93%) in 3000 to 4500 s (65%; k_c 95 at D 19.75 here took 3066 s, dh170's k_c 87 at D 19 4578 s on his machine); accepted by the k_c 95 check with both controls exit 1 (90%), the k_c 87 check refusing it (97%).
- Steps 3575 +- 40 (65%; winb's 3575; k_c 87 to 95 added 9.13% at winb's D 19 and 9.19% here at D 19.75, on 3276 that is 3575 to 3577). Delta(k_c 95) minus Delta(k_c 87) = -5.13e-07 +- 1.5e-07 (60%; winb's), that is Delta about 1.06776918; norm F 3e-10 to 5e-10 (80%); the constraint within 10% of winb's 1.398e-4 (60%).
- The lane ends 19:20 to 19:55 UTC (the leg lane's D 20.875 scan, due about 19:15 UTC, runs beside it for about 30 minutes).

## Status
- 2026-11-23 18:30 UTC: folder, inputs and lane written; dry run of the source check passed (18:30:28 UTC).
- 2026-11-23 18:31:01 UTC the regrid started (source check passed, unit i1025ak, 8 threads, nice 10); 20:05:29 UTC it exited 0; 20:05:35 UTC the k_c 95 check ACCEPTED it (both controls exit 1, the k_c 87 check refusing); the state and record are copied to this folder's root (`in_blobs_regrid.txt`).

## Result (`python3 -I summarize_d19k95.py > summary.txt` prints the tables and the scorecard from the files; `--mutate` plants a Delta shift of 1e-6 and a norm F scale of 1.4 and exits 1 when the scorecard's verdicts change, which they do)
Acceptance is by `kc95_syscheck_1025.py` (record at its own k_c, |F| at most 1e-9, state |F| within 1% of the record's, freeze_from steps equal), `--mutate=F` and `--mutate=steps` exit 1, and `kc87_syscheck_1025.py` refuses the result: `regrid/syscheck*.txt`, `regrid/steps.txt`, `regrid/VERDICT.txt`.

regrid 2026-11-23 18:31:01 to 2026-11-23 20:05:29 UTC, exit 0, wall 5668 s (the record's seconds 5667); kc95 check exit 0, controls --mutate=F 1, --mutate=steps 1, kc87 check on the result 1; peak RSS (60 s samples) 2.55 GiB

| record | norm F | F_start | steps | constraint | Delta | seconds |
|---|---|---|---|---|---|---|
| dh170 k_c 87 (the source) | 2.897762648832e-10 | 2.992207e-06 | 3276 | 3.918806e-04 | 1.06776969696562 | 4576 |
| this regrid, k_c 95 | 2.932640526780e-10 | 1.185238e-06 | 3575 | 1.397558e-04 | 1.0677690868324767 | 5667 |
| winb k_c 87 (Windows) | 2.900647440612e-10 | 2.992207e-06 | 3276 | 3.919128e-04 | 1.0677698834525378 | 7965 |
| winb k_c 95 (Windows) | 2.930751034295e-10 | 1.183945e-06 | 3575 | 1.397862e-04 | 1.0677693701519553 | 10230 |

Delta(k_c 95) - Delta(k_c 87): here -6.1013e-07 (dh170's k_c 87 source), winb -5.1330e-07; Delta(k_c 95) here minus winb's k_c 95 -2.8332e-07
steps ratio k_c 95 / k_c 87: here +9.1270%, winb +9.1270%; constraint here / winb's k_c 95: -0.0218%; F_start here / winb's +0.1092%

| prediction | result | verdict |
|---|---|---|
| regrid exit 0 (93%) | exit 0 | right |
| wall 3000 to 4500 s (65%) | 5668 s | WRONG |
| kc95 check accepts, controls 1 1 (90%) | exits 0 1 1 | right |
| kc87 check refuses the result (97%) | exit 1 | right |
| steps 3575 +- 40 (65%) | 3575 | right |
| Delta(95) - Delta(87) = -5.13e-7 +- 1.5e-7 (60%) | -6.1013e-07 | right |
| norm F 3e-10 to 5e-10 (80%) | 2.9326e-10 | WRONG |
| constraint within 10% of winb's 1.39786e-4 (60%) | 1.39756e-04 (-0.022%) | right |
| lane ends 19:20 to 19:55 UTC | 2026-11-23 20:05:29 | WRONG |

The new files, for dh170 to pin by blob (`in_blobs_regrid.txt`; copies equal the solver's `data/` files, `cmp`):
```
545406e41043cedb1ea43f4c47e7331ec111eada sol_l1kc95dh610d19_D19.0000.npy
6cfed1aad1633dc961d92c3e8a2bc219d3aa9dc5 l1kc95dh610d19.jsonl
```
Winb's reference summaries (copied from `I1025-dh170/d19_lower/k87/in/`, blobs in `in_blobs_ref.txt`):
```
725b42096fec80ce44bdc64a2afcce780940f72e ref_winb_kc95_d19_regrid_summary.txt  (I1025-dh170/d19_lower/k87/in/ at origin/main 982cc1789ba442b678fb6ff25e29ca4260c01152)
514342325f5bf02b9d2e0e9301fb9fa45ba88b88 ref_winb_kc87_d19_regrid_summary.txt  (I1025-dh170/d19_lower/k87/in/ at origin/main 982cc1789ba442b678fb6ff25e29ca4260c01152)
```

- **Same step count as winb's Windows regrid** (3575, +9.127% over the k_c 87 record's 3276 on both) and the constraint within 0.022% of winb's. |F| is 2.9326e-10, below my registered floor 3e-10 by 2.2%, so that line of the scorecard is WRONG; it is the record class's value (winb's 2.9308e-10, dh170's k_c 87 2.8978e-10).
- **Delta(k_c 95) - Delta(k_c 87) is -6.10e-7 on dh170's k_c 87 state and -5.13e-7 on winb's own pair.** Delta(k_c 95) is 2.83e-7 below winb's. The two k_c 87 sources differ in Delta (dh170's 1.06776969697, winb's 1.06776988345); I did not test why the shifts differ by 0.97e-7. The registered +-1.5e-7 around winb's -5.13e-7 held.
- **The wall was 5668 s**, longer than my 3000 to 4500 s: this regrid ran beside the #1076 recount (2 processes) and, from 19:17 to 19:58 UTC, the D 20.875 leg scan (8 processes); for comparison, dh170's k_c 87 regrid at this D (3276 steps) took 4576 s on his machine, and this machine's k_c 95 regrid at D 19.75 (3411 steps, `../kc95_d1975/l1kc95dh610d1975.jsonl`) took 3064 s. Load as the cause of the longer wall is not tested. Peak RSS (60 s samples) 2.55 GiB.

### Predictions scorecard (written before the run; the table above is from `summarize_d19k95.py`)
Right: exit 0, the k_c 95 check accepting with controls 1 1, the k_c 87 check refusing, steps 3575 +- 40, the Delta difference, the constraint. WRONG: the wall (3000 to 4500 s), norm F (3e-10 to 5e-10: 2.9326e-10), the lane's end time (19:20 to 19:55 UTC: 20:05).

