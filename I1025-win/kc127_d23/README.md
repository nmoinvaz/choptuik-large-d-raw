# I1025-win/kc127_d23: k_c 127 at D 23.0, regridded from macm3's accepted k_c 119 state, then the new scanner and the secant refinement of lambda_1's root (winb)

Written before the run, 2026-11-26 10:47:19 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan nor the refinement had been run for this folder when the order, the registration and the estimates below were written. Run beforehand, read-only: the source checks by hand (about 2 min), the dry run of the regrid driver (pins, three selftests, lambda_0). Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc, stamped 2026-11-26 10:40 UTC; winb section, quoted)

"Next lane, the sixth resolution: k_c 127 at D 23.0, from macm3's k_c 119 state there, to test whether the k_c steps keep shrinking (D 23.0 roots: steps +0.034112, +0.017798, +0.009058, +0.005497, ratios 0.52, 0.51, 0.61).
- Inputs, pinned by blob: raw I1025-macm3/kc119_d23/in/sol_l1kc119macm3d23_D23.0000.npy (2771cf87) and l1kc119macm3d23.jsonl (158e3086). The acceptance check is raw I1025-mac/checks/kc127_syscheck_1025.py at raw d1baa986c (blob 898ebefa). It is the kc111 check with 111 changed to 127, plus one header line.
- Folder: raw I1025-win/kc127_d23/. Write the README registration first.
- Step 1, source: kc119_syscheck_1025.py (fc6e0dd6) exits 0 on it, its --mutate=F and --mutate=steps exit 1, and the kc111 and kc127 checks refuse it.
- Step 2, regrid with your k_c 103 regrid driver, below normal, killed at 43200 s: ell_refine.py l1kc119macm3d23 119 l1kc127wind23 127 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
- Step 3: the kc127 check exits 0 on the result, both controls exit 1, and the kc119 check refuses. Report the steps ratio, |F|, constraint and Delta beside the source's.
- Step 4: scan with the NEW scanner, d18_secant.py scan at wip/ell1-speed 92b9bf53 (blob eb1396ad; selftest 0 and its three mutations 1, logged first), lambda 0.03, 0.04, 0.05, 0.06 plus a repeat of 0.04, at most 2 processes (a k_c 127 process may need 8 GB). Then d18_secant.py run (92b9bf53) --tol=1e-5 --maxev=10 on the robust bracket, one process.
- Stop and report on: not accepted, an exception (an array limit at k_c 127 included), no robust change or more than one, or any step over 12 h.
- My registered prediction: the root at D 23.0 is +0.0444 +- 0.003 (the last step times about 0.6). The regrid should take 3-5 h on your machine.
- Post on #1025 at each step's end."

