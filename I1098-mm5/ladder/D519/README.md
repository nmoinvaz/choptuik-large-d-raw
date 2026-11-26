# I1098-mm5/ladder/D519: D 519 full direct solve, recipe v1, then the tail in mode u (#1098)

Part of `../`. D 519: ks 796, kc 180 (Moebius a 8, M 32) for the jump and the h5..h13 release (`jump/`, `rls/`; `run.log`); the v1 tail was stopped at 17:17:53 UTC by exact pid (timeout 45223, python 45224; `tail rc 143`) by the tail-switch watcher.

- jump: converged, 48 s; Delta 1.663780890961391892686148674624040080906 (qd |F| 3.687e-30, bound 3.89e-22).
- rls (h5..h13, `rls rc 0` at 17:17:52, 67 min): h5 -1.9825e-8, h7 +2.4786e-10, h9 +4.4081e-12, h11 -4.4689e-14, h13 -4.4805e-16, each released (pending dDelta -3.12e-45, -6.61e-47, -3.65e-32, +4.05e-31, -2.54e-29);
  Delta after h13 (full, h1-13, M 32 Moebius): **1.663780871388325147627787775846586161411**.

## Tail mode: u (started 17:17:56 UTC, from `../mode.txt`, the coordinator's order)

`tools/ladder_tail.sh u 519 rls/release_ls_h13_D519.0000.npz tail_u 4`: the u horizon at M 32 with ks = ceil(1.7 (D - 2)) = **879** (`mob0,ks=879`: kt 36, kc 180, 126 Taylor steps), h13 re-converged, then h15..h31 (kmax 31, qq, od, tol 1e-48, --ddelta 1e-25, 4 threads).
**Why u:** as for D 250 and D 432 (`../README.md`, `../D250/README.md`): u at M 32 is clean at D 300 through h31 and agrees with the Moebius tail through h21 to 8.9e-25 (`../D300u/README.md`); the whole 250-519 band is u at M 32.
