# I190-macm3: the D 45 cut scan extended to kf 23, 25 and 27 (small circles)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel 0.1.0 cp314 neon,
modecount_cx rebuilt for 3.14), main 84d166fe. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/190. Extends I178-macm3 (Python 3.13, main e04d6f17).

`run_kf.sh K [K ...]` runs, for each K in turn (1 thread, nice 10, caffeinate -is): python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz 1.14,0,0.06 2.057,0,0.1 --M=48 --kf=K --fmax=1e-15
--tag=D45.0507_M48_kfK_circ --res=<raw>/I190-macm3/circles.jsonl, then moves the cache, the log and any re-converged state from hp/data into data_kf<K>/. The up7 state is M 32 native, so every K resamples to M 48
and re-converges in its layout (Newton, then Levenberg-Marquardt), as in I178. kf pins the p1 harmonics above kf to zero (make_solver's docstring), so a higher kf frees more harmonics: kf 21 frees the odd
harmonics up to 21 (11 of them), kf 23, 25, 27 free 12, 13, 14.

Written before the run.
  Control of the new geometry (an addition to the issue's list, so that the new circle can fail): kf 21 runs first, and its 1.14 circle (R 0.06) must wind +1 (I178 placed the zero in |lambda - 1.14| < 0.03
  and found +1 at 1.14 R 0.03); if it does not, the K above 21 are not read. The 2.057 circle (R 0.1) must wind +1 at every K, the issue's control.
  Verdict per K: the winding of the 1.14 circle with its largest phase step and verification mismatches, and the setup |F| after LM. A setup above 1e-15 raises (hp/modecount_common.setup) and is
  reported, not forced; the state it saves is moved out of hp/data.
  Reading rule, fixed now: winding +1 at kf 23, 25, 27 means one zero stays in the disc; 0 means it left (moved out of the disc or vanished); +2 or more means more zeros inside; a winding that
  differs from the others in size or sign is reported with the circle's data. Only the winding is read, the location is not (a moved zero needs a locating round, as in I178, which is not part of this task).

Results (macm3, main 84d166fe, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall in every run, caffeinate -is held; the kf 21 run shared the machine with I70-macm3/job3's count).
  The kf 21 control passed (exit 0 22:41:15 UTC): 1.14 R 0.06 winds +1 (24 points, max step 0.375 rad), 2.057 R 0.1 winds +1. So the K above were read.
  kf 23, 25, 27 (exit 0 each, 25.1 min wall): the 2.057 circle winds +1 at all three (24 points, max step 0.353 rad, 0 mismatches), and the 1.14 circle (R 0.06) winds 0 at all three (16 points,
  max step 0.024 rad, 0 mismatches). Setup |F| after Levenberg-Marquardt 2.0e-19 at each (Newton alone stays at 3.3e-09), below the 1e-15 gate; no setup raised. By the reading rule above: 0 means the zero left.
  The zero of I178 is therefore present at kf 21 only (kf 13 to 19 absent, kf 23 to 27 absent). summarize.txt: every circle.
  Not a replay: compare_K.txt, ln|det| at the 44 shared points shifts by -105 to -113 and -110 to -116 between kf 23, 25, 27 and |d arg| reaches 0.27, the saved states differ by 1.0e-11 and 1.2e-11.
  state_vs_kf.txt (from the saved states of I178 and this folder): the converged state moves with the cut by 2e-4 to 3e-3 between consecutive kf up to 21 (kf 21 to 23: 8.4e-04) and by about 1e-11 from kf 23 on;
  Delta(kf) differs from Delta(27) by at most 1.4e-10 at every kf (5.2e-12 at the production kf 13).
