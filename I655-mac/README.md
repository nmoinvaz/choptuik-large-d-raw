# I655-mac: Kantorovich estimates of the octo-double corrector's attempts (#603 and crawlJ logs), planted check and analysis

Machine: mac (the coordinator's Apple M5 Mac), one process at nice 10, OPENBLAS_NUM_THREADS=1, Python 3.14 with numpy 2.5.4
and mpmath 1.3.0. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/655 (a subagent of the coordinator). Analysis of
logs only, no solver runs. The note is notes/CORRECTOR_BASIN.md of the code repository, the script hp/kantorovich_log.py.

Inputs (not copied here), from this repository: `I603-win2/chain.log` and `I603-win2/chain/anm_run.jsonl` at be58c93
(training, lines 1-514) and at c5ed39b (step 38, held out), `I461-win2/crawlJ.log` and `I461-win2/crawlJ/anm_run.jsonl`
at be58c93 (held out).

- `run_655.sh`: every run below, from the code checkout's hp/ (`bash run_655.sh IN OUT`).
- `exits.txt`: each run's exit code (the selftest's two controls must exit 1).
- `selftest.log`: the planted check (P1)-(P3), PASS, with the planted log of (P1) as anm_run.py would print it.
- `selftest_mutate_F.log`, `selftest_mutate_nofloor.log`: the controls, FAIL as required.
- `parse.log`: the parser against anm_run.py's records (a, accepted, steps): ok for all three inputs.
- `corrector_attempts.csv`: one row per attempt, equal to the code repository's hp/data/corrector_attempts.csv.
- `analyse.log`: the separation test (h* = 0.31 fixed before crawlJ was read, code commit f57dfe11), the fits, the
  bootstrap and the a-rule. `analyse_mutate_F.log`: the same with theta from |F|. `analyse_crawlJ_fits.log`: crawlJ's own
  fits, after its held-out use.
