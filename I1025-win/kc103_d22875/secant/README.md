# I1025-win/kc103_d22875/secant: Brent refinement of the k_c 103 root at D 22.875 with xfkappa's `d18_secant.py` (winb)

Written before the run, 2026-11-25 23:03:51 UTC (the time of the README-first push; later pushes keep it). Neither the scan of the folder above nor this refinement had ended when the order, the registration and the estimates below were written (the scan started 21:59:50 UTC and ends about 01:20 to 03:45 UTC on 26 Nov). Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-25, read at about 22:50 UTC, winb section, quoted)

"Coordinator (t5), #1025, queue after your D 22.875 k_c 103 scan (do not stop it): refine its root with the new secant tool. Code: branch wip/ell1-speed at 6010e37b (git fetch, new worktree), solver/matter/d18_secant.py; pin it by blob; run its selftest and the three controls (half, norobust, nosigncheck must fail) first; setup in solver/matter/SPEED_ELL1.md. Command, with LO HI = the scan's robust bracket: RAYON_NUM_THREADS=1 nice d18_secant.py run <your stub>.jsonl <your k_c 103 state>.npy 22.875 LO HI <raw>/I1025-win/kc103_d22875/secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=<stateblob>,<stubblob>, one process, BelowNormal. Register first: the refined root lies inside the scan's estimator range. Report the evaluations, the final bracket, and the time per evaluation."

My reading, and what I add:

