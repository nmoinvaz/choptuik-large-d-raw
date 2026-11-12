# I570-win: the newer code from a state in memory, a two-step chain from D 228.13125 (win_d6)

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/570 (recommended by win in #532; the coordinator's message `choptuik-large-d/2026-11-12/061423Z-coordinator-8599.md`). Worktree `choptuik-i513` at main 14dc3863 (hp/anm_run.py, octo_corrector.py, reseed.py and hp/src are unchanged to e295b495), venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 12600 s.

`i570_chain.cmd` is the resume of #462's win_d6 chain (`I462-win/d6_long3.cmd`: win_d6's stored `I462-win/chain_d6/anm_pin3_D228.1312.npz`, sha256 first 16 3b3082cba12fe91b, `held_fit_d6.json`, `--held_o 1 --reseed_o 3 --tol_od 1e-60`) with `--steps 2` and the output in `chain_d6/`: the step into D 229.13125 starts from the loaded state, the step into D 230.13125 from the previous step's state in memory, as in #462. The log is `chain_d6.log`, the exit code `chain_d6.exit`.

**What it decides (the issue's).** The step into D 230.13125 must leave a last residual of 1.95e-95 with the horizon rung ending at 2.49e-76, and its saved state `chain_d6/anm_pin3_D230.1312.npz` must be within 1e-90 of `I462-win/chain_d6/anm_pin3_D230.1312.npz`. Any other pair is reported. The grid of the code x base cells: cc6d51ba from the state in memory (#462's original: 1.95e-95 and 2.49e-76), cc6d51ba from the loaded state (#532) and 14dc3863 from the loaded state (#514): both 2.68e-95 and 2.84e-62, byte-identical states.

## Result

Ran 06:18:46 to 08:08:23 UTC on 2026-11-12 (6577 s, under the 12600 s cap), exit code 0 (`chain_d6.exit`), no Traceback. Both criteria of the issue are met.

| step | rung max\|R\| (before, then after each pass) | Newton steps | last residual | Delta (exact, the sum of the eight parts) |
|---|---|---|---|---|
| base polish at D 228.13125 | | 3 | 8.19e-90 | 1.68884683988080542 -3.5313e-17 (log) |
| into D 229.13125 | 1.56e-29 -> 6.22e-63 -> 2.18e-69 -> 1.85e-75 | 6, one halved | 1.77e-95 | 1.688652856236830128285004412884 |
| into D 230.13125 | 1.34e-29 -> 1.18e-62 -> 1.39e-70 -> **2.49e-76** | 6, one halved | **1.95e-95** | 1.688460540033102312943252156251 |

The step into D 230.13125 starts at 7.08e-34 and moves 4.4e-31 in its first Newton step, as in #462.

**Criterion 1, the saved state** `chain_d6/anm_pin3_D230.1312.npz` against `I462-win/chain_d6/anm_pin3_D230.1312.npz` (`cmp_states.py`: the sum of the eight parts of each of the 769 entries as an exact fraction, then the largest difference): 0 of 769 entries differ, the largest difference is 0, the Delta entry (768) differs by 0, against the criterion 1e-90 (`compare_D230_state.txt`). The two files have the same sha256 (first 16 digits 6382a51e3286ee83). The state of the first step, `anm_pin3_D229.1312.npz`, is also identical to #462's (0 of 769, sha256 fd7f22f3a3d59689, `compare_D229_state.txt`).

**Criterion 2, the last residual and the rung**: 1.95e-95 ("on 5: |F| 1.95e-95 converged", max|F| 1.9e-95) and the rung ending 2.49e-76, as #462.

Beyond the criteria, `cmp_logs.py` compares this log with #462's line by line with the trailing wall times removed (from the "held values" line of the base polish to the second step's last line, 32 lines): 0 differ (`compare_log.txt`). Only the wall times differ: the two steps took 797 s and 808 s here and 1120 s and 1142 s in #462, and a Newton step of the base polish 113.5 s against 154.7 s.

**Controls** (each can fail):

| control | what it shows |
|---|---|
| the new D 230.13125 state against the new D 229.13125 state (`control_D230_vs_D229.txt`) | 769 of 769 entries differ, the largest by 3.9e-4 |
| one entry (z7 of entry 100) changed by 1e-92 (`control_state_nudge.txt`) | the comparison finds exactly one difference, 1.0e-92, and still passes at 1e-90 |
| the same entry changed by 1e-88 | the comparison finds 1.0e-88 and fails at 1e-90 |
| the last-residual digits of this log changed by one unit (1.95e-95 to 1.96e-95, `control_log_mutated.txt`) | the log comparison reports one differing line |

**What it decides.** The cells of code x base, for the step into D 230.13125:

| code | base | run | last residual | rung end | saved state (sha256, first 16) |
|---|---|---|---|---|---|
| cc6d51ba | from the previous step, in memory | #462 | 1.95e-95 | 2.49e-76 | 6382a51e3286ee83 |
| 14dc3863 | from the previous step, in memory | #570 | 1.95e-95 | 2.49e-76 | 6382a51e3286ee83 |
| cc6d51ba | loaded from the stored D 229.13125 state | #532 | 2.68e-95 | 2.84e-62 | 107d4c2d41aed77e |
| 14dc3863 | loaded from the stored D 229.13125 state | #514 | 2.68e-95 | 2.84e-62 | 107d4c2d41aed77e |

The code between cc6d51ba and 14dc3863 does not change the chain from a state in memory: it gives #462's state to the last bit, two steps in a row. So the difference of #514 and #532 comes from the base, loaded from the file or carried in memory, not from the code. The rung already differs before its first pass (1.34e-29 in memory, 1.88e-29 loaded), and the stored D 229.13125 state is the same bit for bit as the in-memory one (above), so what differs is something the file does not give the loaded run, or the base polish a load runs. This run does not decide which.
