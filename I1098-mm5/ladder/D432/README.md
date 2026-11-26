# I1098-mm5/ladder/D432: D 432 full direct solve, recipe v1, then the tail in mode u (#1098)

Part of `../`. D 432: ks 665, kc 180 (Moebius a 8, M 32) for the jump and the h5..h13 release (`jump/`, `rls/`; `run.log`); the v1 tail was stopped at 17:12:17 UTC by exact pid (timeout 44616, python 44617; `tail rc 143`) by the tail-switch watcher.

- jump: converged, 45 s; Delta 1.667761312224664714330111348230222792723 (qd |F| 5.047e-30, bound 1.48e-21).
- rls (h5..h13, `rls rc 0` at 17:12:16, 61 min): h5 -2.0261e-8, h7 +2.613e-10, h9 +4.4345e-12, h11 -4.7534e-14, h13 -4.4882e-16, each released (pending dDelta -4.06e-44, +4.80e-45, -6.84e-40, +5.29e-29, -2.55e-29);
  Delta after h13 (full, h1-13, M 32 Moebius): **1.667761292229811188766750111575809044951**.

## Tail mode: u (chosen 2026-11-26 17:13 UTC, coordinator's order, written to `../mode.txt`)

`tools/ladder_tail.sh u 432 rls/release_ls_h13_D432.0000.npz tail_u 4`: the u horizon at M 32 with ks = ceil(1.7 (D - 2)) = **731** (`mob0,ks=731`: kt 36, kc 180, 114 Taylor steps), h13 re-converged, then h15..h31 (kmax 31, qq, od, tol 1e-48, --ddelta 1e-25, 4 threads),
started 17:12:50 UTC. **Why u:** as for D 250 (`../D250/README.md`): at D 300 the u horizon at M 32 is clean through h31 (no turn at h23, pending dDelta about 1e-26) and agrees with the Moebius tail through h21 to 8.9e-25 (`../D300u/README.md`);
the coordinator preferred starting at once to waiting 30-40 minutes with 8 threads idle for the Moebius M 48 verdict. The whole 250-519 band is u at M 32 with ks = ceil(1.7 (D - 2)).

## The u tail stopped (2026-11-26 18:00:04 UTC, coordinator's order)

Stopped by SIGTERM to the exact pids (timeout 44729, python 44730): `tail_u/run.log` rc 143, end 18:00:04 UTC. Done before the stop: h13 (no step, pending dDelta -2.55e-29) and h15 (-4.5351e-17, 444.0 s, lam 1); Delta at the stop 1.667761292229811143415696681893357440648 (the state after h15). h17 outer 0 had run since 17:23:05 UTC (37 min).
The line search failed at every trial (no step taken, `tail_u/rls.log`), after the u horizon at ks 731 and h13 re-converged:
h17 outer 0 (harmonic step 6.84e-11, the step's dDelta -2.49e-19): lam 1 not converged in 4 steps (|F| 3.55e-45, 508 s), lam 0.5 (3.31e-46, 818 s), lam 0.25 (9.01e-47, 1252 s), lam 0.125 (5.57e-47, 1742 s), lam 0.0625 (6.09e-48 in 3 steps, 2082 s), against the target 1e-48.
**Coordinator's reading:** #1088 found that the u series loses digits above about D 300, which the Moebius horizon fixed; D 250 and D 300 were just inside u's range, and these failing line searches fit that. Not tested here.
Kept: `rls/` (the Moebius h5..h13 states; `rls/release_ls_h13_D432.0000.npz` is the input of the next tail) and `tail_u/` (the u-prepared start state and the states of the stages that ended). **No tail Delta for this point from this run.**

## Tail in mode mob: the Moebius horizon at a larger ks (coordinator's order, 2026-11-26 18:03 UTC)

`tools/ladder_tail.sh mob 432 rls/release_ls_h13_D432.0000.npz tail_mob 6` (new `tools/ladder_tail.sh`, raw a9ed0f2f `I1098-mac-a/tools/ladder_tail.sh`, blob 677d4e580122e242f04ff878575df14db758c8d6, verified; the earlier u version is kept as `tools/ladder_tail_v1_2f1c0156.sh`),
with `variant_state.py` and `resample_m.py` beside it (blobs 19b05a5a, 4de5c317, verified). The Moebius horizon a 8 at M 32 with **ks = ceil(1.5 (D - 2)) + 420 = 1065** (the script's value; the coordinator's order said 1067 for D 432, the script gives 1065 = 645 + 420; D 519: 1196, as ordered),
the h13 state re-converged and h15..h23 released (kmax 23, qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25, 6 threads, fastmul6, Python 478e9d86). Why: the u series loses digits above about D 300 (#1090), where the u tails of D 432 and D 519 failed their line searches (above);
the jump's ks+200 residual change was 5.8e-59 (ks 665) at the jump's ks, and each step of 200 in ks cuts it by about 1e10.

### Bars, written before the run (coordinator's order)

- The tail falls as at D 300: h15 about **-7e-17**, h21 about **1e-23**. h23 is released with a pending dDelta of about **1e-26 or less**, and there is **no turn**.
- Stop and report on any inner solve that does not converge, or an outer step 3x its harmonic's first.
- Reported: the final Delta, each stage's time and the ks used.
