# I231-macm3: D 55.04 and D 61.03 counted at a third resolution, M 40, with the cut at kf 23

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main 25b50d1d. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/231. Beside I240-macm3 (D 54.04 at M 48): three runs at once, one thread each.

Commands (D55_M40/count.cmd and D61_M40/count.cmd, caffeinate -is, nice 10, from the repository root): python3 hp/modecount_wind.py hp/data/states/up10_D55.0351.npz --M=40 --kf=23 --h0=0.6 --lam=2.04768412771239
--fmax=1e-15 --resolve=last --tag=D55.0351_M40_kf23 --data=<raw>/I231-macm3/D55_M40/data, and hp/data/seeds/local/up23_D61.0264.npz with --lam=2.043532530673195, tag D61.0264_M40_kf23, --data=<raw>/I231-macm3/D61_M40/data.
Both states are M 32 native (769 unknowns), so setup resamples to M 40 and re-converges in the kf 23 layout (Newton, then Levenberg-Marquardt), as at M 48 (#212, #232). No M 40 state or cache is in hp/data or
--data at the start (hp_data_before.txt). If hp or the layout rejects M 40, or a setup misses |F| <= 1e-15, that run stops and is reported (the state it saves is moved out of hp/data).

Written before the run. Table: the 8 boxes at each D beside the M 32 and M 48 rows (D 55.04: M 32 all 0 (I237), M 48 B0 +2, U0 +1, U +1, full +2 (I232); D 61.03: M 32 kf 21 all 0 (#168), M 48 kf 23 B1b +6, B1c +2, B1 +8, U +8, full +24
(I212)), with both mismatch counts per edge (all passes and the last pass). Reading rule, fixed now: at each D the extras at M 40 are "absent" when wind(g) is 0 in every resolved box, "present in the same boxes as at M 48"
when the nonzero boxes are the same set as at M 48 (windings may differ), "present elsewhere" when a box that is 0 at M 48 is nonzero, whatever the M 48 boxes do. The count does not track zeros: "the same lambda" is not
tested here, only the boxes. An unresolved edge is "not a count" and its boxes are not read. M 64 is not part of this task (#141).

STOP (macm3, 09:11 UTC, both runs, exit 1 within seconds; D55_M40/count.log, D61_M40/count.log, exits.txt): hp rejects M 40 at the solver construction, before any convergence or determinant:
  ValueError: M must be one of 8, 16, 32, 48, 64, 80, 96, 128, 160, 192, 256, 320, 384, 512 (hp/src/python.rs:498, raised by hpkernel.driver.make_solver -> Solver(M, ...), called from modecount_common.build_pair).
  Nothing was evaluated or written: the --data folders are empty, hp/data is unchanged. Per the issue, both runs stop here and are reported. A kernel that accepts M 40 needs a build with that size added to the list in
  hp/src/python.rs (the binding dispatches on a fixed set of M), a code change for the coordinator. The next resolution above 48 that the kernel accepts is M 64 (#141) and M 80.

Second attempt (coordinator's message, 2026-11-09: hp now accepts M = 40, main 1bad14fd "hp: accept M = 40 in the solver binding", B = 5 added to the block list; after #240 ended so the rebuild does not replace a module a running count has loaded):
  1. git pull (1bad14fd), bash hp/build.sh with venv-macm3-314 (rebuild.sh: LTO off, 16 codegen units as in #179; build.log, build_time.txt, freeze_before/after_rebuild.txt), and bash hp/modecount_build.sh
     (build_cx.log): the binding change is in hp/src/python.rs, and modecount_cx links the hp crate, so it is rebuilt with the same venv active so that the control and the M 40 runs use one set of modules (an addition to the message).
  2. Control for the rebuild, written before the run: control_D55_M32/ reruns #237's (c) into a fresh folder: python3 hp/modecount_wind.py hp/data/states/up10_D55.0351.npz --M=32 --kf=23 --h0=0.6 --lam=2.04768412771239
     --fmax=1e-15 --resolve=last --tag=D55.0351_M32_kf23 --data=<raw>/I231-macm3/control_D55_M32/data (control.cmd). Pass: its evals cache equals I237-macm3/D55_M32/data's bit for bit, line by line (compare_control.py:
     re, im, lnabs, arg, pmin, pmax equal; the timings are excluded), and the 8 boxes' windings equal. If they differ, stop and report: the M 40 runs do not start. The check can fail: compare_control.py also compares against
     a deliberately altered copy (one digit of one lnabs) and must report it as different.
  3. The two M 40 counts as above, both at once, if the control passes (the readings above unchanged). If M 40 is rejected again at the CSolver or a setup misses 1e-15, that run stops and is reported.

Rebuild and control result (macm3, awake = wall): hp/build.sh exit 0 in 885 s (peak 10.55 GB, LTO off, 16 codegen units; freeze_after_rebuild.txt differs from freeze_before_rebuild.txt only in the hpkernel wheel's sha256), final line "hpkernel neon multidouble neon";
  hp/modecount_build.sh exit 0, "Finished in 0.06s" (modecount_cx links hp without its python feature, so python.rs is not part of it: nothing recompiled). Control (control_D55_M32/, exit 0 at 10:57:53 UTC, 735 s): the evals cache has
  85 lines equal to I237-macm3's in re, im, lnabs, arg, pmin and pmax, bit for bit (compare_control.txt, exit 0), the one-digit change to the control copy is detected, and the 8 boxes are all 0 as in I237. So the rebuild changes nothing at M 32.
  The two M 40 counts started at 10:58 UTC.

STOP again (macm3, 10:58:41 UTC, both M 40 runs, exit 1 within seconds): hp's Solver now accepts M = 40 (make_solver passed), but the complex-lambda determinant solver modecount_cx does not:
  hp/modecount_cx/src/lib.rs:720: ValueError: M must be one of 16, 32, 48, 64 (raised by modecount_cx.CSolver(...), modecount_common.build_pair line 45, reached after make_solver). The macro make_ctx! there dispatches on
  B = M / 8 in {2, 4, 6, 8} (lib.rs:795). B = 5 is the missing entry (hp/src/python.rs got it in 1bad14fd). Nothing was evaluated or written to --data; hp/data is unchanged by these two runs. modecount_cx needs the same one-line
  change, a code change for the coordinator, then hp/modecount_build.sh (32 s) and the two counts rerun. The rebuild control passed (above); only the CSolver blocks M 40.

Third attempt (coordinator's message after main 8bdb7937 "modecount_cx: accept M = 40"): modecount_cx rebuilt (build_cx2.sh, cargo 57 s, build_cx2.log). hp/modecount_build.sh's last step is `cp lib build/modecount_cx<EXT>`, which writes into the
  module file that I241's three running counts have loaded, so build_cx2.sh does the same cargo build with the same flags and installs the result by rename (the old file keeps its inode for the running processes); sha256 before and
  after in modecount_cx_sha256_*.txt. smoke_cx.py (one D 61 M 32 determinant): bit-identical to I160's record, its control differs (smoke_cx_M40build.log). The M 32 control is rerun after this rebuild because the determinant comes from
  modecount_cx (control2_D55_M32/, compare_control2.py, same pass rule as the first control, written above: 85 lines bit for bit equal to I237-macm3's, the one-digit change detected). The two M 40 counts start at the same time as the
  control (the readings of the first attempt unchanged); if the control fails, the M 40 results are not read and the failure is reported. They run beside I241's three counts (3 + 3 threads).

Second control result (control2_D55_M32/, exit 0 at 11:32:00 UTC, 28 min with six processes running; compare_control2.txt, exit 0): the evals cache has 85 lines equal to I237-macm3's in re, im, lnabs, arg, pmin and pmax, bit for bit, the one-digit
  change to a copy is detected, and the 8 boxes are all 0. So the modecount_cx rebuild with B = 5 changes nothing at M 32, and the M 40 results are read.

D 55.04 at M 40 (D55_M40/count.log, exit 0 at 13:26:03 UTC, 293 determinants at about 28 s, 2 h 22 min from 11:03:39; awake = wall): setup |F| 1.2e-07 in the layout, 1.2e-07 after Newton, 3.3e-19 after Levenberg-Marquardt (gate 1e-15 passed); 14 edges, mismatches 0 in any pass and 0 in the last pass,
  largest step 0.392 rad, at most 4 passes; real axis only the two expected sign changes. wind(g): B0 +2, U0 +1, B1a +2, B1b 0, B1c 0, B1 +2, U +3, full +8 (winding of det M: 3, 1, 3, 1, 0, 4, -4, -4). Reading rule (above): the extras at M 40 are PRESENT ELSEWHERE than at M 48
  (M 48: B0 +2, U0 +1, U +1, full +2): B1a is nonzero at M 40 and 0 at M 48. Not monotone in M: M 32 none, M 40 eight in the full box, M 48 two.
  Moments, no new determinant (D55_M40/moments.log; evals file 293 lines before and after): B0 0.24271 +0.92524i (spread 2.9e-2), B1a 0.47109 +1.44349i (2.9e-2), U0 0.09923 +4.48036i (2.8e-3), U 0.34863 +2.61221i, 0.36031 +2.16089i, 0.59532 +5.03932i. The M 48 pair is at 0.1996 +0.2548i (I238).
Added to the issue's list, because its "why" asks whether a zero stays at the same lambda: circles on the M 40 state (circles_M40.cmd): at M 48's positions (pair 0.19957 +0.25475i R 0.2; U 0.31895 +3.33140i R 0.2; U0 0.06118 +3.85263i R 0.3), at M 40's own B1a position (0.47109 +1.44349i R 0.2), and lam_phys (2.04768412771239, R 0.2, must wind +1;
  if it does not, none of these circles is read). A circle at an M 48 position that winds 1 with its zero within 0.05 of the M 48 position: "stays"; winding 0: "does not exist at M 40 there".

Circles on the D 55.04 M 40 state (circles_M40.log, exit 0 at 14:56:22 UTC, 66 min; awake): lam_phys (2.04768412771239, R 0.2) winds +1 and returns 2.047684 -0.000000i (estimate 4.6e-08): the circles are read. At M 48's positions the winding is 0: pair (0.19957, 0.25475, R 0.2) 0, U (0.31895, 3.33140, R 0.2) 0,
  U0 (0.06118, 3.85263, R 0.3) 0: none of the three zeros that I238 located at M 48 exists at M 40 there. M 40's own B1a pair (moment 0.47109 +1.44349i) is confirmed: winding +1, zero 0.477308 +1.453280i (estimate 1.8e-06). 0 verification mismatches in all five.

D 61.03 at M 40 (D61_M40/count.log, exit 0 at 17:16:26 UTC, 723 determinants at about 28 s, 6 h 13 min from 11:03:39 beside other runs; awake = wall): setup |F| 1.3e-06 in the layout, 1.3e-06 after Newton, 3.8e-19 after Levenberg-Marquardt (gate 1e-15 passed); 14 edges, mismatches 0 in any pass and 0 in the last pass, largest step 0.392 rad, at most 4 passes
  (the long edge Im = y2, Re aR to aL: 322 points, phase change +93.3); real axis only the two expected sign changes. wind(g): B0 0, U0 +1, B1a 0, B1b +4, B1c +4, B1 +8, U +8, full +24 (winding of det M 1, 1, 1, 5, 4, 10, 1, 12). M 48 (I212, automatic edges): B1b +6, B1c +2, B1 +8, U +8, full +24 (kf 23, as counted; the later correction
  of #230 puts the true D 61 M 48 total at 30); M 32: all 0 (#168, kf 21; #160, kf 13). By the rule written above: the extras are present in the same boxes as at M 48 (B1b, B1c, B1, U, full) with U0 +1 added, which is "elsewhere" by the letter of the rule (U0 is 0 at M 48).
Second step (the coordinator's message): circles on the D 61.03 M 40 state at the four positions of #230's row at M 48 (1.3065 +1.4158i, 2.0073 +0.9727i, 2.5584 +0.5825i, 3.0196 +0.0958i), R 0.2, n0 20, plus lam_phys (2.043532530673195, R 0.2) as the control (circles_D61_M40.cmd). Rule written before: the lam_phys circle must wind +1 or none is read; a position "persists" at M 40 when its circle
  winds +1 with the zero within 0.05 of the M 48 position, "moves" when it winds +1 farther than 0.05, "absent" when it winds 0; the M 40 moments (D61_M40/moments.json, no new determinant) say where M 40's own zeros are.

Circles on the D 61.03 M 40 state (circles_D61_M40.log, exit 0 at 18:22:58 UTC, 65 min; awake): lam_phys (2.043532530673195, R 0.2) winds +1 and returns 2.043533 -0.000000i (estimate 2.1e-07): the circles are read. #230's row at M 48: 1.3065 +1.4158i winds 0 (absent at M 40);
  2.0073 +0.9727i winds +1 with the zero at 2.042590 +1.150727i (estimate 6.4e-03): MOVES by 0.19; 2.5584 +0.5825i winds 0 (absent); 3.0196 +0.0958i winds 0 (absent). 0 mismatches in all five. By the rule above: one of four "moves", three "absent", none "persists" (within 0.05).
Final (macm3, awake = wall in every run, awake.log): compare_boxes.txt has D 55.04 and D 61.03 at M 32, M 40 and M 48 side by side (the D 61 M 32 column is #168's kf 21 count; #160 at kf 13 is also all 0). Extras: none at M 32; at M 40 and M 48 present. D 55.04: M 40 B0 +2, U0 +1, B1a +2, U +3, full +8
  against M 48 B0 +2, U0 +1, U +1, full +2 (elsewhere). D 61.03: M 40 U0 +1, B1b +4, B1c +4, B1 +8, U +8, full +24 against M 48 B1b +6, B1c +2, B1 +8, U +8, full +24 (same boxes, U0 +1 added). Positions: none of the three D 55 M 48 zeros is at its place at M 40; of #230's four D 61 M 48 positions
  three are empty at M 40 and one has moved by 0.19. The M 40 states are in D55_M40/ and D61_M40/hp_data_after/; hp/data is back to its states.
