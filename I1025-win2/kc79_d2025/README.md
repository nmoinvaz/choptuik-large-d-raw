# I1025-win2/kc79_d2025: lambda_1 past D 20 on win2's build: leg 3's k_c 71 D 20.25 state regridded to k_c 79 and scanned at lambda 1.12 to 1.24, then k_c 87

Written before the run, 2026-11-23 06:43 UTC (`date -u`). Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator: t5.

## Order (the coordinator's task, #1025 comment 7093559078, "λ₁ past D 20 on one build, k_c 79 then 87 at D 20.25", 2026-11-23 07:45 UTC; hc of about 07:50 UTC)

D 20 is converged in k_c on Windows: 1.248340 (k_c 79) and 1.247484 (k_c 87), raw 9e520757. Since the build moves lambda_1 by up to 0.014 past D 19.5, the march past D 20 stays on win2's build.

- **Step 1:** pin leg 3's accepted k_c 71 D 20.25 state and record (raw `I1025-win2/kc71_leap/states/`, 589d5f2a: `sol_l1kc71Lw1025c_D20.250000.npy` blob 8e137d6b, `l1kc71Lw1025c.jsonl`). Then regrid to k_c 79 with `ell_refine.py l1kc71Lw1025c 71 l1kc79win2d2025 79 1 20.25 <lam0_at(20.25)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, as at D 20. Accept by `kc79_syscheck_1025.py` (selftest 0, both controls exit 1).
- **Step 2:** `d18_hybsign.py` at 1.12 to 1.24 by 0.01 and a repeat of 1.18 (14 evaluations, 7 processes of 1 thread), then `read_lower.py` with its selftest and both mutations.
- **Step 3:** k_c 87 from the accepted k_c 79 state, as at D 20, then a scan over the k_c 79 root's bracket +-0.03 by 0.005.
- **Written before the run (the coordinator's):** lambda_1(20.25) lies near 1.17 (the line's -0.31 per unit D from D 20), with one robust change in the window, and k_c 87 within 0.002 of k_c 79.
- Headless conhost launches, **Normal priority** beside leg 3 (`../kc71_leap/`, untouched), memory: alerts only. A verdict is sent to the coordinator at each step. Estimate: regrid about 1.5 h, scan about 1 h, k_c 87 about 3 h. Follow-on: D 20.5 the same way, from leg 3's state.

## Inputs (pinned in `inputs/`, checked with `git hash-object --no-filters`)

