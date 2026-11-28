# I1101-mm5: #1101 R3, the l = 1 refinement at kc 127, kappa 0.25, D 23 on the Mac mini M5 Pro

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1101 (the record is the coordinator's newest #1101 comment).

Coordinator's order (2026-11-28 00:45 UTC): #1101 R3 in the 6 free threads (D 8000's k* keeps its 12), in a worktree of `choptuik-large-d` at **48c36355** (`~/Source/choptuik-1101-r3`, detached), code blobs checked: `solver/matter/ell_refine.py` **631e58016c3912dc0871e56791c3e3f99ce04239**, `solver/matter/dss_ell.py` **5d28c19e17efa6b0103cb81d650891706605532d** (both equal to the order's).
R1's state and record copied from raw `I1101-macm3/in/` into the worktree's `solver/matter/data/` and blob-checked: `sol_l1kc127k050m3_D23.0000.npy` **0124dbd2cc25c949d374dbc722159b712c86598b**, `l1kc127k050m3.jsonl` **944a8179a615bae62a9e66e302e2b0acc3a4f79c**.

Command, from `solver/matter` with `~/venv-314/bin/python`, detached, `nice -n 10`, `timeout 43200`, OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=VECLIB_MAXIMUM_THREADS=6:

```
python ell_refine.py l1kc127k050m3 127 l1kc127k025mm5 127 1 23.0 2.0992182200 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

(source `l1kc127k050m3` at kc 127 re-solved at kc 127 with the RK stiffness target kappa 0.25, tag `l1kc127k025mm5`, l = 1, D 23.0, lam0 2.0992182200, K 30, u0 0.04, tol 1e-12, no gamma.) Output: `data/sol_l1kc127k025mm5_D23.0000.npy` and `data/l1kc127k025mm5.jsonl` in the worktree, pushed here at the end.

## Bars, written before the run (coordinator's order)

- **|F| <= 5e-10** at the end.
- **steps 11700 +- 2%** (11466 to 11934).
- Reported: the start (with any import error at once) and the end; the state and the record pushed here, with this README.

## Result (ended 2026-11-28 02:39:19 UTC; started 00:45:09: 6850 s by the wall clock, the record's `seconds` 6840; the 12 h cap was not reached)

By script from `l1kc127k025mm5.jsonl` (the record `ell_refine.py` wrote; blob 19848ea0f839ae23f36232d3adeb198eb6d6efb2) and its state `sol_l1kc127k025mm5_D23.0000.npy` (blob a6360ccccef12a7ba5fc7daafdfd3ad11a7b04bd), both copied here with the run's log `r3_run.log`:

| quantity | value | bar | verdict |
|---|---|---|---|
| \|F\| | **3.0997299661e-10** | <= 5e-10 | PASS |
| steps | **11687** (-0.111% of 11700) | 11466 to 11934 | PASS |
| Delta | 1.174322923351034 | (reported) | |
| kappa | 0.25 | | |
| constraint | 1.4638400868e-03 | (reported) | |

Start |F| of the run (`F_start`) 6.2196868426e-10. The log holds the start line, 18 `RuntimeWarning` lines of `dss_ell.py` (overflow and invalid value in the series sums at lines 211-219, 307 and 325, from the line search's trial steps; the run continued and ended with a finite record) and the final record line; no import error.
