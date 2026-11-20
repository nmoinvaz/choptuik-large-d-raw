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

Seeds under the seed bug (20 Nov, 03:20-03:30 UTC, `diag/seedfix_replay/`, `run.sh`, `compare.py`): every cache made
with `--seed` before 6da7da7b replayed twice by `diag/replay_runs.py`, with the copies of the 0.2 file's records as that
code made them and as 6da7da7b makes them (`--keepfix`, new). The replay now matches a batch's records by key, since
argcount writes them as they return from db28e274 on; without `--keepfix` it gives the stored seed files byte for
byte. 0 of 2339 seeds differ (Mac 835, b11-15 555, b16-20 334, b21-25 425, b26-31 190). The control, box 16's
relocation at 998fd290 (`loc/z16`), differs in 4 of 5, as it must.

Merge dry run (20 Nov, `merge_dry/`; `run.sh DH b21-25 CODE PY` with DH = I1021-dh610 at 19ad1c0e, CODE at 6da7da7b;
inputs in `in/SHA256SUMS`, the dh610 and Mac points files are not copied here). Base: the Mac cache (1049 lines);
parts: b11-15, b16-20, b21-25, b26-31, and `in/part_fix2931.jsonl` (the prefix and fix2931's records of
(3.6623456, 1.06904321) and (3.7873456, 0.90654321), its lines 889 and 808). `merged.jsonl`: 2448 lines, 2386 points,
2381 valued, 5 without value; `--mutate=prefix` fails. `diag/merge_check.py` (`spec.json`) finds each record's source:
every continuation-valued record has final noise3 <= 1e7 (largest 2.06e3, b21-25 line 669, (3.9123456, 0.30654321))
and start noise3 <= 1e7 by a replay row (largest 5.7e-4) or by its code's cap (728f59c7: 1e2, 998fd290: 1e7); 28
points are valued in one source and without value in another, each listed with both files (`merge_check.log`);
`--mutate=noise` fails. 90 points valued by two parts keep the first part's record; the two records agree to 6.5e-8
in F_3 and within 1.41 sigma in R. The sheet check passes along grid lines (0 of 4102 pairs) and on every part's
leaves (0 of 136, 179, 104, 122 and 45 cells), and the planted switch fails (`sheet_check.log`). samebits: the Mac
cache is the merged file's first 1049 lines with all 994 valued records unchanged; each dh610 part is not a prefix by
construction and differs only at those 90 points; `--mutate=flip` fails (`samebits.log`).

Box 16's -1 zero at 6da7da7b (`loc/run_loc2.sh`, 00:36-03:42 UTC on 20 Nov, `loc/z16_6da7da7b/`, log
`loc/loc_z16_6da7da7b.log`): the relocation cell's boundary winds -1 at xi1 0.17 (32 points, 1 leaf). At 0.17 the
zero is not located: the locate's last nine points lie under the 10 sigma guard (|R| 29-215 against sigma 58-126). At
0.18 (`--r1b`, 61 points, sigma 4.3-10.6) it is located at A 3.553347, w/w_inf 0.413172 (|R| 0.96 at the last step,
floor 8.86), 8.2e-5 from the nearest 0.17 guard point (3.5534143, 0.41321881; |R| 28.9) and 6.5e-4 from the farthest. Every point is on b16-20's sheet: |dF_3| to the nearest b16-20 point is
1.0e-4-1.8e-3 at 0.17 and 1.0e-4-2.4e-4 at 0.18 (`diag/nearest_f3.py`, `nearest_f3.log`; the 998fd290 bad-seed points
of `loc/z16/` read 0.315-0.318 and fail, as they must), and `sheet_check.log` passes on the cell's edges. The M = 5
start (`m5/m5_start.py --r1b`, new; without it the file has no zero located at 0.17 and exits 1) is
`m5/z16_start.txt`.

