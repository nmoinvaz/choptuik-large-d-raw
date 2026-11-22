# I1025-win2/kc71_leap: carry lambda_1 on to D 20 at k_c 71: the k_c 71 leap from D 18.5 to D 20 (ell_leap.py) and hybrid scans at D 19, 19.5 and 20

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session, beside win2b's jobs (its `kc_break` scans: four processes, 16 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-22 (~03:00 UTC), after
`../kc71_d185/` (post 7073281788): lambda_1 at D 18.5 is 1.675995 at k_c 71 against 1.677016 at k_c 63, so lambda_1's branch is k_c-converged through D 18.5 (the other roots move with k_c). Carry lambda_1 on to D 20 at k_c 71.
(1) Leap the accepted k_c 71 D 18.5 state to D 20 with `ell_leap.py` and winb's flags (header of raw `I1025-win/leap_kc63.log`; quoted below), h 0.0625, seeded with the D 18.5 state and a second state made the same way at D 18.4375 (the k_c 63 leap state there regridded to k_c 71 as at D 18.5);
save every state, 4 threads, BelowNormal, 12 h cap; report the fold watch and the psi-constraint (cap 1e-2; 1.9e-3 at D 18.5 at k_c 63). (2) Then at D 19, 19.5 and 20: a hybrid scan of lambda 1.40 to 1.80 at 0.01 around the extrapolated path (slope about -0.26 per unit D).
Post on #1025 after the leap and after each D.

## The commands (written 2026-11-22 03:06 UTC, before any run)

**winb's leap flags, quoted from the header of `I1025-win/leap_kc63.log`:**

```
== 2026-11-20 04:27:23 -u ell_leap.py l1kc63W1025 1 63 data/sol_l1kc63Fw1025_D17.0000.npy 17 data/sol_l1kc63Fw1025_D17.5000.npy 17.5 18 0.125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold   (D_end 18 in place of the script's 20 and 4 BLAS threads in place of 2, the coordinator's orders; ...)
```

So the flags are `--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold` (kappa 0.7, u0 0.04, Ks 30 are `ell_leap.py`'s defaults, the records' values). `ell_leap.py` (blob in `exits_kcl.txt`): the predictor is the secant through the two previous states; each state is solved as `ell_refine.py` solves it; with `--fold` a failed solve (|F| above `--fmax` or the constraint above `--cmax`)
halves h and retries (down to `--hmin 0.015625`), a fall of the smallest regular singular value of J by more than half or a doubling of |J+ dF/dn| over a step halves h for the next step (the fold watch), and every state is saved (`sol_{tag}_D{D:.6f}.npy`, also the `.4f` name at multiples of 0.5). It stops when the solve fails at `--hmin`.

**Step 1a, the second seed (D 18.4375 at k_c 71), the way the D 18.5 state was made** (`../kc71_d185/`, the command the coordinator confirmed): from the k_c 63 leap state `I1025-mac/d18/sol_l1kc63Wm1025_D18.437500.npy` (blob 16a17e5f, copied as the `.4f` name `ell_refine.py` reads; k_c 63 record: |F| 2.7871e-10, 2471 steps, constraint 1.778e-3):

