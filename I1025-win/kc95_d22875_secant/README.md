# I1025-win/kc95_d22875_secant: Brent refinement of k_c 95's root at D 22.875 on win2's accepted state and bracket (0.10, 0.12), with `d18_secant.py` (winb)

Written before the run, 2026-11-26 06:15:54 UTC (the time of the README-first push; later pushes keep it). The refinement had not been run for this folder when the order, the registration and the estimates below were written. Run beforehand, read-only: the driver's dry run (pins, the four `d18_secant.py` selftests, the selftests and the five acceptance checks of the state, the planned command). Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc, stamped 2026-11-26 06:35 UTC; this machine's clock read 06:12 UTC when I read it; winb section, quoted)

"Coordinator (t5): ruling: k_c 103 at D 22.875: exit 4 with a non-robust interior point stands as the ROBUST BRACKET [0.11859005, 0.11874136] (width 1.5e-4), det-linear 0.11872688 inside it, as for k_c 95 at D 23.0. No rerun. With D 23.0 (0.02650535) and D 23.0625 (-0.02851243), this is k_c 103's third D. Push the folder, then post on #1025 with the eval lines as printed.

Next lane, #1025 k_c 95 at D 22.875, the secant on win2's (0.10, 0.12) bracket (the third D for k_c 95, for the curvature of lambda_1 in D):
- Inputs, pinned by blob: raw I1025-win2/kc95_d22875/sol_l1kc95win2d22875_D22.8750.npy (blob a14f0d50) and its record l1kc95win2d22875.jsonl (blob 5381f89d). win2's scan reading: robust change (0.100, 0.120), det-linear 0.118242, range [0.104198, 0.118242], and a second change in (-0.04, -0.02) that this lane does not touch.
- Folder: raw I1025-win/kc95_d22875_secant/. Write the README registration first. Use your kc103d22875 secant driver with the state, record, bracket and acceptance check changed (kc95_syscheck_1025.py must accept the record and state; its --mutate=F and --mutate=steps exit 1; the k_c 103 check refuses). Put the driver diff in the folder.
- Command: d18_secant.py (a3d90cd5) --tol=1e-5 --maxev=10 on (0.10, 0.12), one process, below-normal priority, its pins on.
- Stop and report on: a state that is not accepted, an exception, signs at 0.10 and 0.12 that do not differ, or any step over 8 h.
- My registered prediction: the root is 0.1182 +- 0.002.
- ETA about 2.5 h at your 1400 s per evaluation. Post on #1025 when it ends. I give the ruling."