Box 16's -1 zero, M = 5 (20 Nov 03:44-04:06 UTC, `m5/`, summary `m5/z16_m5_summary.log` from `m5_read.py`): one
fixed-(A, w) `hier.py 5 --fixA --schur` solve at the zero located at 0.18 (`z16_start.txt`), at xi1 0.17, then at
#1026's radii 0.2 and 0.25. No first attempt reaches the bar (|r_3| 1.9e6, 1.1e6, 7.5e5). `m5/m5_repeat.py` (new)
applies #1027's repeats (the protocol of #976, #977, #1002: up to three from the best end state, harmonics times
1 + 1e-7 u, random.Random(1027); A and w as the FIXED-A line prints them, 3e-10 from the start). At 0.25 the first
repeat converges (|r_3| 2.3e-7, |r_5| 2.2e-7): |F_5/F_3| 0.2913, under #1027's 0.3, so the zero is kept by that rule.
At 0.2 the three repeats reach |r_3| 1.2e-4 to 2.0e-4 with the same 0.2913; the 0.2 and 0.25 harmonics agree to
3.8e-5 (F_3/F_1) and 1.1e-5 (F_5/F_1). The control is checked at 0.2 only (`control_1026_xi0.2.log`, |F_5/F_3|
0.0556); at 0.25 dh610's #1026 control did not converge (|r_3| 8.3e3) and the Mac's (`control_1026_xi0.25.log`) had
not printed its start residuals after 20 min.

`m5/z16_m7_inputs.json` (the coordinator's order, for dh610's M = 7 solve of box 16's zero): from the converged
0.25 log by `m5/m5_inputs.py` (new; it refuses a log not under the bar, and refuses the 0.2 repeat): (A, w/w_inf)
(3.553346605, 0.413172285) as the solve ran them, xi1 0.25, x = (B3, C3, B5, C5) = (0.843294116, 0.003092743,
0.24539945, 0.010876743) from the last level-3 line (9 digits as printed), F_3/F_1, F_5/F_1, the residuals, the
command, and the M = 3 zero's 0.18 location from the count file.

Boxes 29-31 recount (`fix2931/`, `loc/run_loc.sh fix2931`, 998fd290, 00:17-04:09 UTC on 20 Nov): the 3 unresolved
cells of `I1021-dh610/b26-31/leaves_M3_cand_r0.17_fix_b26-31_998fd290.jsonl`, recounted with `--retry` and starts
0.2 then 0.25, seeded from `I1021-dh610/b26-31/points_M3_r0.2.jsonl`, on a copy of b26-31's 0.17 cache at raw
e2bb13a0 (807 lines; the inputs are byte for byte dh610's raw files and are not copied here). Count
(`count_M3_cand_r0.17_fix_b29-31_998fd290.json`): 54 leaves, 17 splits; boxes 29, 30 and 31 wind 0 (|boundary
winding| at most 1.4e-16), leaf sums 0. Box 31 keeps 2 unresolved cells, A 3.8498-3.9123 by w/w_inf 1.0065-1.0315 and
1.0315-1.0565, from one point without value at the midpoint of their shared edge: (3.8810956, 1.03154321), line 907,
info 2.1e-4 at 0.17, fix.ok false with an empty trail. Since the box winds 0 and its valued leaves sum to 0, the two
cells together hold 0. The sheet check passes on the leaves (0 of 54 cells across a switch) and along grid lines (0 of
1429 pairs, largest |dF_3| 0.0479), and the planted switch fails (`sheet_check.log`, `sheet_check_mutate.log`). The
argcount log of this run is lost. `run_loc.sh` was edited at 00:23 UTC while this job ran from it, and when argcount
ended, bash read the edited file from its old offset. It ran the tail of the argcount line as a command, and that
line's redirect rewrote `recount.log` with the error (the "exit 127" in `exits.txt`, and `run.out`). argcount wrote
the points, leaves and count files itself, and they are whole. `loc/run_loc3.sh` and `final/run_record.sh` are now
one block, which bash reads whole before it runs; a test with an in-place edit during a run misreads the plain form
and not the block.

The 0.25 control (20 Nov 04:06-06:06 UTC, `m5/control_1026_xi0.25.log`): it ended at its 2 h cap (exit 124) without
printing its start residuals. `m5/trace_run.py` (new) dumps the stacks every 60 s; a rerun of 5 min at nice 19
(`control_1026_xi0.25_trace.log`) is in the first residual throughout, in inner_np's DOP853 integration (hier.py
res -> demixed_multi -> inner_np.jumps -> integrate -> solve_ivp). dh610's hier_nb run of the same solve
(`I1026-dh610/logs/fix_control_xi0.25_01.log`) prints start residuals |r_1| = |r_3| = 0 and ends at |r_3| 8.3e3.
The control has converged at 0.2 only, so box 16's M = 5 verdict is the one at 0.2, where no attempt reaches the bar
(best |r_3| 1.2e-4 of three repeats): M = 5 gives no verdict on box 16. `m5/m5_read.py` reads the logs for
`z16_m5_summary.log`.

Box 7's -1 zero at 6da7da7b (`loc/run_loc2.sh`, 03:42-06:39 UTC on 20 Nov, `loc/z7_6da7da7b/`, log
`loc/loc_z7_6da7da7b.log`): the relocation cell's boundary winds -1 at xi1 0.17 (83 points, 1 leaf). The zero is
located at 0.17, A 3.245479, w/w_inf 0.345852 (|R| 0.358, floor 1.83), and at 0.18, 8.5e-6 away (|R| 0.054, floor
0.222). Every point is on the Mac cache's sheet: |dF_3| to the nearest point of `m3/points_M3_r0.17.jsonl` is
1.1e-8-9.8e-4 at 0.17 and 1.1e-8-8.5e-5 at 0.18 (`nearest_f3.log`), and `sheet_check.log` passes on the cell's
edges. The M = 5 start from the 0.17 location is `m5/z7_start.txt`.

