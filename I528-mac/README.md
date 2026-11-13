# I528-mac: the strong-row term S of the reduced cubic and the reduced map at the D 242.5146 starts (hp/reduced_cubic.py)

Machine: the M5 Mac (the coordinator's), 2 threads, nice 10, OPENBLAS_NUM_THREADS=1. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/528.

Code: `hp/reduced_cubic.py` of choptuik-large-d (branch `wip/i528-subagent`; the results from 2946e078, earlier
versions in the table), run by `run_i528.sh` from `hp/`. Kernel: main 3c35f0c's hpkernel build (multishoot 1.2.2, the exact freeze projector), the Mac's scratchpad build
`i599/site2`, with venv-314's Python 3.14 and its multidouble package. Inputs, from this repository at 5e8dbd6:
base `I461-win2/probeG03125a/anm_pin3_D242.5146.npz`, the accepted attempt
`I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz` (ACC) and the refused one
`I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz` (REF). Protocol and results: `notes/REDUCED_CUBIC.md`.

| file | what | exit |
|---|---|---|
| `planted.log`, `.json` | the plant (seed 5), code 2946e078 | 0, every check passes |
| `planted_mut_w0.log`, `_Ssign`, `_Sh`, `_hF` | the four mutations, code 2946e078 | 1 each, as they must |
| `ref.log`, `.json` | REF, the refused attempt, code 2946e078 (the results) | 1: the S control fails (2.72e-2 against 1e-2); every other check passes |
| `acc.log`, `.json` | ACC, the accepted attempt, code 2946e078 (the results) | pending |
| `ref_hF1e-24_stopped.log`, `.json` | REF run 1 (86b33a52), stopped by hand at the w_jl stage: w_jl at h 1e-24 was all truncation (0.99) | 143 |
| `ref_hF1e-32_stopped.log`, `.json` | REF run 2 (bb5866c0), stopped by hand: the w_jl check fired, 1e-32 against 1e-33 at 1.41e-2 | 143 |
| `ref_run3_d0225a8b.log`, `.json` | REF run 3 (d0225a8b), complete; the S control failed (2.72e-2) | 1 |
| `ref_run4_30a7bd35.log`, `.json` | REF run 4 (30a7bd35), complete, with the S control's scan; its stall rule stopped the chord between two cancelling corrections | 1 |
| `acc_run4_30a7bd35_stopped.log` | ACC run 4, stopped by hand at its start for the stall rule's fix | 143 |
| `run_i528.sh`, `exits.txt` | the runner, and every start and exit | |

The planted files were rewritten by each code version's rerun; those above are 2946e078's, and `exits.txt` lists the
earlier ones (every plant run exited 0 and every mutation 1).
