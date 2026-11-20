# I1021-mac: M = 3 points argcount could not value in #1013's candidates' box, their cause and a way to value them

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021.
Code: `solver/inner_stokes/argcount.py` on branch `wip/excited-zeros-m3` of choptuik-large-d at 068913b4 (from
wip/excited-zeros fc7dee4d), `/Users/nathan/venv-314/bin/python`, nice 10, 2 worker processes.

Inputs, copied from I1013-dh610/m3 (f9e4bea4): `leaves_M3_cand_r0.25.jsonl` (its 32 unresolved cells are the ones
recounted), `points_M3_r0.17.jsonl` (the cache at xi1 0.17; `points_M3_r0.17_I1013.jsonl` is the untouched copy) and
`points_M3_r0.2.jsonl` (seeds and the relocation cache at 0.2).

Criteria (the issue's, fixed before the runs): the selftest and its mutations pass as before; every point valued in
I1013's 0.17 file keeps its record bit for bit; a planted zero (sign +1 at A 3.53, w/w_inf 0.555, inside the cell
A 3.4123-3.6623, w/w_inf 0.5065-0.6065) is counted; the recount of the 32 cells at xi1 0.17 leaves 0 unresolved, or
a cause is named for those left.

Split (proposed 2026-11-19 14:30 UTC, used only on the coordinator's go): the recount had done boxes 0-6 of the 32
(the unresolved cells in file order). `split/points_M3_r0.17_in.jsonl` is the live cache's 617 complete lines at
14:30 UTC (its first 214 lines are I1013's file). Boxes 7-10 (`split/leaves_b07-10.jsonl`) stay on the Mac, and
boxes 11-31 go to dh610 as four jobs (`split/run_dh610.sh`, raw I1021-dh610). Every part starts from a cache that
holds all of I1013's points, and with --retry it computes only points without value, so it never computes a valued
I1013 point again. The parts are merged into one cache, where a later record never replaces a valued one, and then
recounted over all 32 boxes on the Mac at 068913b4 from the merged cache.

Mac part (boxes 7-10, `run_b07-10.sh`): restarted 14:33:17 UTC, ended 19:36:28 UTC with exit 0. Its 432 new points
are all valued by the continuation. Boxes 7-10 resolve with 0 unresolved cells (136 leaves after 44 splits,
`m3/count_M3_cand_r0.17_fix_b07-10.json`). Box 7 holds a zero of sign -1, located at A 3.245478, w/w_inf 0.345851;
the locate at xi1 0.2 did not find it. Bit checks (`argcount_samebits.py`, 3a76a2f9): I1013's 161 valued points and
the split input's 562 keep their records, PASS; the `--mutate=flip` control exits 1.

Noise cap (2026-11-19 19:42-19:49 UTC, `diag/onepoint_cap.py`, logs `diag/cap*.log`): two points of rpi5's #1013 box at
17c51597, with the 0.2 start first and the known zero's F3 as seed. With the cap at 1e2, A 4.3623 (w/w_inf 0.5065) is
lost at xi1 0.18, with noise3 from 67 to 1.85e3 there, and A 5.1123 is lost at its 0.2 start (noise3 4.2e5). With the
cap at 1e7, A 4.3623 is valued at 0.17 with noise3 929. A 5.1123 is lost near 0.186, with noise3 9.5e6 at 0.19 and
2.5e8 at 0.18. The default became 1e7 at 998fd290. rpi5's box is cut to A 3.6-4.35 (`split/run_rpi5_upper.sh`), and
dh610's b21-25 is rerun at 998fd290 with `--retry` (`split/rerun2_b21-25.sh`). `diag/replay_runs.py` replays any
cache's seeds; on the 964-line Mac cache it gives `seeds_replay.jsonl` byte for byte, and without the 0.2 file's
seeds (R02N 0) 12 of 750 seeds differ.
`split/rerun2_box.sh` does the same for dh610's 068913b4 jobs b11-15, b16-20 or b26-31, given as its fourth argument.
It refuses while that job runs, or if its cache does not begin with the 617-line input or ends inside a line; these
refusals were tested on scratch copies on the Mac.

Start-noise check (b), `diag/start_noise.py` at 068913b4: noise3 at the start radius of every continuation-valued
point of the Mac cache, from its replayed seed. `start_noise.jsonl` covers the cache's first 964 lines (748 points,
17:47-20:22 UTC), and `start_noise_after964.jsonl` the other 85 (seeds `seeds_after964.jsonl` from
`seeds_replay_1049.jsonl`, 20:07-20:26 UTC); together they are all 833 such points. None is above the cap of 1e2 or
1e7, and every start passes |r3| <= 3 noise3; the largest start noise3 is 4.6e-4. The largest final noise3 in the
cache is 4.73. So neither cap changes the bits of any Mac point.

The same check for dh610's three parts at 068913b4 (b11-15, b16-20, b26-31), on their files of raw 7bb8f659 (20:11
UTC): `seeds_dh610_b*.jsonl` (replayed seeds, lines 618 on), `start_noise_dh610_b*.jsonl` (230, 282 and 149
continuation-valued points, 20:28-00:10 UTC, logs `start_noise_dh610_A.log` and `_B.log`). None of the 661 starts is
above 1e2 or 1e7, every start passes |r3| <= 3 noise3, and the largest start noise3 is 5.7e-4. Three replayed points
were lost by the continuation (b11-15 lines 652 and 659, b26-31 line 764, counted from 1).

