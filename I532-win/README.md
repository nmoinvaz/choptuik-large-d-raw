# I532-win: #514's control command on #462's checkout, to separate the code from the base

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/532 (recommended by win in #514; the coordinator's message `choptuik-large-d/2026-11-12/044316Z-coordinator-4a90.md`). Checkout `choptuik-t151c` at cc6d51ba, #462's code, venv-t151's hpkernel, 3 threads at BelowNormal, under `I462-win/run_capped.py` with a cap of 7200 s (the 2 h stop condition).

`i532_run_c.cmd` is `I514-win/i514_s6f6_a.cmd` (win_d6's stored `I462-win/chain_d6/anm_pin3_D229.1312.npz`, `held_fit_d6.json`, `--steps 1`, the flags of #462's resume) with the checkout and the output folder replaced; `data/held_fit_d6.json` has the same sha256 in both checkouts (bc4403ace795fdb0). Output `run_c/`, log `run_c.log`, exit code `run_c.exit`.

**What it decides (the issue's).** The step into D 230.13125 from the stored state, with the same options, on cc6d51ba. If the code is the cause of the last-residual difference, its last residual is 1.95e-95 and its horizon rung ends at 2.49e-76 (#462's original, run from a state in memory). If the base or the load is, it gives 2.68e-95 and 2.84e-62 (#514's two controls, on 14dc3863). Any other pair is a discrepancy. For the comparison: #462's original step and #514's controls agree in every other number to the digits printed and in the saved state to 1.6e-87.

## Results (2026-11-12)

`run_c`: started 04:45 UTC, ended 06:05:00 UTC, exit 0, no Traceback. The step into D 230.13125 was accepted at a = 1 (6 Newton steps, the second solve halved, Delta 1.688460540033, moved 4.4e-31; series 2942 s, re-seed 203 s, Newton 1161 s).

| quantity | #462's original (cc6d51ba, state in memory) | run_c (cc6d51ba, loaded from the stored state) | #514's controls (14dc3863, loaded) |
|---|---|---|---|
| last residual of the step | 1.95e-95 | **2.68e-95** | 2.68e-95 |
| horizon rung (before, after each of three passes) | 1.34e-29 -> 1.18e-62 -> 1.39e-70 -> **2.49e-76** | 1.88e-29 -> 1.60e-49 -> 6.87e-56 -> **2.84e-62** | 1.88e-29 -> 1.60e-49 -> 6.87e-56 -> 2.84e-62 |
| start \|F\|, first move | 7.08e-34, 4.4e-31 | 7.08e-34, 4.4e-31 | 7.08e-34, 4.4e-31 |
| solves 0 to 3 \|F\| | 9.49e-29, 4.74e-29, 1.23e-48, 1.23e-48 | the same | the same |
| series line at the base | 1.53e-29, 252.9, 3.135 | the same | the same |

**Verdict by the issue.** The pair is 2.68e-95 and 2.84e-62: the base or the load is the cause, not the five commits since cc6d51ba. The saved state `run_c/anm_pin3_D230.1312.npz` is byte-identical to `I514-win/run_s6f6_a` and `run_s6f6_b` (sha256 107d4c2d41aed77e all three), so cc6d51ba and 14dc3863 give the same state to the last bit from the stored state. Against #462's original it differs by 6.95e-88 in Delta and at most 1.61e-87 in any entry, as #514's controls do. The meta records of the two are equal.

**What this does not separate.** The original ran from the previous step's state in memory and these runs load the stored state and polish it; "the base" (the polished state against the state in memory) and "the load" (reading the file and re-forming the held offsets and the plan) are not separated by it. The one cell not run is the newer code from a state in memory (a two-step chain from D 228.13125 on 14dc3863); that the code is bit-identical in the loaded case makes it unlikely to differ there, but it is not tested.
