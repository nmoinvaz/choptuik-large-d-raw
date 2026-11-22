# I1070-dh170: γ at D 3.15 at M 160 (hp/lowD_gamma.py), beside macm3b's M 128 with the same lam0

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1070 (macm3b runs the M 128 half in `I1070-macm3/`). Written 2026-11-21 22:29:13 UTC, before the run.

Order (coordinator's hc ~22:27 UTC 21 Nov), quoted: "a low-D task, #1070 (read it first): γ at D 3.15 at M 160, with hp/lowD_gamma.py on raw I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz, --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977, nice 10, cap 6 h, output raw I1070-dh170/lowD_gamma_D3.15_M160.jsonl, README first. It runs beside macm3b's M 128 with the same lam0. Readings as in the issue (one sign change, F below 1e-27); if there is no sign change, stop and report. Post on #1070."
**Why (the issue):** our γ stops at D 3.5 (#628: 0.3223855827556097 at M 128; M 128 - M 96 = 3.77e-9); Ecker, Ecker, Grumiller and Jechtl (arXiv:2602.10185, §5.3) find γ -> 0 faster than Delta as D -> 3, so Delta/(2γ) diverges. macm3b's pilot with the script's own guess found no sign change (all 9 determinants -1 in lam 3.674 to 3.754: the guess `lam_guess(3.15)` = 3.7137, extrapolated from D 3.64 to 3.70, misses); the coordinator then set lam0 4.3977 from their GammaList (γ 0.2225464 at D 3.14, 0.2486066 at D 3.2; interpolated to D 3.15: γ 0.227280 to 0.227411, lam 4.3973 to 4.3999) and macm3b reruns M 128 with it (started 22:19:33 UTC).
**Input:** raw `I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz`, git blob 2515013d1ed23e09e5ca7d4aee82ac5781f72d12 (read from origin/main of the raw repository into `~/scratch1070/I927-mac/inputs/`, hash checked by the wrapper), D 3.15, kt 36, kc 100, ks 250, 17 nodes (per macm3b's README).
**Command** (`run_1070_dh170.sh`): `python -u hp/lowD_gamma.py lowD_gamma_D3.15_M160.jsonl <input> --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977`, from the worktree `~/Source/choptuik-large-d-1058b` (hp/lowD_gamma.py unchanged since 8179068d, macm3b: no change to it, hp/src, Cargo or pyproject up to 6c4d845d), its venv (the 8179068d hpkernel, x86 avx2), `nice -n 10`, `timeout -s TERM 21600` (6 h), output in this folder (a worktree of the raw repository). Against the issue's pilot command, token by token (`cmd_diff_M160.txt`): the interpreter, the output and input paths (M 160), `--threads=4` (the order) and the added `--lam0=4.3977` (the order). Memory and cpu sampled every 60 s (`memlog_M160.log`, alert-only below 2 GiB free).
**Acceptance (the issue's), `accept_1070.py`:** exactly one sign change in the bracket (`n_signchanges` 1) and F after the polish below 1e-27; if not, report and stop. Its control: `--selftest` (a passing record and four broken ones: no sign change, two, F 1e-26, F missing: all give the verdicts written in it, `selftest_accept.log`) and `--selftest --mutate` (the F bar loosened to 1e-20 must fail the selftest, exit 1: `selftest_accept_mutate.log`). Also reported: the determinants (lam, sign, ln|det|, seconds), the bracket's sign changes, F after the polish, lam, γ, the wall, cpu and memory; γ(160) - γ(128) against macm3b's M 128 value at the same lam0 when their record exists (a resolution change, not a bound); γ(3.15) against γ(3.5) = 0.32238558 and against the interpolated Ecker et al. value 0.22728 to 0.22741.
**Readings, fixed now (the issue and the order):** one sign change and F below 1e-27: γ(3.15) at M 160 stands; no sign change: stop and report (the script itself ends, there being no other bracket than its widening of +-1e-4, 1e-3, 1e-2, 4e-2 about lam0, i.e. lam 4.3577 to 4.4377).
**Predictions, registered before the run:**
- a sign change in the window (about 80%): the interpolated root (lam 4.3973 to 4.3999) lies inside it, and the M 160 state differs from M 128 by a resolution error far smaller than the window; exactly one (about 85% given a change);
- F after the polish below 1e-27 (about 65%): macm3b's M 128 pilot had 1.103e-28 (6.69e-26 -> 1.29e-28 in 2 Newton steps); M 160 on its own plan is likely of the same order, possibly above 1e-27;
- |γ(160) - γ(128)| between 1e-9 and 1e-6 (about 70%): #628's M 128 - M 96 was 3.77e-9 at D 3.5, and the plan at D 3.15 is longer;
- γ(3.15) within 1e-3 of the interpolated 0.2274 (about 80%);
- wall: a determinant at M 160 on 4 threads of this CPU I estimate 20 to 30 min (macm3b's M 128 on 6 threads of the M3: 308 s); with 8 to 14 determinants plus the polish, 4 to 6 h; about 50% that it ends inside the 6 h cap. A cap during the search would leave the bracket without a root; I would report the determinants done.

## Result (written 2026-11-21 22:31:10 UTC): the run cannot start at M 160 with this kernel; stopped, no record
`run_M160.log`: the command ended after 2.10 s (time -v; wrapper wall 60 s, exit 1, no record written, `exits_1070.txt`) at the polish: `hp/lowD_gamma.py` line 81 -> `newton_solve` -> `newton_step` -> `s.newton(zh, zl)` -> `ValueError: newton: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage)`. **Diagnostic, not part of the issue's command:** the same command without `--polish` (`diag_nopolish_M160.log`, 2.5 s, output to a scratch path) ends at the first determinant: `ValueError: mode_det: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage)`. So neither the polish nor any determinant can run at M 160 with this kernel, and `--polish=0` is no way round it.
Where, in the source of the kernel (hp/src/python.rs, unchanged between 8179068d and macm3b's 6c4d845d): `const DENSE_M_MAX: usize = 128` (line 569); `fn dense_ok` (line 665) returns the error above when `self.api.m() > DENSE_M_MAX`; `Solver.newton` and `Solver.mode_det` (line 1529, `self.dense_ok("mode_det")?`) call it. `newton_mixed` has block storage above M 128 (python.rs line 1013, notes/HIGH_M.md); `mode_det` has no block version.
Sizes, for the choice of a way round: the M 160 state has n = 11521 unknowns; a dense double-double n x n matrix is 2.12 GB (hi and lo), about 6.4 GB with the matrix copies `mode_matrix` and the LU make; macm3b's M 128 pilot peaked at 3.36 GB rss, scaled by (11521/9217)^2 = 1.56 about 5.2 GB. Either fits dh170 (31 GiB) and the M3 (24 GB): the limit looks like a safety bound, not a need; I did not test that.
I made no workaround (the stop rule of the issue's plan: a bug stops the work, no workaround without the coordinator). `I927-mac/inputs/` holds D 3.15 states at M 128 and M 160 only (no M 96 for a cross-check).
**Predictions against the result:** all of them (a sign change in the window, F below 1e-27, |gamma(160) - gamma(128)|, gamma(3.15) within 1e-3, the wall) assumed the run could start: moot. I did not check the dense limit before registering them; the issue's plan and macm3b's README do not mention it either.
**Resources:** the failing run: 2.10 s, 118% cpu, max rss 101492 kB (99 MiB); the diagnostic 2.5 s; nothing else ran; lowest MemAvailable in the wrapper's samples 28903 MiB, no alert.

## M 96 pair (written 2026-11-21 22:38:19 UTC, before the run)

Order (coordinator's hc, received after my 22:31 UTC #1070 post, after "thanks, the right stop. No hp change now: M 160 waits for macm3b's M 128 result, and if it is needed, DENSE_M_MAX gets raised on a 62 GB machine later"), quoted: "the resolution pair from below. #1070 at M 96: (1) the M 96 state: python3 lowD_dd.py RAW/I1070-dh170/m96.jsonl --start RAW/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --Ms 96, with that state's own nodes, kt, kc and ks from its meta, --jac f64 --tol 1e-29 --threads 4 --tag lowD1070, nice 10, cap 4 h. (2) then: lowD_gamma.py on that state, --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977 (macm3b's M 128 run uses the same), cap 3 h. Readings as in the issue (one sign change, F below 1e-27); with macm3b's M 128 value this gives gamma(128) - gamma(96). If there is no sign change, stop and report."
**Orchestrator:** `run_m96.py` (stage 1 and 2 in one script, session-wide kills by exact pid, memory log `memlog_m96.log`, events `exits_m96.txt`). Stage 1 command, from `hp/` of `~/Source/choptuik-large-d-1058b` (hp at 8179068d): `nice -n 10 timeout -s TERM 14400 python -u lowD_dd.py m96.jsonl --start <M 128 input, blob df2ab378105434a07bad081e0ce4a973ff6b97cc> --Ms 96 --nodes 0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9 --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 4 --tag lowD1070` (nodes, kt 36, kc 100 and ks 250 are the input's own meta; 17 nodes, n 9217 at M 128). Stage 2: `python -u hp/lowD_gamma.py lowD_gamma_D3.15_M96.jsonl states/lowD1070_D3.1500_M96.npz --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977`, cap 3 h; `accept_1070.py` on its record.
**Readings, fixed now.**
- Stage 1, after each Newton call (the checkpoint is copied, `resid1070.py` measures its max|F| at its own plan with a planted +1e-20 control that must read 1.000e-20): max|F| <= 1e-27: converged (the state stands); max|F| <= 1e-26 and the call gained less than a factor 2: at the floor, as #1014 accepted its B1 (stage 2 runs, and I report Delta's last Newton correction); max|F| above 1e-26 after 3 or more calls with no factor 2 gain: stalled (stop, report, no stage 2); a planted control not within 1e-22 of 1e-20: stop.
- Stage 2 (the issue's): exactly one sign change in the bracket (`n_signchanges` 1) and F after the polish below 1e-27. No sign change: stop and report.
**Controls and their results before the run:**
- `decide()` of run_m96.py: `--selftest` 7 of 7 cases pass (`selftest_decide.log`), `--selftest --mutate` (floor gain factor 2 -> 1.2) exits 1 with 2 cases failing (`selftest_decide_mutate.log`).
- The session kill (`timeout` puts its child in a process group of its own, so a process-group kill leaves it running): my first version left `timeout` and its child alive in the test and failed it; the version kept kills every pid of the session and leaves none (`test_killgroup_m96.log`).
- `measure()` on the M 128 input: max|F| 4.908e-29, planted +1e-20 reads 1.000e-20 (`test_measure_m96.log`).
**Predictions, registered before the run:**
- stage 1 takes 3 to 5 Newton calls from the resampled M 128 state (about 80%: the f64 Jacobian gains about 8 to 9 digits per call), each 3 to 10 min on 4 threads of this CPU (n = 72 M + 1 = 6913; about 60%), so 15 to 50 min in all (about 60%);
- stage 1 ends converged or at the floor (about 85%); it ends at max|F| <= 1e-27 (about 60%);
- Delta(96) differs from Delta(128) = 2.961319687827138 by 1e-10 to 1e-6 (about 65%);
- stage 2: a sign change in the window (about 80%), exactly one (about 85% given a change), F after the polish below 1e-27 (about 65%);
- |gamma(128) - gamma(96)| between 1e-8 and 1e-5 (about 70%; #628 had 3.77e-9 at D 3.5);
- stage 2 wall: 4 to 10 min per determinant, 8 to 14 determinants plus the polish: 0.7 to 2 h (about 60%); it ends inside its 3 h cap (about 85%).

## Run 1 of the M 96 pair stopped at 2026-11-21 22:40:05 UTC by my own control, which was mis-specified (corrected rule below)
Run 1 (launched 22:38:34 UTC): stage 1 start |F| 7.3e-04 (671 steps, n 6913); Newton call 1 took 22.8 s (accepted, lam 1, |dz| 1.48, dDelta +1.48e-06, Delta 2.961321170059160, piv 3.1e-04..2.3e+01); the checkpoint read max|F| 8.518e-07 and the planted +1e-20 read 8.518e-07. My rule above ("a planted control not within 1e-22 of 1e-20: stop") fired and `run_m96.py` stopped lowD_dd.py by the pids of its session at 22:39:17 UTC, during call 2 (`exits_m96_run1.txt`, `run1_stage1_m96.log`; no record written; the call 1 checkpoint is `states/run1_ckpt_after_call1.npz`, the interrupted run's checkpoint `states/run1_hp_ckpt.npz`).
**Cause (known):** the plant adds 1e-20 to one residual component and the reading is the maximum over all components, so at max|F| = 8.5e-7 the plant is invisible and the reading equals the as-saved max|F|. The rule was valid only where max|F| is below about 1e-22 (as at the floor, where #1014 used it); I wrote it for every call without checking that. This is an error of my rule, not of the solver or the state.
**What I changed, and what I did not:** `decide()` now applies the strict reading (planted within 1e-22 of 1e-20) when max|F| <= 1e-22, which includes every case that can declare converged (<= 1e-27) or the floor (<= 1e-26); above 1e-22 the control is that the planted reading is at least the as-saved max|F| (a plant cannot lower the maximum), which a wrong measurement can still fail. No threshold on max|F| changed. `--selftest` now has 11 cases and passes; the mutated run (the old rule applied everywhere, and the floor gain 2 -> 1.2) exits 1 with 4 cases failing, including the F 8.518e-07 case that fired live (`selftest_decide_mutate.log`). Run 2 starts from the M 128 input again, not from the checkpoint (45 s of run 1 are not reused).
**Predictions against run 1:** I predicted 3 to 10 min per Newton call: call 1 took 22.8 s. I did not predict the start |F| 7.3e-04 (the M 128 state resampled to M 96) nor the max|F| after call 1, 8.518e-07 (a gain of 860).
**Predictions for run 2, added after call 1 (the earlier ones above stand for the rest):** 5 to 8 Newton calls in all to max|F| <= 1e-26 (about 60%), each about 20 to 60 s, so stage 1 takes 3 to 8 min (about 60%).

## Result of run 2 of the M 96 pair (written 2026-11-21 23:14:38 UTC): PASS, gamma(3.15) at M 96 = 0.22738618769170593
**Stage 1** (`stage1_m96.log`, `exits_m96.txt`; run 2 started 22:40:18 UTC, done 22:42:09 UTC, wall 111 s): converged at Newton call 4. Start |F| 7.31e-04 (the M 128 state resampled to M 96; 671 steps, n 6913).
| call | `|F|` at its start | `|dz|` | Delta after the step | seconds | max\|F\| of the checkpoint (`resid1070.py`) | planted +1e-20 reads |
|---|---|---|---|---|---|---|
| 1 | 7.31e-04 | 1.48 | 2.961321170059160 | 21.6 | 8.518e-07 | 8.518e-07 (masked) |
| 2 | 8.52e-07 | 1.07e-03 | 2.961321309196560 | 37.5 | 9.339e-12 | 9.339e-12 (masked) |
| 3 | 9.34e-12 | 2.90e-09 | 2.961321309196662 | 22.3 | 1.15e-22 | 1e-20 |
| 4 | 1.15e-22 | 1.77e-19 | 2.961321309196662 | 22.5 | 3.737e-29 | 1e-20 |
`decide()` said converged at call 4 (max|F| <= 1e-27); the script stopped lowD_dd.py during call 5 by the pids of its session and took the call 4 checkpoint as the M 96 state: `states/lowD1070_D3.1500_M96.npz`, git blob e540d3e7d2e84b34227cb5e6328245f8190be797, 168282 bytes. Delta(96) = 2.961321309196662 + (-1.9781123151858868e-16); Delta(128) of the input = 2.961319687827138 + (-1.0086792570140185e-16); Delta(96) - Delta(128) = 1.62137e-06 (sum of the parts, 60 digits; the last Newton step moved Delta by +8.92e-23).
**Stage 2** (`stage2_gamma_M96.log`, `lowD_gamma_D3.15_M96.jsonl`; 22:42:09 to 23:13:30 UTC, script 1864.7 s): the polish took 2 Newton steps (|F| 3.74e-29 with lam 0.125, then 3.63e-29), to F 2.98e-29 after it; 11 determinants.
| lam | sign | ln\|det\| | min pivot | seconds |
|---|---|---|---|---|
| 4.3976 | -1 | 2120.729570 | 2.80e-04 | 139.8 |
| 4.3977 | -1 | 2120.118294 | 2.80e-04 | 143.9 |
| 4.3978 | -1 | 2117.033775 | 2.80e-04 | 147.5 |
| 4.3967 | -1 | 2121.875297 | 2.80e-04 | 143.3 |
| 4.3987 | +1 | 2122.867403 | 2.80e-04 | 208.4 |
| 4.397760137027 | -1 | 2119.297681 | 2.80e-04 | 133.1 |
| 4.397806123434 | +1 | 2116.015961 | 2.80e-04 | 134.3 |
| 4.397804458559 | -1 | 2112.403262 | 2.80e-04 | 140.8 |
| 4.397804502295 | -1 | 2105.468893 | 2.80e-04 | 212.0 |
| 4.397804502338 (4.3978045023377454) | -1 | 2093.356403 | 4.39e-09 | 142.2 |
| 4.397804502343 | +1 | 2103.326209 | 9.39e-05 | 145.2 |
The first grid (lam0 +- 1e-4) had none, the second (+- 1e-3) had 4.3967 -1 and 4.3987 +1: one change, between 4.3978 and 4.3987; brentq took it to xtol 1e-11. Record: lam 4.3978045023377454, gamma 0.22738618769170593, F 2.980415107538135e-29, n_signchanges 1, n_det 11 (the xtol is the root search's stopping tolerance, not an error bar of the discretization). ln|det| falls toward the root (2112.4 at 4.4e-8 from it, 2105.5 at 4.3e-11, 2093.4 at the reported root) and the smallest pivot at it is 4.39e-9 against 2.80e-04 elsewhere.
**Acceptance (the issue's, `accept_1070.py`): PASS.** n_signchanges 1; F after the polish 2.98e-29 (below 1e-27). Its own controls (`selftest_accept.log`, `selftest_accept_mutate.log`) passed and failed as required before the runs. gamma(3.15) at M 96 lies inside the interpolation of Ecker, Ecker, Grumiller and Jechtl's GammaList quoted in the issue, 0.227280 to 0.227411 (an interpolation spread, not an enclosure); 1.4e-5 from 0.2274.
**gamma(128) - gamma(96):** not available yet: macm3b's M 128 rerun (`--lam0 4.3977`, started 22:19:33 UTC) had no record on origin/main at 23:13 UTC (`I1070-macm3/` holds the pilot's, `lowD_gamma_D3.15_M128.jsonl`, with no sign change). Their pilot's M 128 state has Delta 2.961319687827138, the input's, as above.
**Predictions against the result:**
| prediction | result |
|---|---|
| 3 to 5 Newton calls (about 80%) | 4: right |
| each call 3 to 10 min; stage 1 15 to 50 min (about 60%) | 21.6 to 37.5 s per call, stage 1 111 s: wrong by an order of magnitude |
| after call 1: 5 to 8 calls in all, 3 to 8 min (about 60%) | 4 calls, 111 s: wrong |
| stage 1 converged or at the floor (about 85%), max|F| <= 1e-27 (about 60%) | converged, 3.737e-29: right |
| Delta(96) - Delta(128) between 1e-10 and 1e-6 (about 65%) | 1.62e-06: just outside |
| stage 2: a sign change (about 80%), exactly one (about 85%), F below 1e-27 (about 65%) | right in all three |
| |gamma(128) - gamma(96)| between 1e-8 and 1e-5 (about 70%) | not yet known |
| stage 2 wall 0.7 to 2 h (about 60%); inside the 3 h cap (about 85%) | 31 min, inside the cap: the first wrong, the second right |
Not predicted: the start |F| 7.31e-04.
**Resources** (4 threads at nice 10, nothing else of mine running; MemAvailable stayed above 27.9 GiB, no alert): stage 1 111 s wall, one memory sample 476 MiB RSS at 268% CPU (its `time -v` block was lost when the script stopped it); stage 2 wall 31:05.10, user 6607.18 s, system 23.57 s, 355% CPU, max RSS 1701532 kB (1.62 GiB, `time -v`; the 60 s samples in `memlog_m96.log` peaked at 1056 MiB). Run 1 (45 s, stopped by the mis-specified control, above) is kept as `run1_stage1_m96.log`.

## D 3.35 pair (written 2026-11-21 23:18:01 UTC, before the runs)

Order (coordinator's hc after my 23:15 UTC report, "PASS accepted ... and the fix is fine"), quoted: "a cheap low-D point on the same issue (#1070), D 3.35, filling the curve between 3.15 and 3.5: (1) gamma at M 96 on raw T39-win/hp/data/lowD_states/lowDvh96_D3.3500_M96.npz: python3 -u lowD_gamma.py RAW/I1070-dh170/lowD_gamma_D3.35_M96.jsonl <state> --threads=4 --polish=2 --xtol=1e-11 --lam0=3.4094 (the Vienna GammaList has gamma 0.2933033 at D 3.35 exactly); (2) lift that state to M 128 with lowD_dd.py --Ms 128 (its own nodes, kt, kc, ks; --jac f64 --tol 1e-29 --threads 4 --tag lowD1070b), then gamma at M 128 with lam0 set to (1)'s lam. nice 10, caps 3 h each. Readings as in the issue: one sign change, F below 1e-27; report gamma(128) - gamma(96) and both against 0.2933033. If there is no sign change, stop and report. Post on #1070."
**Input:** `T39-win/hp/data/lowD_states/lowDvh96_D3.3500_M96.npz` from origin/main of the raw repository, git blob 255be3715930bf22d449bf243ca3a541c143e67d (checked), copy `~/scratch1070/T39-win/hp/data/lowD_states/`; meta: D 3.35, M 96, 13 nodes 0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8, kt 36, kc 100, ks 250, no stored step plan; n 5377; Delta 3.3234620916757938 + 2.1782756359383167e-16. T39-win also holds `lowDvh41_D3.3500_M128_fail.npz` (a failed M 128 solve at this D from another start): the lift can fail.
**Orchestrator:** `run_d335.py A` (gamma at M 96) and `run_d335.py B` (the lift, judged after each Newton call as in the M 96 pair with run_m96.py's `decide()`, then gamma at M 128 once A has finished with exactly one sign change). A and B share nothing until B's last stage, so they run side by side, 4 threads each (8 logical CPUs, nothing else of mine running), each stage under its own cap of 3 h. The order lists the two parts in sequence; running the independent ones together changes no number and saves about the length of A. Selftest: `selftest_d335.log` (4 of 4 pass), `selftest_d335_mutate.log` (the mutated rule exits 1 with 1 case failing); dry runs checked the commands (`DRY=1`).
Commands, from `~/Source/choptuik-large-d-1058b` (hp 8179068d) at nice 10: A: `python -u hp/lowD_gamma.py lowD_gamma_D3.35_M96.jsonl <input> --threads=4 --polish=2 --xtol=1e-11 --lam0=3.4094`; B1: `cd hp && python -u lowD_dd.py lift128_d335.jsonl --start <input> --Ms 128 --nodes <its 13> --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 4 --tag lowD1070b`; B2: A's `lam` as `--lam0`, otherwise A's command on the M 128 state `states/lowD1070b_D3.3500_M128.npz`.
**Readings, fixed now.** Lift: as for the M 96 pair (converged at max|F| <= 1e-27 on the checkpoint's own plan with the planted +1e-20 reading 1e-20 once max|F| <= 1e-22; at the floor at <= 1e-26 with a gain under a factor 2; stalled otherwise; a lift that fails or stalls stops B and is reported). Each gamma stage (the issue's): exactly one sign change and F after the polish below 1e-27; no sign change: stop and report (B2 does not start if A has none). Then gamma(128) - gamma(96) and both against 0.2933033 (the GammaList's seven digits: a rounding of 5e-8 in the reference).
**Predictions, registered before the runs:**
- A: a sign change in the first grid (lam0 +- 1e-4) about 55%, in the second (+- 1e-3) about 35%, none about 10%; exactly one given a change about 90%; F after the polish below 1e-27 about 70%; 8 to 14 determinants; wall 8 to 25 min (about 65%; the M 96 determinant at D 3.15, n 6913, took 140 s, here n 5377, so about 65 s by n^3);
- B1: converged at <= 1e-27 about 75% (a failure like T39's about 20%); 4 to 6 Newton calls (about 60%), each 30 to 90 s, 2 to 8 min in all (about 60%);
- B2: one sign change about 85% (given A has one); 8 to 12 determinants at about 155 s each (n 7169), 20 to 45 min (about 65%);
- |gamma(128) - gamma(96)| between 1e-9 and 1e-6 about 60%;
- gamma(96) within 1e-5 of 0.2933033 about 65%, gamma(128) within 1e-6 about 45%.

## Result of the D 3.35 pair (written 2026-11-21 23:38:28 UTC): A passes, gamma(3.35, M 96) = 0.29330274206849105; the lift to M 128 fails, so B2 is not run
**A (gamma at M 96)** (`stageA_gamma96_d335.log`, `lowD_gamma_D3.35_M96.jsonl`; 23:18:12 to 23:37:33 UTC, script 1159.6 s): the polish found the input at the floor (|F| 7.65e-30, converged at its first step, no step taken); 7 determinants.
| lam | sign | ln\|det\| | seconds |
|---|---|---|---|
| 3.4093 | -1 | 1161.812031 | 181.2 |
| 3.4094 | -1 | 1160.715951 | 181.6 |
| 3.4095 | +1 | 1160.909054 | 186.6 |
| 3.409445187354 | -1 | 1157.153151 | 213.3 |
| 3.409446476108 | +1 | 1150.247294 | 102.6 |
| 3.409446474818 | -1 | 1142.935949 | 88.6 |
| 3.409446474823 | +1 | 1144.506520 | 88.0 |
The first grid (lam0 +- 1e-4) held the change (-1 at 3.4094, +1 at 3.4095); brentq took it to xtol 1e-11. Record: lam 3.409446474818443, gamma 0.29330274206849105, F 7.65441597097263e-30, n_signchanges 1, n_det 7. Acceptance (`accept_1070.py`): PASS. Against the Vienna GammaList value 0.2933033 (seven digits, so a rounding of 5e-8): gamma(96) - 0.2933033 = -5.58e-07, 11 times that rounding. The determinants ran 181 to 213 s beside the lift and 88 to 103 s after it ended. Resources: wall 19:19.98, user 4497.36 s, 389% CPU, max RSS 1083788 kB (1.03 GiB).
**B1 (the lift to M 128)** (`lift128_d335.log`, `lift128_d335.jsonl`; 23:18:12 to 23:33:53 UTC): FAILED at its first Newton call. Start |F| 3.04e+08 (L 7169, 505 steps); "no decrease along the f64-Jacobian step; retrying with the exact Jacobian", then "no decrease along the Newton step, giving up"; `converged: false, failed: line search`, 936.5 s, exit 0, Delta unchanged. The orchestrator stopped B (`exits_d335.txt`: "STOP: the lift did not reach a converged M 128 state"); B2 was not started and no gamma(128) exists. Failed state `states/lowD1070b_D3.3500_M128_fail.npz` (blob d2adfb27124516a53fe34f683c3b9eb590b91bbc). Resources: wall 15:36.86, user 3485.17 s, 372% CPU, max RSS 1340492 kB (1.28 GiB).
**Diagnostics outside the order** (all read-only: `lowD_dd.py --start_residual_only`, 6 s each, no solve; logs `diag_startres_*_d335.log`). They do not repair the lift.
| start state, target M | start max\|F\| | per block (14 blocks at 13 nodes) |
|---|---|---|
| D 3.35 M 96, M 96 (its own plan, f64) | 1.30e-14 | 1.1e-16 to 2.8e-16 in every block |
| D 3.35 M 96, lifted to M 128 | 3.04e+08 | block 0: 3.0e+08; then 4.1e-05 5.3e-05 1.6e-05 1.9e-08 1.6e-09 3.8e-10 1.2e-10 5.2e-11 3.3e-11 1.4e-11 1.0e-11 7.7e-12 1.1e-11 |
| D 3.15 M 96 (my state of the M 96 pair, 17 nodes from 0.000625), lifted to M 128 | 1.16e-03 | every block between 5e-08 and 1.2e-03 |
So the upward lift works in general (the D 3.15 control), and the 3e8 sits in block 0 of the D 3.35 state, whose nodes start at 0.005 (the D 3.15 states start at 0.000625). I did not find why. `--reintegrate` (node states recomputed from the centre data) gives NaN from block 3 on at M 96 and M 128 alike and leaves block 0 unchanged: no help. The kernel's allowed M are 8, 16, 32, 40, 48, 64, 80, 96, 128, 160, ... (the error of `--Ms 104,112,...` in `diag_startres_Mscan_d335.log`): there is no M between 96 and 128, so a staged lift is not available.
**What T39 saw at this D** (its `lowD_logs/local_t41.log`, read as data): continuing at M 128 downward from its D 3.4 state, D 3.3875 converged (|F| 3.5e-30, 14 steps, 2636 s), D 3.375 stalled (|F| 6.7e-05 after 24 steps, 5733 s) and D 3.35 failed at its first step (start |F| 0.65, "giving up", 1487 s). Those are continuations in D from M 128 states, not lifts, and the D 3.35 M 128 state does not exist in T39-win except as `lowDvh41_D3.3500_M128_fail.npz`.
**Predictions against the result:**
| prediction | result |
|---|---|
| A: change in the first grid (about 55%); exactly one (about 90%); F below 1e-27 (about 70%) | right in all three (F 7.65e-30) |
| A: 8 to 14 determinants | 7: wrong |
| A: wall 8 to 25 min (about 65%) | 19.3 min: right (the n^3 scaling to 65 s per determinant was wrong: 88 to 103 s alone) |
| B1: converged at <= 1e-27 (about 75%); 4 to 6 calls, 2 to 8 min | failed at call 1 after 15.6 min: the 20% case, as T39's failed M 128 at this D allowed |
| B2 (one change, 8 to 12 determinants, 20 to 45 min) and |gamma(128) - gamma(96)| in 1e-9 to 1e-6 | not run |
| gamma(96) within 1e-5 of 0.2933033 (about 65%) | 5.6e-07: right; gamma(128): not run |
**Not run (the coordinator's choice):** the M 128 lift needs another route. Ones I can see, none started: (a) a smaller-x0 node set for D 3.35 (the D 3.15 control lifts), which re-nodes the state (lowD_dd has the machinery) and is a larger task; (b) continuation at M 128 in small D steps down from T39's converged D 3.3875 state (T39 stalled at 3.375 with its steps, so the steps would be smaller, at 2636 s a point); (c) a resolution estimate from below instead, gamma at M 80 (lowD_dd --Ms 80 from this state, a downward lift as the D 3.15 one) beside gamma(96).

## D 3.35 option (c): the resolution change gamma(96) - gamma(80) (written 2026-11-21 23:40:23 UTC, before the runs)

Order (coordinator's hc after my 23:39 UTC report), quoted: "the M 128 failure is accepted as reported. Take the cheapest option, (c): lift the D 3.35 M 96 state down to M 80 (lowD_dd.py --Ms 80, its own nodes, kt, kc, ks; --jac f64 --tol 1e-29 --threads 4 --tag lowD1070c), then gamma at M 80 with --lam0 3.409446474818443, the same settings, nice 10, caps 2 h each. Report gamma(96) - gamma(80) as the resolution change at D 3.35, named as such (not a bound). If it is below about 1e-7, the 5.6e-7 gap to the Vienna value is theirs; if it is above, it is ours. Post on #1070."
**Orchestrator:** `run_d335c.py` (the lift judged after each Newton call with run_m96.py's `decide()`, then gamma at M 80; names and caps of this task, 2 h each). Input as above (blob 255be371…, 13 nodes, kt 36, kc 100, ks 250). Commands, from `~/Source/choptuik-large-d-1058b` (hp 8179068d), nice 10: lift `cd hp && python -u lowD_dd.py lift80_d335c.jsonl --start <input> --Ms 80 --nodes <its 13> --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 4 --tag lowD1070c`; gamma `python -u hp/lowD_gamma.py lowD_gamma_D3.35_M80.jsonl states/lowD1070c_D3.3500_M80.npz --threads=4 --polish=2 --xtol=1e-11 --lam0=3.409446474818443`. A dry run checked the commands; the lift watcher and `decide()` are the ones of the M 96 pair and the D 3.35 pair (selftests `selftest_decide*.log`).
**Start reading (read-only, `--start_residual_only`, `diag_startres_M80_d335c.log`):** D 3.35 M 96 state lifted to M 80: start max|F| 6.81e-01 (L 4481); block 0: 6.8e-01, blocks 1 to 3: 9.9e-05 1.3e-04 3.1e-05, then 2.2e-07 falling to 1.7e-10. Block 0 dominates again, as it did at M 128 (3e8), but at M 80 it is 0.68: T39's failed D-continuation start at M 128 was 0.65.
**Readings, fixed now.** Lift (as before): converged at max|F| <= 1e-27 on the checkpoint's own plan with the planted +1e-20 reading 1e-20 once max|F| <= 1e-22; at the floor at <= 1e-26 with a gain under a factor 2; stalled otherwise; a failed or stalled lift stops the task and is reported (no gamma(80), no resolution change). Gamma at M 80 (the issue's): exactly one sign change and F after the polish below 1e-27. Then gamma(96) - gamma(80), named the resolution change at D 3.35 between M 80 and M 96 (not a bound); the coordinator's reading: below about 1e-7 the 5.6e-7 gap of gamma(96) to the Vienna 0.2933033 is theirs, above it is ours. What the change shows and does not: two resolutions, no extrapolation; it does not give M 128's value.
**Predictions, registered before the runs:**
- the lift converges at <= 1e-27 about 50% (the start has block 0 at 0.68, and the M 128 lift and T39's M 128 steps at this D failed from similar starts; the D 3.15 downward lift, start 7e-4, converged in 4 calls); if it does, 5 to 12 Newton calls, each 10 to 30 s (n 4481), so 2 to 6 min (about 60%);
- gamma at M 80 given a converged lift: a sign change in the first grid (lam0 +- 1e-4) about 75%, exactly one about 90%, F after the polish below 1e-27 about 70%; 7 to 12 determinants at 50 to 90 s each, so 8 to 20 min (about 60%);
- |gamma(96) - gamma(80)| below 1e-7 about 20%, between 1e-7 and 1e-5 about 60%, above 1e-5 about 20%.

## Run 1 of the M 80 lift stopped at 23:41:37 UTC by my own stall rule, which was wrong here; run 2 follows the order as written (written 2026-11-21 23:42:18 UTC, before run 2)
Run 1 (started 23:40:31 UTC): start |F| 6.81e-01 (L 4481), Newton calls of 11.1 to 11.7 s each: call 1 |F| 6.81e-01 (|dz| 124, lam 0.00195), call 2 6.79e-01 (lam 0.0625), call 3 6.39e-01 (lam 0.0625), call 4 6.07e-01 (lam 0.25), call 5 5.16e-01 (lam 0.25). The watcher measured the checkpoints after calls 1, 3 and 5 (calls 2 and 3 landed together): max|F| 0.679, 0.6066, 0.3541, the planted control reading the same as max|F| each time (masked, valid). At call 5 `decide()` said stalled (0.3541 > 0.6066 / 2) and `run_d335c.py` stopped lowD_dd.py by the pids of its session (`exits_d335c_run1.txt`, `run1_lift80_d335c.log`). max|F| was still falling (0.68 to 0.35 in 5 calls) and the call limit of lowD_dd.py is 14 calls, 2.6 min in all, so the stop saved nothing and could be a false stop: it cut the ordered command short. **The error is mine:** I registered the rule "above 1e-26 after 3 or more calls with no factor 2 gain: stalled" for the M 96 pair's regime (max|F| 1e-12 to 1e-29) and applied it unchanged to a lift that starts at 0.68, where damped steps (lam 0.002 to 0.25) fall slowly.
**Change, made before run 2 and for this reason only:** the watcher no longer stops the lift on "stalled" (it logs the verdict and goes on); it still stops on converged or floor (max|F| <= 1e-27, or <= 1e-26 with a gain under a factor 2) and on a failed planted control, and lowD_dd.py ends by itself at its 14 Newton calls or on a line-search failure. The thresholds for converged and the floor are unchanged. Run 2 starts from the input again, not from run 1's checkpoints (they are kept as `states/run1_lowD1070c_ckpt_after_call{1,3,5}.npz` and `states/run1_c_hp_ckpt.npz`). The order's command is unchanged: `--Ms 80 ... --tag lowD1070c` with lowD_dd's default 14 calls; a larger `--it_max` is not in the order and is not used.
**Predictions for run 2, registered before it:** converged within the 14 calls about 15% (from 0.35 at call 5 with damped steps; T39's M 128 steps at D 3.3875 converged from 1.6e-3 in 14 steps and at D 3.375 stalled at 6.7e-5 after 24); ends "NOT converged" after 14 calls about 65%; ends on a line-search failure (`giving up`) before that about 20%. If converged, gamma at M 80 as predicted above; if not, no gamma(80) and no resolution change, and I report where it stood.

## Result of option (c), run 2 (written 2026-11-21 23:45:51 UTC): the lift to M 80 did not converge in its 14 Newton calls; no gamma(80), no resolution change
Run 2 (23:42:27 to 23:45:19 UTC; `lift80_d335c.log`, `lift80_d335c.jsonl`, `exits_d335c.txt`): the ordered command ran to its own limit: "D 3.35 M 80: NOT converged, |F| 2.8e-02 after 14 iterations (170s)"; record `converged: false`, F 0.02803612232763945, Delta 3.3225581605495553 (+8.2e-17), exit 0. Start |F| 6.8e-01 (L 4481, 389 steps), as the read-only diagnostic had it.
| call | `|F|` at its start | `|dz|` | lam | Delta after | max\|F\| of the checkpoint (watcher; planted control masked and valid) |
|---|---|---|---|---|---|
| 1 | 6.81e-01 | 1.24e+02 | 0.00195 | 3.323468824 | 0.679 |
| 2 | 6.79e-01 | 5.24 | 0.0625 | 3.323189305 | |
| 3 | 6.39e-01 | 3.90 | 0.0625 | 3.323115920 | 0.6066 |
| 4 | 6.07e-01 | 3.04 | 0.25 | 3.323264127 | |
| 5 | 5.16e-01 | 3.68 | 0.25 | 3.322079961 | 0.3541 |
| 6 | 3.54e-01 | 80.4 | 0.0156 | 3.322948010 | |
| 7 | 2.40e-01 | 13.2 | 0.0625 | 3.321481755 | 0.05233 |
| 8 | 5.23e-02 | 11.5 | 0.0312 | 3.321608795 | 0.05118 |
| 9 | 5.12e-02 | 11.5 | 0.0312 | 3.321781627 | |
| 10 | 5.16e-02 | 1.95 | 0.0625 | 3.322033307 | 0.05137 |
| 11 | 5.14e-02 | 22.7 | 0.0312 | 3.322197037 | |
| 12 | 3.79e-02 | 16.3 | 0.00781 | 3.322316901 | 0.03765 |
| 13 | 3.77e-02 | 1.78 | 0.125 | 3.322486667 | |
| 14 | 3.42e-02 | 2.32 | 0.125 | 3.322558161 | 0.02804 |
Every step was damped (lam 0.002 to 0.25); max|F| fell 24-fold in 14 calls and was still falling slowly (0.0523 to 0.0280 over the last 7 calls). Delta moved from 3.3234688 (call 1) to 3.3225582, and the input's Delta is 3.3234621: the iterate has moved 9e-4 away from the M 96 value while max|F| is still 0.028, far larger than any resolution change I expect (the D 3.15 pair's Delta(96) - Delta(128) was 1.6e-6). I did not test whether it is heading to a different solution. The `decide()` verdict "stalled" appeared at calls 5, 8, 10, 12 and 14 and was not acted on (run 2's rule above). The failed state is `states/lowD1070c_D3.3500_M80_fail.npz` (blob 055288683e197cffef66c66acfa5480d2a404cd8); every checkpoint after calls 1, 3, 5, 7, 8, 10, 12, 14 is in `states/`.
**Not run:** gamma at M 80 (needs a converged state), so there is no gamma(96) - gamma(80) and the coordinator's reading (below or above about 1e-7) is not answered: the 5.6e-7 gap of gamma(96) to the Vienna 0.2933033 stays open. **Not done without the coordinator:** a larger `--it_max` (calls take 11 to 14 s, so 60 calls are about 12 min); T39's M 128 steps at D 3.375 stalled after 24 steps and its D 3.3875 converged in 14, so a rerun may converge or may stall again.
**Predictions against run 2:** "ends NOT converged after 14 calls about 65%": right; converged within 14 (about 15%) and line-search failure (about 20%): not what happened. The 2 to 6 min wall for a converged lift: the run took 2:50 wall.
**Resources** (4 threads, nice 10, nothing else running): wall 2:50.14, user 632.97 s, system 4.85 s, 374% CPU, max RSS 420724 kB (0.40 GiB); MemAvailable never below 28619 MiB, no alert. Run 1 (cut short by my stall rule at call 5, 1.5 min) is kept as `run1_*`.

## D 3.45 pair, no lift (written 2026-11-21 23:47:40 UTC, before the runs)

Order (coordinator's hc after my 23:46 UTC report: "no on --it_max 60 ... D 3.35 stays at M 96 only"), quoted: "a pair with no lift: D 3.45 from T39's stored states, raw T39-win/hp/data/lowD_states/lowDvh41_D3.4500_M96.npz and _M128.npz. lowD_gamma.py on each, --threads=4 --polish=2 --xtol=1e-11 --lam0=3.18611 (the Vienna gamma 0.3138622 at D 3.45), nice 10, cap 3 h each, M 96 first and then M 128 with lam0 set to M 96's lam. Readings as in the issue; report gamma(128) - gamma(96) and both against 0.3138622. Post on #1070."
**Inputs** (from origin/main of the raw repository, git blobs checked against the tree, copies in `~/scratch1070/T39-win/hp/data/lowD_states/`): M 96 `lowDvh41_D3.4500_M96.npz` blob 1b515220e5bb86eff98072b3c59762583124a1f9, n 5377, Delta 3.398624651987525 + (-4.07e-17); M 128 `lowDvh41_D3.4500_M128.npz` blob 92c8c5ccbffa2894ea3fde83b6d6acb5c17b5705, n 7169, Delta 3.3986246505411715 + (-1.44e-16). Both: D 3.45, 13 nodes 0.005 ... 0.8, kt 36, kc 100, ks 250. Delta(128) - Delta(96) = -1.45e-09 (the states' own values, before any polish).
**Orchestrator:** `run_d345.py` (A, then B only if A has exactly one sign change; the commands are `lowD_gamma.py` of the order, from `~/Source/choptuik-large-d-1058b`, hp 8179068d, nice 10, cap 3 h each, 4 threads; sequential, as ordered, because B's lam0 is A's lam). A dry run checked the commands; `lam_of` is `run_d335.py`'s, with its selftest (`selftest_d335*.log`).
**Readings, fixed now (the issue's).** Each stage: exactly one sign change in the bracket and F after the polish below 1e-27 (`accept_1070.py`); no sign change in A: stop and report, B not started. Then gamma(128) - gamma(96), named the resolution change at D 3.45 between M 96 and M 128 (a difference of two resolutions, not a bound), and both against the Vienna 0.3138622 (seven digits: a rounding of 5e-8).
**Predictions, registered before the runs:**
- A: a sign change in the first grid (lam0 +- 1e-4) about 85% (lam0 has 5 decimals, a rounding of 5e-6; at D 3.35 our lam was 4.6e-5 from the Vienna lam0); exactly one about 90%; F after the polish below 1e-27 about 75% (D 3.35's M 96 input was at 7.7e-30); 7 to 12 determinants at 80 to 110 s each (n 5377, alone on the machine), so 10 to 22 min (about 65%);
- B: a sign change in the first grid about 90% (lam0 = A's lam); exactly one about 90%; F below 1e-27 about 70%; 7 to 12 determinants at 150 to 220 s each (n 7169), so 20 to 40 min (about 60%);
- |gamma(128) - gamma(96)| between 1e-10 and 1e-7 about 65% (the stored states' Delta differ by 1.45e-09 here, against 1.6e-6 at D 3.15; #628 had 3.77e-9 at D 3.5);
- gamma(96) within 1e-6 of 0.3138622 about 60% (D 3.35 was 5.6e-7 below it, D 3.5 was 1.4e-7 from the list), gamma(128) within 1e-6 about 65%.

## Result of the D 3.45 pair (written 2026-11-22 00:20:50 UTC): both PASS; gamma(96) = 0.3138622492236686, gamma(128) = 0.3138622497447941, gamma(128) - gamma(96) = +5.211e-10
**A (M 96)** (`stageA_gamma96_d345.log`, `lowD_gamma_D3.45_M96.jsonl`; 23:47:49 to 23:57:09 UTC, script 559.3 s): the polish found the input at the floor (|F| 7.02e-30, converged at its first step, no step taken); 6 determinants. Record: lam 3.1861111123541552, gamma 0.3138622492236686, F 7.019629461302597e-30, n_signchanges 1, n_det 6. Acceptance: PASS.
| lam | sign | ln\|det\| | seconds |
|---|---|---|---|
| 3.18601 | -1 | 1021.134 | 81.7 |
| 3.18611 | -1 | 1016.677 | 84.8 |
| 3.18621 | +1 | 1021.216 | 81.6 |
| 3.186111056259 | -1 | 1013.690 | 87.5 |
| 3.186111112354 | +1 | 1003.645 | 84.8 |
| 3.186111112349 | -1 | 1003.698 | 88.0 |
**B (M 128, lam0 = A's lam 3.1861111123541552)** (`stageB_gamma128_d345.log`, `lowD_gamma_D3.45_M128.jsonl`; 23:57:09 to 00:20:29 UTC on 22 Nov, script 1390.0 s): the polish found the input at the floor (|F| 5.05e-30, no step taken); 6 determinants. Record: lam 3.186111107064052, gamma 0.3138622497447941, F 5.047477198250068e-30, n_signchanges 1, n_det 6. Acceptance: PASS.
| lam | sign | ln\|det\| | seconds |
|---|---|---|---|
| 3.186011112354 | -1 | 1336.366 | 204.9 |
| 3.186111112354 | +1 | 1326.589 | 208.3 |
| 3.186211112354 | +1 | 1336.506 | 209.3 |
| 3.186111106682 | -1 | 1323.961 | 212.4 |
| 3.186111107064 | -1 | 1311.575 | 213.6 |
| 3.186111107069 | +1 | 1319.625 | 211.8 |
The M 128 root lies below the M 96 root: lam(96) - lam(128) = 5.290e-09. The xtol 1e-11 of each search is its stopping tolerance, not an error bar of the discretization.
**The resolution change at D 3.45, named as such (two resolutions, not a bound):** gamma(128) - gamma(96) = 0.3138622497447941 - 0.3138622492236686 = +5.211e-10 (decimal arithmetic on the two records).
**Against the Vienna GammaList value 0.3138622** (seven digits, so a rounding of 5e-8): gamma(96) - 0.3138622 = +4.922e-08; gamma(128) - 0.3138622 = +4.974e-08. Both lie inside that rounding half-unit and both round to the printed 0.3138622; the list's seven digits do not resolve a difference below 5e-8. For comparison, D 3.35's gamma(96) lay 5.6e-07 below its Vienna value (no M 128 there), and #628's gamma(3.5) differs from the list by 1.4e-7 (M 128). Delta(128) - Delta(96) of the stored states was -1.45e-09.
**Predictions against the result:**
| prediction | result |
|---|---|
| A: change in the first grid (about 85%), exactly one (about 90%), F below 1e-27 (about 75%) | right in all three (F 7.0e-30) |
| B: change in the first grid (about 90%), exactly one (about 90%), F below 1e-27 (about 70%) | right in all three (F 5.0e-30) |
| 7 to 12 determinants in A and in B | 6 in each: wrong |
| A wall 10 to 22 min (about 65%) | 9.3 min (559 s): just below |
| B wall 20 to 40 min (about 60%) | 23.2 min: right |
| |gamma(128) - gamma(96)| between 1e-10 and 1e-7 (about 65%) | 5.2e-10: right |
| gamma(96) and gamma(128) within 1e-6 of 0.3138622 (about 60%, about 65%) | 4.9e-08 and 5.0e-08: right |
**Resources** (4 threads each, nice 10, nothing else running, sequential as ordered): A wall 9:19.71, user 2141.75 s, 385% CPU, max RSS 1069900 kB (1.02 GiB); B wall 23:10.39, user 5442.87 s, 393% CPU, max RSS 1945512 kB (1.86 GiB); MemAvailable never below 27706 MiB, no alert. Determinants took 82 to 88 s at M 96 (n 5377) and 205 to 214 s at M 128 (n 7169).

## D 3.475 pair, no lift (written 2026-11-22 00:22:14 UTC, before the runs)

Order (coordinator's hc after my 00:21 UTC D 3.45 report: "both PASS accepted"), quoted: "the last stored pair in that range: D 3.475 from raw T39-win/hp/data/lowD_states/lowDvh41_D3.4750_M96.npz and _M128.npz, the same commands with --lam0 from the Vienna list interpolated at 3.475 (gamma 0.3182605, so --lam0=3.14208; an interpolation through D 3.4, 3.45 and 3.5), M 96 first and then M 128 with lam0 set to M 96's lam, nice 10, caps 2 h. Report gamma(128) - gamma(96) and both against the interpolated Vienna value. Post on #1070."
**Inputs** (from origin/main of the raw repository, git blobs checked against the tree, copies in `~/scratch1070/T39-win/hp/data/lowD_states/`): M 96 `lowDvh41_D3.4750_M96.npz` blob 18811cf5502ad4c0dafa5e31de83446e93472df4, n 5377, Delta 3.41161964251176 + (-4.78e-17); M 128 `lowDvh41_D3.4750_M128.npz` blob d1467b1e3c69dd8b3d81c50b6816c9fc9b2c16a4, n 7169, Delta 3.4116196409153514 + 1.79e-16. Both: D 3.475, 13 nodes 0.005 ... 0.8, kt 36, kc 100, ks 250. Delta(128) - Delta(96) = -1.60e-09 (the stored states' own values).
**Orchestrator:** `run_d3475.py`, `run_d345.py` with the D, the blobs, lam0 3.14208 and the cap of 2 h changed (a dry run checked the commands). A, then B only if A has exactly one sign change, B's lam0 = A's lam; `lowD_gamma.py --threads=4 --polish=2 --xtol=1e-11` from `~/Source/choptuik-large-d-1058b` (hp 8179068d), nice 10.
**What the comparison value is:** 0.3182605 is an interpolation of the Vienna list through D 3.4, 3.45 and 3.5 (the coordinator's), not a list entry: it carries the list's seven-digit rounding (5e-8 each) and an interpolation error I cannot bound. A difference below about 1e-6 from it is not evidence of anything. From the two lam0 of the last pairs, the slope d(lam)/d(gamma) is about -10 here ((3.18611 - 3.14208) / (0.3182605 - 0.3138622)).
**Readings, fixed now (the issue's).** Each stage: exactly one sign change in the bracket and F after the polish below 1e-27 (`accept_1070.py`); no sign change in A: stop and report, B not started. Then gamma(128) - gamma(96), named the resolution change at D 3.475 (two resolutions, not a bound), and both against the interpolated 0.3182605.
**Predictions, registered before the runs:**
- A: a sign change in the first grid (lam0 +- 1e-4) about 90% (an interpolation error of 1e-5 in gamma moves lam by 1e-4); exactly one about 90%; F after the polish below 1e-27 about 75% (the D 3.35 and D 3.45 M 96 inputs were at 7e-30); 5 to 8 determinants at 80 to 90 s, so 7 to 12 min (about 65%);
- B: a sign change in the first grid about 90%; exactly one about 90%; F below 1e-27 about 75%; 5 to 8 determinants at 205 to 215 s, so 20 to 30 min (about 65%);
- |gamma(128) - gamma(96)| between 1e-10 and 1e-8 about 75% (5.2e-10 at D 3.45, 3.77e-9 at D 3.5 in #628; the stored Delta differ by 1.6e-9 here);
- both gamma within 1e-6 of 0.3182605 about 55% (the interpolation's own error is the unknown).
