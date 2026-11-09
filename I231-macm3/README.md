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
