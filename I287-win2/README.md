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
