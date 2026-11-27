# I1105-mac: the u0 effect on the last block of win2's k_c 135 D 23.0 state, on the Mac: machine and noise checks

Machine: Nathan's MacBook Air (Apple M5, macOS 27, the coordinator's), venv-314 (numpy with Accelerate). Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1105. Written 2026-11-27 08:06 UTC by the clock, after the runs
(they take seconds; dh170's sweep, raw I1105-dh170 b508c982b, came first).

- State: raw `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy`, blob cd134e2c (k_c 135, D 23.0).
- Code: `solver/matter/i1105_u0.py` on `wip/i1105-u0` at 5b1e38e8 (blob e522a5e7); threads 1 (OMP, OPENBLAS, VECLIB).
- `u0_kc135_d23_mac.log` / `.json`: `i1105_u0.py STATE 23.0 135 OUT --u0=0.02,0.03,0.04,0.05 --N=408,544`, exit 0
  (the sanity check passes). The same cases as dh170's, to compare machines.
- `noise.py`, `noise.log`: the state times (1 + 1e-16 g), g standard normal per entry (seeds 1-4, the period kept), then
  dF_last at u0 0.02 and 0.03 against u0 0.04, with the record's steps except the horizon segment's. Exit 0.

| quantity | dh170 (Linux, OpenBLAS) | Mac (Accelerate) |
|---|---|---|
| dF_last, u0 0.02, N 408 | 1.725e-8 | 2.018e-8 |
| dF_last, u0 0.02, N 544 | 1.698e-8 | 1.628e-8 |
| hz2 (horizon steps x2) against u0 0.02 | 1.5% change | 13% change, its bands rearranged |
| 1e-16 noise, seeds 1-4, dF_last at u0 0.02 | - | 2.020, 1.846, 2.036, 2.021e-8 (none: 2.018e-8) |