```
python.exe -u ell_refine.py l1kc63Wm1025 63 l1kc71Wm1025 71 1 18.4375 2.1184454184 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

(lambda_0(18.4375) = 2.1184454184, unused with `--no-gamma`.) Accepted only by `kc71_syscheck.py`, as the D 18.5 state was: the record's |F| <= 1e-9 (the class: 2.8314e-10 at k_c 71 D 18.5) and the saved state reproducing its record (the step count from `freeze_from` equal to the record's and |F| within 1%), with the two built-in controls; if it does not converge or is not accepted the task stops with a report and no leap starts.

**Step 1b, the leap:**

```
python.exe -u ell_leap.py l1kc71Lw1025 1 71 data/sol_l1kc71Wm1025_D18.4375.npy 18.4375 data/sol_l1kc71Wm1025_D18.5000.npy 18.5 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
```

(D 20 as the script's own end, h 0.0625 as ordered; the seeds are the D 18.4375 state just made and the accepted D 18.5 state `../kc71_d185/sol_l1kc71Wm1025_D18.5000.npy`, blob 28bf6bac, |F| 2.8314e-10, 2772 steps, constraint 9.994e-4.)
Both steps: cwd `D:/choptuik-i1025k71/solver/matter` (the worktree at 48c36355 made for `../kc71_d185/`: `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` blob 631e5801, `ell_delta.py` equals 48c36355's, checked by the driver), venv-md510 (multidouble 5.1.0), 4 BLAS threads,
BelowNormal, caps: the regrid 21600 s, the leap **43200 s (12 h)** by the exact root pid (`taskkill /T /F /PID` after the command line is checked). A leap that stops (the solve fails at `--hmin`) or is capped is reported as it is; no retry. D 19, 19.5 and 20 lie on the leap's grid (18.5 + 0.0625 k, also after halvings).
Every state and the record `data/l1kc71Lw1025.jsonl` are copied into `states/` by a copier loop (every 120 s, files at least 30 s old); `leap.log` is the leap's output.

**What is reported for the leap** (`leap_report.py`, from the leap's records): per point D, h, |F|, |F| at the secant start, steps, the **psi-constraint** (cap 1e-2; the k_c 63 record is 1.912e-3 at D 18.5, the k_c 71 record 9.994e-4), seconds, and the **fold watch**: the smallest regular singular value of J (`sv_reg_small[0]`), the tangent's size |J+ dF/dn| (`tan_norm`, which diverges at a fold),
the smallest singular value of the bordered matrix (`sv_B_min`), the fold candidate's |cos| and sv_fold, `n_null`; the events (h halvings by the fold watch or by failures, the stop or "reached D 20"); the extremes; the k_c 63 records at D 18.4375 and 18.5 beside.

## The scans (written before the run)

At **D 19, 19.5 and 20**, on the leap's saved state and its record line (copied here), xfkappa's `d18_hybsign.py` (blob e089207a, as in `../d18mid/`, `../d185map/`, `../kc71_d185/`), the noise test and the float64 sign, **lambda 1.40 to 1.80 at 0.01 (41 points)**, `P4_WT_MATTER=D:/choptuik-i1025k71/solver/matter`, venv-md510, BelowNormal.
Not specified in the order, set as in `../kc71_d185/`: **four processes** (4 threads each, caps 28800 s by the exact root pid), the points in four consecutive blocks (P1 1.40 to 1.50: 11 points, P2 1.51 to 1.60, P3 1.61 to 1.70, P4 1.71 to 1.80: 10 each), the pairs (P1, P2) and (P3, P4) each repeating one point
(1.50 and 1.70, the last of the first block of the pair, evaluated first in both: 11, 11, 10 and 11 evaluations); the pair gate compares them at the first points (same sign, ln|det| within 1e-6; a disagreement kills the four scans by exact pid and stops). Each process runs the scanner's own record-system check first (exit 3 stops it).
The scans run when the state exists (concurrently with the later leap steps), one D after another so that the scans do not overlap (`kcl_scan.sh D LO HI PATH [WAIT_FILE]`).

**The extrapolated path (fixed before the run): p(D) = 1.675995 + s (D - 18.5) with s = -0.26 per unit D** (lambda_1 = 1.675995 at k_c 71, D 18.5; the slope about -0.26 of the order): **p(19) = 1.545995, p(19.5) = 1.415995, p(20) = 1.285995.**

**Reading (the coordinator's, fixed before the run; definitions of `kc71_leap_read.py`):** the robust minus-to-plus root (xfkappa's reader, `d18d_read.py` 6b608903 pinned; both grid points noise-robust) nearest the extrapolated path is lambda_1 at that D; **its delta against lambda_0(D) is reported** (lambda_0 = 2.1156378446 at D 19, 2.1132623525 at 19.5, 2.1110019498 at 20; `ell_delta.lam0_at`, errors 4e-8 to 6e-7).
**A missing root, or two within 0.03, is reported, not read:** there is no minus-to-plus robust root in the window; or two or more minus-to-plus robust roots are within 0.03 of the path; or a robust root (either orientation) is within 0.03 of the nearest minus-to-plus root (a near-tangent pair). Then every root is listed and no lambda_1 is read. The root's distance from the path is reported, with no bar on it.
Orientation labels are each scan's own det-sign convention (the sign convention across states is xfkappa's check); every robust root of either orientation is listed.

**An open point, named before the run, answered by the coordinator (see "Window changes" below): the window 1.40 to 1.80 does not contain the extrapolated path at the later D.** With slope -0.26, p(19.5) = 1.416 is 0.016 above the window's lower edge 1.40 and **p(20) = 1.286 is 0.114 below it**. D 19 (p = 1.546, inside) is as ordered; the D 19.5 and D 20 windows follow the rule below.

## Controls

`kc71_syscheck.py --selftest` and its two built-in controls (|F| x 1.5 and steps + 1 must be refused) for the D 18.4375 state; `kc71_leap_read.py --selftest` (planted root lists: a clear root, two minus-to-plus roots within 0.03 of the path, none, a near-tangent pair, a far root, a second root beyond 0.03) and `--selftest --break` (exit 1); `pair_check2.py --selftest` and `--break`;
`next_window.py --selftest` (the planted windows 1.22 to 1.62 at D 19.5 and 1.11 to 1.51 at D 20); `kcl_ext.py selftest` and `--break` (the extension lists), and the edge rule in `kc71_leap_read.py --selftest` (a root 0.03 above the edge is an edge case, 0.031 is not; run on a planted D 19.5 scan with a root at 1.2435 it prints `EDGE LOW`); the reader's pinned copies; `leap_report.py` was run on planted leap records before the launch; each scan process's record-system check. The leap's own checks are its |F| bar (`--fmax`) and the constraint bar (`--cmax`) at every point.

## Window changes: the coordinator's rule (hc, noted here at 03:10 UTC 22 Nov, after the launch at 03:07:17 UTC; nothing had been scanned)

The coordinator: yes, the 1.40 to 1.80 window was wrong for D 19.5 and D 20 (thanks for catching it). **The rule from now on:**

- **D 19 runs as ordered** (1.40 to 1.80, path 1.545995).
- **At D 19.5 and D 20: a 0.40-wide window at 0.01 (41 points), centered on the path extrapolated from the last two measured lambda_1 of my own k_c, rounded to 0.01:** for D 19.5 from lambda_1(18.5) = 1.675995 and lambda_1(19); for D 20 from lambda_1(19) and lambda_1(19.5). Implemented in `next_window.py`:
  p(D) = lambda_b + (lambda_b - lambda_a) / (D_b - D_a) (D - D_b), window [round(p, 2) - 0.20, round(p, 2) + 0.20]; the path the reading uses is p itself (not rounded); the lambda_1 used are the det-linear estimates of the readings (the last reading of that D, none with an unresolved EDGE line).
  The slope -0.26 of the order is no longer used for these two D (it was the order's estimate; it stays in the pre-run post).
- **If the root read sits within 0.03 of a window edge, extend that side by 0.10 before reading it** (`kcl_ext.sh D SIDE K PATH`; `kc71_leap_read.py` prints `EDGE LOW` or `EDGE HIGH` and "NOT READ YET" in that case). An extension re-evaluates the edge point (a repeat, first in both processes) and adds 10 points (X1: 6 evaluations, X2: 6), 4 threads each;
  the reader's repeat rule compares the repeats with the original scan; after it the root is read again, and the rule applies again to the new edge (if the root is still within 0.03 of an edge, another extension; I would report after three). The rule is applied at D 19 too if a root read there sits within 0.03 of 1.40 or 1.80 (not expected: p(19) = 1.546); if that happens I report it first.
- **Each window is posted before its scan starts** (the D 19.5 and D 20 windows, and each extension).

So the D 19.5 and D 20 scans start only after the previous D has been read (`next_window.py 19.5`, `next_window.py 20`), by hand, with the window posted first; the D 19 waiter (`kcl_scan.sh 19 1.40 1.80 1.545995`) is already armed.

## Takeover and the second leg (the coordinator's hc, 2026-11-22 ~06:40 UTC)

The runner that started this task hit its usage limit at about 03:10 UTC. A new session on win2 took it over at 06:20 UTC and changed nothing in the running leap, its driver (`run_leap.sh`, root pid 6756, leap root pid 35992, python 23496), its copier, its watchers or the armed D 19 waiter (`kcl_scan.sh 19 1.40 1.80 1.545995`, pid 12280). State at 06:34 UTC: 2 of 24 points done (D 18.5625: 3512 s, |F| 2.82e-10, psi-constraint 1.063e-3, 2759 steps; D 18.625: 4530 s, 2.81e-10, 1.130e-3, 2748 steps), no fold watch or h halving event, the third point running since about 06:04 UTC. Both saved states reproduce their records under `kc71_syscheck.py` (ACCEPTED, checked 06:33 UTC).

**The coordinator's order for the end of the first leg:** the order on #1025 is D 20. When the first leg's 12 h cap (03:50:08 + 12 h = 15:50:08 UTC) ends the run (or it stops for another reason before D 20), start a new run from its last two saved states whose records reproduce, with the same flags (winb's, `--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`), h as the run left it, to D_end 20, a new 12 h cap, 4 threads, BelowNormal. **The command is posted on #1025 before it starts.** The D 19 scan runs as armed, and its window is posted before it starts.

Tools written for it (new files, none of the running ones touched; each was tested before the cap):

- `leg2_pick.py`: from the newest record back, takes a state when `kc71_syscheck.py` accepts it (the record's |F| within the class bar, the state's |F| within 1% of the record's, `freeze_from`'s step count equal to the record's, with the checker's two controls); the first two accepted are the seeds. h is the last `h -> X` of `leap.log` (0.0625 when none). Prints `DA DB H`. Controls: `--mutate=F` makes every state refused (exit 1; seen), a planted log with `h -> 0.03125` then `h -> 0.015625` gives 0.015625 and one without gives 0.0625 (seen), `--n 3` with two states exits 1 (seen).
- `run_leap2.sh DA DB H` (`DRY=1` prints the command after the pin checks): pins `ell_leap.py` 1eb873e4, the worktree 48c36355 with solver code = 505d8399, the two seed states equal to their `states/` copies, no earlier `l1kc71Lw1025b` record; runs `ell_leap.py l1kc71Lw1025b 1 71 data/sol_l1kc71Lw1025_D<DA>.npy DA data/sol_l1kc71Lw1025_D<DB>.npy DB 20 H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold` with the cap 43200 s by the exact root pid (command line checked), a copier into `states/`, output `leap2.log`, driver lines `exits_kcl2.txt` and `summary_kcl2.txt`, end markers `leap2.finished` and `all2.done`. Launched by `launch_leap2.ps1 DA DB H` (BelowNormal). A dry run on the first leg's two states (06:34 UTC) printed the command and passed the pins; a dry run with a missing state exited 2 (refused). The first line of `exits_kcl2.txt` is that dry run.
- `kcl_scan2.sh`: `kcl_scan.sh` with `TAGL` and `LEAPFIN` taken from the environment (the only two changed lines), for the scans of states the second leg makes (`TAGL=l1kc71Lw1025b LEAPFIN=leap2.finished`). The armed D 19 waiter, `kcl_scan.sh`, gives up at `leap.finished` when D 19 is not there; if the first leg is capped before D 19, the D 19 scan is armed again with `kcl_scan2.sh` on the second leg's states.

The D 19 window is as written above and in the pre-run post: lambda 1.40 to 1.80 at 0.01 (41 points), path 1.545995, four processes (P1 1.40 to 1.50, P2 1.51 to 1.60 with 1.50 repeated first in both of the pair, P3 1.61 to 1.70, P4 1.71 to 1.80 with 1.70 repeated first), 4 threads each, BelowNormal. D 19.5 and D 20 follow the coordinator's rule above.

## Result

Not yet run.

## Processes outside the terminal (the coordinator's hc, 2026-11-22 ~08:00 UTC)

The terminal of the old runner was ended at 07:17 UTC and took its driver tree with it (see above). Every helper of this task is now started outside the terminal that holds the session, by `cim_start.ps1` (`Win32_Process.Create` of `cmd.exe /c NAME.cmd`; the `.cmd` starts bash at BelowNormal with `start /wait /belownormal /b`, so the chain reads bash <- cmd.exe <- WmiPrvSE.exe <- svchost.exe <- services.exe <- wininit.exe and never touches claude.exe). `chain.ps1 PID...` prints the ParentProcessId chains. `cim_probe.sh` (run through it at 08:09 UTC) showed that the tree has git, gh, python, tasklist, taskkill, powershell, the md510 venv and BelowNormal, and that its chain does not contain claude.exe.

At 08:10 UTC the helpers started from the terminal at 07:45 (`relaunch_leg1.ps1`) were replaced by the same four started with `cim_start.ps1`: `leg1_guard.sh` (copier, 12 h cap at 15:50:08 UTC by exact pid, end markers), the D 19 waiter (`kcl_scan.sh 19 1.40 1.80 1.545995`), `mem_watch.ps1` and `commit_watch.ps1`. The replacement first left the old guard and old waiter running (their script processes have a different parent than the `bash -c` stubs that the kill followed); both were killed by exact pid after their command lines and start times (07:45:20 UTC) were checked, so only one guard and one waiter remain. Leg 2 starts the same way: `launch_leap2.ps1 DA DB H`, and its scan waiters with `cim_start.ps1 -Name <n> -Bash 'TAGL=l1kc71Lw1025b LEAPFIN=leap2.finished bash kcl_scan2.sh D LO HI PATH'`.

## Restart 1 of the leap (the coordinator's ruling (b), 2026-11-22 ~09:00 UTC)

At D 18.75 the fold watch fired for the first time and halved h to 0.03125 (posted, comment 7076839449): n_null fell from 65 to 64, the new smallest regular singular value 1.217e-11 sits 1.10 times above the cutoff 1.103e-11 (1e-12 sigma_max), the three older regular values continue smoothly (+8 to 9%), tan_norm rose from 0.3 to 1.26 because J+ now divides by the new value, and dDelta/dD is smooth (0.02328, 0.02336, 0.02344). The coordinator's reading: a near-null value crossing the cutoff upward, not a fold (a fold drives a regular value toward zero); order: stop the leap and restart it from the D 18.6875 and D 18.75 states at h 0.0625 with the same flags, the guard retargeted to the new pid with the same cap.

- 09:01:36 UTC old guard 34420 stopped (first, so that it does not read the leap's death as the end); 09:01:38 old leap 35992 (child 23496) stopped by exact pid after the command-line check; the abandoned point (D 18.78125 at h 0.03125, started 08:56:20) cost 5 min 18 s.
- 09:01:43 `leap_r1.sh` (through `cim_start.ps1`): pins (ell_leap.py 1eb873e4, worktree 48c36355, solver code 505d8399, both seeds equal to their states/ copies and accepted by `kc71_syscheck.py`, blobs a007c106 and 6f5c373e), then `ell_leap.py l1kc71Lw1025 1 71 data/sol_l1kc71Lw1025_D18.687500.npy 18.6875 data/sol_l1kc71Lw1025_D18.750000.npy 18.75 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`, appended to `leap.log` (header line `RESTART 1`), root pid 42624 (worker 24500) in `leap_root_r1.pid`. Same tag: the records of the first four points and the new ones share `data/l1kc71Lw1025.jsonl`.
- 09:02:04 `leg1_guard2.sh` (`GROOT=42624`, cap 15:50:08 UTC, copier, end markers; `leg1_guard.sh` plus the `GDRY=1` dry run): dry run on pid 42624 passes; planted tests (a dummy with `ell_leap.py` in its command line is killed at a past cap, one without is spared, a missing pid is reported) pass. Guard script pid 23772.
- `foldsig.py` implements the coordinator's same-signature rule for a second restart (n_null down by exactly one, the new regular value within 2 times the cutoff, dDelta/dD within 1% of the step before); it reads SAME SIGNATURE on the D 18.75 record, its planted cases read NOT, `--selftest --break` exits 1 (`selftest_records.jsonl` holds the four records it uses). At most one more restart; any other signature or a third firing: h stays as the watch sets it, report.
