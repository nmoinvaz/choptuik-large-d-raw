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
