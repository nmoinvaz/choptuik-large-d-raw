# I1109-mm5: the l = 1 selection pair along D at k_c 55

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1109 (its body is the record: "l = 1: where the selection pair stops being pinned along D, and a formulation that pins it"). Stage 1 only.

Coordinator's order (2026-11-28 01:16 UTC): stage 1 on 2 threads at nice 10, beside #1101 R3 (6 threads) and the #1098 D 8000 tail (12 threads); those keep priority, and if the load passes 16 this is paused between states.
Code: branch `wip/i1101-weakdir` at **db7f9c60** (worktree `~/Source/choptuik-1109`, detached), `solver/matter/i1101_weakdir.py` (blob 8709abbdbdc8986f00a4228815679f366329ce23), run from `~/Source/choptuik-1109/solver/matter` with `~/venv-314/bin/python` (the one R3 uses; the issue names venv-1025dd).

**Inputs** (`in/`, each read with `git show origin/main:<path>` and its blob checked with `git hash-object --no-filters`): the k_c 55 states `I1025-mac/out/sol_l1kc55Fb1025_D{14.5000,15.0000,15.5000,16.0000,16.5000}.npy` (blobs d9238215, ad055605, 990ccde2, 94c8b048, 557bfff0), their record `I1025-mac/out/l1kc55Fb1025.jsonl` (5be40af4);
the control `I1101-dh170/in/sol_l1kc31r1025_D10.5000.npy` (f07a8984) and its record `I1101-dh170/in/l1kc31r1025.jsonl` (e5a87ec5), a converged low-D state.

**Commands**, per state (REC the record, STATE the state, D its D, STATEBLOB and RECBLOB their blobs), one state at a time, each under `timeout 3600`, `OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2 nice -n 10`, logs in this folder:

```
python3 i1101_weakdir.py jac REC STATE D jac_D.npz --pin=STATEBLOB,RECBLOB
python3 i1101_weakdir.py svd jac_D.npz svd_D.npz
python3 i1101_weakdir.py report jac_D.npz svd_D.npz D base=REC:STATE --out=rep_D.json
python3 i1101_weakdir.py valley jac_D.npz svd_D.npz REC STATE D --ts=1e-3
```

Order: the control (D 10.5) first, then D 16, then D 14.5, 15, 15.5, 16.5. The `jac_*.npz` and `svd_*.npz` files (100-200 MB) stay on the machine (not pushed, none deleted until the coordinator says); their logs and the `rep_*.json` are pushed as each state ends.

## Bars, written before the run (the issue's stage 1 acceptance, each can fail; coordinator's order)

1. **Control:** at D 10.5 the Gauss-Newton |dDelta| (the line `valley` prints) is at most **1e-8**. If it is larger: stop and report (the measure does not separate a pinned state from a path-set one).
2. **D 16 reproduces #1105:** U_w^T F within **1%** of **(+1.116e-10, -1.392e-10)**. If not: stop and report.
3. Report the first D at which |dDelta| > **1e-6**, or say that all five are above or below it.

Reported, a table per D: s/s_max of the two weakest non-null vectors, U_w^T F, |F|, the Gauss-Newton dDelta, seconds; and the first D with |dDelta| > 1e-6. Posted on #1109, pushed, reported to the coordinator. Estimate: about 2 min of J and SVD per state, 6 states, under 1 h.
