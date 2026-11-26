# I1098-mm5/fix6: D 300 and D 1000 re-solves and the D 1000 M 48 tail on fastmul6, exact 1/k and d/dtheta remainders (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's fastmul6 tests (relayed by coordinator t5), with `tools/fix6_mm5.sh` (blob 9c3af9c8510914169bdfd6d4c3441d58b8652224, raw ef8bd0cb `I1098-mac-a/tools/`, verified with `git hash-object --no-filters`).
Kernel: `~/Source/fastmul6-site` (d368a0c0: exact 1/k and the d/dtheta matrices' f64 remainders); Python: `~/Source/choptuik-fastmul6/hp` at f1b3cb8b (taylor_mp_check now uses the solver's own matrices, hi + lo + c when the remainders are on;
horizon_mp_check.py added; Python only, no rebuild). Settings: HP_EXACT_RECIP=1, HP_EXACT_DMAT=1, HP_HORIZON_RELAXED=1, qq Jacobian, od residual, tol 1e-48.

## Bars, written before the runs (2026-11-26 15:03 UTC; relayed by the coordinator)

1. **taylor_mp_check at D 300**, with HP_EXACT_DMAT=1 and with 0: both must PASS, and the first must print "hi + lo + c".
2. **D 300**: D300_mob6 - D300_u6 **below 1e-23**. D300_u6's change from its start should be **+1.288e-19** (plus about 2e-32) and D300_mob6's **+1.289e-19**. If the gap stays at 3.2e-21, the row-sum reading is wrong.
3. **D 1000**: D1000_base6's change is the remainders' effect by a direct re-solve; dmat_perturb predicts **+1.212e-24 within 1%**.
4. **M 32 -> 48 at kfree 13**: D1000_M48_6 minus D1000_base6, against fastmul5's **-8.40e-25**.
5. **The tail** (D1000_M48_tail6, h15..h31 from D1000_M48_6's state): each harmonic's change, beside the old m48_1000 numbers (h17 shift +1.39e-19, h19 +1.21e-19, h21 -3.48e-21, h23 -1.51e-21).

Stop rules: an exception, the floor stop, or an outer step 3x its harmonic's first. Reported: the two check lines, then each run's change and the verdicts as they land (all differences by script from the logs' digits).

## Inputs (`inputs/`, blobs verified) and runs

| file | from | blob |
|---|---|---|
| D300_full_base.npz | I1098-mac-a/budget300_src | 569779b213ca7334c01417ae53b7389863220cc9 |
| D300_full_mob8,ks=600.npz | I1098-dh610/budget300_src | b8e2b0008c7cca3c1ad4102888eddb2499045341 |
| D1000_base.npz | I1098-dh610/fix/D1000_base/release_ls_h13_D1000.0000.npz | 57af5b81bf3f21bb583bbbd6773bb0a4e28a6fbc |
| D1000_M48.npz | I1098-dh610/fix/D1000_M48/release_ls_h13_D1000.0000.npz | a3735a1f1f1c756bdd6f143a54e273c0d681b428 |

`bash tools/fix6_mm5.sh inputs <this folder>`, detached, nice 10: first the two taylor_mp_check runs; then together on 16 threads D300_u6 and D300_mob6 (3 threads each, 1 h cap), D1000_base6 (4, 3 h) and D1000_M48_6 (6, 3 h), all
`release_ls --harm 13 --kmax 13 --jac_by 13:qq --outer 8`; then D1000_M48_tail6 from D1000_M48_6's state (`--harm 15,...,31 --kmax 31`, qq for each, 16 threads, 12 h cap). The script logs no kernel path, so each run's `rls.log` starts without a
`hpkernel` line; the kernel is the `PYTHONPATH=~/Source/fastmul6-site` one set in the script (checked: `fastmul6-site/hpkernel/__init__.py`).

## Results so far (2026-11-26 15:18 UTC)

First attempt (relative `inputs` path, the script `cd`s into hp/ first): all jobs failed at once, kept in `attempt0_relative_inputs/` with a NOTE. Second attempt 15:04:11 UTC with absolute paths, the script unchanged (blob 9c3af9c8), driver pid 36629. Differences by script from the logs' digits (mpmath).

**Check 1, taylor_mp_check at D 300 (exit 0 both):** HP_EXACT_DMAT=1: `max |kernel - mpmath| 1.096e-124 over 96 values`, control (HP_EXACT_RECIP=0) `2.356e-31`, `the matrices on both sides: hi + lo + c (the remainders applied)`,
`PASS: lane-precision reciprocals 1.1e-124 (bar 1e-60), the control 2.36e-31 (must exceed 1e-40)`; HP_EXACT_DMAT=0: `1.24e-124` and `2.356e-31`, `the matrices on both sides: hi + lo`, `PASS ... 1.24e-124 (bar 1e-60), the control 2.36e-31`.

| run | change in Delta (log's "h13's change") | steps | Delta |
|---|---|---|---|
| D300_u6 | +1.2884779e-19 (+1.288e-19) | o0 +1.0593e-19 (289.5 s), o1 +2.2922e-20 (181.1 s), released | 1.678171015400871567861061965988636601014 |
| D300_mob6 | +1.2884018e-19 (+1.288e-19) | o0 +1.0592e-19 (316.6 s), o1 +2.2922e-20 (192.7 s), released | 1.678171015400871567861054353749636973374 |
| D1000_base6 | +1.212211e-24 (+1.212e-24) | o0 +1.21221e-24 (404.6 s), outer 1 released (step 1.66e-25) | 1.654240854145891738986195293587439721842 |
| D1000_M48_6 | +2.0309904e-24 (+2.031e-24) | o0 +2.03099e-24 (645.9 s), outer 1 released (step 1.86e-25) | 1.654240854145891738986195272305515987672 |

| bar | observed | verdict |
|---|---|---|
| D300_mob6 - D300_u6 below 1e-23 (fastmul5: +3.23341e-21) | **-7.61224e-24** | **met** (the row-sum reading holds; the remaining value equals horizon300's u_ks+200 change, -7.6122e-24, to the digits shown) |
| D300_u6's change +1.288e-19 (+ about 2e-32); D300_mob6's +1.289e-19 | +1.28848e-19; +1.28840e-19 | u6 as expected; mob6 reads +1.288e-19 (the expected +1.289e-19 is 7.6e-24 higher) |
| D1000_base6's change +1.212e-24 within 1% | +1.212211e-24 (ratio 1.00017) | **met** |
| D1000_M48_6 minus D1000_base6 against fastmul5's -8.40e-25 | **-2.12819e-26** (the two start states differ by -8.40061e-25; the remainders add +1.212e-24 at M 32 and +2.031e-24 at M 48) | the M 32 -> 48 shift at kfree 13 on fastmul6 is 39x smaller than fastmul5's |

The tail (D1000_M48_tail6, h15..h31 from D1000_M48_6's state, 16 threads, 12 h cap) started 15:17:52 UTC; its table follows.

## D1000_M48_tail6 stopped (2026-11-26 15:39:51 UTC) and rerun as D1000_M48_tail6b

Stopped by hand, with SIGTERM to the `timeout` pid 37374 (python 37375; `D1000_M48_tail6/run.log`: rc 143) at h29 outer 0, on the coordinator's order: h19-h27 were released at outer 0 **by the residual criterion
alone** (target |F| 1.9e-54 to 2.4e-54 at tol 1e-48) with no step taken, while the pending Newton steps' first-order dDelta was +2.644e-22 (h19), +2.678e-22 (h21, h23) (h25, h27 in `release_ls.jsonl`), so the numbers past h17 are
not usable. The release now also requires the pending step's |dDelta| <= --ddelta (default 1e-25; wip/large-d-fastmul6 dcd93f55); `../fix6/D1000_M48_tail6b/` reruns h19-h31 from this run's h17 state
(`D1000_M48_tail6/release_ls_h17_D1000.0000.npz`, blob 6a79f7dd862e9a4b8f7dc74cfbd9d49cb5a59964). What this run gave that stands: h15 -2.24025e-17 and h17 -1.27399e-19 at M 48 (both stepped and released by their step size).
