# I699-mac: where the weak left vectors U live on #553's and #543's re-noded layouts (reduced_cubic.py rows)

Machine: the Mac (Apple M5, the coordinator's machine), one process at a time, 2 threads, nice 10, OPENBLAS_NUM_THREADS=1.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/699. Code: main 6e57093b, unchanged (`hp/anm_run.py`,
`hp/reduced_cubic.py rows`). Kernel: the post-#523 scratchpad build `i599/site2` (as #694 and #713), venv-314.
Inputs, raw-data repository: `I553-win2/renode_last077_D242.3642.npz` and `I543-win2/renode_last080_D242.3642.npz`, crawlJ's D 242.3642 state re-noded to nodes 0.3, 0.4, 0.5, 0.6 and x_last = 0.77 or 0.80. Both lie above #553's crossing at 0.7428, where the weakest direction is the pure Δ direction (the chain's 0.70 layout has the harmonic-3 pair).

## Files

- `run_i699.sh`: everything, in order (`bash run_i699.sh RAW OUT` from the checkout's `hp/`). `exits.txt`: each start and exit.
- `l077.log`, `l077/`, `l080.log`, `l080/`: `anm_run.py --steps 1 --save_dz0 1` from each re-noded state, on #677's flags with
  `--base_polish 0` and `--a0 0.476837158203125`. Each was stopped (exit 143) once its dz0 was saved. The series steps took 5439 s and 4827 s,
  and both re-seeds were ok.
- `rows_planted*.log`, `.json`: the plant (exit 0) and its controls `--mutate=quadA` and `--mutate=parity` (exit 1 each, as they must).
- `rows_l077.*`, `rows_l080.*`: `reduced_cubic.py rows` at the two starts. `rowsum.txt`: their summary.

## Results

| start | U by block | share on the last two blocks (node4, horizon) | pairing of the last two blocks | σ of B (the four weakest) | \|P_V e_Δ\|² | checks W1–W3 |
|---|---|---|---|---|---|---|
| x_last 0.77 | node4 0.5, horizon 0.5, node3 3.5e-32, node2 5.2e-42 | 1 − 3.5e-32 | 4.4e-30 | 1.05e-30, 2.03e-30, 4.71e-30, 5.26e-30 | 0.99945 | pass |
| x_last 0.80 | node4 0.5, horizon 0.5, node3 3.2e-33, node2 2.5e-43 | 1 − 3.2e-33 | 6.4e-39 | 2.83e-39, 5.02e-39, 9.16e-39, 1.28e-37 | 0.99938 | pass |
| chain layout 0.70, #694's REF | node4 0.5, horizon 0.5, node3 3.3e-11 | 1 − 3.3e-11 | 2.7e-26 | 2.12e-27, 2.16e-27, 3.19e-26, ... | 0.99949 | pass |

**The bars.** The share on the last two blocks is above 0.99, and the pairing below 1e-15, at both starts. U does not move to
another block, and so stays on the last matching.

**The weakest direction.** At both starts the bottom of the weak spectrum is no longer a near-degenerate pair:
- σ₂/σ₁ is 1.94 at 0.77 and 1.78 at 0.80, against 1.016 on the chain's layout (REF) and 1.04 at #694's class A start.
- That fits #553's finding that the Δ mode is weakest above 0.7428.
- The per-vector Δ content was not computed here, so this is supporting evidence, not a measurement of the change.

**The 0.80 start.** Its first Newton move is of order 1: |dz0| 0.43, all but 9.9e-33 of it on span(V). That is as #501
found for that layout's polish. The first move then leaves |U^T F + B a| / |B a| = 0.54, so the along-e diagnostics there
are outside the linear regime. U's location depends only on J at the start.

**Deviation.** `--base_polish 0`, stated in the started comment. The stored re-noded state is the base.
