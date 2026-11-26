# I1098-mm5/ladder/D519: D 519 full direct solve, recipe v1, then the tail in mode u (#1098)

Part of `../`. D 519: ks 796, kc 180 (Moebius a 8, M 32) for the jump and the h5..h13 release (`jump/`, `rls/`; `run.log`); the v1 tail was stopped at 17:17:53 UTC by exact pid (timeout 45223, python 45224; `tail rc 143`) by the tail-switch watcher.

- jump: converged, 48 s; Delta 1.663780890961391892686148674624040080906 (qd |F| 3.687e-30, bound 3.89e-22).
- rls (h5..h13, `rls rc 0` at 17:17:52, 67 min): h5 -1.9825e-8, h7 +2.4786e-10, h9 +4.4081e-12, h11 -4.4689e-14, h13 -4.4805e-16, each released (pending dDelta -3.12e-45, -6.61e-47, -3.65e-32, +4.05e-31, -2.54e-29);
  Delta after h13 (full, h1-13, M 32 Moebius): **1.663780871388325147627787775846586161411**.

## Tail mode: u (started 17:17:56 UTC, from `../mode.txt`, the coordinator's order)

`tools/ladder_tail.sh u 519 rls/release_ls_h13_D519.0000.npz tail_u 4`: the u horizon at M 32 with ks = ceil(1.7 (D - 2)) = **879** (`mob0,ks=879`: kt 36, kc 180, 126 Taylor steps), h13 re-converged, then h15..h31 (kmax 31, qq, od, tol 1e-48, --ddelta 1e-25, 4 threads).
**Why u:** as for D 250 and D 432 (`../README.md`, `../D250/README.md`): u at M 32 is clean at D 300 through h31 and agrees with the Moebius tail through h21 to 8.9e-25 (`../D300u/README.md`); the whole 250-519 band is u at M 32.

## The u tail stopped (2026-11-26 18:00:04 UTC, coordinator's order)

Stopped by SIGTERM to the exact pids (timeout 45259, python 45260): `tail_u/run.log` rc 143, end 18:00:04 UTC. Done before the stop: h13 (no step, pending dDelta -2.54e-29); Delta at the stop 1.663780871388325147627787775846586161411 (the start). h15 outer 0 had run since 17:19:50 UTC (40 min).
The line search failed at every trial (no step taken, `tail_u/rls.log`), after the u horizon at ks 879 and h13 re-converged:
h15 outer 0 (harmonic step 6.91e-10): lam 1 not converged in 3 steps (|F| 7.88e-39, 554 s), lam 0.5 (9.50e-39, 4 steps, 1117 s), lam 0.25 (1.02e-39, 5 steps, 1927 s), against the target 1.32e-44 (the residual before the step).
**Coordinator's reading:** #1088 found that the u series loses digits above about D 300, which the Moebius horizon fixed; D 250 and D 300 were just inside u's range, and these failing line searches fit that. Not tested here.
Kept: `rls/` (the Moebius h5..h13 states; `rls/release_ls_h13_D519.0000.npz` is the input of the next tail) and `tail_u/` (the u-prepared start state and the states of the stages that ended). **No tail Delta for this point from this run.**

## Tail in mode mob: the Moebius horizon at a larger ks (coordinator's order, 2026-11-26 18:03 UTC)

`tools/ladder_tail.sh mob 519 rls/release_ls_h13_D519.0000.npz tail_mob 6` (new `tools/ladder_tail.sh`, raw a9ed0f2f `I1098-mac-a/tools/ladder_tail.sh`, blob 677d4e580122e242f04ff878575df14db758c8d6, verified; the earlier u version is kept as `tools/ladder_tail_v1_2f1c0156.sh`),
with `variant_state.py` and `resample_m.py` beside it (blobs 19b05a5a, 4de5c317, verified). The Moebius horizon a 8 at M 32 with **ks = ceil(1.5 (D - 2)) + 420 = 1196** (the script's value; the coordinator's order said 1067 for D 432, the script gives 1065 = 645 + 420; D 519: 1196, as ordered),
the h13 state re-converged and h15..h23 released (kmax 23, qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25, 6 threads, fastmul6, Python 478e9d86). Why: the u series loses digits above about D 300 (#1090), where the u tails of D 432 and D 519 failed their line searches (above);
the jump's ks+200 residual change was 2.8e-59 (ks 796) at the jump's ks, and each step of 200 in ks cuts it by about 1e10.

### Bars, written before the run (coordinator's order)

- The tail falls as at D 300: h15 about **-7e-17**, h21 about **1e-23**. h23 is released with a pending dDelta of about **1e-26 or less**, and there is **no turn**.
- Stop and report on any inner solve that does not converge, or an outer step 3x its harmonic's first.
- Reported: the final Delta, each stage's time and the ks used.

### Result of the Moebius tail (ks 1196; : rc 0, start 18:03:11, end 18:25:06 UTC, 1315 s)

By script from  and . Stage wall times are the gaps between the logged start times:

| stage | change in Delta | wall |
|---|---|---|
| h13 (re-converge, ks 1196) | none, pending -2.54e-29, released at outer 0 | 61 s |
| h15 | -3.7424e-17 (outer 1 pending +6.76e-32) | 390 s |
| h17 | -2.0975e-19 (outer 1 pending -1.25e-35) | 319 s |
| h19 | +5.9792e-22 (outer 1 pending -1.01e-32) | 251 s |
| h21 | +6.9188e-24 (outer 1 pending -8.99e-31) | 238 s |
| h23 | none, pending **+1.86e-27**, released at outer 0 (harmonic step 1.93e-14) | 55 s |

Total since the Moebius h13 state -3.76336e-17. **Final Delta (the state's  summed at 60 digits): 1.663780871388325109994156946730624660369** (the h23 pending +1.86e-27 is not in it); ks 1196, a 8, M 32, kc 180.
State , blob 2ef0b5012752211978a1ad73469421c33ba019a2; od solve max |F| 4.43430e-55, qd check 4.43430e-55; Hamiltonian check at the four nodes: p at most 1.3e-22, m 1.4e-22, a 2.7e-23, c 4.7e-21.
No inner solve failed, no outer step above 3x its harmonic's first, every trial converged at lam 1 ().

**Bars:** the tail falls (h15 -3.7424e-17, then -2.10e-19, +5.98e-22, +6.92e-24: h21 is the bar's about 1e-23; h15 is D 519's, not the bar's "about -7e-17" of D 300) met;
h23 released with pending dDelta +1.86e-27, at most 1e-26 met, no turn met.
