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

## Amendment (2026-11-28 01:21 UTC, coordinator's reply to the first control; written before any further run)

- **The first control stopped at bar 1:** D 10.5 (k_c 31, state f07a8984, record e5a87ec5), run 01:17:07-01:17:22 UTC, 15 s: valley's line "Gauss-Newton step |dz| 8.3941e-04, dDelta -3.5212e-08": the full Gauss-Newton |dDelta| is **3.52e-8 > 1e-8** (the measure is the full step, not the t = 1e-3 line, whose dDelta is -3.4515e-11). The coordinator's error: ELL.md section 6 puts the onset of the weak selection at D about 9 (|dDelta/dF| 1.0e5 at D 8.15, x5 per unit D), so D 10.5 is past it and is not a pinned state.
  **Its numbers are kept as the scan's first point (D 10.5, k_c 31: |dDelta| 3.52e-8)**; its logs are , , , , , . Weak vectors below 1e-8: 8, the two weakest at s/s_max 2.10e-11 with U_w^T F +2.5269e-14 and -2.8222e-14, |F| 4.2644e-12.
- **The new control, the same bar (|dDelta| <= 1e-8; if it fails too: stop and report, the bar does not move):** D 7.0,  (blob **b62fac557136485d34216e1cdd5f31bcf70fcf88**) and its record  (**21f83e6b2f33320c61381d611ee9e4f0a8177bfd**), both read from  and blob-checked into ; record |F| 7.9e-15, steps 1859. The same four commands, .
- **If D 7 passes:** D 16, then 14.5, 15, 15.5, 16.5, as written above (bars 2 and 3 unchanged).
- **The gauge check's exit 1 is known, not one of #1109's bars:** `report` exits 1 when the gauge generator at h = sin 2 w tau reads |J g|/(s_max |g|) above 1e-6 (the control at D 10.5: 2.150e-06); it is a known failure reported in #1105 (comment 7229260535: 2.3e-6 and 2.5e-6 at D 16, from the generator's part above k_c). It is noted in the table of each state and the runs go on.
