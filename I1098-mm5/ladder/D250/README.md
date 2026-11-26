# I1098-mm5/ladder/D250: D 250 full direct solve, recipe v1, then the tail in mode u (#1098)

Part of `../`. D 250: ks 392, kc 146 (Moebius a 8, M 32) for the jump and the h5..h13 release (`jump/`, `rls/`; `run.log`), the v1 tail (h15..h31 on the Moebius M 32 horizon) was started by `tools/ladder_point.sh` and
stopped at 16:59:14 UTC by exact pid (timeout 43085, python 43086; `run.log`: `tail rc 143`) after 9 s, at h15 outer 0, by the tail-switch watcher.

- jump: converged, 28 s; Delta 1.684955176829943625636843711545282524537; Delta - Track C -2.91199e-8 (+- 8.13e-11).
- rls (h5..h13, `rls rc 0` at 16:59:05, 49 min): h5 +2.9549e-8, h7 -4.3122e-10, h9 -5.9653e-12, h11 +8.1001e-14, h13 +6.0807e-16, each released (pending dDelta -1.65e-42, +2.60e-42, +4.99e-37, -3.91e-48, -4.22e-29);
  Delta after h13 (full, h1-13, M 32 Moebius): **1.684955205941560483378678483556634985116**.

## Tail mode: u (chosen 2026-11-26 17:00 UTC, coordinator's order)

`tools/ladder_tail.sh u 250 rls/release_ls_h13_D250.0000.npz tail_u 4` (tool blob 2f1c0156d6d224f3672ce0287a5099c77afc1a56): the u horizon at M 32 with ks = ceil(1.7 (D - 2)) = **422** (`variant_state.py` `mob0,ks=422`: kt 36, kc 146, ks 422, 92 Taylor steps),
h13 re-converged, then h15..h31 (kmax 31, qq, od, tol 1e-48, --ddelta 1e-25, Python 478e9d86, 4 threads), started 16:59:57 UTC.
**Why u:** at D 300 the u horizon at M 32 (ks 506) shows no turn at h23 (pending dDelta -1.19e-26; h25 -1.24e-26, h27 -1.33e-26, h29 -1.58e-27) where the Moebius M 32 run's h23 had a pending dDelta of -3.89e-22 and an inner floor of 1.36e-42,
and the u tail agrees with the Moebius tail through h21 to 9.2323e-25 (D300u: h21 +1.5418e-23, Moebius +1.4486e-23). So the result stands whichever mode D 432 and D 519 get. (The D 300 M 48 Moebius tail, the other candidate, had not reached h23.)
