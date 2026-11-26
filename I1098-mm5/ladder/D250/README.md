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

## Result of the u tail (2026-11-26 17:28 UTC, `tail_u/run.log`: rc 0, start 16:59:57, end 17:28:09, 1692 s)

By script from `tail_u/rls.log` and `release_ls.jsonl`. Stage wall times are the gaps between the logged start times (h13 includes the u-prepared state's re-convergence at outers 0-2):

| stage | change in Delta | wall |
|---|---|---|
| h13 (re-converge on the u horizon) | -2.4606e-17 (o0), -7.7819e-25 (o1), then pending -2.26e-47 | 483 s |
| h15 | -9.3336e-17 | 289 s |
| h17 | -4.4259e-19 | 246 s |
| h19 | +2.4370e-21 | 245 s |
| h21 | +2.0893e-23 | 197 s |
| h23 | none, pending -2.98e-26 | 47 s |
| h25 | none, pending -3.05e-26 | 47 s |
| h27 | none, pending -3.05e-26 | 45 s |
| h29 | none, pending -3.07e-26 | 48 s |
| h31 | none, pending -1.37e-26 | 45 s |

h23-h31 were released at outer 0 by the residual with the pending dDelta below --ddelta 1e-25 (no step taken, no turn, no floor). The five pending shifts sum to -1.352e-25, not in the state's Delta.

Total since the Moebius h13 state: -1.18382e-16. **Final Delta (the state's `Delta_parts` summed at 60 digits, `tail_u/direct_s.jsonl`): 1.6849552059415603649964497491180504272** (Moebius M 32 after h13: 1.684955205941560483378678483556634985116).
State `tail_u/release_ls_h31_D250.0000.npz`, blob 32b250942a9b58563646604ac65528860891cd7a. The full system's qd check: max |F| 1.87e-52 (od solve 1.8687435872027878e-52); the Hamiltonian check at the four nodes: 2.3e-21 (p), 2.5e-21 (m), 8.3e-22 (a), 9.2e-20 (c) at node 1, all below 1.1e-19.

### Discrepancy noted (2026-11-26 17:50 UTC)

Re-converging h13 on the u horizon moved D 250 by -2.4606e-17 (residual 1.56e-36 before the step, 271 s) but D 432 and D 519 by nothing (residual 1.12e-53 and 1.65e-53, below --tol; pending dDelta -2.55e-29 and -2.54e-29, no step).
The Moebius states' ks go to the u ks by +30 at D 250 (392 -> 422), +66 at D 432 (665 -> 731). Cause not known; not investigated (D 250's h13 shift is 27% of its tail's total -1.18382e-16, so the D 250 tail's Delta is not comparable to the other two at the 1e-17 level without it).