The k_c 103 D 22.875 secant is pushed (`I1025-win/kc103_d22875/secant` at a83c9a635) and posted (#1025 comment 7184197506).

My reading, and what I add:

- **The command is t5's:** `d18_secant.py run STUB STATE 22.875 0.10 0.12 secant.jsonl --tol=1e-5 --maxev=10 --pin=a14f0d50...,5381f89d...` (the full blobs), the tool at 6010e37b, blob a3d90cd5 (the worktree `choptuik-i1025secant` of the k_c 103 lane, unchanged), one process, 1 thread (`RAYON_NUM_THREADS`, `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` = 1), BelowNormal, outside my terminal, from a headless console. No `--ends` (both ends are evaluated, two evaluations); `--mm`, `--b12`, `--dln`, `--eps` at their defaults, as at k_c 103.
- **The driver** is my k_c 103 D 22.875 secant driver with the state, record, bracket and acceptance check changed; the diff is `diff_secant_driver_vs_kc103.txt` (made by `make_kc95d22875s_1025.py`). The acceptance replaces the k_c 103 regrid marker and the scan-record check: `kc95_syscheck_1025.py` accepts the record and state (exit 0), its `--mutate=F` and `--mutate=steps` exit 1, and the k_c 87 and k_c 103 checks refuse them (exit 1 each); the selftests of the three checks exit 0. The state and record are win2's files themselves (the same blobs my k_c 103 regrid started from), copied to `in/` and checked by blob; nothing of win2's is modified.
- **Stops** (t5's): a state that is not accepted, an exception, signs at 0.10 and 0.12 that do not differ (the tool refuses after its two end evaluations, exit 2), or any step over 8 h: the driver kills the process by the exact pid at 28800 s and reports; one hc at 14400 s if it still runs. Also as before, each reported as printed, no rerun with other options, no widening: exit 3 (a pin differs or not the record system), exit 4 (`--maxev`, or a non-robust interior point as at k_c 103: the bracket is valid and t5 rules). The second change in (-0.04, -0.02) is not touched.
- Nothing else of mine runs beside it; the other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Written before the run (t5's registration)

**PREDICTION (t5's): the root is 0.1182 +- 0.002.** By position: the det-linear root inside the final bracket (`lam_lin` of the last record, kind `root`, in `secant.jsonl`) lies in [0.1162, 0.1202]. **Met** if so, **not met** otherwise (then the offset from the nearer end is reported). If the run ends at a non-robust interior point (exit 4), the same `lam_lin` of the valid bracket is compared, and the bracket itself is reported as printed.

Information beside it, not criteria: the final bracket and its width (the tool stops at 1e-5, status `tol`, or earlier); Brent's last point (`lam_brent`); whether the whole final bracket lies in [0.1162, 0.1202]; win2's reading and whether `lam_lin` lies in win2's estimator range; the hybrid signs and ln\|det\| at each evaluation, with the float64 sign beside it, and the two end evaluations beside win2's scan records of the same state at 0.10 and 0.12. I do not interpret the result against other k_c readings or D; t5 rules.

For reference (win2's reading as printed in his `read_lower.txt`, raw `I1025-win2/kc95_d22875` at b22754638; my k_c 103 reading at this D beside it; neither is a prediction of mine, and printed orientation is not compared across k_c):

| reading at D 22.875 | bracket | det-linear | range | orientation as printed |
|---|---|---|---|---|
| k_c 95, win2's scan (window -0.06 to 0.30) | (0.100, 0.120), hybrid sign + at 0.10, - at 0.12 | 0.118242 | [0.104198, 0.118242] | + to - |
| k_c 95, win2's scan, a second change (not touched here) | (-0.040, -0.020) | -0.025724 | [-0.038477, -0.025724] | - to + |
| k_c 103, my scan then my secant (t5's ruling: robust bracket) | scan (0.100, 0.120); secant [0.11859005, 0.11874136] | scan 0.119801; secant 0.11872688 | scan [0.103345, 0.119801] | scan - to + |

What I report (t5's list for the earlier lane, kept): the evaluations (lambda, hybrid sign, ln\|det\|, dln, robust, float64 sign, seconds and the three parts), the final bracket, the status and exit, the time per evaluation, and the peak private memory.

## The tool, the state and the pins

| item | value |
|---|---|
| tool | `d18_secant.py` committed blob a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49 at 6010e37b30f92688dd5c659e383c6d0c8d14b6da (branch `wip/ell1-speed`; worktree `choptuik-i1025secant`, made for the k_c 103 lane); `ell_fastm.py` 93f963f6; `ell_ddm.py`, `dss_ell.py`, `ell_dd.py`, `ddnp.py` the same blobs as in my regrid worktree (`prep_kc95d22875s_pins_1025.txt`) |
| state | `in/sol_l1kc95win2d22875_D22.8750.npy`, blob a14f0d50edb575e85387851a61cb2324c1983317 (49848 bytes; win2's `I1025-win2/kc95_d22875`, commit 55161c546, ACCEPTED by win2 2026-11-25 14:20 UTC; the same file my k_c 103 regrid started from) |
| record | `in/l1kc95win2d22875.jsonl`, blob 5381f89d5fe4f81a113295cdde8eb6358de937e8 (371 bytes, one row: k_c 95, D 22.875, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.5210384140874643e-10, F_start 7.520694957814806e-05, steps 3126, constraint 7.113644147048331e-03, Delta 1.170668364709999, 5901 s, src `l1kc87Lmacm3c`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628, `kc103_syscheck_1025.py` 3ab58d16 (`inputs/`, the ones of my regrids) |
| python | `venv-md510` (python 3.14, multidouble 5.1.0 with `dd_logdet`) |

Source quality, as win2 states it: macm3's part c lineage (h 0.0625), psi-constraint 7.114e-03, F_start 7.521e-05 (the k_c 87 source's constraint is 9.932e-03).

The acceptance, run by the driver's dry run at 06:14 UTC (`*.txt.dry` in this folder; the driver repeats it and stops if any differs): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 3.5210384141e-10, the state's \|F\| on this machine 3.5250023129e-10 (0.11 % apart, inside the 1 % bar), `freeze_from` 3126 steps = the record's), `--mutate=F` exit 1 (state \|F\| 3.525002e-10 against 5.281558e-10), `--mutate=steps` exit 1 (3126 against 3127), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 22.875 (kc 95, D 22.875)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 22.875 (kc 95, D 22.875)"); the selftests of the three checks exit 0; `d18_secant.py selftest` exit 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 each (the same four as the k_c 103 lane's, repeated).

## Cost, written before the run

| source of the estimate | number |
|---|---|
| my k_c 103 D 22.875 secant (`I1025-win/kc103_d22875/secant`), one process | 1388 to 1448 s per evaluation (mean 1408 s: float64 matrix 211 to 243 s, block 12 1165 to 1193 s, `dd_logdet` calls 11 to 12 s), 6 evaluations, 8460 s, peak private 2.91 GB, lowest free memory 20.84 GB |
| size here | k_c 95: 3126 steps against 3387 (the work per evaluation falls with k_c, as the k_c 95 scan points took 0.6 to 0.8 times the k_c 103 ones: 4041 to 4055 s against 6619 to 6628 s at D 21.0, 4489 to 4619 s at D 22.125 against 5955 to 6034 s at D 22.0) |

| item | estimate | basis |
|---|---|---|
| source checks and selftests in the driver | about 15 to 30 s | the dry run: 16 s |
| each evaluation | about 900 to 1500 s, central about 1150 s | the k_c 103 evaluations (1388 to 1448 s) times 0.6 to 1.0 |
| evaluations | about 6 (the two ends and about 4 interior points; at most 10); the k_c 103 run stopped at a non-robust interior point after 6 | k_c 103 secant, `SPEED_ELL1.md` |
| the refinement | about 5400 to 15000 s (1.5 to 4.2 h), central about 7500 s | the rows above; t5's ETA about 2.5 h; the driver's kill is at 28800 s |
| peak private | about 2.4 to 3.0 GB | 2.91 GB at k_c 103 |
| lowest free memory | about 20 GB | 20.84 GB at k_c 103 (one process alone) |
| together | start about 06:25 UTC, ends about 07:55 to 10:40 UTC (central about 08:30) | the rows above |

The sampler (`rows/secant_samples.csv`, 60 s) gives the real figures.

## Files made here

`kc95d22875s_secant_driver_1025.py` (pins, selftests, the acceptance of the state, the capped run, the hc), `diff_secant_driver_vs_kc103.txt` (its diff against the k_c 103 driver), `make_kc95d22875s_1025.py` (writes the driver, watcher, keep-awake helper, session check, `go_kc95d22875s_1025.cmd` and the publish script from the k_c 103 ones by asserted replacements), `sample_driver_secant_1025.ps1`, `prep_kc95d22875s_pins_1025.txt`, `selftest_secant_dry_1025.txt`, `in/` (win2's state and record), and after the run `secant.jsonl`, `secant.log`, `secant_summary.txt`, `secant_driver_w.log`, `source_kc*_syscheck*.txt`, `selftest_*.txt`, `session_check_secant.txt`.

## Status

**ENDED 2026-11-26 08:57:55 UTC (exit 0, status tol; started 06:16:24 UTC, 9690 s); the chain ended 08:59:10 UTC; Result below.** README first 42a0098c0 (pushed 06:15:54 UTC, before the start); chain started 06:16:08 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc95d22875s_1025.cmd`. The k_c 103 secant was pushed (a83c9a635) and posted (#1025 comment 7184197506) first.

- **Chain** (`rows/launcher_pid.txt`: 23044): conhost --headless 23044 <- cmd 21404 <- driver launcher 18480 and driver 9368 <- `d18_secant.py` pid 17656, sampler 11200, alert-only watcher 17424, keep-awake helper 25284. BelowNormal, one thread, killed by the exact pid at 28800 s, one hc at 14400 s if it still runs.
- **Session check** (`session_check_secant.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the run** (06:16:08 to 06:16:24 UTC, 16 s): the driver's pins matched; `d18_secant.py selftest` exit 0 and its three controls exit 1, 1, 1; the selftests of the three checks exit 0; the state was accepted as ordered: `kc95_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 and k_c 103 checks exit 1 (they refuse it) (`source_kc*_syscheck*.txt`). The tool printed its pin lines and "the record system" (\|F\| 3.5250023129e-10 against the record's 3.5210384141e-10, 3126 steps = the record's).
- **Machine at the start:** the other project's I114 `convergence.py` jobs run beside it, not touched.
- **End:** the process ended 08:57:55 UTC with exit 0 after 9 evaluations (written: about 6 evaluations, ending about 07:55 to 10:40 UTC).

Pushed 2026-11-26 09:00:57 UTC.

## Result

The tool's lines (`secant.log`), as printed (`d18_secant.py run`, default `--mm=fast` (basis jac), `--b12=ddm`, `--tol=1e-5 --maxev=10`, pins matched, "the record system" first):

```
D 22.875 k_c 95: |F| 3.5250023129e-10 (record 3.5210384141e-10), steps 3126 (record 3126): the record system
bracket (0.1, 0.12), tol 1e-05, maxev 10, mode matrix fast (jac), block 12 ddm, noise 1e-15, dln <= 0.1, sol_l1kc95win2d22875_D22.8750.npy
  lam 0.1 (lo): hybrid +1 ln|det| -2661.5070993901, noise [1.0, 1.0] dln 1.07e-06, robust True; float64 +1 -2660.5821559241 (1079 s [164, 905, 10])
  lam 0.12 (hi): hybrid -1 ln|det| -2663.8470057306, noise [-1.0, -1.0] dln 2.52e-06, robust True; float64 +1 -2662.8996697942 (1088 s [162, 916, 9])
  lam 0.11824257157304068 (interior): hybrid -1 ln|det| -2664.0386848392, noise [-1.0, -1.0] dln 3.49e-06, robust True; float64 +1 -2662.7760354580 (1068 s [160, 899, 9])
  lam 0.11053744496727427 (interior): hybrid +1 ln|det| -2663.7822909115, noise [1.0, 1.0] dln 4.83e-06, robust True; float64 +1 -2661.9345322091 (1084 s [160, 914, 9])
  lam 0.11488120726854567 (interior): hybrid -1 ln|det| -2665.1441777046, noise [-1.0, -1.0] dln 1.36e-05, robust True; float64 +1 -2662.3171743652 (1081 s [160, 911, 9])
  lam 0.11355698727076302 (interior): hybrid +1 ln|det| -2666.9168205960, noise [1.0, 1.0] dln 8.86e-05, robust True; float64 +1 -2661.7235974538 (1067 s [160, 897, 9])
  lam 0.11374928251034458 (interior): hybrid -1 ln|det| -2669.3074640666, noise [-1.0, -1.0] dln 9.54e-04, robust True; float64 +1 -2662.3285808539 (1066 s [160, 896, 9])
  lam 0.1137331510613552 (interior): hybrid -1 ln|det| -2673.5688764429, noise [-1.0, -1.0] dln 7.01e-02, robust True; float64 +1 -2662.2372328574 (1073 s [166, 898, 9])
  lam 0.1137281510613552 (interior): hybrid +1 ln|det| -2670.5353761773, noise [1.0, 1.0] dln 3.26e-03, robust True; float64 +1 -2662.2614039124 (1071 s [160, 902, 10])
root: status tol (-), bracket [0.1137281510613552, 0.1137331510613552] width 5.000e-06, signs [1.0, -1.0], det-linear 0.1137329213854384, Brent 0.1137331510613552, 9 evaluations, 9678 s
```

Exit **0** (the bracket reached the tolerance 1e-5; status `tol`). The driver's lines (`secant_driver_w.log`): the process ended with exit 0 after 9690 s (06:16:24 to 08:57:55 UTC); peak private 2.53 GB, peak working set 1.93 GB, lowest free memory 20.71 GB, peak commit 13.8 GB, cpu 9537 s (318 samples).

**The evaluations** (`secant.jsonl`; each seconds figure is the evaluation's wall, with `sec_parts` = float64 matrix, double-double block 12, the `dd_logdet` calls with the noise test):

| # | role | lambda | hybrid sign | hybrid ln\|det\| | dln | robust | float64 sign | seconds | parts (s) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | lo | 0.1 | + | -2661.5070993901 | 1.07e-06 | yes | + | 1079 | 164, 905, 10 |
| 1 | hi | 0.12 | - | -2663.8470057306 | 2.52e-06 | yes | + | 1088 | 162, 916, 9 |
| 2 | interior | 0.11824257157304068 | - | -2664.0386848392 | 3.49e-06 | yes | + | 1068 | 160, 899, 9 |
| 3 | interior | 0.11053744496727427 | + | -2663.7822909115 | 4.83e-06 | yes | + | 1084 | 160, 914, 9 |
| 4 | interior | 0.11488120726854567 | - | -2665.1441777046 | 1.36e-05 | yes | + | 1081 | 160, 911, 9 |
| 5 | interior | 0.11355698727076302 | + | -2666.9168205960 | 8.86e-05 | yes | + | 1067 | 160, 897, 9 |
| 6 | interior | 0.11374928251034458 | - | -2669.3074640666 | 9.54e-04 | yes | + | 1066 | 160, 896, 9 |
| 7 | interior | 0.1137331510613552 | - | -2673.5688764429 | 7.01e-02 | yes (dln <= 0.1) | + | 1073 | 166, 898, 9 |
| 8 | interior | 0.1137281510613552 | + | -2670.5353761773 | 3.26e-03 | yes | + | 1071 | 160, 902, 10 |

All nine evaluations are noise-robust under the tool's test (both noise signs equal the sign and dln <= 0.1); evaluation 7 has the largest dln (0.0701, under the bar 0.1). dln rises as the root is approached (1.1e-6 at the ends to 7.0e-2) while ln\|det\| falls from -2661.5 to -2673.6. The float64 sign is + at all nine lambdas, including the three where the hybrid sign is -.

**Final bracket and root:** [0.1137281510613552, 0.1137331510613552], width 5.000e-06 (the tolerance 1e-5 reached), signs + and -, both ends robust. The det-linear root inside it is **0.113733** (0.1137329213854384); Brent's last point is 0.1137331510613552, the bracket's upper end.

**Against the registration** (t5's prediction: the root is 0.1182 +- 0.002, i.e. `lam_lin` in [0.1162, 0.1202]): `lam_lin` 0.1137329 lies **below** it: **not met**. It is 0.002467 below the nearer end of the interval (0.1162) and 0.004467 below its centre 0.1182; the whole final bracket also lies below. t5 notes (hc, quoted): "My registered 0.1182 +- 0.002 MISSED by 0.0045: I centred it on the scan's det-linear 0.118242. The root lies inside the scan's estimator range [0.104198, 0.118242], as it should." As information: win2's reader estimate 0.118242 is 0.004509 above the root; the root lies inside win2's estimator range [0.104198, 0.118242] (a 0.009535 distance from the range's lower end).

**Beside win2's scan records of the same state at the two shared ends** (`I1025-win2/kc95_d22875/scan_D22.875_all.jsonl` at b22754638: `d18_hybsign.py` with the complex-step float64 matrix; this tool uses the fast float64 matrix, the same double-double block 12 and sign code):

| lambda | hybrid sign, win2 / tool | hybrid ln\|det\|, win2 | hybrid ln\|det\|, tool | difference (tool minus win2) | float64 sign, win2 / tool |
|---|---|---|---|---|---|
| 0.10 | + / + | -2661.5071191646 | -2661.5070993901 | +1.98e-05 | + / + |
| 0.12 | - / - | -2663.8469740147 | -2663.8470057306 | -3.17e-05 | - / + |

The hybrid signs agree at both ends; win2's repeat of 0.10 is bit-identical to his first record. The float64 sign at 0.12 differs between the two codes (win2's - against the tool's +), as at k_c 103; I do not interpret it beyond `SPEED_ELL1.md`'s statement that the float64 block 12 is wrong and the hybrid replaces it.

**t5's ruling** (hc, 2026-11-26 08:59 UTC, quoted): "Ruling on k_c 95 at D 22.875: tol reached (exit 0), root 0.11373292 in [0.11372815, 0.11373315]. ... With D 23.0 and 23.0625, a quadratic in D puts k_c 95's zero at D 23.00863, against 23.00808 from the straight line (+0.00055). k_c 103's is 23.03095 against 23.03011 (+0.00084). Push the folder and post on #1025 with the eval lines as printed."

**Cost against the estimates written before the run:**

| item | written | measured |
|---|---|---|
| source checks and selftests in the driver | about 15 to 30 s | 16 s (06:16:08 to 06:16:24 UTC) |
| each evaluation | about 900 to 1500 s, central about 1150 s | 1066 to 1088 s (mean 1075 s) |
| float64 matrix, block 12, `dd_logdet` calls per evaluation | not written | 160 to 166 s, 896 to 916 s, 9 to 10 s |
| evaluations | about 6 (at most 10) | 9 (the two ends and seven interior points): above my "about 6", inside the maximum of 10 |
| the refinement | about 5400 to 15000 s, central about 7500 s | 9690 s (06:16:24 to 08:57:55 UTC) |
| peak private | about 2.4 to 3.0 GB | 2.53 GB (peak working set 1.93 GB) |
| lowest free memory | about 20 GB | 20.71 GB in the sampler (08:43:50 UTC), 20.46 GB in the alert-only watcher |

An evaluation took 1075 s here against 1408 s at k_c 103 (0.76 times, inside the 0.6 to 1.0 I wrote). Laptop cpu 11 to 59 % (mean 28.4 %), 161 sample times with no gap over 90 s, the other project's I114 `convergence.py` jobs beside it, not touched. No alert, nothing killed (`rows/secant_memwatch.log`: "minimum free memory seen 20.46 GB; 0 alert(s) sent"); the keep-awake helper held until the driver ended (`rows/secant_keepawake.log`); the System log shows no power event in 06:10 to 09:05 UTC. The 14400 s hc was not needed.

Raw: `secant.jsonl` (nine `eval` records and the `root` record), `secant.log`, `secant_summary.txt`, `secant_driver_w.log`, `source_kc*_syscheck*.txt`, `selftest_*.txt`, `session_check_secant.txt`.
