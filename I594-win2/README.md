# I594-win2: #445's unfinished R 0.2 circle around 0.032 + 3.086i on the exact determinant of the double-double matrix (--ball=320)

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/594, part (b), queued by the coordinator at 12:23 UTC and started 14:06:00 UTC, 2026-11-12. Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads. Cap 6 h (20:06 UTC), enforced by a background timer that killed the process tree at 20:06:00 UTC.
Code: worktree `D:\choptuik-i594` detached at main `4b33cc9` (`hp/modecount_circle.py --ball=PREC`, `hp/modecount_qdet.py`; with a given `--tag` the `_ball<PREC>` suffix is kept, which `f338b9e` did not do). `modecount_cx` copied from `D:\choptuik-i573` (sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3, built from Rust sources identical between 80b5056 and f338b9e), Python 3.12.8 in venv-t126, python-flint 0.9.0.
State `modecount_state_D61.0264_M64_kf23.npz` from `I252-mac/states/` of the raw repository, sha256 179d0bd69aae77c9..., read as `hp/data/modecount_state_D61.0264_M64_kf23.npz`; the state's gate reads |F| 8.5e-21.
Command (`run_594b.sh`, which logs the start and the exit to `exits_594.txt`): `python modecount_circle.py data/modecount_state_D61.0264_M64_kf23.npz 0.032,3.086,0.2 --kf=23 --n0=20 --fmax=1e-15 --tag=D61.0264_M64_kf23 --ball=320 --threads=9 --data=<RAW>/I594-win2/data --res=<RAW>/I594-win2/data/res.jsonl`, from `hp/`. These are #445's arguments plus `--ball=320 --threads=9`. The cache is `data/modecount_D61.0264_M64_kf23_ball320_evals.jsonl` (checked after the start: the suffix is there, and #445's double-double cache is not read), the log `data/modecount_D61.0264_M64_kf23_ball320.log`, the run's stdout `run_594b.log`.
Acceptance (#594): the circle either resolves (every step at most pi/4, no verification mismatch, no alias left) with an integer winding, or the record says which steps stay above pi/4 and where; where it resolves, the windings of the sub-circles of #569 and #571 are compared with it. Results follow in this README.

## Result at the cap (2026-11-12 20:06:00 UTC)

**The circle did not resolve and no winding is read.** The run was stopped by the cap (the timer's kill, `exits_594.txt`: "594b exit 1 2026-11-12 20:06:00 UTC" is the kill, not a result; the determinant in flight, about 100 s of work, was lost). The coordinator's order of 18:11 UTC was to keep the cap and to post the state; an extension waits on #605 (macm3: is det M at M 64 smooth in lambda at the ulp scale).

`final_594b.py` on the cache (`final_594b.log`, `data/steps_at_cap.csv`, one row per point on the circle with the arg step to the next):

| quantity | value |
|---|---|
| determinants | 205 (203 on the circle, 2 at distance 0.4 from the centre), median 104.8 s, 5.97 h of determinant time in 6.00 h |
| steps above pi/4 | **119 of 203** (56 between pi/4 and pi/2, 63 between pi/2 and pi), the largest 3.123 rad |
| largest angular gap | 0.0393 rad (the 160-point pass; 86 intervals are already at 0.020) |
| sum of the step sizes | 228.9 rad, a lower bound of the total variation of arg on the circle (steps near pi hide more), which needs at least 291 points at pi/4 a step, 88 more than done; it grew 101.8, 135.9, 174.4, 213.5, 228.9 rad at 90, 112, 142, 183, 203 points |
| where the steps above pi/4 are | in every quadrant of the circle: 40 of 80 points in 0 to pi/2, 27 of 43 in pi/2 to pi, 29 of 40 in pi to 3pi/2, 23 of 40 in 3pi/2 to 2pi (the points are denser where the bisection refined); the list is `data/steps_at_cap.csv` |

Step size by gap, the points on the circle ordered by angle: at gap 0.039 rad (117 intervals) the median |step in arg| is 1.14 rad and 64% of the steps are above pi/4; at gap 0.020 rad (86 intervals) the median is 0.80 rad and 51% are above pi/4. Halving the gap lowers the median step by 0.70, between 0.5 (a smooth arg) and 1.0 (a step that does not depend on the gap); uniform random phases would give a median of pi/2 = 1.57. The median step of ln|det| goes 1.02 to 0.80 the same way. So the exact determinant of the double-double matrix at M 64 on this circle is neither smooth at this resolution nor pure noise; this is an observation of 203 points and decides nothing about #605's question.

**Acceptance (#594).** The circle does not resolve (every step <= pi/4 not reached; no verification run); the record says which steps stay above pi/4 and where (above, `steps_at_cap.csv`); there is no winding to compare with the sub-circles of #569 and #571. Part (a) and the control are macm3's (`I594-macm3/`, both passed per its comments of 13:51 and 14:43 UTC).

**To resume:** `bash I594-win2/run_594b.sh` continues from the cache with the same command (the cache is appended; `exits_594.txt` logs the new start and exit). A 6 h run gave 205 points; at least 88 more (about 2.6 h at 105 s) are needed, and probably many more.

