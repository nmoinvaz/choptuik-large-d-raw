# I1025-win/kc87_d22875_secant: Brent refinement of k_c 87's lambda_1 root at D 22.875 on macm3's leg state and the scan's bracket (0.12, 0.13), with `d18_secant.py` (winb)

Written before the run, 2026-11-26 09:03:54 UTC (the time of the README-first push; later pushes keep it). The refinement had not been run for this folder when the order, the registration and the estimates below were written. Run beforehand, read-only: the driver's dry run (pins, the four `d18_secant.py` selftests, the selftests and the five acceptance checks of the state, the planned command). Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc, stamped 2026-11-26 08:59 UTC; winb section, quoted)

"Coordinator (t5): ruling on k_c 95 at D 22.875: tol reached (exit 0), root 0.11373292 in [0.11372815, 0.11373315]. My registered 0.1182 +- 0.002 MISSED by 0.0045: I centred it on the scan's det-linear 0.118242. The root lies inside the scan's estimator range [0.104198, 0.118242], as it should. With D 23.0 and 23.0625, a quadratic in D puts k_c 95's zero at D 23.00863, against 23.00808 from the straight line (+0.00055). k_c 103's is 23.03095 against 23.03011 (+0.00084). Push the folder and post on #1025 with the eval lines as printed.

Next lane, the same for k_c 87, its third D: the secant on macm3's k_c 87 leg state at D 22.875, on the bracket of the lambda_1 root there (scan reading (0.120, 0.130), det-linear 0.127834).
- Inputs, pinned by blob: raw I1025-macm3/kc87_leg_lambda/22.875/in/sol_l1kc87Lmacm3c_D22.875000.npy (b1e4f8ca) and l1kc87Lmacm3c.jsonl (338bd7f1). The acceptance check is kc87_syscheck_1025.py: exit 0, --mutate=F and --mutate=steps exit 1, and the kc95 check refuses.
- Folder: raw I1025-win/kc87_d22875_secant/. Write the README registration first. Use your kc95 secant driver with the state, record, bracket and check changed, and put the diff in the folder.
- Command: d18_secant.py run (wip/ell1-speed 92b9bf53 or your a3d90cd5 copy; say which) --tol=1e-5 --maxev=10 on (0.12, 0.13), one process, below normal.
- Stop and report on: not accepted, an exception, signs at 0.12 and 0.13 that do not differ, or any step over 8 h.
- My registered prediction, corrected for the det-linear bias seen in both refinements: the root is 0.124 +- 0.003.
- ETA about 2.5 h. Post on #1025 when it ends."

