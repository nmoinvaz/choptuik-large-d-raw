# I1025-win2/kc87_d20: win2's k_c 79 D 20 state regridded to k_c 87 and scanned at lambda 1.20 to 1.33

Written before the run, 2026-11-23 02:58 UTC (`date -u`). Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator: t5.

## Order (the coordinator's task, #1025 comment 7090320838, "win2: k_c 87 at D 20, from win2's own k_c 79 D 20 state", 2026-11-23 03:05 UTC; hc of about 03:10 UTC)

**Why.** The same-build k_c 79 to 87 change at D 20, as dh170 does at D 19.75. The scan also tests the ln|det| minimum without a sign change at 1.31 (k_c 79, D 20, `../kc79_d20/`) for a close pair.

- **Step 1, regrid:** pin win2's accepted k_c 79 D 20 state and record (raw c9d6762c) and dh610's `kc87_syscheck_1025.py` (blob 6df5d960, raw ec9fb489:I1025-dh610/kc87_d195/in/). `kc79_syscheck_1025.py` accepts the source (controls exit 1) and the k_c 87 check refuses it. Then `ell_refine.py <k_c 79 D 20 tag> 79 l1kc87win2d20 87 1 20.0 <the lambda_0 of the k_c 79 D 20 regrid> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, started through WMI with the headless conhost. Accept only by `kc87_syscheck_1025.py` (selftest 0, `--mutate=F` and `--mutate=steps` exit 1) with `kc79_syscheck_1025.py` refusing the result.
- **Step 2, after ACCEPTED:** `d18_hybsign.py` at 1.20 to 1.28 by 0.01 (9 values), 1.29 to 1.33 by 0.005 (9 values) and a repeat of 1.25: 19 evaluations on 7 processes of 1 thread, beside leg 3 of the leap. Then `read_lower.py` selftest, `shift`, `round2` and the reader.
- **Report:** Delta beside k_c 79's 1.092257255093; every robust change by position, lambda_1 beside 1.248340; what the 0.005 grid shows at 1.31. Leg 3 of the leap runs on untouched (`../kc71_leap/`). Memory: alerts only.
- **Estimate:** regrid about 2 h (5281 s at k_c 79); scan 3 rounds of about 25 min each.

## Inputs (pinned in `inputs/`, checked with `git hash-object --no-filters`)

| file | origin | blob |
|---|---|---|
| `sol_l1kc79W20m1025_D20.0000.npy` (the k_c 79 D 20 state) | raw c9d6762c, `I1025-win2/kc79_d20/` | 7e288cc8 |
| `l1kc79W20m1025.jsonl` (its record, one line, equal to `rec_k79_D20.0000.jsonl`) | raw c9d6762c | d659667f |
| `kc79_syscheck_1025.py` | `I1025-win/kc79_d19/` | 29dce7ea |
| `kc87_syscheck_1025.py` | raw ec9fb489, `I1025-dh610/kc87_d195/in/` | 6df5d960 |
| `read_lower.py`, `d185_scan_read.py` | `I1025-dh170/lower_root/` | 89309d3c, 7c9d400f |
| `d18_hybsign.py` (xfkappa's scanner) | `I1025-mac/d18/` | e089207a |

The worktree's copy of the state (`D:/choptuik-i1025k79/solver/matter/data/sol_l1kc79W20m1025_D20.0000.npy`, where the k_c 79 regrid wrote it) has the same blob 7e288cc8. Code: worktree `D:/choptuik-i1025k79` at 48c36355 (solver code = 505d8399, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), venv-md510 (multidouble 5.1.0). Leg 3 runs in `D:/choptuik-i1025k71`.

## Step 1: the regrid (`regrid87_d20.sh`)

```
ell_refine.py l1kc79W20m1025 79 l1kc87win2d20 87 1 20.0 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

lambda_0 = 2.1110019498 is the k_c 79 D 20 regrid's (`ell_delta.lam0_at(20)`, error 3.8e-7; unused with `--no-gamma`). 8 BLAS threads, BelowNormal, cap 21600 s by the exact root pid with the `ell_refine.py` command-line check (`crun` of `../kc71_leap/lib_kcl.sh`; its planted test is in `../kc71_leap/`), started outside the terminal through `../kc71_leap/cim_start.ps1` (the headless form, `conhost.exe --headless cmd.exe /c`). Before it: both `--selftest` runs exit 0; `kc79_syscheck_1025.py` accepts the source, its `--mutate=F` and `--mutate=steps` exit 1; `kc87_syscheck_1025.py` refuses the source (it is k_c 79, not 87). **Acceptance (fixed now):** `kc87_syscheck_1025.py REC STATE 20 WTM` exits 0 (the record's |F| at most 1e-9, the record is k_c 87 at D 20, the state reproduces its record: `freeze_from` gives the record's steps and |F| within 1%), its controls on the same numbers are refused, `--mutate=F` and `--mutate=steps` exit 1, and `kc79_syscheck_1025.py` exits 1 on the result. A refusal, a failed control or a regrid that does not converge stops with a report; no retry. The accepted record goes into `regrid_accepted.txt` beside the k_c 79 source's numbers.

