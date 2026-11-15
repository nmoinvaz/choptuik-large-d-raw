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