The k_c 95 D 22.875 secant is pushed (`I1025-win/kc95_d22875_secant` at 75a10de70) and posted (#1025 comment 7187315219).

My reading, and what I add:

- **Which tool: my a3d90cd5 copy.** `d18_secant.py` committed blob a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49 at `wip/ell1-speed` 6010e37b, the one of both earlier lanes (k_c 103 and k_c 95 at this D), in the worktree `choptuik-i1025secant`. The branch tip 92b9bf53 (commit "d18_secant: a scan command, d18_hybsign.py's records through the fast float64 matrix") has another `d18_secant.py`, blob eb1396ad; I do not use it, so that the three refinements are the same code. The other solver files at 92b9bf53 have the same blobs as at 6010e37b.
- **The command is t5's:** `d18_secant.py run STUB STATE 22.875 0.12 0.13 secant.jsonl --tol=1e-5 --maxev=10 --pin=b1e4f8ca...,338bd7f1...` (the full blobs), one process, 1 thread (`RAYON_NUM_THREADS`, `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` = 1), BelowNormal, outside my terminal, from a headless console. No `--ends` (both ends are evaluated, two evaluations); `--mm`, `--b12`, `--dln`, `--eps` at their defaults, as in both earlier lanes. The tool reads the last row of the record file with D 22.875 (the file holds six rows, D 22.5625 to 22.875, and is pinned whole).
- **The driver** is my k_c 95 D 22.875 secant driver with the state, record, bracket and acceptance check changed; the diff is `diff_secant_driver_vs_kc95.txt` (made by `make_kc87d22875s_1025.py`). The acceptance: `kc87_syscheck_1025.py` accepts the record and state (exit 0), its `--mutate=F` and `--mutate=steps` exit 1, and the k_c 95 and k_c 103 checks refuse them (exit 1 each; t5 names the k_c 95 check, the k_c 103 one is added); the selftests of the three checks exit 0. The state and record are macm3's files themselves (copies in `in/`, blobs checked); nothing of macm3's is modified.
- **Stops** (t5's): a state that is not accepted, an exception, signs at 0.12 and 0.13 that do not differ (the tool refuses after its two end evaluations, exit 2), or any step over 8 h: the driver kills the process by the exact pid at 28800 s and reports; one hc at 14400 s if it still runs. Also as before, each reported as printed, no rerun with other options, no widening: exit 3 (a pin differs or not the record system), exit 4 (`--maxev`, or a non-robust interior point: the bracket is valid and t5 rules).
- Nothing else of mine runs beside it; the other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Written before the run (t5's registration)

**PREDICTION (t5's, "corrected for the det-linear bias seen in both refinements"): the root is 0.124 +- 0.003.** By position: the det-linear root inside the final bracket (`lam_lin` of the last record, kind `root`, in `secant.jsonl`) lies in [0.121, 0.127]. **Met** if so, **not met** otherwise (then the offset from the nearer end is reported). If the run ends at a non-robust interior point (exit 4), the same `lam_lin` of the valid bracket is compared, and the bracket itself is reported as printed.

Information beside it, not criteria: the final bracket and its width; Brent's last point (`lam_brent`); whether the whole final bracket lies in [0.121, 0.127]; macm3's scan reading and whether `lam_lin` lies in his estimator range [0.123345, 0.127834]; the hybrid signs and ln\|det\| at each evaluation, with the float64 sign beside it, and the two end evaluations beside macm3's scan records of the same state at 0.12 and 0.13. I do not interpret the result against other k_c readings or D; t5 rules.

For reference (macm3's scan reading as printed in his `read_lower.txt`, raw `I1025-macm3/kc87_leg_lambda/22.875`; the two other k_c at this D beside it as t5 ruled them; none is a prediction of mine, and printed orientation is not compared across k_c):

| reading at D 22.875 | bracket | det-linear | range | orientation as printed |
|---|---|---|---|---|
| k_c 87, macm3's scan (window 0.100 to 0.160; hybrid signs 0.100- 0.110- 0.120- 0.130+ 0.140+ 0.150+ 0.160+; float64 differs at 0.15 and 0.16; repeat of 0.13 agrees) | (0.120, 0.130) | 0.127834 | [0.123345, 0.127834] | - to + |
| k_c 95, win2's scan, then my secant (t5's ruling) | scan (0.100, 0.120); secant [0.11372815, 0.11373315] | scan 0.118242; secant 0.11373292 | scan [0.104198, 0.118242] | scan + to - |
| k_c 103, my scan, then my secant (t5's ruling: robust bracket) | scan (0.100, 0.120); secant [0.11859005, 0.11874136] | scan 0.119801; secant 0.11872688 | scan [0.103345, 0.119801] | scan - to + |

What I report (t5's list, kept): the evaluations (lambda, hybrid sign, ln\|det\|, dln, robust, float64 sign, seconds and the three parts), the final bracket, the status and exit, the time per evaluation, and the peak private memory.

## The tool, the state and the pins

| item | value |
|---|---|
| tool | `d18_secant.py` committed blob a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49 at 6010e37b30f92688dd5c659e383c6d0c8d14b6da (branch `wip/ell1-speed`; worktree `choptuik-i1025secant`, unchanged since the k_c 103 lane); `ell_fastm.py` 93f963f6; `ell_ddm.py`, `dss_ell.py`, `ell_dd.py`, `ddnp.py` the same blobs as in my regrid worktree (`prep_kc87d22875s_pins_1025.txt`) |
| state | `in/sol_l1kc87Lmacm3c_D22.875000.npy`, blob b1e4f8cad92d4384f3c2e2dffe15cd2b801251dd (45688 bytes; macm3's `I1025-macm3/kc87_leg_lambda/22.875/in`, his `pins.txt` lists the same blob b1e4f8ca) |
| record | `in/l1kc87Lmacm3c.jsonl`, blob 338bd7f1afa55d6afd80f03051402b855e198a3f (6482 bytes, six rows, D 22.5625 to 22.875; the D 22.875 row: k_c 87, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.612901529332311e-10, F_start 3.8785018824828824e-05, steps 2862, constraint 9.93176604195248e-03, Delta 1.1707181271818858, h 0.0625, 2267 s) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628, `kc103_syscheck_1025.py` 3ab58d16 (`inputs/`, the ones of my earlier lanes) |
| python | `venv-md510` (python 3.14, multidouble 5.1.0 with `dd_logdet`) |

Source quality: the state is macm3's part c state at h 0.0625, psi-constraint 9.932e-03 (win2 calls it a normal-quality source, just under the leaps' 1e-2 bound).

The acceptance, run by the driver's dry run at 09:02 UTC (`*.txt.dry` in this folder; the driver repeats it and stops if any differs): `kc87_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 3.6129015293e-10, the state's \|F\| on this machine 3.6170124824e-10 (0.11 % apart, inside the 1 % bar), `freeze_from` 2862 steps = the record's), `--mutate=F` exit 1 (state \|F\| 3.617012e-10 against 5.419352e-10), `--mutate=steps` exit 1 (2862 against 2863), `kc95_syscheck_1025.py` exit 1 ("the record is not k_c 95 at D 22.875 (kc 87, D 22.875)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 22.875 (kc 87, D 22.875)"); the selftests of the three checks exit 0; `d18_secant.py selftest` exit 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 each.

## Cost, written before the run

| source of the estimate | number |
|---|---|
| my k_c 103 D 22.875 secant | 1388 to 1448 s per evaluation (3387 steps), 6 evaluations (stopped at a non-robust point), 8460 s, peak private 2.91 GB |
| my k_c 95 D 22.875 secant | 1066 to 1088 s per evaluation (3126 steps), 9 evaluations (tol reached), 9690 s, peak private 2.53 GB, lowest free memory 20.71 GB |
| size here | k_c 87: 2862 steps; the evaluation time fell by 0.76 for a step ratio of 0.923 (k_c 103 to 95), so I take 0.7 to 0.8 for the ratio 0.915 here |

| item | estimate | basis |
|---|---|---|
| source checks and selftests in the driver | about 15 to 30 s | the dry run: 12 s |
| each evaluation | about 700 to 1000 s, central about 800 s | 1075 s at k_c 95 times 0.7 to 0.9 |
| evaluations | about 7 (the two ends and about 5 interior points; at most 10); 9 at k_c 95 (bracket 0.02), 6 at k_c 103 (stopped early); the bracket here is 0.01 wide | the two earlier lanes |
| the refinement | about 4200 to 9500 s (1.2 to 2.6 h), central about 5600 s | the rows above; t5's ETA about 2.5 h; the driver's kill is at 28800 s |
| peak private | about 2.1 to 2.6 GB | 2.53 GB at k_c 95, 2.91 GB at k_c 103 |
| lowest free memory | about 20 GB | 20.71 GB at k_c 95 (one process alone) |
| together | start about 09:10 UTC, ends about 10:20 to 11:50 UTC (central about 10:45) | the rows above |

The sampler (`rows/secant_samples.csv`, 60 s) gives the real figures.

## Files made here

`kc87d22875s_secant_driver_1025.py` (pins, selftests, the acceptance of the state, the capped run, the hc), `diff_secant_driver_vs_kc95.txt` (its diff against the k_c 95 driver), `make_kc87d22875s_1025.py` (writes the driver, watcher, keep-awake helper, session check, `go_kc87d22875s_1025.cmd` and the publish script from the k_c 95 ones by asserted replacements), `sample_driver_secant_1025.ps1`, `prep_kc87d22875s_pins_1025.txt`, `selftest_secant_dry_1025.txt`, `in/` (macm3's state and record), and after the run `secant.jsonl`, `secant.log`, `secant_summary.txt`, `secant_driver_w.log`, `source_kc*_syscheck*.txt`, `selftest_*.txt`, `session_check_secant.txt`.

## Status

**RUNNING since 2026-11-26 09:04:24 UTC.** README first c152b76c5 (pushed 09:03:54 UTC, before the start); chain started 09:04:10 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87d22875s_1025.cmd`. The k_c 95 secant was pushed (75a10de70) and posted (#1025 comment 7187315219) first.

- **Chain** (`rows/launcher_pid.txt`: 20604): conhost --headless 20604 <- cmd 22580 <- driver launcher 24264 and driver 26304 <- `d18_secant.py` pid 21832 (one child process 8296), sampler 6800, alert-only watcher 25548, keep-awake helper 9560. BelowNormal, one thread, killed by the exact pid at 28800 s, one hc at 14400 s if it still runs.
- **Session check** (`session_check_secant.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the run** (09:04:10 to 09:04:24 UTC, 14 s): the driver's pins matched; `d18_secant.py selftest` exit 0 and its three controls exit 1, 1, 1; the selftests of the three checks exit 0; the state was accepted as ordered: `kc87_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, the k_c 95 and k_c 103 checks exit 1 (they refuse it) (`source_kc*_syscheck*.txt`). The tool printed its pin lines and "the record system" (\|F\| 3.6170124824e-10 against the record's 3.6129015293e-10, 2862 steps = the record's).
- **Machine at the start:** the other project's I114 `convergence.py` jobs run beside it, not touched.
- **ETA** (the estimates above counted from 09:04:24 UTC): about 7 evaluations at 700 to 1000 s each, so the refinement ends about 10:20 to 11:50 UTC (central about 10:45 UTC).

Pushed 2026-11-26 09:04:41 UTC.

## Result

Not yet run.