b11-15's +1 at 6da7da7b (`loc/run_loc3.sh`, 06:09-06:40 UTC on 20 Nov, `loc/b1115p_6da7da7b/`, log
`loc/loc_b1115p_6da7da7b.log`): the cell (`leaf_b1115p.jsonl`) winds +1 at xi1 0.17; after 1 split its 4 leaves keep
2 unresolved cells, A 3.5131-3.5288 by w/w_inf 0.2078-0.2140 and 0.2140-0.2203, and its valued leaves sum to 0, so the
+1 lies in those two. Their shared edge holds one point under the 10 sigma guard, (3.5248456, 0.21404321): |R| 5995
against 10 sigma 7277 (continuation-valued, noise3 35.9). The points are on b11-15's sheet (|dF_3| to the nearest
b11-15 point 8.8e-5-2.4e-3, `nearest_f3.log`), and the sheet check passes on the 4 leaves (0 cells across a switch).
`loc/run_loc4.sh` counts the same cell at 0.18 (located again at 0.2), seeded from these points, as box 16's zero
was located at 0.18.

Box 7's -1 zero, M = 5 (20 Nov 06:40-06:46 UTC, `m5/`, summary `m5/z7_m5_summary.log`): one fixed-(A, w)
`hier.py 5 --fixA --schur` solve at the zero located at 0.17 (`z7_start.txt`), at xi1 0.2 only (the coordinator's
rule: the 0.25 control never converged), then #1027's repeats (`z7_repeat_xi0.2.log`). The first attempt ends at
|r_3| 2.2e3; the three repeats reach |r_3| 1.0e-5, 2.8e-6 and 6.9e-5 (|r_5| 9.1e-8 to 2.0e-7), none under the bar,
all with |F_5/F_3| 0.3186 and the same printed harmonics. By the rule the M = 5 test gives no verdict on box 7.

b11-15's +1 at xi1 0.18 (`loc/run_loc4.sh`, 06:42-09:47 UTC on 20 Nov, `loc/b1115p_r0.18_6da7da7b/`, log
`loc/loc_b1115p_r0.18_6da7da7b.log`; seeded from the 0.17 relocation's points): the cell winds +1 (boundary winding 1.000),
10 leaves after 3 splits, none unresolved, leaf sum 1. The zero is located at 0.18 at A 3.526471, w/w_inf 0.211495 (|R| 9.3,
floor 14.3), and again at 0.2, 3.7e-6 away (|R| 0.14, floor 0.77). Its points are on b11-15's sheet (|dF_3| to the nearest
b11-15 point 1.6e-4 to 2.9e-3 at 0.18 and 3.2e-4 to 9.9e-4 at 0.2, `nearest_f3.log`), and the sheet check passes on the
10 leaves (`sheet_check.log`). `m5/b1115p_start.txt` is the M = 5 start from the 0.18 location (`m5/m5_start.py`).

