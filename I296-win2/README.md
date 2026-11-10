# I296-win2: the rest of the I19-win2 crawl, D 214.6 to 215.03125, reproduced on win2's new firmware

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/296 (recommended by win2 in #287's summary).

The crawl's command (`../I19-win2/README.md`) with `--steps 40` (its own stop rule), from `../T138-win2/chain_o/anm_pin3_D214.5000.npz`, run
from `hp/` of the worktree `D:\choptuik-t126` that ran #19 (hp code equal to e743608 and c691ae3), `venv-t126` (Python 3.12.8), 18 threads (the
crawl's count), Normal priority, no affinity (`run_i296.sh`). It waits for #295 step 1 to end. Output `crawl/`, log `crawl.log`, exits `exits.txt`.

Stop rules, before the run: the crawl's own acceptance and halving rule, a 4 h cap, and the crawl's hang rule (no log line for 20 min while one
core is busy: one py-spy dump, kill the tree, post).

A fact about the reference. `../I19-win2/crawl.log` (169 lines) does not end with a stop line. The crawl was stopped by the coordinator's call at
03:25 UTC on 2026-11-08 (process tree killed, #19's comments of 03:19Z and 03:27Z) in its third attempt past D 215.03125, after about 40 min with
nothing accepted. The issue's third acceptance item ("stops at D 215.03125 after three halvings, as the crawl did") cannot be checked against the
crawl as written. What is compared: every line of the crawl's log against the new log. What the new run does after the crawl's last line (accepts a
step, or reaches its own stop line, or runs to the cap) is reported as new information.

`compare_296.py` (`--selftest`) compares the logs line by line with elapsed times removed, the seven accepted steps (D 214.6, 214.7, 214.8, 214.9,
215.0, 215.025, 215.03125) with `hp/data/delta_all.csv` (Delta as a double, the correction to its 5 printed digits), the first seven records of
`anm_run.jsonl`, and every saved state and prediction file bit for bit.
