# I1025-win/kc143_d23: k_c 143 at D 23.0, regridded from win2's accepted k_c 135 state, then the scan and the secant refinement of lambda_1's root with the Rust block 12 (winb)

Written before the run, 2026-11-27 06:07:23 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan nor the refinement had been run for this folder when the order, the registration and the estimates below were written. Run beforehand, read-only: the pins, the source checks by hand (`prep_source_checks_by_hand.txt`, 6 runs, 30 s), the dry run of the regrid driver (pins, three selftests, lambda_0). Runner: the winb session (surface-laptop-4, Windows 11, i7-1185G7 4 cores / 8 threads, 32 GB); coordinator t5.

## Order (t5's hc, stamped 2026-11-27 05:59 UTC; winb section, quoted)

"Next lane for winb (#1025): k_c 143 at D 23.0. It is the third D of k_c 143 (macm3 does 23.0625 and 23.125), and it tests whether the root's step stalls at D 23.0 as it did at 23.0625.
1. Regrid from win2's accepted k_c 135 state at D 23.0 (raw I1025-win2/kc135_d23, state blob cd134e2c, record bc295fbc), with the code of your k_c 127 regrid (48c36355):
   ell_refine.py l1kc135win2d23 135 l1kc143winbd23 143 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
   Cap 43200 s. Source check: kc135_syscheck (b353d466) accepts the source. Acceptance: raw 5370db0e3 I1025-mac/checks/kc143_syscheck_1025.py (blob e15b0ee2) exits 0, its controls exit 1, and the kc135 check refuses the result.
2. Scan with the RUST block: the branch wip/ell1-rust-b12's d18_secant.py scan with --b12=rust --b12_threads=2 --pin=..., your SITE on PYTHONPATH, OPENBLAS_NUM_THREADS=1, 2 processes. Points 0.050, 0.055, 0.060 plus a repeat of 0.055: my prediction for the root is 0.0496 + 0.84 x 0.0039 = +0.0529 +- 0.003.
3. Secant on the robust bracket, same tool and Rust block, with --tol=5e-5, not 1e-5. Reason: #1101's dh370 test measured a root scatter of 1.75e-4 between two solves of one state, so digits below about 5e-5 are not in the state. Reuse the scan's ends.
New folder I1025-win/kc143_d23, README with the bars and your registrations first. Same stop rules as your k_c 127 lane. Post on #1025 at the end."

