# I586-win: is the load's base polish the whole cause? #578's step into D 230.13125 with --base_polish 0

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/586 (recommended by win in #578; the coordinator's message `choptuik-large-d/2026-11-12/091550Z-coordinator-5a03.md`). Worktree `choptuik-i578` at main 80b50568, the checkout of #578 (the coordinator said 80b5056 or later; main has since changed `hp/octo_corrector.py`, and this run stays on #578's code so that the flag is the only difference from #578), venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 10800 s.

`i586_run_nopolish.cmd` is #578's `i578_run_save.cmd` (win_d6's stored `I462-win/chain_d6/anm_pin3_D229.1312.npz`, sha256 first 16 fd7f22f3a3d59689, `held_fit_d6.json`, `--steps 1`, `--save_base 1`) with `--base_polish 0` added, so the loaded base enters the step unpolished (`--save_base 1` is kept as in #578; it saves nothing when the polish is skipped). The output is in `run_nopolish/`, the log `run_nopolish.log`, the exit code `run_nopolish.exit`.

**What it decides (the issue's).** If the step returns the in-memory result of #462 and #570, the polish is the whole cause of the loaded-versus-in-memory difference: last residual 1.95e-95, the horizon rung ending at 2.49e-76, and the saved state `run_nopolish/anm_pin3_D230.1312.npz` with sha256 (first 16) 6382a51e3286ee83. Any other result is reported with the numbers, as a further cause. For comparison: loaded and polished (#514, #578) 2.68e-95, 2.84e-62, 107d4c2d41aed77e.

## Result

Ran 09:16:45 UTC to 10:08:57 UTC on 2026-11-12 (the exit file's time; under the 10800 s cap), exit code 0 (`run_nopolish.exit`), no Traceback. Main 80b50568, 3 threads. The log says "base polish skipped (--base_polish 0): the stored state is the base", so the step starts from the file as it stands.

**The step into D 230.13125** (`run_nopolish.log`), against the in-memory run of #462 and #570 and the loaded, polished runs of #514 and #578:

| | #586 (loaded, no polish) | #570 and #462 (in memory) | #514 and #578 (loaded, polished) |
|---|---|---|---|
| rung max\|R\| (before, then after each pass) | 1.34e-29 -> 1.18e-62 -> 1.39e-70 -> **2.49e-76** | same | 1.88e-29 -> 1.60e-49 -> 6.87e-56 -> 2.84e-62 |
| Newton steps, start, first move | 6 (one halved), 7.08e-34, 4.4e-31 | same | same |
| last residual | **1.95e-95** | 1.95e-95 | 2.68e-95 |
| sha256 of the eight arrays (first 16) | 69958b4298bc659a | 69958b4298bc659a | dbd858ddd77f2926 |
| sha256 of the file (first 16) | 8a66869b712cafa1 | 6382a51e3286ee83 | 107d4c2d41aed77e |
| wall of the step | 793 s | 808 s | 795 s (#578), 811 s and 1209 s (#514) |

**The saved state** `run_nopolish/anm_pin3_D230.1312.npz`, exact comparison (`I570-win/cmp_states.py`, the sum of the eight parts of each of the 769 entries as an exact fraction):

| compared with | entries that differ | largest difference | Delta entry |
|---|---|---|---|
| #570's in-memory state (`compare_D230_vs_inmemory.txt`) | 0 of 769 | 0 | 0 |
| #462's original (`compare_D230_vs_462.txt`) | 0 of 769 | 0 | 0 |
| #514's loaded, polished state (`compare_D230_vs_loaded.txt`) | 769 of 769 | 1.61e-87 (entry 11) | 6.95e-88 |

**The file hash is not the issue's 6382a51e3286ee83, and the cause is the metadata, not the numbers.** The npz differs from #570's only in the `meta` field `source`, the state the run started from: `I462-win/chain_d6/anm_pin3_D229.1312.npz` here, `.../anm_pin3_D228.1312.npz` in the two-step chain of #570 and #462 (the other fields are equal). The eight arrays are equal bit for bit (the hash of their bytes, 69958b4298bc659a, is the same in the three files). So the issue's criterion, read as the state, is met exactly; read as the literal sha256 of the file, it is not, and it could not be for a run that starts from another file.

**The log** (`cmp_logs3.py`, from the series line of the step to its last line, 12 lines, wall times removed): against #570's second step 11 lines are equal and 1 differs, the printed tol of the step line (1.4e-20 here, 2.1e-20 there: the tolerance grows with the distance from the run's start state, one step against two); the same against #462's (`compare_log_vs_570.txt`, `compare_log_vs_462.txt`). Against #578's polished run 4 lines differ: the rung line, the last two Newton lines and the Newton summary (`compare_log_vs_578.txt`). Control (`control_log_mutated.txt`): one digit of the last residual changed, one more line differs.

**Controls** (`control_nudge.txt`, on the new state): a 1e-92 change in entry 100 of z7 passes at 1e-90 (1 difference, 1.0e-92), a 1e-88 change fails (1.0e-88), and the state against the D 229.13125 state of #570 differs in 769 of 769 entries by up to 3.9e-4.

**What it decides.** A loaded state whose base is not polished gives the in-memory step to the last bit of the arrays: the polish a load runs is the whole cause of the difference of #514, #532 and #578 from #462 and #570, and no data the file lacks plays a part for this step. The polish moves the base by 8.5e-38 (#578) and leaves a horizon rung of 2.84e-62 where the unpolished start leaves 2.49e-76, and a final state 1.6e-87 away. The in-memory base and the file are the same bits (#570), so the polish is all that differs between the two arms.
