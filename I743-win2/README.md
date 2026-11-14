# I743-win2: s132's first Newton step with a log line per failed ElimO projection

Machine win2 (desktop-pc, Core Ultra 7 265K, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/743.

`run_743.sh` (written by the coordinator) runs, from the worktree D:/choptuik-i743 at main 807d74d8 with venv-i600:
- the plant `reseed.py projlog` (exit 0) and its controls `--mutate=silent` and `--mutate=stage` (exit 1 each);
- `anm_run.py` on `I696-win2/D245/r131k/base_pin3_D245.1366.npz` at `--ks 132` with s132's flags, `--qd_it 1` and
  `--log_proj 1`, 10 threads, output `s132p/` and `s132p.log`;
- `compare_743.py` against `I696-win2/D245/s132.log` (exit 0), and its controls `--mutate=drop` and `--mutate=count`
  (exit 1 each).

Pass criteria, written before the run: the step-0 lines equal s132's with the timings cut, the number of
"projection failed" lines equals the counts line's `failed`, and every line names a failed stage. `exits_743.txt`
has one line per step.
