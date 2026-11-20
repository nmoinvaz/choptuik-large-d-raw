# I1025-win2b/p4: #1025 P4 hybrid re-roots, k_c 71 D 16.5

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, Windows 11), runner `win2b`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

The coordinator's GO for amendment 7 (hc 2026-11-20 about 21:45 UTC): the hybrid re-root (float64 blocks 0-11, double-double horizon block 12, multidouble 5.1.0 `dd_logdet`) of win2b's own k_c 71 recheck at D 16.5 (tag `l1kc71Fw1025c`, lam 2.1471294562703465 from `ell_refine.py`), on its own state and discrete system, by xfkappa's `p4_driver_rows.sh`. The built-in cross-check row runs first: Fb, D 16, k_c 55 must give the Mac's hybrid root 2.244042809616683 to 1e-5 or the batch stops.

## Setup (all blobs by `git hash-object --no-filters`)

| item | pin |
|---|---|
| code worktree | `D:/choptuik-1025p4` at wip/ell1-highD 505d839940456a3d04321d75cf66cc3b5bc831c4 (detached, clean) |
| driver | raw `I1025-mac/p4_driver_rows.sh`, blob e004c9ec5c722578b460a1354adc337626e75129 |
| `p4_hybrid.py` | raw `I1025-mac/p4_hybrid.py`, blob a402559b5d37661b49da50f07f877af21fd29b3a |
| row list | raw `I1025-mac/p4_rows_win2b.txt`, blob e0c173234c69941b16135ea529145c391599d80a (one row: the k_c 71 record and state below, D 16.5, timeout 43200 s) |
| k_c 71 record | raw `I1025-win2b/out/l1kc71Fw1025c.jsonl`, blob 0d174f3abea1dcc8f78dbe17ac5ee66980f7116b (raw 7d298661) |
| k_c 71 state | raw `I1025-win2b/out/sol_l1kc71Fw1025c_D16.5000.npy`, blob 8c8aa44ed5ca1e6349399f73311e50be580ec45c |
| cross-check inputs | raw `I1025-mac/out/l1kc55Fb1025.jsonl` (5be40af4) and `sol_l1kc55Fb1025_D16.0000.npy` (94c8b048) |
| python | `C:/Users/nathan/Source/venv-md510` (python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0) |
| raw clone read | origin/main 8def2687 (the row-list commit), by `git show` of each path into a fresh directory `D:/choptuik-p4in-1025-20261120` (`../p4_extract1025.sh`, which refuses a blob that differs from the pin or from the tree; its planted wrong-blob case exits 1); no live folder touched |
| threads | `THREADS=4` (BLAS and rayon), BelowNormal |

The driver's RAW argument is that fresh extraction directory and its OUT argument is this folder (`I1025-win2b/p4`), so the log, the jsonl and the per-row logs land in the live raw folder. The coordinator's command wrote OUT under RAW; this differs only in where the inputs are read from.

## Checks before the start

- The driver's own import line (`import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet`) passes in venv-md510; a nonexistent name fails with AttributeError, so the probe can fail.
- `dss_ell`, `ell_ddm` and `ddnp` import from `D:/choptuik-1025p4/solver/matter`.
- Planted `dd_logdet` check: random 40x40 against numpy's slogdet (same sign, ln|det| to 7e-15), diag(2,-3,5,7) gives sign -1 and ln 210, one row interchange gives sign -1; the wrong expectation (sign +1) is rejected.
- The driver caps its rows with `timeout`. Run on a dummy sleeper with venv-md510's python, `timeout 8` leaves no python process behind (the probe `listpy.ps1`, which lists the stub and its child while the dummy runs, shows none afterwards). As the standing rule asks for caps by exact pid, `p4cap1025.sh` also runs: for each `p4_hybrid.py` root python it kills the tree by its exact pid, after a command-line check, at the row's cap plus 120 s (cross-check 14400 s, k_c 71 43200 s). It is a fallback, not a memory watcher: nothing is stopped for memory.

## Log

(appended below as the run goes)
- 2026-11-20 21:46:13 UTC, first launch (`run1025p4.sh`): the driver refused before writing anything (`refuse: /d/choptuik-p4in-1025-20261120/I1025-mac/p4_hybrid.py is not blob a402559b`): it exports `MSYS2_ARG_CONV_EXCL='*'`, so native git got my `/d/...` path unconverted. Output kept as `../p4_launcher_attempt1_refused.out`. No `p4_w.log` or jsonl was created.
- 2026-11-20 21:46:47 UTC, second launch with RAW and OUT as `D:/...` paths: inputs checked (2 rows, the cross-check first), row 1 (Fb, D 16, k_c 55, timeout 14400 s) started 21:46:51 UTC. Both python pids (stub 25812 and child 34744) were Idle (the driver's `nice -n 10`), set to BelowNormal at 21:47:46 UTC by `p4prio1025.ps1` through `p4cap1025.sh`, which also holds the exact-pid fallback caps (cross-check 14520 s, k_c 71 row 43320 s, tested on a dummy `p4_hybrid.py` process: killed at its cap, none left).
- 2026-11-20 23:29:25 UTC, row 1 (cross-check) PASS: Fb, D 16, k_c 55, hybrid root 2.2440431253968165 against the Mac's 2.244042809616683, difference +3.16e-07 (bar 1e-5). The state is the record system (|F| 1.7855576974e-10 against the record's 1.7853243545e-10, steps 2565 = 2565). 12 evaluations, 1 sign change on the grid and 1 over all, bracket [2.2440431253968165, 2.244043147963646] (width 2.26e-8), noise-robust True (the float64 blocks 0-11 sign agrees in both noise draws at every point), 6149 s. Hybrid root minus the float64 record 2.2426280416106374: +1.415e-3. Raw: `p4_w.log`, `ell_p4_hybrid_1025_w.jsonl`, `p4_rows/row1_D16.log`.
- 2026-11-20 23:29:25 UTC, row 2 (k_c 71, D 16.5, `l1kc71Fw1025c`, timeout 43200 s) started by the driver; both python pids (stub 11484 and child 14088) were Idle and set to BelowNormal at 23:29:37 UTC. Cap fallback by exact pid at 43320 s (about 11:31 UTC 21 Nov). Verdict expected about 03:45 UTC 21 Nov.
