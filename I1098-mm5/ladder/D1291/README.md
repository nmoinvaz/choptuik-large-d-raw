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
