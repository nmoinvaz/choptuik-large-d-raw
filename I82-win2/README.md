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

Node 1.10, 2026-11-08 07:00-07:06 UTC: a spawn worker (PID 15108) died with an access violation in libflint
(Application Error 1000, c0000005, offset 0x6830c4). The main then exited with BrokenPipeError / EOFError at its next
receive (S_many, amp_flint_par.py line 498), so `w1.10_run2.log` ends in a traceback after `k 23` at 4745 s, with
`w1.10_run2_done.txt` recording the exit. Nathan's decision, relayed by the coordinator (2026-11-08): keep everything
running and accept the fault risk. Node 1.10 was relaunched from k 1 at 07:05:49 UTC with the same command at Normal
priority, to `w1.10.log` (`_launch_utc_w1.10_run3.txt`). Nodes 1.09 and 1.11 are unchanged since 05:24:49 UTC.
Results from this period are accepted only after cross-checks against other machines: sigma_0..sigma_16 against
T153-macm3 and T155-win2's K33 values at the same nodes, and the agreement between nodes.

## Memory guards (history)

Until 2026-11-08 13:30 UTC the 1.11 main (PID 12852) had a guard, `util_report.py --guard 10` (kills its process tree when
free memory is under 10 GB), launched at 2026-11-08 05:25 UTC with the runs. On the coordinator's decision it was replaced at
13:29:51 UTC by `util_report.py --guard 6` (PIDs 22912 shim, 18504) and `commit_guard.py` (`commit_guard.py 10`, kills the tree
when the commit charge comes within 10 GB of the limit; PIDs 9428, 27888); the 10 GB guard (shim 10624, python 13968) was
stopped at about 13:30:20. On Nathan's instruction (relayed by the coordinator) every guard that kills a process was then
removed: both new guards were stopped at 13:31:21 UTC (`taskkill /T /F` on their own trees only; all 12 #82 processes were
untouched). No process is killed for its memory use from then on. `mem_guard.log` is the guard-era log (to 13:29 UTC);
`mem_log.txt` (written by `mem_log.py`, which kills nothing) continues the same report line every 5 min. `commit_guard.py`
stays here as the record of what ran for 90 s.