- **The scan is not stopped.** Nothing of this refinement runs before the scan's chain (cmd 26024) has ended and its reading is reported to t5. LO and HI are the scan's robust bracket as the reader prints it (the two scan points that bracket the robust change; both are in `scan_kc103_D22875_p*.jsonl`, and the driver checks that both are noise-robust with opposite hybrid signs).
- **The command is t5's:** `d18_secant.py run STUB STATE 22.875 LO HI secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB`, one process, 1 thread (`RAYON_NUM_THREADS=1`, and `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` = 1 as `SPEED_ELL1.md`'s example), BelowNormal (`nice`'s equivalent on Windows), outside my terminal, from a headless console. No `--ends`: the tool evaluates both ends again (two evaluations that the scan already made, with its own robustness test, `dln <= 0.1`, added), and `--mm`, `--b12`, `--dln`, `--eps` stay at their defaults (fast float64 matrix, `ell_ddm`'s block 12, 0.1, 1e-15).
- **The cap is mine, because the order names none:** 54000 s (15 h) by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running; nothing is stopped at 6 h. The tool appends one record per evaluation to `secant.jsonl`, so a kill at the cap would leave the evaluations (the `root` record is written at the end only).
- Stops: exit 2 (refused: an end not robust or the ends with the same sign), exit 3 (a pin differs or the state is not the record system), exit 4 (`--maxev` or a non-robust interior point), an exception. Each is reported as printed; I do not rerun with other options and do not widen the bracket. If the reader prints more than one robust change, I refine the one the scan's registration compares (the one nearest 0.11) and report that the others were not refined; the choice of another is t5's.
- Nothing else runs beside it from me; the other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Written before the run (t5's registration)

**The refined root lies inside the scan's estimator range.** Precisely: the det-linear root inside the final bracket (`lam_lin` of the last record, kind `root`, in `secant.jsonl`) lies in [R_LO, R_HI], the estimator range the reader prints for the robust change that is refined (`read_lower_kc103_D22875.log` in the folder above, the `range [R_LO, R_HI]` on its `robust change` line). **Met** if R_LO <= `lam_lin` <= R_HI, **not met** otherwise (then the offset from the nearer end of the range is reported). R_LO and R_HI, and LO and HI, are copied from the reader's lines into the Status below before the run starts.

Information beside it, not criteria: the final bracket and its width (the tool stops at 1e-5, status `tol`); Brent's last point (`lam_brent`); whether the whole final bracket also lies inside the range; the offset of `lam_lin` from the reader's det-linear estimate; the hybrid signs and ln\|det\| at each evaluation, with the float64 sign beside it. `SPEED_ELL1.md` puts the float64 floor of the hybrid determinant's root at about 1.4e-6 at k_c 55 and at about 1.5e-7 estimated for k_c 103 (not measured); the tolerance 1e-5 lies above both. I do not interpret the result against other k_c readings; t5 rules.

What I report (t5's list): the evaluations (lambda, hybrid sign, ln\|det\|, dln, robust, float64 sign, seconds and the three parts), the final bracket, the status and exit, the time per evaluation, and the peak private memory of the process.

## The tool and its pins

| item | value |
|---|---|
| branch, commit | `wip/ell1-speed` at 6010e37b30f92688dd5c659e383c6d0c8d14b6da ("SPEED_ELL1.md: where the runs' raw output is (#1025)"), `git fetch origin wip/ell1-speed`, new detached worktree `C:/Users/nathan/Source/choptuik-i1025secant` (made 22:52 UTC from the `choptuik-i1025k79` repository; none of my other worktrees is touched) |
| `solver/matter/d18_secant.py` | committed blob a3d90cd5ab9986f4670bdd81e3e2e3f3678bfe49 (`git hash-object` with the filters; the CRLF bytes on this disk hash to e10ef97eda1853f1fe37fe857d2334a17820218a); the driver checks the committed blob |
| `ell_fastm.py` | 93f963f6102f48e35c56c9eace25e1afd03b6ea2 (imported for the float64 matrix and `load_system`) |
| `ell_ddm.py`, `dss_ell.py`, `ell_dd.py`, `ddnp.py` | 86578feeab868691778019b79771aef727510a76, 5d28c19e17efa6b0103cb81d650891706605532d, 7e58fcbc2288eca8f8f1ebfc36f7250a328b0c4e, 9b1fb195d0fa95d5dd7abd1083ac9b36fef04869: the same blobs as in my regrid worktree `choptuik-i1025k79` at 48c36355 (compared one by one), so the runners' pins of those files hold, as `SPEED_ELL1.md` says |
| state | `sol_l1kc103win22875_D22.8750.npy`, blob 280515313e580cccbf14a6e0828e4eaa9b22086d (`git hash-object --no-filters`; my accepted k_c 103 state, the scan's) |
| stub (the record) | `l1kc103win22875.jsonl`, blob f623d3e67b94a5ac4e38e2c55d05d3bf247e4c71 (one row: k_c 103, D 22.875, \|F\| 3.4634221167e-10, 3387 steps) |
| python | `venv-md510` (python 3.14, multidouble 5.1.0 with `dd_logdet`, as the scan) |
| `--pin` | `280515313e580cccbf14a6e0828e4eaa9b22086d,f623d3e67b94a5ac4e38e2c55d05d3bf247e4c71` (the tool compares by prefix; I pass the full blobs) |

## Checks run by hand before writing this (`prep_secant_selftests_by_hand.txt`, 22:52 to 23:01 UTC, one thread, the scan running beside them)

| check | exit | wanted |
|---|---|---|
| `d18_secant.py selftest` (planted cases C1 to C4) | 0 (PASS) | 0 |
| `d18_secant.py selftest --mutate=half` | 1 (C1 and C2 not as written) | 1 |
| `d18_secant.py selftest --mutate=norobust` | 1 (C2 and C4 not as written) | 1 |
| `d18_secant.py selftest --mutate=nosigncheck` | 1 (C3 not as written) | 1 |
| `ell_fastm.py selftest` (the toy state; fast matrix against the complex step, every block, three bases) | 0 (PASS; 204 s) | 0 |
| `ell_fastm.py selftest --mutate=nolam` | 1 (201 s) | 1 |

`ell_fastdd.py` is not run: the run keeps `--b12=ddm` (`ell_ddm`'s block 12) and does not import it. The driver repeats the four `d18_secant.py` rows and stops if any differs. The driver's dry run on stand-in scan files (`selftest_secant_dry_1025.txt`): it reaches "would start" for a bracket with opposite robust signs, and refuses a bracket with equal signs, a missing end, a non-robust end, another state's records, LO >= HI, a non-number and `--scandir` without `--dry`.

## Cost, written before the run

`SPEED_ELL1.md` gives, on the Mac (Apple M5, one process, load 11 to 62 on 10 cores), 15 to 25 min per evaluation at k_c 103 (float64 matrix 0.6 to 2.4 min, `ell_ddm`'s block 12 12 to 19 min, the three `dd_logdet` under 0.5 min) and about 6 evaluations (the ends included) from a 0.01 bracket to under 1e-6. My machine runs slower than the Mac's old-code figure: my scan points at k_c 103 (`d18_hybsign.py`, four processes at once) took 5955 to 6034 s at D 22.0, against the Mac's 959 + 749 s for the old float64 matrix and block 12 in one process (about 3.5 times). One process alone here has no contention from three siblings, so I take 2000 to 5000 s per evaluation (central about 3200 s; the new float64 matrix 150 to 500 s, block 12 1800 to 4500 s, the `dd_logdet` calls 30 to 100 s).

| item | estimate | basis |
|---|---|---|
| source checks and selftests in the driver | about 10 to 30 s | the by-hand run: the four `d18_secant.py` selftests 4 s |
| each evaluation | about 2000 to 5000 s, central about 3200 s | the Mac's 15 to 25 min times 2 to 3.5; the records' `sec_parts` give the real split |
| evaluations | about 7 (the two ends and about 5 interior points: the bracket is 0.02 wide, twice the Mac's); at most 10 (`--maxev=10`, the ends included) | `SPEED_ELL1.md`: 6 from 0.01 |
| the refinement | about 12000 to 50000 s (3.3 to 14 h), central about 22000 s (6 h) | the rows above; the cap is 54000 s |
| peak private | no figure for this tool at k_c 103; I expect 2.5 to 6 GB (the scan's worker had 3.96 GB; the fast matrix keeps (block x block) stage matrices) | not measured |
| lowest free memory | not written; the machine has about 22 GB free when nothing else runs | one process; the scan's four had 13.7 GB left |

The sampler (`rows/secant_samples.csv`, 60 s) gives the real figures.

## Files made here

`kc103d22875_secant_driver_1025.py` (pins, selftests and controls, bracket check, the capped run, the hc), `sample_driver_secant_1025.ps1` (the sampler of the other stages with the stage name `secant`), `go_secant_kc103d22875_1025.cmd` (written when LO and HI are known; started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_secant_kc103d22875_1025.cmd`), `prep_secant_selftests_by_hand.txt`, `selftest_secant_dry_1025.txt`, and this folder's `secant.jsonl`, `secant.log`, `secant_summary.txt` after the run. The watcher (`kc103d22875_watch_alert_1025.py`) and the keep-awake helper (`keepawake_1025.py`) are the scan's, unchanged.

## Status

The D 22.875 scan ended 2026-11-26 03:46:50 UTC (20821 s, exits 0, 0, 0, 0; its Result is in the README above). The reader's lines as printed (`read_lower_kc103_D22875.log`):

```
points 9 in 0.040-0.200; not noise-robust: none
hybrid signs: 0.040- 0.060- 0.080- 0.100- 0.120+ 0.140+ 0.160+ 0.180+ 0.200+
float64 sign differs from the hybrid sign at: none
repeated points: [(0.1, 'agree')]
  robust change (0.100, 0.120), - to +, det-linear 0.119801, range [0.103345, 0.119801]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.040, + at 0.200
read_lower exit 0
```

One robust change, so no choice among several arose. t5's ruling on the scan (hc read about 03:47 UTC, quoted): "k_c 103 at D 22.875, lambda_1 (F) by position in (0.100, 0.120), det-linear 0.119801; registered 0.10-0.13 MET; no second root in 0.04-0.20 ... Go ahead with the queued secant refinement on that bracket (0.100, 0.120)."

**Filled in before the start: LO = 0.100, HI = 0.120, R_LO = 0.103345, R_HI = 0.119801.** The registration above reads: the refined `lam_lin` lies in [0.103345, 0.119801]. Note that the reader's det-linear estimate 0.119801 is the upper end of its own range.

Pushed 2026-11-26 03:49:42 UTC.

## Result

Not yet run.