| file | origin | blob |
|---|---|---|
| `sol_l1kc71Lw1025c_D20.250000.npy` (leg 3's D 20.25 state) | raw 589d5f2a, `I1025-win2/kc71_leap/states/` | 8e137d6b |
| `l1kc71Lw1025c.jsonl` (leg 3's records through D 20.25, 4 lines; the D 20.25 line is the same in the later file) | raw 589d5f2a | cc1e872c |
| `kc71_syscheck.py` (the source acceptance) | `I1025-win2/kc71_leap/` | 4cd86cd4 |
| `kc79_syscheck_1025.py` | `I1025-win/kc79_d19/` | 29dce7ea |
| `kc87_syscheck_1025.py` (step 3) | raw ec9fb489, `I1025-dh610/kc87_d195/in/` | 6df5d960 |
| `read_lower.py`, `d185_scan_read.py` | `I1025-dh170/lower_root/` | 89309d3c, 7c9d400f |
| `d18_hybsign.py` (xfkappa's scanner) | `I1025-mac/d18/` | e089207a |

The state equals the leap worktree's and the live `states/` copies byte for byte. Code: worktree `D:/choptuik-i1025k79` at 48c36355 (solver code = 505d8399, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), venv-md510 (multidouble 5.1.0). Leg 3 runs in `D:/choptuik-i1025k71`.

## Step 1: the regrid (`regrid79_d2025.sh`)

```
ell_refine.py l1kc71Lw1025c 71 l1kc79win2d2025 79 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

lambda_0(20.25) = `ell_delta.lam0_at(20.25, *ell_delta.lam0_table())` = 2.1099063840 (error 3.9e-6; unused with `--no-gamma`). `ell_refine.py` reads `data/sol_l1kc71Lw1025c_D20.2500.npy`: the pinned state is copied there under that name (leg 3 saves the `.4f` name only at multiples of 0.5), blob checked. 8 BLAS threads, Normal priority, cap 21600 s by the exact root pid with the `ell_refine.py` command-line check (`crun` of `../kc71_leap/lib_kcl.sh`; its planted test is in `../kc71_leap/`), started outside the terminal through `../kc71_leap/cim_start.ps1 -Normal` (the headless form). **Source first:** `kc71_syscheck.py` accepts the state (the record's |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%, both controls refused, `--mutate=F` and `--mutate=steps` exit 1); a refusal stops the task. **Acceptance of the result (fixed now):** `kc79_syscheck_1025.py REC STATE 20.25 WTM` exits 0, its selftest exits 0, its controls on the same numbers are refused, `--mutate=F` and `--mutate=steps` exit 1. A failed control or a regrid that does not converge stops with a report, no retry. Estimate 1.5 to 2 h (the k_c 79 regrid of D 20 took 5281 s).

**Rehearsal of the source checks (`rehearsal/`, no regrid):** `kc71_syscheck.py` accepts the D 20.25 state: record |F| 4.7845e-10, the state's |F| 4.7852e-10, `freeze_from` 2484 steps = the record's, controls refused, both `--mutate` exit 1.

## Step 2: the scan (`scan79_d2025.sh`, starts itself when `regrid_accepted.txt` is non-empty)

xfkappa's `d18_hybsign.py` (e089207a, unchanged) on the accepted k_c 79 state and its record line, the 1e-15 noise test (2 seeds) and the float64 sign; first line of each process: the record-system check (exit 3 if not). **Lambda 1.12 to 1.24 by 0.01 (13 values) and a repeat of 1.18: 14 evaluations in seven processes of one thread:**

| process | lambda, in this order |
|---|---|
| P1 | 1.18, 1.12 |
| P2 | 1.18, 1.13 |
| P3 | 1.14, 1.15 |
| P4 | 1.16, 1.17 |
| P5 | 1.19, 1.20 |
| P6 | 1.21, 1.22 |
| P7 | 1.23, 1.24 |

Normal priority, caps 28800 s by the exact root pids, `P4_WT_MATTER` the worktree. **Repeat gate** (`pair2025.py`, a copy of `../kc79_d20/pair79.py`): the first records of P1 and P2 (both 1.18) must agree in hybrid sign, noise signs, float64 sign and ln|det| within 1e-6, else the seven scans are killed by exact pid. **Reading:** `read_lower.py SCAN_DIR 1.12 1.24` as it prints, after its selftest and `--mutate=shift` and `--mutate=round2` (exit 1 each); roots named by position. Estimate: k_c 79 D 20 took 1047 to 1332 s a point at one thread, so about 45 min for the two rounds.

## Step 3: k_c 87 (written now, window fixed after step 2's reading)

From the accepted k_c 79 state, as at D 20 (`../kc87_d20/`): `ell_refine.py l1kc79win2d2025 79 l1kc87win2d2025 87 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, source accepted by the k_c 79 check (controls exit 1) and refused by `kc87_syscheck_1025.py`; result accepted only by `kc87_syscheck_1025.py` (selftest 0, `--mutate=F` and `--mutate=steps` exit 1) with `kc79_syscheck_1025.py` refusing it; 8 threads, Normal, cap 21600 s. Then `d18_hybsign.py` over **the k_c 79 root's bracket (lo, hi) +-0.03 by 0.005**, i.e. lambda lo - 0.03 to hi + 0.03 (15 values for a bracket of width 0.01) plus one repeat of the value nearest the bracket's low edge, one thread per process, read with `read_lower.py`. The window, the lists and the repeat are posted on #1025 before the scan starts. The regrid of step 3 does not depend on step 2's result (only its scan window does); it starts when step 2 has ended unless the coordinator allows it beside step 2's scan (threads 8 + 7 + 4 of leg 3 = 19 of 20).

## Run

The regrid and scan drivers of step 1 and 2 start outside the terminal through `../kc71_leap/cim_start.ps1 -Normal` as soon as this README is pushed and the plan is posted on #1025: the regrid driver at once, the scan driver waits for `regrid_accepted.txt`. No script sends hc; verdicts are read from `summary_kc79.txt` and `exits_kc79.txt` and reported by hand.

## Step 3 scan: window and lists, fixed before the run (the coordinator's hc ~09:10 UTC 23 Nov, after the two robust changes of step 2)

The k_c 79 scan found two robust changes (1.165140 and 1.203492), so the order's "the k_c 79 root's bracket +-0.03 by 0.005" is read as both brackets: **lambda 1.130 to 1.240 by 0.005 (23 values) plus a repeat of 1.160: 24 evaluations on 8 processes of 1 thread** (`scan87_d2025.sh`, `d18_hybsign.py` e089207a, Normal priority, caps 28800 s by the exact root pids; starts itself when `regrid87_accepted.txt` is non-empty):

| process | lambda, in this order |
|---|---|
| P1 | 1.160, 1.130, 1.135 |
| P2 | 1.160, 1.140, 1.145 |
| P3 | 1.150, 1.155, 1.165 |
| P4 | 1.170, 1.175, 1.180 |
| P5 | 1.185, 1.190, 1.195 |
| P6 | 1.200, 1.205, 1.210 |
| P7 | 1.215, 1.220, 1.225 |
| P8 | 1.230, 1.235, 1.240 |

The repeat of 1.160 (P1, P2) is gated at 1e-6 (`pair2025.py`; a disagreement kills the eight scans). Read with `read_lower.py SCAN_DIR 1.13 1.24` after its selftest and both mutations. **Written before it (the coordinator's):** by position the root near lambda_1's line is 1.1651 (slope -0.33 per unit D from D 20, continuing -0.28, -0.31); the root that stays within 0.002 between k_c 79 and k_c 87 is lambda_1, and the other moves with k_c (a discretization root). Both roots are reported by position beside k_c 79's (1.165140 and 1.203492).

## Result (steps 1 and 2; step 3 running)

**Step 1, the regrid: ACCEPTED** (started 06:44:13 UTC 23 Nov, exit 0 at 08:07:30 UTC, 4997 s, uncapped, 8 threads, Normal priority, root pid 46104, beside leg 3 of the leap; `regrid.log`). Source first: `kc71_syscheck.py` accepts the pinned D 20.25 state (record |F| 4.7845e-10, the state's 4.7852e-10, 2484 steps = the record's, both controls refused, `--mutate=F` and `--mutate=steps` exit 1; `source_kc71_syscheck*.txt`). Result: `kc79_syscheck_1025.py` exit 0, selftest 0, controls refused, `--mutate=F` and `--mutate=steps` exit 1 (`syscheck*.txt`).

| | k_c 71 source (leg 3, D 20.25) | k_c 79 (this regrid) |
|---|---|---|
| \|F\| | 4.7845e-10 | 4.6133e-10 |
| steps | 2484 | 2762 |
| constraint | 4.401e-3 | 2.629e-3 |
| Delta | 1.098622994386 | 1.098607275130 |
| F_start | 4.407e-05 | 3.761e-05 |
| seconds | 3625 (the leap step) | 4977 |

Delta(k_c 79) minus Delta(k_c 71) = -1.5719e-5 (at D 20: -1.1878e-5). Files: `sol_l1kc79win2d2025_D20.2500.npy`, `l1kc79win2d2025.jsonl`, `rec_k79_D20.2500.jsonl`, `regrid_accepted.txt`.

**Step 2, the scan: done** (started 08:07:58 UTC, seven processes of one thread, Normal priority; ended 09:03:16 UTC; `scan_k79d2025_p1..p7.jsonl`; exit 0 for all seven, 3280 to 3316 s, 2 evaluations each, 1629 to 1649 s a point, no cap). The system check of every process passed (|F| 4.6163579914e-10 against the record's 4.6133024092e-10, 2762 steps = the record's). **The repeat of 1.18 (P1, P2) agrees: sign +1 and ln|det| -2424.4288453048 in both, difference 0.0 (bar 1e-6); the gate passed after 1656 s.**

`read_lower.py 1.12 1.24` as it prints (`read_lower_k79_D2025.txt`): 13 points in 1.120 to 1.240, none not noise robust; hybrid signs minus at 1.12 to 1.16, plus at 1.17 to 1.20, minus at 1.21 to 1.24; the float64 sign differs from the hybrid at 1.12 to 1.16 and 1.21 to 1.24 (it reads plus there; information, the hybrid is the sign used); repeated points 1.18 agree; **two robust changes: (1.160, 1.170), minus to plus, det-linear estimate 1.165140, estimator range [1.162108, 1.165140]; and (1.200, 1.210), plus to minus, det-linear estimate 1.203492, range [1.202702, 1.203492]** (spreads over estimator choices, not enclosures); changes touching a non-robust point: none; ln|det| local minima without a sign change: none; endpoint signs minus at 1.120 and at 1.240. A plus well of width 0.0384 between the two roots.

**Against the order's written prediction** ("lambda_1(20.25) near 1.17, with one robust change in the window"): the root at 1.165140 is 0.0049 below 1.17, but the window has TWO robust changes, not one. By position, at D 20 the k_c 79 window 1.20 to 1.32 had one root, 1.248340 (and nothing in 1.20 to 1.24 besides it, minus below it), and k_c 87 gave 1.247484 there. Which of the two D 20.25 roots continues the D 20 root (-0.332 per unit D to 1.1651, or -0.179 per unit D to 1.2035) is not shown by two values of D; the line (-0.31 per unit D) is nearer 1.1651.

<details><summary>All 14 evaluations (hybrid sign, ln abs det, noise test, float64 sign, seconds)</summary>

| lambda | process | hybrid sign | ln abs det | noise (2 seeds) | float64 sign | s |
|---|---|---|---|---|---|---|
| 1.12 | P1 | - | -2418.3438 | -,- | + | 1647 |
| 1.13 | P2 | - | -2419.4135 | -,- | + | 1645 |
| 1.14 | P3 | - | -2420.5849 | -,- | + | 1629 |
| 1.15 | P3 | - | -2421.9776 | -,- | + | 1648 |
| 1.16 | P4 | - | -2424.2841 | -,- | + | 1630 |
| 1.17 | P4 | + | -2424.3401 | +,+ | + | 1643 |
| 1.18 | P1 | + | -2424.4288 | +,+ | + | 1630 |
| 1.18 | P2 | + | -2424.4288 | +,+ | + | 1648 |
| 1.19 | P5 | + | -2425.1494 | +,+ | + | 1640 |
| 1.20 | P5 | + | -2426.9671 | +,+ | + | 1646 |
| 1.21 | P6 | - | -2426.3445 | -,- | + | 1649 |
| 1.22 | P6 | - | -2425.8712 | -,- | + | 1642 |
| 1.23 | P7 | - | -2425.8345 | -,- | + | 1634 |
| 1.24 | P7 | - | -2425.9621 | -,- | + | 1647 |

</details>

**Step 3, the k_c 87 regrid: ACCEPTED** (started 08:10:35 UTC beside the step-2 scan, the gate having measured exactly 8 logical cores idle, the rule's minimum; exit 0 at 10:13:37 UTC, 7385 s, uncapped, 8 threads, Normal priority, root pid 40780, beside leg 3 of the leap; `regrid87.log`). The source (the accepted k_c 79 D 20.25 state, blob 51b3973a, record file f6f5a3ab) was accepted by `kc79_syscheck_1025.py` (controls exit 1) and refused by `kc87_syscheck_1025.py` first (`source_kc79_syscheck*.txt`, `source_kc87_syscheck.txt`). Result: `kc87_syscheck_1025.py` exit 0, selftest 0, controls refused, `--mutate=F` and `--mutate=steps` exit 1, and `kc79_syscheck_1025.py` refuses it ("the record is not k_c 79 at D 20.25 (kc 87, D 20.25)") (`syscheck87*.txt`, `syscheck_kc79_on_k87_result.txt`).

| | k_c 79 source (D 20.25) | k_c 87 (this regrid) |
|---|---|---|
| \|F\| | 4.6133e-10 | 4.5096e-10 |
| steps | 2762 | 3042 |
| constraint | 2.629e-3 | 1.625e-3 |
| Delta | 1.098607275130 | 1.098603666283 |
| F_start | 3.761e-05 | 1.066e-05 |
| seconds | 4977 | 7378 |

Delta(k_c 87) minus Delta(k_c 79) = -3.6088e-6 (at D 20: -2.9719e-6). Files: `sol_l1kc87win2d2025_D20.2500.npy`, `l1kc87win2d2025.jsonl`, `rec_k87_D20.2500.jsonl`, `regrid87_accepted.txt`.

**Step 3, the k_c 87 scan: done** (started 10:14:17 UTC, eight processes of one thread, Normal priority; ended 12:08:37 UTC; `scan_k87d2025_p1..p8.jsonl`; exit 0 for all eight, 6823 to 6858 s, 3 evaluations each, 2190 to 2326 s a point (mean 2276 s), no cap). The system check of every process passed ("the record system": |F| 4.5117744977e-10 against the record's 4.5095811903e-10, 3042 steps = the record's). **The repeat of 1.160 (P1, P2) agrees: sign -1 and ln|det| -2731.7353253669 in both (bar 1e-6); the gate passed after 2365 s.**

**A defect of the driver, found at the reading and corrected here:** `read_lower.py` reads every `scan_*_p*.jsonl` of the folder it is given, and `scan87_d2025.sh` gave it this folder, which also holds the k_c 79 scan's files. Its printed reading (`read_lower_k87_D2025.txt`: 8 robust changes, 13 DISAGREE repeats) therefore mixes the two k_c at the 13 values of the 0.01 grid and is void. The reading below is of a folder with the eight k_c 87 files alone (`read87/`, copies; reader blob 89309d3c unchanged; selftest 0, `--mutate=shift` and `--mutate=round2` exit 1) and is the one that counts: `read_lower_k87_D2025_only87.txt`.

`read_lower.py read87 1.13 1.24`, as it prints: 23 points in 1.130 to 1.240, none not noise robust; hybrid signs minus at 1.130 to 1.165, **plus at 1.170 to 1.240** (every value, to the window's edge); the float64 sign differs from the hybrid at 1.17 only (information); repeated points 1.16 agree; **one robust change: (1.165, 1.170), minus to plus, det-linear estimate 1.165265, estimator range [1.165184, 1.165265]** (a spread over estimator choices, not an enclosure); changes touching a non-robust point: none; ln|det| local minima without a sign change: none; endpoint signs minus at 1.130 and plus at 1.240.

**By position, beside k_c 79 at the same D 20.25:**

| root | k_c 79 | k_c 87 | k_c 87 minus k_c 79 |
|---|---|---|---|
| near lambda_1's line (minus to plus) | 1.165140 (bracket (1.160, 1.170)) | 1.165265 (bracket (1.165, 1.170)) | +0.000125 |
| the second (plus to minus) | 1.203492 (bracket (1.200, 1.210)) | none in 1.130 to 1.240 | above 1.240 if it exists |

The first root moves by 0.000125 between k_c 79 and k_c 87, inside the 0.002 written before (the coordinator's rule: the root that stays within 0.002 between k_c 79 and 87 is lambda_1). The second root does not: at the 12 values the two scans share (1.13 to 1.24 by 0.01) the signs agree for 1.13 to 1.20 and differ for 1.21 to 1.24 (k_c 79 minus, k_c 87 plus), and ln|det| at k_c 87 falls steadily from -2732.43 (1.20) to -2734.27 (1.24) with no sign change. So the second root moved above 1.240 (by more than 0.036) or left the window, which is the behavior the rule names for a discretization root; where it is at k_c 87 the window does not show (a scan above 1.240 would).

lambda_1 against D at k_c 79 and k_c 87 (D 20 values from `../kc79_d20/` and `../kc87_d20/`, D 18.5 and D 19.5 the coordinator's): k_c 79 1.248340 (D 20) to 1.165140 (D 20.25), slope -0.3328 per unit D; k_c 87 1.247484 to 1.165265, slope -0.3289 per unit D; the earlier slopes -0.28 (D 18.5 to 19.5) and -0.30 (D 19.5 to 20, from 1.398 and 1.248340).

<details><summary>All 24 evaluations (hybrid sign, ln abs det, noise test, float64 sign, seconds)</summary>

| lambda | process | hybrid sign | ln abs det | noise (2 seeds) | float64 sign | s |
|---|---|---|---|---|---|---|
| 1.130 | P1 | - | -2727.8671 | -,- | - | 2312 |
| 1.135 | P1 | - | -2728.3469 | -,- | - | 2195 |
| 1.140 | P2 | - | -2728.8542 | -,- | - | 2309 |
| 1.145 | P2 | - | -2729.4013 | -,- | - | 2192 |
| 1.150 | P3 | - | -2730.0113 | -,- | - | 2319 |
| 1.155 | P3 | - | -2730.7358 | -,- | - | 2316 |
| 1.160 | P1 | - | -2731.7353 | -,- | - | 2326 |
| 1.160 | P2 | - | -2731.7353 | -,- | - | 2325 |
| 1.165 | P3 | - | -2735.3473 | -,- | - | 2199 |
| 1.170 | P4 | + | -2732.4630 | +,+ | - | 2312 |
| 1.175 | P4 | + | -2732.0747 | +,+ | + | 2314 |
| 1.180 | P4 | + | -2731.9875 | +,+ | + | 2198 |
| 1.185 | P5 | + | -2732.0212 | +,+ | + | 2317 |
| 1.190 | P5 | + | -2732.1209 | +,+ | + | 2315 |
| 1.195 | P5 | + | -2732.2620 | +,+ | + | 2199 |
| 1.200 | P6 | + | -2732.4316 | +,+ | + | 2324 |
| 1.205 | P6 | + | -2732.6221 | +,+ | + | 2317 |
| 1.210 | P6 | + | -2732.8285 | +,+ | + | 2198 |
| 1.215 | P7 | + | -2733.0475 | +,+ | + | 2303 |
| 1.220 | P7 | + | -2733.2766 | +,+ | + | 2304 |
| 1.225 | P7 | + | -2733.5141 | +,+ | + | 2201 |
| 1.230 | P8 | + | -2733.7587 | +,+ | + | 2319 |
| 1.235 | P8 | + | -2734.0093 | +,+ | + | 2323 |
| 1.240 | P8 | + | -2734.2650 | +,+ | + | 2190 |

</details>
