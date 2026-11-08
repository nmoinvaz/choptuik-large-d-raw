# I82-win2: sigma to k = 45 (K 45, J 1500, 1280 bits) at omega/omega_inf = 1.09, 1.10, 1.11 for the second zero of S1

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/82
Worktree `..\choptuik-t126` at origin/main c691ae3 (Python only, no hp build). venv-t126 (python-flint 0.9.0, as T155).
Three nodes in parallel, --procs 3 each (9 workers + 3 mains), below normal, thread env pinned to 1.

Recompute sigma to k = 45 to settle the candidate second zero of the harmonic-1 Stokes multiplier S1 near
omega/omega_inf ~ 1.10 (second-zero test #18 resolved a crossing only to +-0.006 with 17 coefficients). The coordinator
extends second_zero_nodes.py to the [m/(22-m)] sums and runs the test when the JSONs land.

From solver\inner_amp\, each node (>> appends to its log):
  amp_flint_par.py <wf> 45 1500 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out I82-win2\sigF_w<wf>_K45_J1500_p1280.json
  wf = 1.09, 1.10, 1.11.
Memory guard on the 1.11 main (the run to lose first): util_report.py --guard 10 --interval 300 <1.11 main PID>.
Pilot at 1 h: each log's last order + time vs T99-win2/scan45J1500/w1.0000.log (log_compare.py); stop if any run is
>3x slower per order than T99, or a worker exceeds 3 GB at k 31. Stops: guard fires (free mem < 10 GB, kills 1.11, keep
1.09/1.10); no new order line for 3 h -> py-spy the main, post, wait; 36 h wall.

Run 1 stopped at 04:29:05 UTC, about 58 min in. Windows Update (MoUsoCoreWorker.exe, "Operating System: Service pack
(Planned)", System event 1074) restarted win2, which came back on build 26300 at 04:30:06 UTC. The three logs end at
k 19 (3002 s, 3013 s, 3010 s, against T99's 3224 s), with no traceback and no JSON written. mem_guard.log ends at
04:28 UTC with 37.2 GB free.

Run 2, relaunched 2026-11-08 05:24:49 UTC (coordinator's go on #82): the issue's three commands at Normal priority,
from the same worktree `..\choptuik-t126` at c691ae3 (solver/inner_amp and util_report.py unchanged at 700da3a) and
venv-t126, through `run_i82_one.cmd <wf>`, which appends the exit code to `w<wf>_done.txt`. The memory guard watches
the new 1.11 main. Run 1's files are `w<wf>_run1.log`, `mem_guard_run1.log` and `_launch_utc_run1.txt`.
