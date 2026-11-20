# I1025-win: the l = 1 DSS solution at k_c 63 from D 17 to 20, its growth rate, and the eigenvalues near it on the Mac's k_c 47 and 55 states (#1025, winb's lane)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, 4 cores / 8 threads, 32 GB, Windows 11), agent claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025 (xfkappa's #1025, lane handed over by the coordinator). Status: **running** (started 2026-11-20 00:14:05 UTC; publishes at 03:10, 03:23 and 04:30 UTC; this README is rewritten at each publish). **The eigenvalue scans (`eigs_a.log`, `eigs_b.log`) are INVALID and were stopped at 03:21 UTC** (see Changes during the run).

## Question

#1025 asks whether the l = 1 multiplet's growth rate at finite D heads to #994's 1.997 or to ELL.md's 2.09 to 2.31. Its comment of 2026-11-20 00:08 UTC found lambda_1 at k_c 47 under-resolved at D 17.5 by about 0.07 (k_c 55 gives 1.9522284 against 1.8831583), with the two k_c moves of opposite sign (-0.011 at D 17, +0.069 at D 17.5), so two k_c do not pin lambda_1 there, and k_c 55's psi-constraint (7.9e-4 at D 17, 1.3e-3 at D 17.5, about 1.8x per half unit of D) likely cannot reach D 20. This lane adds a third k_c at D 17 and 17.5, continues at k_c 63 from D 17.5 to 20, and scans the eigenvalues near lambda_1 on the Mac's stored states. Numerical evidence only; the reading belongs to the issue.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1025`, detached at `56b8f680` (branch `wip/ell1-highD`, `solver/matter/ell_win1025.sh` with `ell_refine.py`, `ell_leap.py`, `ell_eigs.py`, `dss_ell.py`). The worktree has `core.autocrlf=true`, so I re-checked out `ell_win1025.sh` alone with LF (`git -c core.autocrlf=false checkout -- solver/matter/ell_win1025.sh`; the blob is unchanged), since bash does not run it with CRLF |
| inputs (RAW) | the push worktree `choptuik-large-d-raw-754`, detached at origin/main `a1ccd3af` (the coordinator asked for `aa5f2d40` or later); the six input states of `I1025-mac/out` (`sol_l1kc55Fs1025_D17.0000`, `_D17.5000`, `sol_l1kc47Fr1025_D16.0000`, `_D16.5000`, `_D17.0000`, `_D17.5000`, `.npy`) equal the git blobs byte for byte (`cmp`) |
| interpreter | `venv-choptuik-314`: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0 |
| run | `start_win1025.cmd` (detached, BelowNormal priority, which the issue did not ask for and I use on this machine as usual): `bash ell_win1025.sh` from `solver/matter` with `RAW`, `PY`, `LOGS` set. Four processes at 2 BLAS threads each (P1 k_c 63 starts, then the continuation; P2 lambda on the continuation's states; P3a and P3b the eigenvalue scans), every python under a 12 h `timeout` |
| nothing written in the raw repo while jobs run | outputs go to the code worktree's `solver/matter/data/` and `logs1025/`; the `publish` step copies them into this folder |

## Commands (as `ell_win1025.sh` runs them, from `solver/matter`)

```
ell_eigs.py planted ; ell_eigs.py planted --mutate=beyn                                             # checks.log
ell_refine.py l1kc55Fs1025 55 l1kc63Fw1025 63 1 17,17.5 2.025718689014619 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60       # P1, kc63_start.log
ell_leap.py l1kc63W1025 1 63 data/sol_l1kc63Fw1025_D17.0000.npy 17 data/sol_l1kc63Fw1025_D17.5000.npy 17.5 20 0.125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold   # P1, leap_kc63.log
ell_refine.py l1kc63W1025 63 l1kc63Fw1025 63 1 18,18.5,19,19.5,20 1.9 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 7200   # P2, lam_kc63.log
ell_eigs.py <state> D kc lambda --r 0 --N 24 --p 12 --dlam 0 --no_polish_complex [--check] --out data/eigs_win1025_{a,b}.jsonl    # P3a, P3b, eigs_a.log, eigs_b.log
    a: kc 47 D 17.5 (--check), D 17, D 16;  b: kc 55 D 17.5 (--check), D 17, kc 47 D 16.5
```

## Checks, fixed before the runs (the coordinator's)

- `logs1025/checks.log` has `planted OK` with exit 0, then `--mutate=beyn` BAD with exit 1. I ran the two once by hand before the start (`pre/planted.log` 6 of 6 true eigenvalues found, exit 0 after 2 s; `pre/planted_beyn.log` 0 of 6 BAD, exit 1), since the script starts its jobs without waiting for them.
- The first job of `eigs_a.log` and of `eigs_b.log` has check (a) <= 1e-6 and (b) <= 1e-12 OK.
- Any failed check stops the lane and is reported.

## Files

| file | what |
|---|---|
| `README.md` | this file |
| `start_win1025.cmd` | the detached launcher |
| `pre/` | the two planted checks run by hand before the start |
| `checks.log` | `ell_eigs.py planted` (exit 0) and its mutation `--mutate=beyn` (exit 1), then the lane's end line |
| `kc63_start.log`, `out/l1kc63Fw1025.jsonl`, `out/sol_l1kc63Fw1025_D*.npy` | k_c 63 at D 17 and 17.5 from k_c 55, with lambda (no lambda at D 18 to 20, by the coordinator's order) |
| `leap_kc63.log`, `out/l1kc63W1025.jsonl`, `out/sol_l1kc63W1025_D*.npy` | `ell_leap --fold` at k_c 63, D 17.5 to 18 (D_end 18 in place of the script's 20) |
| `lam_kc63.log` | lambda at k_c 63 on the continuation's half-integer states (never written: P2 stopped, see Changes) |
| `kc63_D16.5.log`, `out/l1kc63Fw1025b.jsonl`, `out/sol_l1kc63Fw1025b_D16.5000.npy`, `run_D16.5_1025.sh`, `start_D16.5_1025.cmd` | the k_c 63 refine at D 16.5 (the coordinator's job) and its launcher |
| `signtest.log`, `out/signtest_l1kc63_1025.jsonl`, `run_signtests_1025.sh`, `start_signtests_1025.cmd` | xfkappa's `signtest.py` (raw `I1025-mac/signtest.py`, hash a2f53a90): the planted control, then the k_c 63 records at D 17.5, D 16.5 and D 17 (D 17 from 07:18 to 07:31 UTC), and the JSON lines alone |
| `check_1025.py`, `check_D17.5_1025.log`, `check_D16.5_1025.log` | the coordinator's record checks (n_signchanges, 2% test or edge test, distance to the Mac's k_c 55 value); `python check_1025.py --selftest` passes |
| `kc71_D16.5.log`, `out/sol_l1kc71Fw1025_D16.5000.npy`, `run_kc71_1025.sh`, `start_kc71_1025.cmd` | the coordinator's two jobs of 07:20 UTC in one driver: the D 17 signtest, then the k_c 71 refine at D 16.5 (its record `out/l1kc71Fw1025.jsonl` follows when it lands) |
| `eigs_a.log`, `eigs_b.log` | **INVALID.** `ell_eigs` (Beyn's contour method) on the Mac's k_c 47 and 55 states at D 17.5, stopped at 03:21 UTC: its rank test printed `rank = p: raise --p` and M is ill-conditioned along the whole contour. Kept as written; no `out/eigs_win1025_*.jsonl` record was produced |
| `guard_leap_1025.py`, `start_guard_1025.cmd`, `guard_1025.log`, `guard_main.log` | the guard that holds the k_c 63 leap at D 18 (coordinator's order) and its launcher and logs |
| `stop_P1_1025.log`, `stop_P2_1025.log`, `guard_now_main.log`, `start_guard_now_1025.cmd` | the stops of the script's P1 and P2 subshells (exact pids) and the guard's `--now` mode that started the leap at 04:27 |
| `stop_eigs_1025.log` | the stop of the eigenvalue scans: times, pids killed, cause |
| `pre/selftest_guard.log`, `pre/selftest_guard_4threads.log` | the guard's selftests on dummy processes (2 BLAS threads, then 4 with the thread assertion) |
| `main.log` | the script's own stdout and stderr |

## Changes during the run

| time (UTC) | change | why |
|---|---|---|
| 03:14 | `guard_leap_1025.py` started (selftest passed) | the coordinator's order: after D 17.5's lambda the k_c 63 leap goes only to D 18, as one cross-check of the Mac's k_c 55 there, under the same 12 h cap, then stops. The script's P1 subshell already holds `ell_leap.py ... 17.5 20 ...`, so the guard kills only that leap tree at its start and runs the identical command with `D_end` 18 (the leap clamps its last step to `D_end` and saves `sol_l1kc63W1025_D18.0000.npy`), then runs lambda at D 18 on that state (`ell_refine.py l1kc63W1025 63 l1kc63Fw1025 63 1 18 ...`) unless P2 did |
| 03:21 | the eigenvalue scans P3a and P3b stopped by exact pid, their remaining jobs (a: k_c 47 at D 17 and 16; b: k_c 55 at D 17 and k_c 47 at D 16.5) not run | the coordinator's order. A control fired on them: Beyn's rank test prints `rank = p: raise --p` (line 30 of `eigs_a.log` and of `eigs_b.log`, with the singular values of A_0 from 1.2e+16 down to 4.4e+14 in a and 6.6e+17 down to 2.7e+15 in b), and M is ill-conditioned along the whole contour (12 scipy `LinAlgWarning`s per log, rcond 1e-18 to 1e-20). Their output is invalid until `ell_eigs` is fixed. I first read the logs with a filter that hid their indented lines and missed the `rank = p` line; xfkappa found it |
| 03:23 | the guard restarted with 4 BLAS threads for the leap and the lambda run instead of the script's 2 (the guard had not acted yet) | the scans' cores are free, the coordinator's order. The k_c 63 refine of D 17.5 keeps the 2 threads it started with. Threads can change the last bits of a solve; the leap's converged states are judged by F and the psi-constraint as before |
| 03:29 | k_c 63 lambda at D 16.5 added (the coordinator's job), `run_D16.5_1025.sh` | `ell_refine.py l1kc55Fb1025 55 l1kc63Fw1025b 63 1 16.5 2.159124821824751 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60`, 4 BLAS threads, 12 h timeout, from the Mac's k_c 55 state at D 16.5 taken by `git show origin/main:I1025-mac/out/sol_l1kc55Fb1025_D16.5000.npy` (hash 557bfff0f27bb581b705d7bf9592581eb7f03d2e, as required); log `kc63_D16.5.log`, record `out/l1kc63Fw1025b.jsonl`, state `out/sol_l1kc63Fw1025b_D16.5000.npy` (copied by hand, the script's globs miss that tag). Record checks: n_signchanges 1 and lam within 2% of its guess (the same-D k_c 55 lambda); for D 17.5, whose guess is D 17's lambda, n_signchanges 1 and the root not at its bracket's edge (`check_1025.py`, selftest `pre/selftest_check1025.log`) |
| 03:56 | the script's P2 (lambda at k_c 63 on the leap's states, D 18 to 20) stopped by exact pid, subshell winpid 22384 | the coordinator's order: xfkappa found ell_refine's root finder fails past D 17 (det M's sign is set by rounding-floor pivots at D 17.5 and D 18); P2 was in its wait loop, no python child; `stop_P2_1025.log` |
| 03:58 | the guard's lambda-at-D-18 phase turned off | the same order; the leap to D 18 stays and its state is kept for later (`pre/selftest_guard_nolam.log`) |
| 03:59 | `run_signtests_1025.sh` started | the D 17.5 and D 16.5 k_c 63 records are suspect until xfkappa's `signtest.py` (raw `I1025-mac/signtest.py`, hash a2f53a90, extracted by `git show`) passes on them: agree true in both JSON lines and opposite signs at lam - 0.02 and lam + 0.02, run one at a time, 4 threads, timeout 7200. Its planted control printed agree, agree, DISAGREE (03:58:41); output `signtest.log`. A record whose signtest fails is not used |
| 04:27 | the script's P1 subshell stopped by exact pid (winpid 1836, cygwin 782179), and the leap to D 18 started at once by `guard_leap_1025.py --now` at 4 BLAS threads | the coordinator's order, with the cores idle (CPU 43%). The leap needs only the saved D 17 and D 17.5 states, not lambda. P1's child, the k_c 63 refine of D 17.5, keeps running. With its subshells gone the script's main bash ended and wrote `== 2026-11-20 04:27:07 all done` into `checks.log`: that marks the script's end after these stops, not the lane's completion. `stop_P1_1025.log`, `leap_kc63.log`, `guard_1025.log`, `pre/selftest_guard_now.log` |
| 07:19 | `run_kc71_1025.sh` started at 4 BLAS threads, BelowNormal, two jobs in order: (1) `signtest.py` of the k_c 63 D 17 record (lam 2.0265465, around lam -+ 0.02), then (2) `ell_refine.py l1kc63Fw1025b 63 l1kc71Fw1025 71 1 16.5 2.1454677 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60`, k_c 71 lambda at D 16.5 from the k_c 63 D 16.5 state, 12 h timeout, log `kc71_D16.5.log` | the coordinator's order for the cores the finished refine jobs and signtests freed (the leap keeps its 4). At D 16.5 the k_c moves grow (47 to 55 +4.3e-3, 55 to 63 -1.37e-2), so k_c 63 is not converged there. Record checks for k_c 71: n_signchanges 1 and the 2% test against 2.1454677, then a signtest at lam -+ 0.02. Its first 20 min: check that the solve runs (no shape or memory error) and note its process memory |

The planted checks and the first-job checks (a), (b) of the scans below are as measured. They passed, and they do not make the scans' output valid.

## Prediction for the k_c 71 run at D 16.5 (the coordinator's, written 2026-11-20 about 07:20 UTC, before the run)

If the 63 to 71 move of lambda at D 16.5 is under 4.3e-3 in size, D 16.5 converges at k_c 71. If it is as large as 1.37e-2, D 16.5 is not resolved at any k_c run so far, and the slope table marks it so.

## Result (interim, first publish 2026-11-20 03:10 UTC, updated 08:54 UTC)

The checks passed, and lambda_1 at D 17 is in at k_c 63. Everything else is still running.

Checks (the coordinator's):

| check | result |
|---|---|
| `checks.log`: `ell_eigs.py planted` | exit 0, 6 of 6 true eigenvalues found (OK) |
| `checks.log`: `planted --mutate=beyn` | exit 1, 0 of 6 found (BAD, as it must) |
| `eigs_a.log` first job (k_c 47, D 17.5): check (a) <= 1e-6, (b) <= 1e-12 | (a) 1.1e-07 OK, (b) 0.0e+00 OK |
| `eigs_b.log` first job (k_c 55, D 17.5): check (a), (b) | (a) 7.7e-08 OK, (b) 0.0e+00 OK |

lambda_1 at D 17 (`kc63_start.log`, `out/l1kc63Fw1025.jsonl`; the k_c 47 and 55 values are the Mac's, I1025-mac):

| k_c | lambda_1 | move to the next k_c | psi-constraint | delta = lambda_1 - lambda_0 (lambda_0 = 2.1263679, the Mac's D 17 value) |
|---|---|---|---|---|
| 47 | 2.0363787 | -1.066e-2 | 3.9e-3 | -0.08999 |
| 55 | 2.0257187 | +8.278e-4 | 7.9e-4 | -0.10065 |
| 63 | 2.0265465 | | 1.47e-4 | -0.09982 |

- The k_c 63 solve: F 2.28e-10 (from a start of 1.0e-5), 2744 steps, Delta 1.0224394673 against the k_c 55 state's 1.0224395378 (change -7.1e-8), |dDelta/dF| 1.35e9; lambda found by one sign change of det M in 16 evaluations, guess 2.0257187 (k_c 55's value), gamma = 1/lambda = 0.493450.
- The change of lambda_1 from k_c 55 to 63 is 8.3e-4, 13 times smaller than the move from k_c 47 to 55 and of the opposite sign. It does not meet the bar |dlambda| <= 1e-6, and is far below the resolution scale |S| 7.68e-2 the Mac quotes at D 17. lambda_1 at D 17 is 0.0291 above #994's 1.997411.
- Cost: the D 17 start state was saved at 01:17 UTC (63 min after the start), the record came at about 03:08 UTC, 10420 s in all, with four processes running (the Mac's k_c 55 record took 1714 s). D 17.5 is next, then the continuation, and P2's lambda on its states.
- The k_c 63 solve prints many numpy overflow and invalid-value RuntimeWarnings from `dss_ell.py` in `kc63_start.log` (trial steps of the Levenberg-Marquardt solve). The solve ended with F 2.3e-10 and no error; the Mac's k_c 55 start log has none.
- The eigenvalue scans (`eigs_a.log`, `eigs_b.log`) are invalid: see Changes during the run (rank = p, ill-conditioned M along the contour). They were stopped at 03:21 UTC and are kept as written.

Since the first publish, the k_c 63 records at D 17.5 and D 16.5 came in, and each went through the coordinator's checks and xfkappa's signtest. The D 17.5 record failed its signtest and is not used. The D 16.5 record passed. The D 17 record, signtested at the coordinator's request after that (07:18 to 07:31 UTC), passed.

### D 17.5 at k_c 63: signtest fails, record not used

Record (`kc63_start.log`, `out/l1kc63Fw1025.jsonl`, written 06:45 UTC): lam 1.9744811, gamma 0.506462, n_eval 28, 13019 s from the start of the lane (the solved state was saved at 03:40 UTC), Delta 1.0334310 (k_c 55: 1.0334300), F 2.29e-10 from a start of 1.8e-5, 2649 steps, constraint 4.69e-4, |dDelta/dF| 1.15e9.

The coordinator's checks (`check_D17.5_1025.log`, edge rule, reference the Mac's k_c 55 value 1.9522284):

| item | value |
|---|---|
| n_signchanges | 1 (OK) |
| guess | 2.0265465 (lambda at D 17, the only history point) |
| bracket | w 0.06, grid 1.904954, 2.026546, 2.148139 (step 0.121593), root in [1.904954, 2.026546]; `check_1025.py` derives w as the first of 0.02, 0.06, 0.15, 0.35 whose grid holds the root, because the record does not keep it |
| distance to the bracket's edges | 0.572 grid steps from the lower edge, 0.428 from the upper; the edge test (at least 0.05 steps from both, a bar I chose) passes |
| 2% test | -2.57% from the guess, fails; it does not apply at D 17.5, by the coordinator's order |
| lam minus the Mac's k_c 55 value | +2.225e-2 (+1.14%) |

The signtest (control `planted` printed agree, agree, DISAGREE at 03:58 UTC; D 17.5 run from 06:45:45, 4 threads):

| lambda | signs of det(QM), four random Q | agree | singular values below 1e-12 / 1e-15 | smallest three | seconds |
|---|---|---|---|---|---|
| 1.9544811 (lam - 0.02) | 1, -1, 1, -1 | false | 56 / 44 | 7.0e-18, 3.6e-18, 2.0e-18 | 580 |
| 1.9944811 (lam + 0.02) | 1, 1, 1, -1 | false | 56 / 44 | 4.0e-18, 2.5e-18, 1.7e-20 | 458 |

The pass condition is agree true in both lines and opposite signs at the two lambdas. Neither line agrees and the signs are not opposite, so the signtest fails and the record is not used. The lines resemble the planted DISAGREE case (40 singular values at 1e-19): the sign of det M at this state is set by the rounding floor, as xfkappa found at k_c 55.

### D 16.5 at k_c 63: signtest passes

Record (`kc63_D16.5.log`, `out/l1kc63Fw1025b.jsonl`, written 07:02 UTC): lam 2.1454677, gamma 0.466099, n_eval 27, 12759 s from the start at 03:29:33 UTC (state saved 04:13 UTC), Delta 1.0117782 (k_c 55: 1.0117787), F 2.06e-10 from a start of 5.3e-6, 2843 steps, constraint 6.95e-5, |dDelta/dF| 1.64e9.

The checks (`check_D16.5_1025.log`, 2% rule): n_signchanges 1 (OK); guess 2.1591248 (the Mac's k_c 55 lambda at D 16.5), lam is -0.633% from it, so the 2% test passes; bracket w 0.02, grid 2.115942, 2.159125, 2.202307 (step 0.043182), root in [2.115942, 2.159125], 0.684 grid steps from the lower edge and 0.316 from the upper; lam minus the Mac's k_c 55 value -1.366e-2.

The signtest (D 16.5 run from 07:03:03):

| lambda | signs of det(QM), four random Q | agree | singular values below 1e-12 / 1e-15 | smallest three | seconds |
|---|---|---|---|---|---|
| 2.1254677 (lam - 0.02) | -1, -1, -1, -1 | true | 55 / 42 | 8.4e-18, 5.3e-18, 6.4e-19 | 386 |
| 2.1654677 (lam + 0.02) | 1, 1, 1, 1 | true | 54 / 41 | 8.5e-18, 4.7e-18, 1.7e-18 | 365 |

Both lines agree, with the sign -1 at lam - 0.02 and +1 at lam + 0.02: pass, by the coordinator's rule. The passing lines also count 54 and 55 singular values below 1e-12 (the failing D 17.5 lines count 56), so the pass rests on the four random Q agreeing in sign. The reading stays with the coordinator and the issue.

### D 17 at k_c 63: signtest passes

The record is the first publish's (lam 2.0265465). The coordinator flagged only the D 17.5 and D 16.5 records as suspect, and asked for this signtest later (07:20 UTC). It ran from 07:18:58 to 07:30:42 UTC at 4 threads (the control printed agree, agree, DISAGREE at 03:58):

| lambda | signs of det(QM), four random Q | agree | singular values below 1e-12 / 1e-15 | smallest three | seconds |
|---|---|---|---|---|---|
| 2.0065465 (lam - 0.02) | -1, -1, -1, -1 | true | 56 / 44 | 5.0e-18, 2.1e-18, 3.0e-20 | 329 |
| 2.0465465 (lam + 0.02) | 1, 1, 1, 1 | true | 56 / 44 | 6.4e-18, 3.9e-18, 2.0e-18 | 375 |

Both lines agree, with the sign -1 at lam - 0.02 and +1 at lam + 0.02: pass, by the coordinator's rule. The counts of singular values below 1e-12 (56) and 1e-15 (44) are the same as on the failing D 17.5 lines, so the counts do not separate pass from fail; the sign agreement over the four random Q does.

### The leap to D 18 (4 threads, since 04:27 UTC, no lambda), as of 08:54 UTC

| D | h | seconds | constraint | F | Delta | abs dDelta/dF | cos_fold | i_fold | n_null |
|---|---|---|---|---|---|---|---|---|---|
| 17.625 | 0.125 | 3266 | 5.93e-4 | 2.35e-10 | 1.0362004 | 1.21e9 | 0.0769 | 2 | 59 |
| 17.75 | 0.125 | 3033 | 7.11e-4 | 2.43e-10 | 1.0389829 | 1.36e9 | 0.0258 | 3 | 57 |
| 17.8125 | 0.0625 | 3062 | 7.75e-4 | 2.48e-10 | 1.0403799 | 1.46e9 | 0.0585 | 1 | 57 |
| 17.875 | 0.0625 | 2291 | 8.41e-4 | 2.53e-10 | 1.0417808 | 1.60e9 | 0.0849 | 2 | 57 |
| 17.9375 | 0.0625 | 2282 | 9.14e-4 | 2.58e-10 | 1.0431859 | 1.78e9 | 0.0633 | 2 | 57 |

After D 17.75 the leap's fold watch printed `sigma_reg 3.489e-11 -> 1.087e-11, |J^+ dF/dn| 0.204 -> 0.22; h -> 0.0625` and halved its step; it printed no other fold line through D 17.9375. One step remains, D 18, started at 08:25 UTC and about 38 min long (a projection: D 18 near 09:05 UTC). The leap then stops and takes no lambda there.

### k_c 71 at D 16.5 (the coordinator's job of 07:20 UTC, running)

Started 07:30:42 UTC from the k_c 63 D 16.5 state (4 BLAS threads, BelowNormal; `kc71_D16.5.log`, `run_kc71_1025.sh`). The coordinator's check of the first 20 min (made at 07:51): no Traceback and no shape or memory error; 22 RuntimeWarnings (overflow and invalid value from `dss_ell.py` lines 211 to 216, the kind of the k_c 63 solves' trial steps); process 12184 working set 642 MB, peak 1833 MB, CPU 2238 s. The solve saved its state `out/sol_l1kc71Fw1025_D16.5000.npy` at 08:49 UTC (79 min after the start). The lambda search is running, so there is no record, no check and no signtest yet (working set 343 MB at 08:54, peak 1833 MB, CPU 9023 s). The prediction above was written before the run.

### Not yet

The leap's last step (D 18). The k_c 71 lambda at D 16.5, then its record checks (n_signchanges 1, the 2% test against 2.1454677) and its signtest at lam -+ 0.02. The eigenvalue scans are invalid and stopped. The lane's k_c 63 values in use: lambda at D 17 (2.0265465, signtest passed) and at D 16.5 (2.1454677, signtest passed). D 17.5 has none. The reading stays with #1025.
