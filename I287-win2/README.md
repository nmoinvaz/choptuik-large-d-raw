# I287-win2: the first step of the I19-win2 crawl past D 214.5, reproduced on win2's new firmware

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/287 (recommended by win2 in #268's summary).

The crawl's command (`../I19-win2/README.md`) with `--steps 1`, from `../T138-win2/chain_o/anm_pin3_D214.5000.npz`, run from `hp/` of the
worktree `D:\choptuik-t126` that ran #19 (hp code equal to e743608 and c691ae3), `venv-t126` (Python 3.12.8), 18 threads (the crawl's
count; #268 found the thread count does not decide the load checks), Normal priority, no affinity (`run_i287.sh`). Output `crawl1/`,
log `crawl1.log`, exits `exits.txt`.

Stop rules, before the run: the step ends accepted or not accepted by the crawl's own rule (the octo corrector returns converged); a
cap of 3 h wall (twice the issue's 90 min upper estimate) and the crawl's hang rule (no log line for 20 min while one core is busy:
one py-spy dump, kill the tree, post).

`compare_287.py` (written during the run) compares the accepted step's Delta and correction with `hp/data/delta_all.csv` row 214.6
(Delta 1.6916473410327395, correction -9.363597087142327e-17) and the new log against `../I19-win2/crawl.log` line by line with the
elapsed-time suffix removed, naming the first differing line.

## Result (2026-11-10 07:05 UTC)

Run: started 2026-11-10 06:33:58 UTC, exit 0 at 07:03:47 UTC, wall 1789 s (29 min 49 s) at 18 threads (`exits.txt`, `crawl1.log`). The base polish
of the start state ends as in the crawl (12 octo-double steps, max|F| 2.4e-29, not converged, accepted by the stall rule), the series and
re-seed follow, and the step is accepted at D 214.6 (octo-double Newton, 5 steps, max|F| 5.7e-48, converged).

`compare_287.py` (`--selftest` ok; it was changed once after the first real run, to drop the log's closing `done` line, which the crawl's
first step cannot have, and to compare the saved prediction as well; the selftest checks both), output in `compare_287_result.txt`: exit 0, ACCEPTED.

- Part A, log against `../I19-win2/crawl.log` up to its "step 1:" line, elapsed times removed: **identical, 28 lines**.
- Part B, Delta 1.69164734103273950 and correction -9.3636e-17 equal `delta_all.csv` row 214.6 (1.6916473410327395, -9.363597087142327e-17 to
  its 5 printed digits), and the step-0 record of `anm_run.jsonl` (the attempt: a 0.1, D 214.6, F_pred, F_final, tol, steps, accepted, Delta, dDelta,
  moved, the re-seed rungs) is equal to the crawl's with the timing keys dropped.
- Part C, `crawl1/anm_pin3_D214.6000.npz` and `crawl1/pred_pin3_D214.6000.npz` against the crawl's: every array bit for bit equal.

Only the first of the crawl's seven steps (to D 214.6) is run here, so rows 214.7 to 215.03125 of `delta_all.csv` are not tested by this run.

Machine over the run (`../I204-win2/sensor_log.txt`, 6 five-minute readings 06:34 to 06:59 UTC): utilization 46 to 126% (mean 103%, Windows
processor-utility counter), package power 80.8 to 191.9 W (mean 159.3), free memory 75.9 to 76.3 GB. No temperature: Core Temp was not running
(the readings say "temp n/a" from about 06:20 UTC on). No crash, WHEA, Kernel-Power 41, BugCheck or Application Error event since the watchers' restart at
23:44 UTC on 2026-11-08 (event logs queried at 2026-11-10 07:05 UTC).
