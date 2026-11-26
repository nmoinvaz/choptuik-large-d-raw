# I1098-mm5/ladder: the first ladder points, recipe v1, on fastmul6 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's recipe v1, relayed by coordinator t5: a full direct solve at each D on fastmul6 (d368a0c0's kernel, Python at 478e9d86: the floor stop also needs a small step, max |dz| <= 1e-12), M 32, the Moebius
horizon a 8 with ks = ceil(1.5 (D - 2)) + 20, in three stages (`tools/ladder_point.sh`, blob 0c312408a8e1a4c98aca68c88a15a2ef3c27b6d4 from raw ee32c8d9 `I1098-mac-a/tools/`, verified):
1. **jump**: the held solve (p1's harmonics 5-13 held at the guess) from a guess fitted in 1/n (degree 1) to fastmul6's full states at D 300 and D 1000 (the two inputs below), double-double solve, quad-double check (`form_s.py jump`);
2. **rls**: release h5..h13 one at a time (`release_ls`, kmax 13, the qd Jacobian handed to qq at its floor), octo-double residual, tol 1e-48, --ddelta 1e-25;
3. **tail**: h15..h31 (kmax 31, qq).
Each stage's log and states are in `<D>/<stage>/`; `<D>/run.log` records each stage's rc and time. Points: D 250 (kc 146), D 432 (kc 180), D 519 (kc 180), 4 threads each; D 360 is dh610's pilot.
**D 300's tail** (from S300): `release_ls --harm 15,...,31 --kmax 31 --jac_by 15:qq,...,31:qq --res od --ddelta 1e-25 --threads 4 --outer 8 --commit 478e9d86`, `timeout 8h`, into `D300/tail/`. 16 threads in all, nice 10.

## Inputs (copies, blobs verified)

- `inputs/S300_D300_mob6_h13.npz` = `../fix6/D300_mob6/release_ls_h13_D300.0000.npz` (my own state; D 300, M 32, ks 600, Moebius a 8, harmonics up to 13 free; Delta 1.678171015400871567861054353749636973374)
- `inputs/S1000_D1000_base6_h13.npz` = `../fix6/D1000_base6/release_ls_h13_D1000.0000.npz` (D 1000, M 32, ks 1517, Moebius a 8; Delta 1.654240854145891738986195293587439721842)

## Bars and stop rules, written before the runs (2026-11-26 16:10 UTC; relayed by the coordinator)

- Each jump ends "converged". Its Delta - Track C is about **1e-8** before the release (D 360 read 1.46e-8).
- h5..h13 each end **released**.
- The tail's changes fall: h15 near **-4.8e-17**, then about 10x per harmonic.
- Stop and report on: any jump rc != 0, a harmonic not released, or an outer step more than 3x its harmonic's first.
- Reported: each point's final Delta and each stage's time, and D 300's tail changes (by script from the logs' digits).

## Tail switch (started 2026-11-26 17:00 UTC)

`tools/ladder_tail.sh` (blob 2f1c0156d6d224f3672ce0287a5099c77afc1a56, raw e4222e00; with `variant_state.py` 19b05a5a and `resample_m.py` 4de5c317 beside it) replaces the v1 tail (the Moebius M 32 horizon, whose h23 turns) at each point: mode **u** (the u horizon at M 32,
ks = ceil(1.7 (D - 2)): 422, 731, 879) or **mob48** (the Moebius horizon at M 48), each re-converging h13 and then h15..h31. Per point a watcher waits for `rls rc 0` in run.log, stops the v1 tail by exact pid, then waits for `mode.txt` (or the coordinator's direct order);
`<D>/switch.txt` records it. D 250: mode u, started 16:59:57 UTC (D250/README.md). D 432 and D 519: the mode is written to `mode.txt` once D300m48's h23..h29 verdict (M 48 Moebius clean or not) is in.

## Mode u for the whole band (decided 2026-11-26 17:13 UTC, coordinator's order)

D 250, D 432 and D 519 all take mode **u** (the u horizon at M 32, ks = ceil(1.7 (D - 2)): 422, 731, 879). Reason: at D 300, u at M 32 is clean through h31 (D300u: no turn at h23, pending dDelta about 1e-26 at h23-h29) and agrees with the Moebius M 32 tail through h21 to 8.9e-25,
while the Moebius M 32 tail turns at h23 (pending -3.89e-22, inner floor 1.36e-42); waiting 30-40 minutes with 8 threads idle for D300m48 (the Moebius M 48 check, which keeps running) costs more than the uniformity of the band. Started: D 250 16:59:57 UTC (the coordinator's direct order),
D 432 17:12:50 UTC (`mode.txt`), D 519 when its rls stage ends (its watcher reads `mode.txt`).

## u tails of D 432 and D 519 stopped (2026-11-26 18:00:04 UTC, coordinator's order)

Both u tails had failing line searches (D 432 at h17 after 37 min, D 519 at h15 after 40 min; `D432/README.md`, `D519/README.md`). Coordinator's reading: the u series loses digits above about D 300, and D 250 and D 300 were just inside u's range. D 250's u tail is the only completed u tail of the band (`D250/README.md`).
D300m48 was stopped at 17:58:38 UTC (`D300m48/README.md`). Next: the Moebius horizon at a larger ks, from each point's `rls/release_ls_h13_D<D>.0000.npz`, on the jump agent's command.

## New tails and D 1291 (2026-11-26 18:03 UTC, coordinator's order)

D 432 and D 519: the Moebius horizon at ks 1065 and 1196 (`tools/ladder_tail.sh mob`, `D432/README.md`, `D519/README.md`). D 1291: `tools/ladder_point2.sh` with KSBAR 1e-70 (`D1291/README.md`). 6 threads each; bars in each README.

## D 622 and D 747 (2026-11-26 18:27 UTC, coordinator's order)

Two more points on the Moebius horizon, `tools/ladder_point2.sh` with KSBAR 1e-64, M 48 tail to h23, 6 threads each (`D622/README.md`, `D747/README.md`).
