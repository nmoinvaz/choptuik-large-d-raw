# I839-mac: #713's planted test at s0_D252 (D 252.6135) in the chain's own system

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/839.

Code: main 4617f876 (with #837's `truth_system`), worktree /Users/nathan/Source/choptuik-large-d-839 (`wip/i839`,
no changes). Build: main 3c35f0c's hpkernel (i599/site2). 3 threads, nice 10, one job at a time (queue.sh).

## Plan and criteria (written by 2026-11-15 12:00 UTC, before the queue)

planted at I603-win2's 252.6135 from #713's offset start (--rel 1e-12: the centre data and the nodes but the last
moved by 1e-12 relative), in the chain's own system (#837: truth residual 5.55e-92):

- **arm A**, #713's flags: `--threads 3 --switch 0 --reseed_o 3 --reseed_start pred --qd 0` (own test, it_max 12,
  tol 1e-40);
- **arm B**, the same plus `--full_drop 1e-2` (#836);
- seed 1 for both arms, then seed 2 (queue.sh). Each gets `--Delta_ref` = the truth's Delta from all eight parts,
  1.68453445011892229445312904531756908899422197089059690341775, so that planted's own (a) judges both bars.

**Bars, per arm and seed:** pinned max|F| below 1e-40 within 12 steps, and |Delta - Delta_truth| <= 1e-30. Otherwise
the step where it stops, with its trials. Where both seeds of an arm converge, they agree in Delta to 1e-30.
`verdict_839.py DIR` reads the four JSONs and states each verdict. Its selftest passes on planted records, and its
control `--mutate=bar` (the Delta bar at 1e-20) fails: verdict_selftest*.log, run before the queue (exit 0, exit 1).

Estimate: a few hours per arm (#713's s0_D252 took 2–6 h). The hourly posts follow the queue.

## Change of plan (2026-11-15 16:07 UTC, the coordinator's reply)

By step 4, every lam-1 trial of A_s1 had point max|F| 1e14–1e18, far above full_drop's 1e-2 of |F|. So B_s1 would take
every step as A_s1 did, bit for bit. The coordinator agreed: A_s1 runs out its 12 steps, then A_s2 runs. A B arm runs
only when its A run had a lam-1 trial within 1e-2 of |F|. queue.sh was stopped at 16:07 UTC while A_s1 kept running,
and queue2.sh took over at 16:08 UTC.

`b_needed.py A_LOG` makes that decision from the A run's log (exit 0: B needed). Its selftest passes on planted log
lines, and its control `--mutate=bar` (the drop at 1e-5) fails: b_needed_selftest*.log (exit 0, exit 1). On real logs
(b_needed_real.log), it says needed for I777-mac/stopped_s0_D252 (step 3's lam-1 trial at 4.3e-4 of |F|) and for
I713-mac/s0_D252 (step 11, 3.6e-17), and not needed for A_s1 through step 4 (closest 5.5e27 of |F|).

`table_839.py NAME` gives the closing summary's per-step table from NAME.json and NAME.log: Delta − truth before
each step (the summed lam·dDelta, since the offset leaves Delta at the truth), max|F|, |dz|, the smallest pivot,
pivot/|dz| and the accepted lam. It also fits the lam-1 trials' point max|F| against |dz| (exponent free, then 4) and
the smallest pivot against |dz|. Its check compares the summed Delta moves at the end with planted's own Delta − truth
(relative 1e-6). The selftest passes on a planted run. The controls `--mutate=lam` (step 0's lam taken as 1) and
`--mutate=power` (planted trials at exponent 3) fail: table_selftest*.log (exit 0, 1, 1).