Stop rules of the k_c 127 lane (t5's order of 2026-11-26 10:40 UTC): stop and report on not accepted, an exception (an array limit included), no robust change or more than one, or any step over 12 h.

## Registered before the run (t5's bars, and my estimates)

**PREDICTION (t5's): the root of lambda_1 at k_c 143 and D 23.0 is +0.0529 +- 0.003** (k_c 135's root +0.0496 plus 0.84 times the last step 0.0039; roots at D 23.0 so far: k_c 87 -0.025404, 95 +0.008707, 103 +0.026506, 111 +0.035564, 119 +0.041061, 127 +0.045711 (mine, det-linear 0.04571076), 135 about +0.0496 (win2)).

**The bars** (what I check and report; t5 rules by position, I do not interpret):

| step | bar |
|---|---|
| regrid | exit 0 inside the cap of 43200 s; `kc143_syscheck_1025.py` exits 0 on the result, its selftest 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc135_syscheck_1025.py` refuses the result (exit 1); report steps and their ratio, \|F\|, constraint, Delta beside the source's |
| scan | `d18_secant.py` selftest 0 and its three mutations `half`, `norobust`, `nosigncheck` exit 1 first (and `ell_b12rs.py` selftest 0, `--mutate=nolam` and `--mutate=harm` 1); exits 0, 0; the reader prints **exactly one robust change**; the repeat of 0.055 agrees; the float64 sign and the orientation are reported as printed |
| the bracket | the bracket by 0.0529 is **(0.050, 0.055)**; a bracket (0.055, 0.060) is a miss of the central bracket (still inside 0.0499 to 0.0559 for part of it only: 0.055 to 0.0559); a change outside (0.050, 0.060), no robust change, or more than one robust change stops the lane (t5's stop) |
| secant | ends reused from the scan (`--ends`, the two scan records at LO and HI verbatim); exit 0 (tol 5e-5) wanted; exit 4 (maxev or a non-robust interior point) with a valid bracket is reported as printed for t5's ruling, as in my k_c 103, 87 and 127 lanes |
| **registered test** | the det-linear root `lam_lin` of the final bracket lies in **[0.0499, 0.0559]** (+0.0529 +- 0.003); the scan's estimator range is information, not the test |

My own estimates (not predictions of the order):

- **Regrid:** the k_c 127 regrid took 10230 s here (4 threads, BelowNormal); win2's k_c 135 regrid took 20068 s on its 20-core machine (8 threads, Normal; README of I1025-win2/kc135_d23). The k_c 119 to 127 step ratio was 1.0677 and the k_c 127 to 135 one 1.0627, so I expect about **4700 steps** (4670 to 4720, ratio about 1.058) and a constraint about 0.68 times the source's (6.7e-4). I do not know how the time scales with k_c: **14000 to 43200 s, central 24000 s (6.7 h)**, and there is a real chance, about one in five, that it reaches the cap of 43200 s, which is then t5's stop.
- **Scan** (the new part: the Rust block): one evaluation is the float64 blocks 0 to 11 (my k_c 127 evaluation: 441 to 613 s, scaling to about 650 s at k_c 143), the Rust block 12 on 2 threads (macm3's Mac at k_c 143: 211 s against `DDEll`'s 1032 s; I have no number for this CPU, so **350 to 1800 s, central 700 s**) and `dd_logdet` (18 to 23 s at k_c 127, about 30 s). So **1000 to 2800 s per evaluation, central 1400 s**; two rounds on two processes: the scan takes **2000 to 6000 s, central 2800 s (0.8 h)**. If the Rust block were no faster than the Python block here (7800 s scaled), the scan would take about 16000 to 30000 s, still inside the cap.
- **Secant** (one process, `--b12_threads=4`): about 1100 s per interior evaluation (800 to 2000 s) and **about 4 interior evaluations** (3 to 6: the bracket is 0.005 wide and the tolerance 5e-5; my k_c 127 run needed 6 from 0.01 to 5e-6): **2400 to 12000 s, central 4400 s (1.2 h)**.
- **The whole lane:** 5 to 16 h, central about 8.5 h, almost all of it the regrid.
- **Memory:** the regrid peaked at 5.93 GB private at k_c 127: about 7 to 9 GB here. The scan processes: 4.33 GB each at k_c 127 with the Python block; with the Rust block and 2 threads I expect 5 to 9 GB each, so the two processes together stay under 18 GB of 32 GB; lowest free memory 10 to 15 GB. The other project's `convergence.py` jobs run beside it (not touched).

## The source (win2's)

| item | value |
|---|---|
| source state | raw `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy`, 70648 bytes, **blob cd134e2c** (`inputs/`; also in `solver/matter/data/` of the regrid worktree) |
| source record | raw `I1025-win2/kc135_d23/l1kc135win2d23.jsonl`, 372 bytes, **blob bc295fbc**: k_c 135, D 23.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.1834404599371294e-10, F_start 4.870300630763123e-06, **steps 4441**, **constraint 9.915118203933646e-4**, **Delta 1.1743190138598711**, 20050 s, src `l1kc127wind23` (my k_c 127 state) |
| checks (raw `I1025-mac/checks/`, each 4821 bytes, the same text with the k_c numbers changed) | `kc127_syscheck_1025.py` 898ebefa, `kc135_syscheck_1025.py` **b353d466** (source check), `kc143_syscheck_1025.py` **e15b0ee2** (acceptance check; raw 5370db0e3 and origin/main hold the same blob) |
| regrid code | worktree `choptuik-i1025k79` at 48c36355 (`ell_refine.py` 631e5801, `ell_delta.py` fde699f5, `dss_ell.py` 5d28c19e, `ell_ddm.py` 86578fee, `ell_dd.py` 7e58fcbc, `ddnp.py` 9b1fb195): the code of my k_c 127 regrid |
| scan and secant code | worktree `choptuik-i1102` (detached) at **d4b6b6ce** = branch `wip/ell1-rust-b12`: `d18_secant.py` **9706e506** (differs from 92b9bf53's eb1396ad by `--b12=rust`, `--b12_threads`), `ell_b12rs.py` a1fff74f, `ellrs/` tree 47ce5fb8, `ell_fastm.py` 93f963f6 and the same `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` blobs as the regrid worktree |
| ellrs (the Rust block) | my #1102 Windows build, `i1102_1025/site/ellrs/` (cp314, `-C target-cpu=native`, avx512, products from scipy's dgemm in the scanner), `ellrs.cp314-win_amd64.pyd` **ddd5a082** (934912 bytes), `__init__.py` 76c7cfbc; gates passed 2026-11-27 05:56 UTC (raw `I1102-win` d64dc10cb; t5 accepted); the scanner's venv untouched |
| readers | `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f (as in my k_c 127 lane); `d18_hybsign.py` e089207a |
| lambda_0 | 2.0992182200 (`ell_delta.lam0_at(23.0, *ell_delta.lam0_table())[0]` in the regrid worktree; unused with `--no-gamma`; the driver checks that it prints the order's string; dry run 06:05 UTC: it does) |
| python | `venv-md510` (python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 with `dd_logdet`) |

By hand, 2026-11-27 06:05:50 to 06:06:17 UTC (`prep_source_checks_by_hand.txt`): the k_c 135 check (selftest 0) **accepts** the source (exit 0: record \|F\| 3.1834404599e-10, the state's 3.1833593455e-10 here, `freeze_from` 4441 steps = the record's), `--mutate=F` and `--mutate=steps` exit 1, and the k_c 127 and k_c 143 checks refuse it (exit 1 each: "the record is not k_c 127 at D 23" and "not k_c 143").

## The run

1. **Pins and source checks** (the regrid driver, repeating the by-hand checks): the three checks and their selftests, the readers, the state and record against their blobs (inputs/ and the worktree's `data/` copies), worktree 48c36355 with `ell_refine.py` 631e5801, `lam0_at(23.0)`; the k_c 135 check accepts the source (0), controls 1 1, the k_c 127 and k_c 143 checks refuse it. Any failure is a stop with an hc.
2. **Regrid** (the order's command, one process, `OPENBLAS/OMP/MKL/RAYON_NUM_THREADS=4`, BelowNormal, no window, cwd the regrid worktree's `solver/matter`, killed by the exact pid at 43200 s, hc at 21600 s if still running).
3. **Acceptance:** `kc143_syscheck_1025.py` exits 0 on the result, its selftest 0, `--mutate=F` and `--mutate=steps` 1 1, and the k_c 135 check refuses the result (1). Marker `regrid_accepted.txt` with the state and record blobs. Report steps and their ratio, \|F\|, constraint, Delta beside the source's.
4. **Scan with the Rust block** (the scan driver, started by the chain only if the marker exists): `d18_secant.py` selftest 0 and its three mutations 1 1 1, `ell_b12rs.py` selftest 0 and `--mutate=nolam`, `--mutate=harm` 1 1, the readers' selftests; then two processes, `d18_secant.py scan STUB STATE 23.0 LAMS OUT --pin=STATEBLOB,STUBBLOB --b12=rust --b12_threads=2`, `PYTHONPATH` the ellrs site, `OPENBLAS_NUM_THREADS=1`, BelowNormal, cap 43200 s: **p0 `0.055,0.050`, p1 `0.060,0.055`** (the repeat of 0.055 on the other process, in round 2, as my k_c 127 scan did with 0.04). Then `read_lower.py 0.05 0.06` on the folder and an hc with its lines.
5. **Secant** (by hand after I read the reader, only if exactly one robust change; the scan files are pushed first): `d18_secant.py run STUB STATE 23.0 LO HI secant/secant.jsonl --tol=5e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB --ends=scan_kc143_D23_ends.jsonl --b12=rust --b12_threads=4`, one process (the two end records are the scan's lines at LO and HI, verbatim, in one file; `--ends` takes one file), `PYTHONPATH` the ellrs site, `OPENBLAS_NUM_THREADS=1`, `RAYON_NUM_THREADS=1`, BelowNormal, cap 43200 s by the exact pid, hc at 21600 s. The thread count (4, the machine's cores) is mine: the order gives none; the Rust block's bits do not depend on it (#1102: "the thread count does not change the bits"). The driver repeats the pins, the tool's selftest and controls, and the acceptance of the state (kc143 check 0, controls 1 1, kc135 and kc127 checks refuse).
6. **Beside each stage:** a sampler (60 s), an alert-only memory watcher (hc below 1 GB, kills nothing) and a keep-awake helper (`SetThreadExecutionState`, power plan untouched), each its own process. The chain is started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc143d23_1025.cmd` (outside my terminal; the session check must report no `claude` in any chain).
7. **Stops** (t5's, as in the k_c 127 lane): not accepted, an exception, no robust change or more than one, any step over 12 h. I report each by hc at once and change nothing. **Post on #1025 at the end of the lane** (t5); I hc t5 at the end of each step.

Dry tests before the scan driver runs (it starts hours after the regrid): the scan driver `--dry --out=<stand-in>` and an end-to-end test of the new flags on the k_c 31 state of #1102 (`d18_secant.py scan ... --b12=rust --b12_threads=2` against `--b12=ddm`, one evaluation each; the records must agree to the last bit): `selftest_scan_dry_1025.txt`, written as they run, in the folder.

## Files made here

`README.md`; `prep_source_checks_by_hand.txt`; the drivers `kc143d23_regrid_driver_1025.py`, `kc143d23_scan_driver_1025.py`, `kc143d23_secant_driver_1025.py` (derived from my k_c 127 drivers by `make_kc143d23_1025.py`; `diff_regrid_driver_vs_kc127.txt`, `diff_scan_driver_vs_kc127.txt`, `diff_secant_driver_vs_kc127.txt` show every change), `kc143d23_watch_alert_1025.py`, `sample_driver_kc143_1025.ps1`, `keepawake_1025.py`, `session_check_1025.ps1`, `go_kc143d23_1025.cmd`, `publish_kc143d23_1025.sh`, `prep_kc143d23_pins_1025.txt`; later `regrid_accepted.txt`, the state and record, `scan_kc143_D23_p*.jsonl`, `read_lower_kc143_D23.log`, `secant/`, `rows/` (samplers, watcher and keep-awake logs). One slip of the k_c 127 regrid driver is fixed here: its sampler file name pointed at a file not in the stage (README of kc127_d23, "Sampler incident").

## Status

README first. Not started when this was written.

Pushed 2026-11-27 06:07:23 UTC.

## Result

Not yet run.
