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
