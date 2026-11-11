# I510-win2: equilibrated sigma_1..4 along the clean chain, D 216.13 to D 242.5264 (near_null_eq.py --plant=7)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/510 (follows from #505, #502).
Code: worktree `D:\choptuik-i505` at `origin/wip/i502-subagent` 0cce81e (Python only; interpreter and `hpkernel` build of `C:\Users\nathan\Source\venv-t126`), as in #505.
Eight states, four at a time (2 threads each, below-normal priority, `run_i510.sh`), then the control `--mutate=rows_only` at D 216.13, which must exit nonzero. Exit codes in `exits.txt`.
States (all under `I461-win2/`): crawlG at D 216.1312, 220.1312, 224.1312, 228.1312, 232.1312; crawlI at D 235.1312; crawlL at D 242.5225; probeH00390625 at D 242.5264.
The four states of #505 (`../I505-win2/eq_D*.log`) are tabled with them. Results follow in this README.

## Results (2026-11-11 21:04:04 to 21:16:34 UTC)

Eight runs exited 0 (wave 1 21:04:06 to 21:08:13, wave 2 21:08:14 to 21:12:33 UTC, 4 min each in parallel), the control `--mutate=rows_only` at D 216.13 exited 1, as it must (`exits.txt`). `table_505.py` of `../I505-win2/` (selftest ok) makes `results_510.txt` from the eight logs here and the four of #505: equilibrated (Curtis-Reid + Ruiz) sigma_1..4, the rates between neighbouring states, the directions.

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 216.1312 | 1.5958e-48 | 5.8191e-48 | 4.4958e-45 | 3.8259e-43 |
| 220.1312 | 2.6221e-50 | 1.3028e-49 | 6.8858e-47 | 5.7239e-45 |
| 224.1312 | 5.0687e-52 | 1.6827e-51 | 8.9379e-49 | 6.2038e-47 |
| 228.1312 | 5.2065e-54 | 2.7302e-53 | 9.0427e-51 | 5.0644e-49 |
| 232.1312 | 6.6298e-56 | 2.3678e-55 | 5.7796e-53 | 3.5870e-51 |
| 235.1312 | 1.7640e-57 | 7.2114e-57 | 1.0301e-54 | 7.3125e-53 |
| 237.1312 (#505) | 1.6003e-58 | 6.1130e-58 | 7.0593e-56 | 4.3170e-54 |
| 239.5375 (#505) | 7.1519e-60 | 3.4004e-59 | 2.1721e-57 | 1.4433e-55 |
| 241.1244 (#505) | 9.2776e-61 | 4.4974e-60 | 2.0620e-58 | 1.4180e-56 |
| 242.3642 (#505) | 1.8825e-61 | 9.3856e-61 | 2.6498e-59 | 2.4555e-57 |
| 242.5225 | 1.5801e-61 | 7.3878e-61 | 2.0257e-59 | 1.9799e-57 |
| 242.5264 | 1.5733e-61 | 7.3439e-61 | 2.0127e-59 | 1.9690e-57 |

Rate of sigma_1, ln(sigma(D1) / sigma(D2)) / (D2 - D1), per unit of D between neighbouring states: 1.027 (216.13 to 220.13), 0.987, 1.145, 1.091 (228.13 to 232.13), 1.209 (232.13 to 235.13), 1.200 (to 237.13), 1.292, 1.287, 1.286 (241.12 to 242.36), 1.106 (242.36 to 242.52, over 0.158 in D), 1.106 (242.5225 to 242.5264, over 0.0039).
Mean rate 216.13 to 232.13: 1.062; 232.13 to 242.36: 1.248; over the whole range 1.135 (ratio 1.014e13 over 26.395). sigma_2 to sigma_4 follow the same shape (sigma_4: 1.05 at 216 to 1.41 at 237).
The reading rule (e^1.29 +- 0.1 from D 216 on: uniform; lower below some D and steeper there: report that D) gives: the rate is **not uniform**. Below D 232 it is e^1.0 to e^1.15 (outside 1.19 to 1.39 in all four intervals), it enters the band at 232.13 to 235.13 (1.209), and is 1.29 from D 237.
Checks: the planted check passes at each state (max deviation 4.66e-14, 4.96e-14, 4.44e-15, 6.00e-15, 2.66e-15, 2.22e-15, 7.33e-15, 5.55e-15; bound 1e-3); the rows-only control fails at D 216.13 (exit 1); D 242.36 repeats #502's 1.8825e-61 (#505's run, the same code). Directions of sigma_1 are the same at all twelve states: a_h 0.53 to 0.55 and m_h 0.45 to 0.47 in the scaled unknowns (top a_h k2, m_h k3, a_h k4, m_h k1, m_h k5), in z p1 0.25, m_h 0.13 to 0.14, node4.p 0.09 to 0.10 (top p1 k3, m_h k3, node4.p k3, node4.m k3, node3.p k3); the Delta share in z varies without trend (4.2e-07 to 1.2e-03).
