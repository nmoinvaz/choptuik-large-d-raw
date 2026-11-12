# I578-win: the base polish of a loaded state against the file (the step into D 230.13125 from the stored D 229.13125 state, with --save_base 1)

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/578 (recommended by win in #570; the coordinator's message `choptuik-large-d/2026-11-12/081224Z-coordinator-b2e5.md`). Worktree `choptuik-i578` at main 80b50568 (hp/anm_run.py, octo_corrector.py, reseed.py and hp/src are identical to 14dc3863, which ran #514 and #570), venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 10800 s.

`i578_run_save.cmd` is #514's `i514_s6f6_a.cmd` (win_d6's stored `I462-win/chain_d6/anm_pin3_D229.1312.npz`, sha256 first 16 fd7f22f3a3d59689, with `held_fit_d6.json`, bc4403ace795fdb0, `--steps 1`) with `--save_base 1` added; the output is in `run_save/`, the log `run_save.log`, the exit code `run_save.exit`. The log is written fresh (`>`), not appended.

**What it decides (the issue's).** The polished base `run_save/base_pin3_D229.1312.npz`, compared with the loaded file by the exact eight-part comparison (`I570-win/cmp_states.py`: the sum of the eight parts of each of the 769 entries as an exact fraction). More than 1e-90 in some entry: the polish a load runs is a cause of the difference between a loaded and an in-memory base (#570). At most 1e-90: it is not, and the difference lies in data the file does not carry. The control: a change of 1e-88 in one entry must fail at 1e-90. The report also says whether the polish ran (`anm_run.py` polishes only when the start's double-double |F| exceeds `--tol`, #576), and whether the step itself gives #514's 2.68e-95, rung end 2.84e-62 and state (sha256 first 16 107d4c2d41aed77e), which `--save_base 1` should not change.

## Result

Ran 08:14 UTC to 09:12:20 UTC on 2026-11-12 (the exit file's time; under the 10800 s cap), exit code 0 (`run_save.exit`), no Traceback. Main 80b50568, 3 threads.

**1. The polish ran.** The start's double-double |F| is 7.7e+03, far above `--tol` (1.0e-20), so the skip of #576 did not apply. The octo-double Newton steps of the base (`run_save.log`): pinned max|F| 8.39e-38 -> 1.11e-42 -> 1.32e-89, 3 steps, converged, adopted, saved at 08:20 UTC as `run_save/base_pin3_D229.1312.npz` (sha256 first 16 762b55ba5356b4a5). The base-polish lines of #514's `run_s6f6_a.log` (the same polish) are identical to these (part of the log comparison in 3).

**2. The polished base against the loaded file** (`I570-win/cmp_states.py`: the sum of the eight parts of each of the 769 entries as an exact fraction; `compare_base_vs_file.txt`):

| quantity | value |
|---|---|
| entries that differ | 769 of 769 |
| largest difference | 8.53e-38 (entry 0) |
| smallest nonzero difference | 8.65e-45 |
| entries above 1e-38, 1e-40 | 336, 571 |
| Delta entry (768), base minus file | 1.43684e-39 |
| criterion | at most 1e-90 |

**Verdict by the issue: more than 1e-90 in some entry, so the polish is a cause.** The loaded run starts from a base 8.5e-38 away from the file, whose bits are the in-memory base (#570). The size is that of the polish's first move (|dz| 8.5e-38) and of the first residual (8.39e-38). The doc of `anm_run.py` says a reloaded state starts off in the held rows because their values are taken again from its first two parts; that fits but is not tested here.

**Control** (`control_nudge.txt`; the base against the file differs by 8.5e-38, so the resolution of 1e-90 is shown on the polished base itself):

| comparison | result |
|---|---|
| base against itself | 0 differences, passes |
| plus 1e-92 in entry 100 of z7 | 1 difference, 1.0e-92, passes at 1e-90 |
| plus 1e-88 in the same entry | 1 difference, 1.0e-88, **fails** at 1e-90 (the control the issue asks for) |
| base against #570's D 230.13125 state | 769 of 769 differ, up to 3.9e-4 |

**3. The step itself** (`--save_base 1` should not change it, and it does not). `compare_log_vs_514a.txt` and `compare_log_vs_514b.txt`: the log against #514's `run_s6f6_a.log` and `run_s6f6_b.log` from the "held values" line to "done", wall times removed and the one line `--save_base 1` adds ("base polish saved as") left out: 20 lines, 0 differ. Control (`control_log_mutated.txt`): one digit of the last residual changed, 1 line differs.

| | #578 (loaded, saved base) | #514 run_s6f6_a / run_s6f6_b | #570 (in memory) |
|---|---|---|---|
| rung max\|R\| | 1.88e-29 -> 1.60e-49 -> 6.87e-56 -> 2.84e-62 | same | 1.34e-29 -> 1.18e-62 -> 1.39e-70 -> 2.49e-76 |
| Newton steps, start, first move | 6, 7.08e-34, 4.4e-31 | same | 6, 7.08e-34, 4.4e-31 |
| last residual | 2.68e-95 | 2.68e-95 | 1.95e-95 |
| saved D 230.13125 state, sha256 first 16 | 107d4c2d41aed77e | 107d4c2d41aed77e | 6382a51e3286ee83 |
| wall of the step | 795 s | 1209 s, 811 s | 808 s |

The saved D 230.13125 state is identical to #514's two (0 of 769 entries differ, `compare_D230_vs_514a.txt`, `compare_D230_vs_514b.txt`). Against the in-memory state of #570 (and #462) it differs in all 769 entries by up to 1.61e-87 (entry 11), the Delta entry by 6.95e-88 (`compare_D230_vs_inmemory.txt`). So bases that differ by 8.5e-38 lead, after the step, to states that differ by 1.6e-87.

**What it decides.** The polish a load runs is a cause of the difference between a loaded and an in-memory base. It is not shown to be the only one: this run polishes in both arms of what it compares. A run from the file with `--base_polish 0` (the stored state is the base as it stands) would show whether the in-memory result (1.95e-95, rung end 2.49e-76, state 6382a51e3286ee83) then returns.
