# I1098-mm5/ladder/D1291: D 1291 full direct solve on the Moebius horizon, recipe v2, tail at M 48 to h31 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Command (coordinator's order, 2026-11-26 18:03 UTC), detached, 6 threads, from the ladder folder:

```
KSBAR=1e-70 bash tools/ladder_point2.sh 1291 220 6 <ladder>/D1291 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 31
```

`tools/ladder_point2.sh` (raw a9ed0f2f `I1098-mac-a/tools/ladder_point2.sh`, blob da887d7143bf94d45d99fcd168550d0e56437370, verified; `S300` and `S1000` of the order are the two inputs of `../inputs/`, absolute paths because the script changes directory).
kc 220, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 1954**, raised by 200 (at most 4 times, to 2554) until the jump's ks+200 |dF| is at most KSBAR = 1e-70 (KMAX 31 needs about 1e-70: the gain at kfree 31 is 1.5e47 at D 300).
Stages (`run.log`, each log and state in its folder): `jump/` (the held solve at M 32 from a degree-1 fit in 1/n to the two inputs, double-double solve, qd check), `rls/` (h5..h11 to tol 1e-36), `rls13/` (h13 to 1e-48, ddelta 1e-25, octo-double residual),
`tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h31, qq, od, tol 1e-48, ddelta 1e-25). fastmul6, Python 478e9d86.

## Bars, written before the run (coordinator's order)

- The jump converges, and the ks it settled on is logged.
- h5..h13 are each released, and the tail falls.
- Stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial (D 432's u tail), or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped (amended 2026-11-26 19:01 UTC, coordinator's order; the order first read: any inner solve that does not converge).
- Reported: the final Delta, each stage's time and the ks used.

## The D 1291 chain on fastmul7 (coordinator's order, 2026-11-26 21:30 UTC)

`tools3/d1291_then_1549_mm5.sh` (raw 42e99e7d4 `I1098-mac-a/tools/mm5/d1291_then_1549_mm5.sh`, blob 6893d73ff6f623685fc872d2e68a6a41775345af, verified), detached, started now; it runs `tools3/tools3_check.sh` first (7 "ok", `tools3/check2.log`) and exports fastmul7 (`~/Source/choptuik-fastmul7` at d40a9c62, `~/Source/fastmul7-site`), `INNER_CHORD=0`. Each step after the one before, on 6 threads:

0. waits for this folder's `run.log` to read "end " (the fastmul6 M 48 tail to kmax 31, started 19:51 UTC, expected about 01:00 UTC), at most 8 h;
1. **D 1291's k* stage** (`tools3/kstar_stage.sh`, kfree 15) on `tail/`, into `kstar/` (expected to end about 01:50);
2. **D 1549's M 48 tail to kmax 31** with its k* stage (`../D1549/README.md`), from dh170's chord-free h13 once dh170's `run.log` in raw origin/main reads "rls h13 rc 0" (a fetch every 10 min, at most 12 h; without it this step is skipped with a log line), expected to end about 11:00-12:30;
3. **the fastmul7 cross-check of this tail**: h23..h31 released again from the fastmul6 h21 state (`tail/release_ls_h21_D1291.0000.npz`, ks 2354, M 48) with the same options, so that only the kernel differs (fastmul6's 1.7e-60 Moebius split offset), into `tail_fm7/`, expected to end about 15:00-16:30.

### Bars, written before the start (as for D 1291 and D 622, with the amended stop rules)

- Step 1: the k* bound (gain x F at kfree 15) is reported before and after (`kstar/kstar.json`); re-converged when it exceeds 1e-27.
- Step 3: h23..h31 are each released with a pending dDelta at most about 1e-26, no turn; the difference of its final Delta against the fastmul6 tail's final is recorded and reported (no bar was set for it).
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Reported at each stage's end; times from `date -u`.

## Result of the tail (the run ended 2026-11-26 22:28:17 UTC, rc 0; 18:03:11 - 22:28:17, 15906 s)

By script from `run.log`, `*/rls.log`, `*/release_ls.jsonl` and `tail/direct_s.jsonl`. (The run used `tools/ladder_point2.sh`, blob da887d71, on Python 478e9d86, kernel fastmul6, `inner_chord` not yet in play: the records say 478e9d86.)

- **ks used: 2354** (a 8, kc 220, M 32 stages at ks 2354 and the M 48 tail). The jump loop: ks 1954 (ks+200 |dF| 1.2e-45, qd floor), ks 2154 (1.8e-45), ks 2354 (exact 0.0); converged, Delta 1.651913425226958092726605139787996750193. The octo-double gate by hand, `ksgate/README.md`: ks 2354 -> 2554 **5.29e-71**, ks 2554 -> 2754 **7.44e-74** (bar 1e-70).
- **Stages (wall):** jump loop 413 s (three jumps); rls h5..h11 4307 s (18:10:05 - 19:21:51); rls13 (h13, M 32) 1755 s (-> 19:51:06; qd Jacobian converged at outer 0 and 1, the qd floor of the smaller points did not occur here; h13's change +2.109e-16); tail (M 48) 9431 s (-> 22:28:17).
- **Tail** (`tail/rls.log`, h13 re-converged on M 48, then h15..h31; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | **-2.8438e-26** | +3.46e-29 (outer 1) | 1395 s |
| h15 | -1.9486e-17 | +3.45e-32 | 1621 s |
| h17 | -1.1002e-19 | -1.90e-36 | 1655 s |
| h19 | +2.1139e-22 | -3.26e-36 | 1458 s |
| h21 | +2.7555e-24 | +2.66e-31 | 1446 s |
| h23 | none | **+2.16e-27** | 371 s |
| h25 | none | +2.80e-27 | 358 s |
| h27 | none | +1.84e-27 | 349 s |
| h29 | none | +2.34e-27 | 378 s |
| h31 | none | -1.36e-26 | 398 s |

- **Final Delta (the state's `Delta_parts` summed at 60 digits): 1.651913434024554227271949663301812275378** (the pendings of h23-h31 not in it); total -1.95954e-17 from the M 48 start. State `tail/release_ls_h31_D1291.0000.npz`, blob 1afc0d7fcd494a515d342dd8655d456dbcfa66fd; od solve max |F| 1.86918e-52, qd check 1.86918e-52;
  Hamiltonian check at the four nodes at most: p 3.0e-32, m 3.0e-32, a 2.5e-32, c 1.1e-30.
- **Bars:** the jump converged and the ks gate passed (ks 2354: 5.29e-71 and 7.44e-74 against 1e-70): yes; h5..h13 each released: yes; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 177, h17/h19 = 520, h19/h21 = 77 (D 622: 176, 391, 83); h21's change 2.76e-24 (at most about 1e-23): met;
  h23..h29 released with pending +2.16e-27 to +2.80e-27 and no step, h31 with -1.36e-26: no turn. The h13 M 32 -> 48 re-converge: -2.84e-26 (below 1e-25). No qq inner solve failed, no line-search trial below lam 1, no outer step above 3x its harmonic's first.
- The k* stage (`kstar/`, step 1 of the chain above) started 22:28:22 UTC; its result follows in its own section.

## The fastmul7 cross-check, run early by hand and cut to kmax 25 (coordinator's order, 2026-11-26 23:34 UTC)

The chain's last step (step 3 above, `tail_fm7/`: h23..h31 released again on fastmul7 from the fastmul6 h21 state) is run early on the 6 chain threads, which are idle until D 1549's h13 lands, and cut to kmax 25 under the kmax rule. In `tail_fm7_early/`, detached, 6 threads, from `~/Source/choptuik-fastmul7/hp` (d40a9c62, kernel `~/Source/fastmul7-site`):

```
HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=~/Source/fastmul7-site nice -n 10 timeout 6h python -u form_s.py release_ls <ladder>/D1291/tail/release_ls_h21_D1291.0000.npz <ladder>/D1291/tail_fm7_early --harm 23,25 --kmax 25 --jac_by 23:qq,25:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 6 --outer 8 --inner_chord 0 --commit d40a9c62
```

Input: `tail/release_ls_h21_D1291.0000.npz` (fastmul6, 478e9d86; blob 466911b99aa339476ca7674b7447c69489d41ed4; D 1291, M 48, kc 220, ks 2354, a 8), whose Delta is **1.651913434024554227271949663301812275378** (the tail's value after h21, which h23-h31 left unchanged).

### Bars, written before the start (coordinator's order)

- **h23's re-converge on fastmul7** gives Delta against the fastmul6 tail's state after h21 (1.651913434024554227271949663301812275378): that difference is D 1291's **kernel cross-check, wanted below 1e-25**.
- **h23 and h25 are released with no step** (pending dDelta at most the release bar 1e-25).
- Stop rules as amended: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first (a qq floor at the first outer step after a resample is logged; here the state is not resampled).
- When D 1549's h13 lands, the chain's D 1549 tail starts beside this run (a brief overload is fine). When the chain later reaches its own step 4 (`tail_fm7/`, kmax 31), that one is stopped by pid as a duplicate, unless the coordinator says otherwise.
- Reported: the shift, pushed at the end.

### Result of the early fastmul7 cross-check (`tail_fm7_early/`; 2026-11-26 23:34:48 - 23:47:05 UTC, 737 s)

By script from `tail_fm7_early/rls.log`, `release_ls.jsonl`, `direct_s.jsonl` and `tail/release_ls.jsonl` (fastmul6). The log ends with the full-system line and `direct_s.jsonl` exists; the exit code was not recorded (my launcher did not wrap the process).

| harmonic | fastmul7 (d40a9c62) | fastmul6 (478e9d86), same state | difference | wall (fastmul7) |
|---|---|---|---|---|
| h23 | released at outer 0, no step; F 1.869180e-52; pending dDelta +2.160983e-27; harmonic step 3.713566e-15 | F 1.869180e-52; +2.160983e-27; 3.713566e-15 | pending -1.53e-36; F ratio 1 + 9.05e-8 | 362 s |
| h25 | released at outer 0, no step; F 1.869180e-52; pending +2.796311e-27; harmonic step 8.414473e-15 | F 1.869180e-52; +2.796311e-27; 8.414475e-15 | pending -2.28e-34 | 364 s |

- **No step was taken at h23 or h25 on fastmul7**, so the state, and its Delta, are unchanged: **fastmul7's Delta after h23 and after h25 is 1.651913434024554227271949663301812275378, equal to the fastmul6 tail's state after h21 and to its final, to every digit of the 60-digit sums (difference 0.0).**
- **The kernel cross-check:** the shift of Delta is 0 (no applied step), against the bar of 1e-25: met. What the two kernels do show is their residual and pending step on the same state: F 1.869180e-52 on both (ratio 1.00000009, an absolute difference of about 1.7e-59, the order of fastmul6's Moebius split offset),
  and the pending dDelta of h23 and h25 differing by -1.53e-36 and -2.28e-34 (relative 7e-10 and 8e-8), far below the release bar 1e-25. The fastmul7 od solve and qd check at h25: max |F| 1.86918e-52 and 1.86918e-52 (fastmul6: 1.86918e-52); Hamiltonian check at the four nodes at most: p 3.0e-32, m 3.0e-32, a 2.5e-32, c 1.1e-30.
- State `tail_fm7_early/release_ls_h25_D1291.0000.npz`, blob 6ffdf15474f55dac06f17dfd7dafcce9672ce207; the record's commit field reads d40a9c62 and the kernel fastmul7-site.
- **Bars:** h23 and h25 released with no step: met. The kernel cross-check below 1e-25: met (shift 0, pending difference at most 2.3e-34). When the chain reaches its step 4 (`tail_fm7/`, kmax 31), it is stopped by pid as a duplicate.

### The chain's step 4 (`tail_fm7/`, kmax 31) stopped as a duplicate (2026-11-27 08:15:19 UTC, coordinator's order)

The early cross-check (`tail_fm7_early/`, h23 and h25 on fastmul7) replaced it. The chain reached its step 4 at 08:14:51 UTC (after D 1549's tail and k* stage ended: D 1549 tail rc 0 08:14:51) and started `tail_fm7/` (h23..h31 from the fastmul6 h21 state); I stopped its `release_ls` python by exact pid (96470) at 08:15:19 UTC, 28 s in: `tail_fm7/run.log` reads "rc 143 08:15:19", `tail_fm7/rls.log` holds its first lines only, no result. The chain script ended with it (`chain.log`).