The k_c 87 D 22.875 secant is pushed (`I1025-win/kc87_d22875_secant` at 557ea8ee3) and posted (#1025 comment 7189716601).

My reading, and what I add:

- **Step 2, the regrid recipe is my k_c 103 one:** one process, 4 BLAS threads, BelowNormal, outside my terminal, from a headless console, in the worktree `choptuik-i1025k79` at 48c36355 (`ell_refine.py` committed blob 631e5801, `ell_delta.py` fde699f5: the code macm3's k_c 119 regrid used). Cap 43200 s (12 h) by the exact pid, one hc to t5 at 21600 s if it still runs. Acceptance (steps 1 and 3) is by the driver: the source through five checks, the result through the k_c 127 check with its selftest and both controls, and the k_c 119 check refusing it (the k_c 111 check is added in step 1 as ordered, not in step 3).
- **Step 4, the new scanner:** `d18_secant.py scan STUB STATE 23.0 LAMS OUT.jsonl --pin=STATEBLOB,STUBBLOB` from the worktree `choptuik-i1025secant92` (detached at 92b9bf53, made for this lane; `d18_secant.py` committed blob eb1396ad, the CRLF bytes on this disk hash to 948a5f2d; the other solver files are the blobs of my earlier worktrees). Before the scan the driver logs `d18_secant.py selftest` (exit 0 wanted) and `--mutate=half`, `norobust`, `nosigncheck` (exit 1 wanted each). Two processes, one thread each (`RAYON_NUM_THREADS`, `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` = 1), BelowNormal, 5 evaluations in 3 rounds: process 0 runs 0.04, 0.03, 0.06 and process 1 runs 0.05, 0.04 (the repeat of 0.04 on the other process); the reader `read_lower.py` (89309d3c) then reads the files (window 0.03 to 0.06). Cap 43200 s. The older `d18_hybsign.py` is not used for this scan. My scan files are `scan_kc127_D23_p0.jsonl` and `_p1.jsonl` (the new scanner writes d18_hybsign's fields plus its own).
- **Step 4, the secant:** `d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=...` from the same worktree (92b9bf53, `d18_secant.py` eb1396ad), one process, 1 thread, BelowNormal, cap 43200 s, started by me on the robust bracket the reader prints, only if the reader prints exactly one robust change. Not chained by the scan driver: I read the reader's lines first (t5's stop on none or more than one) and launch it within minutes.
- **Stops** (t5's): a source or result not accepted, an exception (an array limit at k_c 127 included), no robust change or more than one robust change in the scan, any step over 12 h (the drivers kill by the exact pid at 43200 s and report). Also as before: a refinement that ends at exit 4 with a non-robust interior point is reported as printed (t5 rules); no rerun with other options; no widening. Nothing is killed on memory (alert-only watchers).
- **Posts on #1025** at the end of each step: after the regrid with its acceptance (steps 1 to 3, the source result in the same post), after the scan, after the refinement.
- Nothing else of mine runs beside it; the other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Written before the run (t5's registration, and my estimates)

**PREDICTION (t5's): the root of lambda_1 at k_c 127 and D 23.0 is +0.0444 +- 0.003** (the k_c 111 to 119 step +0.005497 times about 0.6 added to macm3's k_c 119 root; the steps at D 23.0 so far +0.034112, +0.017798, +0.009058, +0.005497, ratios 0.52, 0.51, 0.61). By position: the det-linear root inside the final bracket of the refinement (`lam_lin` of the last record, kind `root`, in `secant/secant.jsonl`) lies in [0.0414, 0.0474]. **Met** if so, **not met** otherwise (then the offset from the nearer end is reported). If the refinement ends at a non-robust interior point (exit 4) the same `lam_lin` of the valid bracket is compared, and the bracket is reported as printed. If there is no refinement (a stop in steps 1 to 4), nothing is compared.

For the scan (steps registered by the order, not by me): exactly one robust change in 0.03 to 0.06 is expected (a stop otherwise); the reader prints its bracket, orientation, det-linear estimate and range as it comes; the expected bracket is (0.04, 0.05) by the registered root, and a bracket (0.03, 0.04) or (0.05, 0.06) is reported as printed. Position and orientation are reported as printed and not interpreted by me (t5: printed orientation is not compared across k_c); t5 rules.

For reference (not predictions of mine): macm3's k_c 119 at D 23.0, scan 06:30 to 07:21 UTC on 26 Nov and secant 07:21 to 08:18 UTC (`I1025-macm3/kc119_d23`, his `point_summary.txt`): root +0.04106 (his README: "t5's register (the root +0.040 +- 0.003) MET (+0.04106...)"), bracket (0.040, 0.060) by his scan; his regrid 2273 s (record) on 6 threads, steps 3914 (k_c 111 source 3653, ratio 1.071), |F| 3.2080e-10, psi-constraint 2.1389e-03 (source 3.4835e-03), Delta 1.174324968657 (source 1.174326550481); his steps ratios at D 23.0: 1.0838 (k_c 95 to 103), 1.0779 (103 to 111), 1.071 (111 to 119); peak RSS 5.64 GiB for the k_c 119 regrid and about 7 GiB per k_c 119 scan process (t5: "a k_c 127 process may need 8 GB").

## The source (macm3's)

| item | value |
|---|---|
| raw folder | `I1025-macm3/kc119_d23` (origin/main 182c001b8 at my fetch) |
| state | `in/sol_l1kc119macm3d23_D23.0000.npy`, blob 2771cf87ee8ca5c9ac32d5289397eace6bc1924b (62328 bytes; his regrid from dh170's k_c 111 state `I1025-dh170/kc111_d23`, accepted 2026-11-26 06:30:46 UTC) |
| record | `in/l1kc119macm3d23.jsonl`, blob 158e30868886465e4226a45de8975a5693852049 (370 bytes, one row: k_c 119, D 23.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.2079513797870025e-10, F_start 1.2512516402778284e-05, steps 3914, constraint 2.13890547520122e-03, Delta 1.1743249686574218, 2273 s, src `l1kc111dh170j`) |
| the checks | `kc111_syscheck_1025.py` 85aeb31275aa9fd3edb786c74d91e69390a1dc75 (macm3's copy in `kc119_d23/in`), `kc119_syscheck_1025.py` fc6e0dd6fbdf6bcf8fb6a2bf9274e404e3caa7ad (raw `I1025-mac/checks`, the k_c 111 check with 111 -> 119 and a header line), `kc127_syscheck_1025.py` 898ebefa65a99e639110e018808c85506a7f5719 (raw `I1025-mac/checks` at d1baa986c, the k_c 111 check with 111 -> 127 and a header line: compared line by line, three lines and the header differ) |
| reader | `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f (the scan files are read by the folder, three-decimal keys); `d18_hybsign.py` e089207a is only a dependency of the reader's folder, not run |
| code, regrid | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` fde699f5, `ell_refine.py` committed blob 631e5801), the one of my k_c 103 regrids |
| code, scan and secant | the worktree `choptuik-i1025secant92` at 92b9bf533ff371247be642c47e067a9042cabed1 (branch `wip/ell1-speed`): `d18_secant.py` committed blob eb1396ad39d9236ae983064da5702164947e0948, `ell_fastm.py` 93f963f6, `ell_ddm.py`, `dss_ell.py`, `ell_dd.py`, `ddnp.py` the same blobs as in my regrid worktree |
| lambda_0 | 2.0992182200 (`ell_delta.lam0_at(23.0, *ell_delta.lam0_table())[0]` in the regrid worktree, equal to macm3's regrid command and to t5's; unused with `--no-gamma`; the driver checks it) |
| python | `venv-md510` (python 3.14, multidouble 5.1.0 with `dd_logdet`) |

The copies are in `inputs/`; the source state and record are also in the regrid worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc127d23_pins_1025.txt` and checked by the driver. Nothing of macm3's is modified.

The source checks, run by hand at 10:44 UTC before writing this (read-only, `REC STATE 23.0 WTM` with absolute paths, 2 threads; `prep_source_checks_by_hand.txt`): `kc119_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 3.2079513798e-10, the state's \|F\| on this machine 3.2218487937e-10 (0.43 % apart, inside the 1 % bar), `freeze_from` 3914 steps = the record's), `--mutate=F` exit 1 (state \|F\| 3.221849e-10 against 4.811927e-10), `--mutate=steps` exit 1 (3914 against 3915), `kc111_syscheck_1025.py` exit 1 ("the record is not k_c 111 at D 23 (kc 119, D 23.0)"), `kc127_syscheck_1025.py` exit 1 ("the record is not k_c 127 at D 23 (kc 119, D 23.0)"); the selftests of the three checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Steps 1 to 3, the regrid driver** (`kc127d23_regrid_driver_1025.py`, a copy of my k_c 103 D 22.875 one with the pins, tags, D, source, lambda_0 and checks changed, `diff_regrid_driver_vs_kc103.txt`): the pins; the selftests of the three checks and the lambda_0 check; the source through the five checks above (step 1); then
   `ell_refine.py l1kc119macm3d23 119 l1kc127wind23 127 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 43200 s by the exact pid, one hc at 21600 s (step 2); ACCEPTED only if `kc127_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc119_syscheck_1025.py` exits 1 on the result (step 3). The marker `regrid_accepted.txt` (state and record blobs) is written from the driver's python process. The driver's summary gives the steps ratio, \|F\|, F_start, constraint and Delta beside the source's.
2. **Step 4a, the scan driver** (`kc127d23_scan_driver_1025.py`, made from my k_c 103 scan driver; started by `go_kc127d23_1025.cmd` only after the marker): the pins (the tool by committed blob, the state and record by the marker's blobs), `d18_secant.py selftest` and its three mutations logged first (exits 0, 1, 1, 1 wanted), the reader's selftest and its two controls (0, 1, 1), then the two processes with the shares

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc127_D23_p0.jsonl` | 0.04, 0.03, 0.06 |
| p1 | `scan_kc127_D23_p1.jsonl` | 0.05, 0.04 (the repeat of 0.04, on another process than p0's) |

   5 evaluations: 4 distinct points 0.03 to 0.06 and the repeat of 0.04; round 1 is the two points that bracket the registered root (0.04, 0.05), round 2 the next two (0.03 and the repeat), round 3 (0.06) runs alone. Then `read_lower.py . 0.03 0.06`; the driver hc's t5 its end and every line the reader printed. Cap 43200 s.
3. **Step 4b, the refinement** (`kc127d23_secant_driver_1025.py`, made from my k_c 87 secant driver; `go_secant_kc127d23_1025.cmd`, written when the bracket is known): its pins, `d18_secant.py` selftest and controls, the acceptance of the state by the k_c 127 check (exit 0, controls 1 1, the k_c 119 and k_c 111 checks refuse), then `d18_secant.py run` as above, cap 43200 s.
4. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched).
5. `go_kc127d23_1025.cmd` runs the regrid driver and, only if `regrid_accepted.txt` exists, the scan driver, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc127d23_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

## Cost, written before the run

What I have:

| source of the estimate | number |
|---|---|
| my k_c 103 regrids on this machine (4 threads) | 8415 to 11520 s (3402 to 3489 steps), 10635 s at D 22.875 (3387 steps; cpu 21420 s); peak private 4.0 GB |
| macm3's regrids at D 23.0 (Mac, 6 threads) | k_c 103: 1391 s; k_c 111: 2102 s (at D 23.0625); k_c 119: 2273 s; peak RSS 3.75, 4.78 and 5.64 GiB; his k_c 103 against mine: about 7.6 times |
| my secant evaluations (one process, `d18_secant.py run`) | 1388 to 1448 s at k_c 103 (3387 steps), 1066 to 1088 s at k_c 95 (3126), 795 to 821 s at k_c 87 (2862); peak private 2.91, 2.53, 2.14 GB; the evaluation time grows by about 0.75 per k_c step of 8 (steps ratio 1.07 to 1.08) |
| macm3's k_c 119 scan | 989 to 1011 s per evaluation on 2 processes (Mac), about 7 GiB per process |
| size here | k_c 127: about 3914 times 1.065 = 4170 steps (his ratios 1.0838, 1.0779, 1.071) |

| item | estimate | basis |
|---|---|---|
| source checks and selftests in the driver | about 30 to 90 s | the by-hand run, 2 threads, about 2 min for the five checks and three selftests |
| regrid | about 14000 to 36000 s (3.9 to 10 h), central about 23000 s (6.4 h); cpu about 2 times wall; peak private about 6 to 8 GB | macm3's k_c 119 2273 s and a further step of 1.1 to 1.5 times, times my 7.6; t5's "3 to 5 h" is below my range |
| steps of the result | about 4100 to 4300 | ratio 1.05 to 1.08 of 3914 |
| each scan evaluation (two processes) | about 2200 to 4500 s, central about 3000 s | my k_c 103 secant 1408 s times about 2 for the step growth, two processes at once |
| the scan (3 rounds) | about 6600 to 13500 s (1.8 to 3.8 h), central about 9000 s | the rows above; round 3 alone is faster |
| peak private per scan process | about 4 to 8 GB (t5: 8 GB) | 2.91 GB at k_c 103 for one secant process, times the growth in k_c; macm3's 7 GiB |
| each secant evaluation (one process) | about 2200 to 4000 s, central about 2800 s | 1408 s times about 2 |
| evaluations of the refinement | about 7 (6 to 9; at most 10); the bracket is 0.01 wide | my three refinements at D 22.875: 6, 9, 7; macm3's k_c 119 secant took 3390 s |
| the refinement | about 15000 to 40000 s (4 to 11 h), central about 20000 s (5.6 h) | the rows above; the cap is 43200 s |
| lowest free memory | about 12 to 15 GB (a regrid with 6 to 8 GB, a scan with two processes of 4 to 8 GB, beside the machine's 9 to 10 GB base) | the earlier stages left 13.7 to 20 GB with 4 to 16 GB of workers |
| together | start about 10:55 UTC; the regrid ends about 15:00 to 21:00 UTC (central about 17:20 UTC); the scan about 3 h later, the refinement about 6 h after that: the lane ends about 03:00 to 05:00 UTC on 27 Nov at the central figures | the rows above |

The samplers (`rows/regrid_samples.csv`, `rows/scan_samples.csv`, `rows/secant_samples.csv`) give the real figures.

## Files made here

`make_kc127d23_1025.py` writes `kc127d23_regrid_driver_1025.py`, `kc127d23_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver_kc127_1025.ps1`, `go_kc127d23_1025.cmd` and `publish_kc127d23_1025.sh` from the k_c 103 D 22.875 ones (staging `kc103d22875_1025`, raw `I1025-win/kc103_d22875` at 557ea8ee3 and `/secant`) by asserted text replacements; `diff_regrid_driver_vs_kc103.txt` is the diff of the regrid driver against the k_c 103 one; `prep_kc127d23_pins_1025.txt` the pins; `prep_source_checks_by_hand.txt` the by-hand source checks. The scan and secant drivers (`kc127d23_scan_driver_1025.py`, `kc127d23_secant_driver_1025.py`, `make_kc127d23_part2_1025.py`, their diffs against my k_c 103 scan driver and my k_c 87 secant driver) are added to this folder while the regrid runs and before the scan starts; their texts are pushed before they are used.

## Status

**Step 1, the source, PASSED 2026-11-26 10:47:57 UTC. Steps 2 and 3, the regrid, ACCEPTED 2026-11-26 13:38:44 UTC. Step 4a, the scan, RUNNING since 13:39:57 UTC.**** README first 1d35e042f (pushed 10:47:19 UTC, before the start); chain started 10:47:36 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc127d23_1025.cmd`. The k_c 87 D 22.875 secant was pushed (557ea8ee3) and posted (#1025 comment 7189716601) first.

- **Chain** (`rows/launcher_pid.txt`: 24572): conhost --headless 24572 <- cmd 4428 <- regrid driver launcher 18668 and driver 26384 <- sampler 25192, alert-only watcher 4720, keep-awake helper 26264, and the regrid process 1652 (worker 14396). The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Step 1, the source** (10:47:36 to 10:47:57 UTC, 21 s): the pins matched; the selftests of the three checks exited 0; ell_delta.lam0_at(23.0) = 2.0992182200; the source checks were as ordered: the k_c 119 check exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 111 check exit 1 and the k_c 127 check exit 1 (they refuse the source; `source_kc*_syscheck*.txt`).
- **Step 2, the regrid:** pid 1652 ran 10:47:57 to 13:38:28 UTC (exit 0, 10230 s): `ell_refine.py l1kc119macm3d23 119 l1kc127wind23 127 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd the worktree's `solver/matter`, 4 threads, BelowNormal, cap 43200 s by the exact pid; the driver sends t5 one hc at 21600 s (16:48 UTC) if it still runs.
- **Machine at the start:** the other project's I114 `convergence.py` jobs run beside it, not touched.
- **Sampler incident (10:47 to 10:49 UTC), no effect on the run:** the regrid driver as run (`kc127d23_regrid_driver_1025.py`, unchanged since its start) starts its sampler from `sample_driver4_1025.ps1`, a file that is not in this stage (my make script copied the sampler as `sample_driver_kc127_1025.ps1`); the driver's sampler therefore never started. I started the same sampler by hand at 10:49:13 UTC through `Win32_Process.Create` of a headless console (no `claude` in its chain): `sample_driver_kc127_1025.ps1 -Drv 26384 -Out rows/regrid_samples.csv -Interval 60`, watching the driver's process tree exactly as the driver's own sampler would have, so `rows/regrid_samples.csv` starts at 10:49:15 UTC (the first 80 s of the regrid are not sampled; peaks come later). The scan and refinement drivers (`kc127d23_scan_driver_1025.py`, `kc127d23_secant_driver_1025.py`) point at `sample_driver_kc127_1025.ps1` and were dry-run before the regrid ended (`selftest_scan_dry_1025.txt`).
- **The scan and secant drivers** (`make_kc127d23_part2_1025.py`, `diff_scan_driver_vs_kc103.txt`, `diff_secant_driver_vs_kc87.txt`) were written while the regrid runs and are pushed before they are used. The scan driver's dry run on stand-ins reaches "would start" for two processes (`d18_secant.py scan ... --pin=...`, exit 0), logs the new tool's selftest (exit 0) and its three mutations (exit 1 each), and refuses a missing marker, a wrong blob, five bad share lists (more than two shares included) and `--out` without `--dry`; the secant driver compiles and was dry-run before the state exists (it refused as it must: no marker, no state).
- **Stale text in two earlier hc messages:** the final hc of my k_c 95 and k_c 87 secant drivers named the folder `I1025-win/kc103_d22875/secant` (a leftover string of the driver I copied them from); the right folders are `I1025-win/kc95_d22875_secant` (75a10de70) and `I1025-win/kc87_d22875_secant` (557ea8ee3), as in my later messages and in the #1025 comments. The drivers of this lane carry the right folder.
- **End of the regrid:** 13:38:28 UTC, the acceptance 13:38:44 UTC, the scan started by itself 13:39:57 UTC (written ETA for the regrid about 14:40 to 20:50 UTC, central about 17:10 UTC: it ended well before that, and below t5's 3 to 5 h as well: 2.84 h).

**Regrid (`regrid_summary.txt`, `regrid.log`, `l1kc127wind23.jsonl`):**

| item | k_c 127 result | macm3's k_c 119 source |
|---|---|---|
| run | 10:47:57 to 13:38:28 UTC, pid 1652 (worker 14396), exit 0, 10230 s wall (the record's seconds: 10215) | 2273 s (record), Mac, 6 threads |
| \|F\| | 3.1939646372e-10 | 3.2079513798e-10 |
| F_start | 8.2571e-06 | 1.2513e-05 |
| steps | 4179 | 3914 |
| steps ratio | **1.0677** | macm3's earlier ratios at D 23.0: 1.0838 (k_c 95 to 103), 1.0779 (103 to 111), 1.071 (111 to 119) |
| psi-constraint | 1.4638e-03 (ratio 0.684) | 2.1389e-03 |
| Delta | 1.174322923415951 | 1.1743249686574218 |
| Delta(k_c 127) minus Delta(k_c 119) | -2.0452e-06 | |
| marker `regrid_accepted.txt` | state 7a1b150c96c12059c81c10927fdf00245a45a88e, record 2b15504f2bcc90f0e9b5b4049fb22ab44ee3c186 | state 2771cf87, record 158e3086 |

Acceptance (step 3; `syscheck.txt`, `syscheck_mutate.txt`, `syscheck_kc119_on_result.txt`, `selftest_kc127_syscheck_after.txt`, 17 s): `kc127_syscheck_1025.py` on the result exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; state \|F\| 3.1939646372e-10 equal to the record's, `freeze_from` 4179 steps = the record's), its selftest exit 0, `--mutate=F` exit 1 (state \|F\| 3.193965e-10 against 4.790947e-10), `--mutate=steps` exit 1, `kc119_syscheck_1025.py` on the result exit 1 ("the record is not k_c 119 at D 23 (kc 127, D 23.0)").

**Cost against the written estimates (regrid):**

| item | written | measured |
|---|---|---|
| source checks | about 30 to 90 s | 21 s (10:47:36 to 10:47:57 UTC, with the pins and selftests) |
| regrid | about 14000 to 36000 s, central about 23000 s (t5: 3 to 5 h) | 10230 s (2.84 h): **below** my range and just below t5's |
| steps of the result | about 4100 to 4300 | 4179 |
| cpu | about 2 times wall | 21700 s (2.12 times wall) |
| peak private | about 6 to 8 GB | 5.93 GB (peak working set 5.48 GB): just below |
| lowest free memory | about 12 to 15 GB (whole stage) | 18.17 GB at 12:11:33 UTC in the sampler, 17.88 GB in the alert-only watcher |
| peak commit | not written | 17.4 GB |
| laptop cpu | not written | mean 44.4 %, max 66 % (sampler: 168 sample times from 10:49:15 UTC, no gap over 90 s) |

My basis was my k_c 103 regrid at D 22.875 (10635 s) against macm3's k_c 103 at D 23.0 (1391 s), a factor 7.6; for the k_c 119 to 127 pair the factor is 4.5 (10230 s against his k_c 119's 2273 s), so the step from k_c 103 to 127 cost me 0.96 times the k_c 103 regrid and macm3 1.6 times his. The memory watcher raised no alert (`rows/regrid_memwatch.log`: "minimum free memory seen 17.88 GB; 0 alert(s) sent"), the keep-awake helper held until the driver ended (`rows/regrid_keepawake.log`), the System log shows no power event in 10:40 to 13:45 UTC, and `rows/regrid_raw.log` holds 24 RuntimeWarning lines from `dss_ell.py` (the Newton step's overflow and invalid-value lines, as in my earlier regrids). The 21600 s hc was not needed.

**Step 4a, the scan, started by itself 71 s after the marker (13:39:57 UTC):**

- **Chain:** the same console (`rows/launcher_pid.txt`: 24572, cmd 4428) <- scan driver launcher 3380 and driver 19932 <- sampler 25864, alert-only watcher 2900 (child 25336), keep-awake helper 15400 (child 10672), and the two `d18_secant.py scan` workers p0 18756 (0.04, 0.03, 0.06) and p1 21332 (0.05, 0.04), each with one child process (16228, 9112). BelowNormal, one thread each, cap 43200 s by the exact pids.
- **Before the scan** (13:39:55 to 13:39:57 UTC): the pins matched (the tool by committed blob eb1396ad, the state and record by the marker's blobs); `d18_secant.py selftest` exit 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1, 1, 1 (logged in `selftest_d18_secant.txt`); the reader's selftest exit 0 and its two controls exit 1, 1.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **ETA** (the estimates above counted from 13:39:57 UTC): each evaluation about 2200 to 4500 s on two processes, so round 1 ends about 14:20 to 15:15 UTC, round 2 about 15:00 to 16:30 UTC and round 3 (0.06, alone) about 15:30 to 17:30 UTC. The refinement follows when I have read the reader's lines.

Pushed 2026-11-26 13:41:00 UTC.

## Result

Not yet run.
