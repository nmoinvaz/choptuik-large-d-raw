# I1013-rpi5-cap: #1013 step 4 rerun, the M = 3 argument-principle count of the upper box A 3.6 to 4.35 with argcount's bounds (998fd290)

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1013 (step 4 of its commands; #995's runner step). Task named by the coordinator by message, 2026-11-19 (the box cut to A <= 4.35, noise cap 1e7 and commit 998fd290 after #1021's measurements). The earlier folder `I1013-rpi5/` (the stopped `--m3fix` run at 068913b4, no count) stays as it is.

Code: `wip/argcount-m3-bounds` at 998fd290 ("argcount: set the M = 3 noise cap's default from measured noise (#1021)"), worktree `~/Source/cl-1013cap7`, `solver/inner_stokes/argcount.py`. Python 3.13.7 (venv-choptuik), numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, python-flint 0.9.0 / FLINT 3.6.0 (the exact versions the run prints are in `logs/exits.txt`).

## Written down before the run (the coordinator's message and the issue's rule)

Driver: `run_rpi5_upper.sh` (copy of `I1021-mac/split/run_rpi5_upper.sh` at choptuik-large-d-raw 205dadd8, read before running), `bash run_rpi5_upper.sh ~/Source/cl-1013cap7 ~/Source/venv-choptuik/bin/python <RAW>/I1013-rpi5-cap`. It refuses unless HEAD is 998fd290 and `m3/` does not exist (a fresh folder), then:

1. the selftest and four mutations (`nocap`, `starts`, `norecount`, `lowcap`): required exits `0 1 1 1 1` (the script stops otherwise);
2. step 1: `argcount.py --M=3 --A=3.6,4.35 --wf=0.5,1.3 --nA=3 --nwf=8 --r1=0.17 --r1b=0.18 --m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4`, at nice 10, 12 h cap: the base grid is A 3.6123 to 4.3623 (step 0.25) by w/w_inf 0.5065 to 1.3065 (step 0.1), 4 x 9 = 36 points, counted at xi1 0.17 (the 0.2 start first; at 0.2 these points have no start);
3. step 2: the recount rung at xi1 0.18 (`--recount` of step 1's leaves, seeded with its points), 6 h cap.

Each point writes one record and one log line (a point stopped by the wall or the call bound is recorded without value, with `fix.bound`; it is reported, not retried). Per-point progress is posted on #1013 every 3 h. The persistence rule is the issue's (an M = 1 zero persists if an M = 3 zero of the same sign lies within |dA| <= 0.2 and |d omega/omega_inf| <= 0.25; each M = 3 zero serves its nearest M = 1 zero); it is applied to the leaves file by the issue's analysis, not by this run. Stop by the coordinator's word or by a failed selftest exit; no per-point cap beyond the script's.

Above A 4.5 real points' noise reaches the fault level (#1021), so that part of the box waits for a different fault test; it is not run here.

## Runs

(filled in below as the run goes)

## Note from the coordinator, 2026-11-19 (about 00:30 UTC)

The run stays as it is, but its counts are not used until xfchecks' sheet check passes on them: the start radius can put a point on a different root of S3 = 0 (F3 on another sheet), and a winding across such a switch is invalid. The run changes nothing for this; the next #1013 post says so.