**Rehearsal of the source checks (`rehearsal/`, no regrid):** the k_c 79 check accepts the source (record |F| 4.4105e-10, 2800 steps, controls refused), both mutations exit 1, the k_c 87 check refuses it ("the record is not k_c 87 at D 20 (kc 79, D 20.0)"), both selftests pass.

## Step 2: the scan (`scan87_d20.sh`, starts itself when `regrid_accepted.txt` exists)

xfkappa's `d18_hybsign.py` (e089207a, unchanged) on the accepted k_c 87 state and its record line, the 1e-15 noise test (2 seeds) and the float64 sign; first line of each process: the record-system check (exit 3 if not). **Lambda 1.20 to 1.28 by 0.01 (9 values), 1.290 to 1.330 by 0.005 (9 values), and a repeat of 1.25: 19 evaluations in seven processes of one thread:**

| process | lambda, in this order |
|---|---|
| P1 | 1.25, 1.20, 1.21 |
| P2 | 1.25, 1.22, 1.23 |
| P3 | 1.24, 1.26, 1.27 |
| P4 | 1.28, 1.290, 1.295 |
| P5 | 1.300, 1.305, 1.310 |
| P6 | 1.315, 1.320 |
| P7 | 1.325, 1.330 |

BelowNormal, caps 28800 s by the exact root pids, `P4_WT_MATTER` the k_c 79 worktree. **The repeat gate** (`pair87.py`, a copy of `../kc79_d20/pair79.py`): the first records of P1 and P2 (both 1.25) must agree in hybrid sign, noise signs, float64 sign and ln|det| within 1e-6, else the seven scans are killed by exact pid (planted cases and `--break` in `selftest_pair87.txt`). **Reading:** `read_lower.py SCAN_DIR 1.20 1.33` as it prints (its selftest and `--mutate=shift` and `--mutate=round2`, both exiting 1, run first); roots by position. Threads: the regrid 8 + leg 3 of the leap 4 = 12 of 20; the scan 7 + 4 = 11.

## Run

Both drivers start outside the terminal through `../kc71_leap/cim_start.ps1`, BelowNormal, as soon as this README is pushed and the plan is posted on #1025: the regrid driver at once, the scan driver waits for `regrid_accepted.txt`. No script sends hc; verdicts are read from `summary_kc87.txt` and `exits_kc87.txt` and reported by hand.

## Result (so far)

**Source (02:59 UTC 23 Nov): accepted by the k_c 79 check, refused by the k_c 87 check** (`source_kc79_syscheck*.txt`, `source_kc87_syscheck.txt`; rehearsal in `rehearsal/`).

**Step 1, the regrid: ACCEPTED** (started 02:59:20 UTC, exit 0 at 04:55:32 UTC, 6972 s, uncapped, 8 threads, BelowNormal, root pid 35008, beside leg 3 of the leap; `regrid.log`): `kc87_syscheck_1025.py` exit 0, its selftest exit 0, controls on the same numbers refused, `--mutate=F` and `--mutate=steps` each exit 1, and `kc79_syscheck_1025.py` refuses the result ("the record is not k_c 79 at D 20 (kc 87, D 20.0)") (`syscheck*.txt`).

| | k_c 79 source (win2, D 20) | k_c 87 (this regrid) |
|---|---|---|
| \|F\| | 4.4105e-10 | 4.3393e-10 |
| steps | 2800 | 3082 |
| constraint | 2.102e-3 | 1.265e-3 |
| Delta | 1.092257255093 | 1.092254283228 |
| F_start | 2.819e-05 | 8.339e-06 |
| seconds | 5273 | 6960 |

Delta(k_c 87) minus Delta(k_c 79) = -2.9719e-6 (k_c 79 minus k_c 71 at D 20: -1.1878e-5). Files: `sol_l1kc87win2d20_D20.0000.npy`, `l1kc87win2d20.jsonl`, `rec_k87_D20.0000.jsonl`, `regrid_accepted.txt`. **A flaw of mine, found at the end of the regrid:** the driver's last step, the one-line python that writes `regrid_accepted.txt`, got MSYS paths and wrote an empty file (its output was lost; the scan driver, which only waits for the file to exist, started on it, after the record and the state existed and the checks above had passed). The line was written again from the two records at 04:57 UTC and appended to `summary_kc87.txt`.

