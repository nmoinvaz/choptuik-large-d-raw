# I505-win2: equilibrated sigma_1..4 along crawlI/crawlJ, D 237.13 to D 242.36 (near_null_eq.py --plant=7)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/505 (follows from #502, #488).
Code: worktree `D:\choptuik-i505` at `origin/wip/i502-subagent` 0cce81e (Python only), interpreter and `hpkernel` build of `C:\Users\nathan\Source\venv-t126`.
Four states at once, 2 threads each, below-normal priority (`run_i505.sh`), then the control `--mutate=rows_only` at D 237.13, which must exit nonzero. Exit codes in `exits.txt`.
States: `I461-win2/crawlI/anm_pin3_D237.1312.npz`, `crawlJ/anm_pin3_D239.5375.npz`, `crawlJ/anm_pin3_D241.1244.npz`, `crawlJ/anm_pin3_D242.3642.npz`.
Results follow in this README.

## Results (2026-11-11 20:50:49 to 20:58:54 UTC)

Four runs exited 0 (20:54:54 to 20:55:05 UTC, 4 min each with the others parallel), the control `--mutate=rows_only` at D 237.13 exited 1, as it must (`exits.txt`). The logs were renamed from `eq_<D>.*` to `eq_D<D>.*` after the runs.
`table_505.py` (selftest ok) makes `results_505.txt`: the equilibrated (Curtis-Reid + Ruiz) sigma_1..4, their rates, the verdict by #505's reading rule, and the directions from the logs.

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 237.1312 | 1.6003e-58 | 6.1130e-58 | 7.0593e-56 | 4.3170e-54 |
| 239.5375 | 7.1519e-60 | 3.4004e-59 | 2.1721e-57 | 1.4433e-55 |
| 241.1244 | 9.2776e-61 | 4.4974e-60 | 2.0620e-58 | 1.4180e-56 |
| 242.3642 | 1.8825e-61 | 9.3856e-61 | 2.6498e-59 | 2.4555e-57 |

sigma_1 falls by a factor 850.1 over 5.233 in D, at e^1.289 per unit of D (1.292, 1.287, 1.286 between the states); sigma_2..4 at e^1.24, e^1.51, e^1.43. The raw sigma_1 fell about 120 times over the same range (#488), e^0.9 per unit.
The reading rule's two bands (e^0.9 per unit, +-0.2, the system's own; under e^0.45, mostly scale) do not contain 1.289: the equilibrated sigma_1 falls faster than the raw one, so the scaling hid part of the decline rather than making it.
Checks: the planted column scaling gives max |sigma_i(J S) / sigma_i(J) - 1| of 5.33e-15, 4.44e-15, 1.55e-15, 1.11e-15 at the four states (bound 1e-3); ||J_eq v_1|| / sigma_1 = 1.000000 at each (bound 1e-2); the rows-only control fails the planted check (deviation 1.00) at D 237.13.
Cross-machine: sigma_1 at D 242.36 is 1.8825e-61, #502's value to the printed digits.
Directions of sigma_1: in the scaled unknowns a_h 0.53 and m_h 0.47 at all four states (top components m_h k3, a_h k2, a_h k4, m_h k1, m_h k5); in z p1 0.25, m_h 0.14, node4.p 0.10, top p1 k3, m_h k3, node4.p k3, the same list at all four; the Delta share of D_c v_1 rises 4.2e-07, 3.3e-05, 6.7e-04, 6.7e-04.