The lines the two parts added later, on their final files: b16-20 lines 900-951 (raw e5f860b6, seeds
`seeds_dh610_b16-20_951.jsonl`, `start_noise_dh610_b16-20_after899.jsonl`, 52 points, log `_C.log`) and b11-15 lines
850-1172 (raw 5247895e, seeds `seeds_dh610_b11-15_1172.jsonl`, whose first 232 rows are `seeds_dh610_b11-15.jsonl`
byte for byte, `start_noise_dh610_b11-15_after849.jsonl`, 323 points, log `_D.log`, 00:43-02:05 UTC on 20 Nov). None
of the 375 starts is above 1e2 or 1e7, every start passes |r3| <= 3 noise3, and the largest start noise3 is 9.1e-6.

Sheets of S_3 = 0 (2026-11-20 00:16-00:37 UTC). `loc/`: box 16's -1 (b16-20's corner (3.5529706, 0.41279321),
|R| 281 under 10 sigma 580) was recounted in one cell placing that corner at 0.4 of each range (`leaf_z16.jsonl`,
`run_loc.sh`, 998fd290). With starts 0.2 first (`z16/`) and 0.25 first (`z16_s0.25-0.2/`) its five points have the
same R, about 2.5e6, and F_3 0.040-0.071 - 0.060-0.075i, against 0.006 - 0.38i at b16-20's points beside them. The
cause is the seed: `--seed` records kept only F3re, F3im and info, so a continuation-valued neighbour did not qualify,
and the seed came from (3.0123456, 1.05654321), 0.84 away. 6da7da7b keeps 'fix' in seeds copied from another file or
radius (`--seed`, `--r1b`), with a selftest case and `--mutate=seedfix`; `run_loc2.sh` relocates both zeros with it.
The z7 runs at 998fd290 were stopped before writing a point. `diag/sheet_check.py`: consecutive valued points on
leaf edges (or grid lines) are flagged at |dF_3| > 0.1; on a sheet F_3 does not depend on xi1 (common points of
different radii agree to 2.3e-3), steps on a sheet reach 0.062, and the sheets seen are 0.16-0.42 apart.
`diag/sheet_all.sh` runs it over every stored count (`sheet_all.log`): only #1020's ext count at 0.25 (22 of 429
cells across a switch) and rpi5's upper box (3 points at A 4.3623456, w/w_inf 0.5065-0.6065) fail; the planted
switch fires in both modes. `diag/sheet_connect.py` pools the 15 files (`sheet_connect_files.txt`, zeros in
`zeros_cells.json`): the known zero, #1013's minus and plus, box 7's -1, box 16's -1 and b11-15's +1 lie on the
known zero's sheet (largest step on the best path 0.0069-0.0092); #1020's new zero (2.338793, 0.096238) lies on
another sheet (every path needs a step of 0.161 or more), so it is a zero of a different branch of S_3 = 0
(`sheet_connect.log`; `--mutate=split` must and does cut box 7 off, `sheet_connect_mutate.log`).
`diag/edge_cause.py`: b11-15's unresolved cells are under the 10 sigma guard at edge midpoints, (3.52562685,
0.21279321) for the +1 pair, (3.640861, 0.344043) and (3.449943, 0.350293), and its two nan boxes have the two points
without value. `m5/control_1026_xi0.2.log`: hier.py (numpy, 998fd290) gives #1026's control solve 01 (hier_nb,
dh610) to its printed digits, F3/F1 0.053613+0.005223i, F5/F1 0.002949+0.000510i.

`fu_seed/point_3.6623456_1.06904321.jsonl` (20 Nov, the coordinator's order, for dh610's `b21-25-fu`): the fix2931
recount's record of (3.6623456, 1.06904321), byte for byte line 889 of `fix2931/points_M3_r0.17.jsonl` (998fd290,
`--m3starts=0.2,0.25`, noise cap 1e7; trail 0.2-0.17, |r3| 1.26e-6, noise3 3.5e-6, F_3 0.005494 - 0.141795i). The
sheet check passes with it appended to b21-25's final cache (0 of 1561 pairs flagged, |dF_3| 0.0025-0.0078 to its
valued neighbours on A 3.6623456).