**Step 2, the scan** started 04:56:10 UTC (seven processes of one thread, roots 34832, 17036, 19024, 34052, 18224, 22888, 35108); the system check of every process passed (|F| 4.3349897102e-10 against the record's 4.3393255460e-10, 3082 steps = the record's). Result below when it ends.

**Step 2, the scan: done** (started 04:56:10 UTC, seven processes of one thread, BelowNormal; ended 06:38:21 UTC; `scan_k87d20_p1..p7.jsonl`; exit 0 for all seven: P1 6112 s, P2 6109 s, P3 6061 s, P4 6129 s, P5 6094 s with 3 evaluations each, P6 4329 s, P7 4283 s with 2; 1786 to 2195 s a point, mean 2052 s; no cap). The system check of every process passed (|F| 4.3349897102e-10 against the record's 4.3393255460e-10, 3082 steps = the record's). **The repeat of 1.25 (P1, P2) agrees: sign +1 and ln|det| -2770.5614321890 in both, difference 0.0 (bar 1e-6); the gate passed after 2215 s.**

`read_lower.py 1.20 1.33` as it prints (`read_lower_k87_D20.txt`): 18 distinct points in 1.200 to 1.330 (19 evaluations), none not noise robust; hybrid signs minus at 1.20 to 1.24 and plus at 1.25 to 1.33; the float64 sign differs from the hybrid at 1.25 and 1.26 (it reads minus there; the hybrid, the sign the reading uses, plus); repeated points 1.25 agree; **one robust change in (1.240, 1.250), minus to plus (as printed), det-linear estimate 1.247484, estimator range [1.246861, 1.247484]** (a spread over estimator choices, not an enclosure); changes touching a non-robust point: none; ln|det| local minima without a sign change: none; endpoint signs minus at 1.200, plus at 1.330.

**Against k_c 79 (`../kc79_d20/`, the same D 20):** Delta 1.092254283228 against 1.092257255093 (difference -2.9719e-6); the one root, 1.247484 against 1.248340 in the same bracket (1.24, 1.25): k_c 87 minus k_c 79 = -0.000856 (the estimator ranges overlap: [1.246861, 1.247484] and [1.244440, 1.248340]). **At 1.31:** the k_c 79 scan (step 0.01) had an ln|det| minimum without a sign change at 1.31 (-2455.0577 against -2454.8054 at 1.30 and -2455.0222 at 1.32). The k_c 87 scan on the 0.005 grid 1.290 to 1.330 shows none: ln|det| falls at every step (-2769.4628, -2769.5706, -2769.6933, -2769.8284, -2769.9742, -2770.1292, -2770.2923, -2770.4625, -2770.6390 at 1.290, 1.295, ..., 1.330) with the step growing from -0.1079 to -0.1765 per 0.005, so no flattening and no turn at 1.31 (the only interior ln|det| minimum of the scan is at 1.25, beside the sign change). The absolute ln|det| differs between k_c (a different discretization), so only the shape is compared.

<details><summary>All 19 evaluations (hybrid sign, ln abs det, noise test, float64 sign, seconds)</summary>

| lambda | process | hybrid sign | ln abs det | noise (2 seeds) | float64 sign | s |
|---|---|---|---|---|---|---|
| 1.200 | P1 | - | -2766.7264 | -,- | - | 2108 |
| 1.210 | P1 | - | -2767.2360 | -,- | - | 1793 |
| 1.220 | P2 | - | -2767.6957 | -,- | - | 2120 |
| 1.230 | P2 | - | -2768.3370 | -,- | - | 1798 |
| 1.240 | P3 | - | -2769.4713 | -,- | - | 2145 |
| 1.250 | P1 | + | -2770.5614 | +,+ | - | 2195 |
| 1.250 | P2 | + | -2770.5614 | +,+ | - | 2164 |
| 1.260 | P3 | + | -2769.4596 | +,+ | - | 2116 |
| 1.270 | P3 | + | -2769.2650 | +,+ | + | 1792 |
| 1.280 | P4 | + | -2769.3051 | +,+ | + | 2158 |
| 1.290 | P4 | + | -2769.4628 | +,+ | + | 2162 |
| 1.295 | P4 | + | -2769.5706 | +,+ | + | 1786 |
| 1.300 | P5 | + | -2769.6933 | +,+ | + | 2158 |
| 1.305 | P5 | + | -2769.8284 | +,+ | + | 2123 |
| 1.310 | P5 | + | -2769.9742 | +,+ | + | 1790 |
| 1.315 | P6 | + | -2770.1292 | +,+ | + | 2191 |
| 1.320 | P6 | + | -2770.2923 | +,+ | + | 2112 |
| 1.325 | P7 | + | -2770.4625 | +,+ | + | 2156 |
| 1.330 | P7 | + | -2770.6390 | +,+ | + | 2118 |

</details>
