# I587-win: #462's win_d6 chain resumed exactly, from D 230.13125 with --base_polish 0, two steps

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/587 (recommended by win in #586; the coordinator's message `choptuik-large-d/2026-11-12/101239Z-coordinator-7dea.md`). Worktree `choptuik-i578` at main 80b50568 (#578's and #586's checkout; main has since changed `hp/octo_corrector.py`, and this run stays on #578's code), venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 12600 s.

`i587_chain.cmd` is the resume of #462's win_d6 chain (`I462-win/d6_long3.cmd`: `held_fit_d6.json`, `--held_o 1 --reseed_o 3 --tol_od 1e-60`) from its stored `I462-win/chain_d6/anm_pin3_D230.1312.npz` (sha256 first 16 6382a51e3286ee83) with `--steps 2 --base_polish 0`: the step into D 231.13125 starts from the loaded state as it stands, the step into D 232.13125 from the previous step's state in memory, as in #462. The output is in `chain_d6/`, the log `chain_d6.log`, the exit code `chain_d6.exit`.

**What it decides (the issue's).** The saved D 231.13125 and D 232.13125 states (`chain_d6/anm_pin3_D231.1312.npz`, `anm_pin3_D232.1312.npz`) must be within 1e-90 of `I462-win/chain_d6/anm_pin3_D231.1312.npz` and `anm_pin3_D232.1312.npz` in every entry (the exact eight-part comparison, `I570-win/cmp_states.py`). The control: a 1e-88 change in one entry fails at 1e-90. If it holds, a chain killed by an update restart resumes exactly with `--base_polish 0`.

## Result

**The criterion holds: the D 231.13125 and D 232.13125 arrays equal #462's in every entry.** Ran 10:13:45 UTC to 11:56:09 UTC on 2026-11-12 (6144 s, under the 12600 s cap; the exit file's time), exit code 0 (`chain_d6.exit`), no Traceback. Main 80b50568, 3 threads. The log says "base polish skipped (--base_polish 0): the stored state is the base".

| step | rung max\|R\| (before, then after each pass) | Newton steps | last residual | Delta (log) | step wall (here, #462) |
|---|---|---|---|---|---|
| into D 231.13125 (from the loaded file) | 3.23e-29 -> 1.29e-62 -> 1.93e-69 -> 1.37e-75 | 5, one halved | 3.31e-95 | 1.68826986985636962 -2.3616e-17 | 572 s, 828 s |
| into D 232.13125 (from the previous step in memory) | 3.86e-29 -> 1.68e-62 -> 4.62e-69 -> 5.91e-75 | 6, one halved | 4.35e-95 | 1.68808082465851705 -2.2899e-17 | 802 s, 1161 s |

The values in the first five columns are the same in #462's log.

**The saved states**, exact comparison (`I570-win/cmp_states.py`: the sum of the eight parts of each of the 769 entries as an exact fraction), against `I462-win/chain_d6/anm_pin3_D231.1312.npz` and `anm_pin3_D232.1312.npz`:

| state | entries that differ | largest difference | Delta entry | sha256 of the eight arrays (first 16) | criterion |
|---|---|---|---|---|---|
| D 231.13125 (`compare_D231_vs_462.txt`) | 0 of 769 | 0 | 0 | 5200860885410ec8 (both) | within 1e-90 |
| D 232.13125 (`compare_D232_vs_462.txt`) | 0 of 769 | 0 | 0 | 0fc7bd0fbec61168 (both) | within 1e-90 |

Exact Delta at D 232.13125: 1.688080824658517031105689087020 in both. The file hashes differ (D 231: 06fdf6ffd6b75536 here, 64f8de358ce5851a in #462; D 232: b809892f6ef5b2f1 and 9e7cfcca2784c2e2) only through the `meta` field `source`, the state the run started from (`I462-win/chain_d6/anm_pin3_D230.1312.npz` here, `.../anm_pin3_D228.1312.npz` in #462); every other field is equal, as in #586.

**Controls** (`control_nudge.txt`, on the new D 232.13125 state against #462's): a 1e-92 change in entry 100 of z7 passes at 1e-90 (1 difference, 1.0e-92), a 1e-88 change fails (1.0e-88, the issue's control); the new D 232.13125 state against the new D 231.13125 state differs in 769 of 769 entries, by up to 3.9e-4. The same 1e-92 / 1e-88 pair on the D 231.13125 state, posted on the issue at 11:03 UTC, gave the same verdicts.

**The log** (`cmp_logs4.py`, the two steps from the series line of D 230.13125 to the end of the step into D 232.13125, 23 lines, wall times removed and `step N:` made the same): as printed 2 lines differ, the printed tol of the two "a 1.000 -> D" lines (1.4e-20 and 2.1e-20 here, 3.0e-20 and 4.4e-20 in #462: the tol grows with the distance from the run's start state, one and two steps here, three and four there); with the tol made the same, 0 differ (`compare_log_vs_462.txt`). Control (`control_log_mutated.txt`): one digit of the last residual of the second step changed, one more line differs. (#462's own log ends there with the cap of its run killing it in the next series, which the slice leaves out.)

**What it decides.** A chain killed at a saved state resumes exactly with `--base_polish 0`: the step from the loaded D 230.13125 state and the next one from memory reproduce #462's uninterrupted chain to the last bit of the arrays, over two steps. Without the flag the load's polish moves the base by 8.5e-38 (#578) and the result by 1.6e-87 over one step (#586). The flag also saves the polish's two Newton steps (about 4 minutes). What it does not show: that other chains (win_d10), other D and steps with a refused first attempt resume the same way, and a real restart, which starts from the last state a killed run saved (here the saved D 230.13125 state of #462, which was itself produced in memory, as such a state would be).
