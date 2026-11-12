# I593-win: #462's win_d10 chain resumed exactly, from D 230.13125 with --base_polish 0, one step

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/593 (recommended by win in #587; the coordinator's message `choptuik-large-d/2026-11-12/120013Z-coordinator-1cfa.md`). Worktree `choptuik-i578` at main 80b50568 (the checkout of #578, #586 and #587, which the coordinator names so that the chain's code is the code that made it), venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 7200 s.

`i593_chain.cmd` is the resume of #462's win_d10 chain (`I462-win/d10_long3.cmd`: `held_fit_d10.json`, sha256 first 16 f970a8f97826e448, `--held_o 1 --reseed_o 3 --tol_od 1e-60`) from its stored `I462-win/chain_d10/anm_pin3_D230.1312.npz` (sha256 first 16 7e9f45feee4526bc) with `--steps 1 --base_polish 0`: the step into D 231.13125 starts from the loaded state as it stands. The output is in `chain_d10/`, the log `chain_d10.log`, the exit code `chain_d10.exit`.

**What it decides (the issue's).** The saved D 231.13125 state (`chain_d10/anm_pin3_D231.1312.npz`) must be within 1e-90 of `I462-win/chain_d10/anm_pin3_D231.1312.npz` in every entry (the exact eight-part comparison, `I570-win/cmp_states.py`; the file hashes are not compared, because the meta field `source` differs). The control: a 1e-88 change in one entry fails at 1e-90.

## Result

**The criterion holds: the D 231.13125 arrays equal #462's in every entry.** Ran about 12:01 UTC to 12:48:54 UTC on 2026-11-12 (about 48 min, under the 7200 s cap; the exit file's time), exit code 0 (`chain_d10.exit`), no Traceback. Main 80b50568, 3 threads. The log says "base polish skipped (--base_polish 0): the stored state is the base".

**The step into D 231.13125** (`chain_d10.log`), against #462's d10 log (its lines 200 to 210):

| quantity | #593 (loaded, `--base_polish 0`) | #462 (d10, in memory) |
|---|---|---|
| series line | \|z_1\| 3.93e-04, \|z_N\| 6.53e-29, ratios 2-5 294.8 265.7 252.9 199.0, a_max 2.942 | same |
| rung max\|R\| (before, then after each pass) | 2.94e-29 -> 1.70e-62 -> 6.60e-70 -> 5.95e-76 | same |
| Newton steps | 5 (no halving) | same |
| first step | 3.42e-33 -> 1.44e-27, moved 5.1e-30 | same |
| last residual | 3.31e-81 | 3.31e-81 |
| Delta (log) | 1.68826986983090555 -4.4521e-17 | same |
| step wall | 567 s | 801 s |

(The d10 chain converges to 3.3e-81 at this D, not the 1e-95 of the d6 chain; both logs say so, `--tol_od` being 1e-60.)

**The saved state**, exact comparison (`I570-win/cmp_states.py`: the sum of the eight parts of each of the 769 entries as an exact fraction; `compare_D231_vs_462.txt`), against `I462-win/chain_d10/anm_pin3_D231.1312.npz`:

| entries that differ | largest difference | Delta entry | sha256 of the eight arrays (first 16) | criterion |
|---|---|---|---|---|
| 0 of 769 | 0 | 0 | 32e402f808a08af4 (both) | within 1e-90 |

Exact Delta: 1.688269869830905500650919509837 in both. The file hashes differ (5feeeb0e558f0108 here, c81bf04f7c16fcd1 in #462) only through the `meta` field `source`, the state the run started from (`I462-win/chain_d10/anm_pin3_D230.1312.npz` here, `.../anm_pin3_D229.1312.npz` in #462's chain, which started one step earlier); every other field is equal.

**Controls** (`control_nudge.txt`, on the new state against #462's): a 1e-92 change in entry 100 of z7 passes at 1e-90 (1 difference, 1.0e-92), a 1e-88 change fails (1.0e-88, the issue's control); the new state against its D 230.13125 start differs in 769 of 769 entries (up to 3.9e-4), and against #587's d6 state at the same D (the other held fit) in 769 of 769 (up to 8.2e-6).

**The log** (`cmp_logs4.py`, 11 lines from the series line of D 230.13125 to the end of the step, wall times removed and `step N:` made the same): as printed 1 line differs, the printed tol of the "a 1.000 -> D 231.13125" line (1.4e-20 here, 2.1e-20 in #462: the tol grows with the distance from the run's start state, one step against two); with the tol made the same, 0 differ (`compare_log_vs_462.txt`). Control (`control_log_mutated.txt`): one digit of the last residual changed, one more line differs.

**What it decides.** The restart recipe of #587 holds on the second chain: win_d10, with the other held fit (degree 10), resumes from its saved D 230.13125 state with `--base_polish 0` and gives #462's D 231.13125 state to the last bit of the arrays. Not shown: more than one step on this chain, other D, a step with a refused first attempt, and an actual kill.
