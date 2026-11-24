# I1080-win2: an M = 5 start at #1080's second excited zero x2, by continuation in (A, w/w_inf), and its walk

Machine win2 (desktop-pc, Windows 11, 20 cores, 95 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1080.
Coordinator t5's order by hc, 2026-11-24 17:21 UTC. Runner: hc terminal t24.

## Code and environment

- Branch `wip/i1080-x2` (from feat/inner-mp 6b807830), worktree `D:\choptuik-i1080x2`; new script
  `solver/inner_stokes/start_path.py` (commit dd00111a). value_mp.py, zero_mp.py, inner_mp.py, hier.py, hier_nb.py
  unchanged from 6b807830.
- venv `C:\Users\nathan\source\venv-i962`: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0 (backend
  python, no gmpy2), numba 0.68.1. One BLAS thread per process.

## Files

Written as the work goes; see the Status list.

## Status
- 2026-11-24 17:59 UTC: `run_start_path.sh` (float64 continuation x1 -> x2; M = 3 control PASS 6.7e-9, its --mutate=end FAIL as required; M = 5 end at n 20 and n 40 agree to 9e-10). `explore/`: the diagnostics of why the start from x2's M = 3 harmonics fails (scratch scripts; `cond5.py` and `cont_try.py` import main 57eda12c's hier from `D:\choptuik-i1080main`). Comment 7140314124.
- 2026-11-24 18:13 to 19:05 UTC: `run_polish.ps1`, the extended-precision polish at x2 (value_mp pointv, r1 0.17): r_rest 1.7e-26, v within 4.8e-3 of the float64 start: both criteria PASS. `logs/polish_x2.json`, `logs/polish_x2_progress.log`, `steps_polish.txt` (the exit code was not captured by the launcher; the JSON line is complete).
- Walk: `run_walk.ps1` (`run_walk.cmd` by WMI), rows `walk_x2.jsonl`, log `logs/walk_x2.log`, steps `steps_walk.txt`; reading of comment 7111416293 (i)-(iii), posted before the start.
