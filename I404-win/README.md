# I404-win: the RT prototype on the N = 3 mod 4 grid ladder, 32x99 to 32x123, at D = 60.001952, 54.996085, 50.007491 and 40.020065

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/404 (the coordinator's message `choptuik-large-d/2026-11-12/151101Z-coordinator-2c36.md`; recommended by #164's subagent; formerly #166).
Code: main f5f9eecb of nmoinvaz/choptuik-large-d, worktree `choptuik-i404` (`solver/rt/`, Python with python-flint 0.9.0 and multidouble's Python package with `dd_dot`, in venv-t151; nothing is built). The set-up is #164's (`I164-mac/README.md`): `rt_run.py --solver mp` (192 bits, N_t = 32).

Starts (the same files as #164, from `I145-mac`, copied unchanged; sha256 first 16 and size):

- a: `I145-mac/cont/cont_32x101_<D>_32x101.npz` (the 32x101 continuation's state): D 60.0020 4d4228bca5df6a23, D 54.9961 fd3170e8ac0340be, D 50.0075 f2f371033276c034, D 40.0201 18221618c647a967 (275656 bytes each).
- b: `I145-mac/fol/fol_32x121_<D>_32x121.npz` (the 32x121 root re-solved from a): D 60.0020 d536261c287d7fef, D 54.9961 782657c8d1dae592, D 50.0075 b5112fff7c82b272, D 40.0201 a6767a7dec01e91c (329416 bytes each).

Each is resampled to 32xN by `rt_run.py --start` and solved there at the same D.

## Criteria, written before the main runs (not changed afterwards)

- Solver and options, as #164 / #145 at D 55-60: `rt_run.py --start ST --grids 32xN --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol NTOL --out roots --tag <a101|b121>_32xN`, with NTOL = 1e-36 at D 60.001952, 1e-38 at D 54.996085 (#164's), and 1e-40 (rt_run.py's default, #145's own value up to D 53) at D 50.007491 and D 40.020065.
- Convergence: a root counts when its record has ok true, that is Newton reached max|F| below NTOL, or stalled within 1e6 of it under --patient. An unconverged solve may be restarted once from its saved last state with the same options (recorded here); if that does not converge either, the root counts as failing.
- Hp: the double-double rows of `hp/data/delta_all.csv` at D 60.001952 (up13), 54.996085 (up10), 50.007491 (up8) and 40.020065 (up7), Delta_q0 + Delta_q1, err 2e-15. Differences are taken in arb from the records' 30-digit Delta_str (`rt_grids.py`).
- Grids: N = 99, 103, 107, 111, 115, 119, 123 (all N = 3 mod 4), at each D from both starts: 14 solves per D. D 60.001952 first, then 54.996085, 50.007491, 40.020065. Four solves at once as separate processes, one thread each (BLAS threads 1), BelowNormal. The raw folder is pushed after each D, and the D 60 result is reported to the coordinator before going on.
- Definitions, per D and N: E(N) is the larger of the two roots' |Delta_RT - Delta_hp|; the spread s(N) = |Delta_a - Delta_b|; a grid passes when `rt_grids.py roots/a101_32xN.jsonl roots/b121_32xN.jsonl --D <D> --tol 1e-14` exits 0, that is both roots converged, both within 1e-14 of hp and their spread below 1e-14 (the hp rows carry err 2e-15, so 1e-14 is 5 times that).
- **Verdict at a D: the ladder falls to below 1e-14 when** some grid N* passes and E decreases strictly along the ladder up to N* (E(99) > E(103) > ... > E(N*)), or N* = 99 (it passes at the first rung; then the later grids are reported beside it). Otherwise the ladder **stops falling** at N_s, the first rung whose E is not below the previous rung's (E(N_{k+1}) >= E(N_k)) or the rung with the smallest E if E falls to the end: the report gives N_s, E(N_s), s(N_s) and the sign of Delta_RT - Delta_hp of each root along the ladder. The verdict of #404 per D is one of these two.
- Pair test: `rt_roots.py A.npz B.npz` (the planted check first, then the pair test of #164) on each pair of roots (a, b) at each N and D; the numbers (the roots' distance and B(e, e) / max|e|) are reported beside the verdict, outside it.
- Controls, once at D 60.001952, each must exit 1: `rt_grids.py --mutate=shift` on the best grid's two roots (2 tol added to one Delta) and `rt_roots.py --mutate=mid` on one pair of roots; the unmutated `rt_roots.py` planted check exits 0.
- Stop conditions: a Traceback, a solve past 4 h, or a failing restart (reported with its lines).

## What ran

(filled in as the runs go)