Merge with b21-25-fu (20 Nov 15:21-15:22 UTC, `merge_fu/`, the coordinator's order: dh610's `I1021-dh610/b21-25-fu`
at raw 18338ce4, #1021 comment 7039639393). Written before the recount of record.

- `sheet_fu.sh` (`sheet_fu.log`): b21-25-fu's cache (1234 lines) is on one sheet along grid lines (0 of 1906 pairs
  flagged, largest |dF_3| 0.056). On b21-25's leaves and on the leaves of all eight follow-up passes, 0 cells lie
  across a switch (of 122, 21, 14, 3, 29, 5, 11, 8, 4). The planted switch fails.
- `run.sh` is `../merge_dry/run.sh` with b21-25-fu's points file in place of b21-25's and the passes' leaves added to
  the sheet check (`sheet_dry.sh`). Its inputs are listed in `in/SHA256SUMS`; the copies of other folders' files are
  not committed. `spec.json` gives b21-25-fu's lines: 1043 is b11-15's line 661 and 1044 is
  fu_seed's record (fix2931's line 889), both appended by dh610's `fu_append.py` with a `fu` key and otherwise the same
  records; 1045-1234 are argcount 6da7da7b with its cap 1e7 (`fu_value.py` and the recounts).
- `merged.jsonl`: 2630 lines, 2563 points, 2556 valued, 7 without value. Merge check PASS: largest final noise3
  2.06e3, largest replayed start noise3 5.7e-4; the 28 points valued in one source and without value in another are
  listed with both files and lines (`merge_check.log`). (3.6623456, 1.06904321) now comes from b21-25-fu's line 1044,
  which precedes fix2931 in the merge order; (3.6623456, 0.20654321) comes from b11-15's line 661, as before. 90 points
  are valued in two sources with different records (largest |dF_3| 6.5e-8, |dR|/|R| 0.017).
- Sheet check of `merged.jsonl`: 0 of 4445 grid-line pairs flagged, 0 cells across a switch on all 13 leaves files.
  samebits: the Mac cache's 994 valued records are unchanged. `--mutate=prefix`, `noise`, `switch` and `flip` fail.

Recount of record (`final/run_record.sh ../merge_fu/merged.jsonl 1`, 1 process at nice 10; argcount 6da7da7b, default
starts 0.25 then 0.2, `--retry`, cap 1e7; then the plant on a copy, samebits and the sheet check). Windings count only
where the record's sheet check passes. Cells left unresolved go into the record as undecided, with the reason.
dh610's follow-up names two: the box A 3.6623-3.9123 x w/w_inf 0.2065-0.3065, nan because its corner
(3.9123456, 0.20654321) has no value in any start ("continuation lost S3's zero after [0.25, 0.24875]"), and four
cells of w/w_inf 0.4065-0.5065, where |R| at (3.7560956, 0.43154321) and (3.8732831, 0.48779321) is 6.5-7.9 times the
rounding floor sig0, under the 10 sigma guard.

dh610's controls in b21-25-fu (`merge_fu/fu_controls.py`, `fu_controls.log`; `--mutate=exits` flips one reported exit
and fails, `fu_controls_mutate.log`). At the start the argcount selftests give 0 1 1 1 and fu_value's selftest and
`--break` give 0 1. In each pass, the rows that the f3 and lowguard retests would change are recomputed from the pass's
rows, without fu_value.py's code, and every exit in `exits_fu.txt` agrees with them:

| step | f3 (F_3 + 0.3i) | lowguard (guard 1 sigma) |
|---|---|---|
| 1, passes 1-3 | fires (3, 4, 4 rows) | vacuous: no row is blocked by the guard alone |
| 2, passes 1-3 | fires (4, 3, 3 rows) | fires (2, 3, 3 rows) |
| 3, pass 1 | fires (1 row) | fires (17 rows) |
| 3, pass 2 | vacuous: no row accepted | fires (12 rows) |

In step 1 every rejected row has no value: pass 1, 9 rows where the continuation lost S3's zero; pass 2, 6 of those,
1 at the right-hand-side bound and 1 at the wall bound; pass 3, 6 of those and 2 inner-solve step-size failures. So
the lowguard mutation has nothing to change there, and its exit 0 tests nothing.
