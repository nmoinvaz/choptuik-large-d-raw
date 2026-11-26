# I1101-win2: is the growing Delta change per k_c step at D 23.0 the RK4 step error? k_c 127 re-solved at kappa 0.7, 0.5, 0.35 (#1101)

Machine win2 (Windows 11, Core Ultra 7 265K, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101 (the record). Written 2026-11-26 20:33 UTC, **before R0 starts**. Beside it, on the same machine, the k_c 135 scan of `I1025-win2/kc135_d23/` (four processes of one thread; it keeps priority).

## Order (coordinator t5, hc 2026-11-26 20:31 UTC), verbatim
"a second task beside your k_c 135 scan, #1101. Read its body; it is the record. In short: re-solve the accepted k_c 127 state at D 23.0 (winb's, raw I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy, blob 7a1b150c) at the same k_c with kappa 0.7 (R0, the control: steps exactly 4179, |Delta - 1.174322923415951| <= 1e-9), then kappa 0.5 and 0.35 (R1, R2) together, with ell_refine.py in D:\choptuik-i1025k79 (48c36355), 6 threads each, Normal, each a WMI process with a cap of 43200 s. Make the raw folder I1101-win2/ and push its README with the issue's bars and commands before R0 starts. Stop and report if R0 fails its control. Report R0, then R1 and R2 with r and E as the issue says. The scan keeps priority: if its evaluations slow by more than 1.5x, tell me."

## The question (issue #1101)
The change of Delta per k_c step at D 23.0 grows instead of shrinking (111 to 119 -1.58e-6, 119 to 127 -2.05e-6, 127 to 135 -3.91e-6; D 23.0625: 127 to 135 -3.76e-6). `dss_ell.freeze_from` sets the RK4 steps per segment from the stiffness k_c omega / |x - c| divided by kappa, so the step counts grow with k_c (4179 to 4441 is 135/127). This task separates the step error from the k_c truncation: it re-solves the accepted k_c 127 state at the same k_c with smaller kappa, so that only the steps change.

## Commands (the issue's, verbatim; from `D:\choptuik-i1025k79\solver\matter`, worktree at 48c36355: `ell_refine.py` 631e5801, `dss_ell.py` 5d28c19e)
```
R0  python ell_refine.py l1kc127wind23 127 l1kc127k070w2 127 1 23.0 2.0992182200 --kappa 0.7  --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
R1  python ell_refine.py l1kc127wind23 127 l1kc127k050w2 127 1 23.0 2.0992182200 --kappa 0.5  --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
R2  python ell_refine.py l1kc127wind23 127 l1kc127k035w2 127 1 23.0 2.0992182200 --kappa 0.35 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```
Input: raw `I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy` (blob 7a1b150c, winb's accepted k_c 127 state; record blob eea03461: kappa 0.7, steps 4179, Delta 1.174322923415951, constraint 1.4638405e-3), in the worktree's `solver/matter/data/` under the same name, blob-checked by the driver before each run. Each run: one process, 6 threads (`OPENBLAS/OMP/MKL/RAYON_NUM_THREADS=6`), Normal priority, started through WMI (`kc71_leap/cim_start.ps1 -Normal`), cap 43,200 s on the exact root pid (`crun`), no retry. **R0 runs first, alone; R1 and R2 start together only after R0 passes its control.** The python is venv-md510 (3.14).

## Acceptance bars, written before the runs (each can fail)
1. **R0 is a pure re-solve (the control).** |F| <= 5e-10, steps exactly 4179, and |Delta_R0 - 1.174322923415951| <= 1e-9. If any fails: stop and report; R1 and R2 then mean nothing.
2. **R1 and R2 converge.** |F| <= 5e-10. Steps 5851 +- 2% (R1) and 8358 +- 2% (R2), i.e. 4179 x 0.7/kappa (5734 to 5968 and 8191 to 8525).
3. **Order check.** r = (Delta_0.7 - Delta_0.5)/(Delta_0.5 - Delta_0.35), Delta_0.7 = Delta_R0. An RK4 error proportional to kappa^4 predicts r = 3.74 ((0.7^4 - 0.5^4)/(0.5^4 - 0.35^4) = 0.1776/0.047494). Report r. **Not formed if |Delta_0.5 - Delta_0.35| < 1e-10.**
4. **Reading.** E = (Delta_0.7 - Delta_0.35) x 16/15, the step error of Delta at kappa 0.7 if the error is proportional to kappa^4. Against the 127 to 135 change of 3.91e-6: **|E| >= 2e-6: the step error dominates the k_c-step changes (kappa must come down before any threshold is quoted); |E| <= 4e-7: the k_c truncation dominates (Delta is not converged in k_c at the 1e-6 level); between: mixed (the follow-on runs).** Also each run's psi-constraint against the source's 1.464e-3.
The reading is computed by `i1101_eval.py` (planted selftest and a mutation; below). My additional report, not a bar: `kc127_syscheck_1025.py` (898ebefa, raw `I1025-mac/checks`) on each result, whose freeze_from step count must come back from the record (a check of the record system at each kappa).
Error bars: Delta, r and E come from single solves each; r and E are differences of solves at the stated kappas, not enclosures; E assumes the kappa^4 law that the order check r tests.

## Follow-on (the issue's)
If the result is mixed or step-dominated: k_c 135 at kappa 0.35 at D 23.0 from win2's accepted state (blob cd134e2c) with the same bars; the k_c shift at fixed kappa is then Delta(135, 0.35) - Delta(127, 0.35). Otherwise win2 goes back to its #1025 lane. I start it only on the coordinator's word.

## Estimates (the issue's) and the load
R0 under 1 h; R1 3 to 6 h and R2 4 to 8 h, run together, about 9 h in all (the k_c 127 to 135 regrid took 5 h 34 min on 8 threads). **The scan keeps priority** (4 processes, one thread each, Normal): I compare its evaluation times (`sec` in its records) with the same lambda's on another process (the repeat of 0.045 on P1 against P2's 0.045) and tell the coordinator if they slow by more than 1.5x. Threads: scan 4 + R0 6 = 10, later 4 + 6 + 6 = 16 of 20 logical CPUs; memory is no limit (a k_c 135 scan process holds 2.3 to 3.1 GB, a regrid 2 to 3.3 GB). Earlier I measured +57 to 67% per evaluation with 12 of my processes on this machine (memory-bandwidth bound), so a slowdown beyond 1.5x with 16 threads is possible and is reported if it happens.

## Files (this folder)
`README.md`; `run_i1101.sh` (the driver: R0, its control, then R1 and R2); `i1101_eval.py` (the table, the control, r and E, with `--selftest` and `--mutate`); per run `R0/`, `R1/`, `R2/`: the record, the state, the log and the exit; the evaluator's output `table.txt`.

## Status
- 2026-11-26 20:33 UTC: README written (bars and commands as the issue gives them); the driver and the evaluator follow, R0 starts after this README is pushed.
