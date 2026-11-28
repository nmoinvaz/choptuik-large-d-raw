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
  **Its numbers are kept as the scan's first point (D 10.5, k_c 31: |dDelta| 3.52e-8)**; its logs are `run_ctl10.5.log`, `jac_ctl10.5.log`, `svd_ctl10.5.log`, `report_ctl10.5.log`, `valley_ctl10.5.log` and `rep_ctl10.5.json`. Weak vectors below 1e-8: 8, the two weakest at s/s_max 2.10e-11 with U_w^T F +2.5269e-14 and -2.8222e-14, |F| 4.2644e-12.
- **The new control, the same bar (|dDelta| <= 1e-8; if it fails too: stop and report, the bar does not move):** D 7.0, `I810-mac/out/sol_l1kc31s810_D7.0000.npy` (blob **b62fac557136485d34216e1cdd5f31bcf70fcf88**) and its record `I810-mac/out/l1kc31s810.jsonl` (**21f83e6b2f33320c61381d611ee9e4f0a8177bfd**), both read from `origin/main` and blob-checked into `in/`; record |F| 7.9e-15, steps 1859.
  The same four commands, with `--pin=b62fac557136485d34216e1cdd5f31bcf70fcf88,21f83e6b2f33320c61381d611ee9e4f0a8177bfd`.
- **If D 7 passes:** D 16, then 14.5, 15, 15.5, 16.5, as written above (bars 2 and 3 unchanged).
- **The gauge check's exit 1 is known, not one of #1109's bars:** `report` exits 1 when the gauge generator at h = sin 2 w tau reads |J g|/(s_max |g|) above 1e-6 (the first control: 2.150e-06); it is a known failure reported in #1105 (comment 7229260535: 2.3e-6 and 2.5e-6 at D 16, from the generator's part above k_c). It is noted in the table of each state and the runs go on.

## Results of stage 1 (2026-11-28 01:17 - 01:28 UTC, 7 states, each state's four commands under timeout 3600, 2 threads, nice 10)

By script (`table.py`, from each state's `report_*.log`, `valley_*.log` and `run_*.log`; the table is `table.md`). The code: `i1101_weakdir.py` at db7f9c60. Every state rebuilt as "the record system" (|F| and steps equal the record's, jac's `--pin` with the full state and record blobs).
The jac and svd npz files (34-209 MB each, 2.5 GB in all) stay on the machine; their logs, the `rep_*.json` and the table are pushed.

| D | k_c | s/s_max, two weakest non-null | U_w^T F (two) | |F| | Gauss-Newton dDelta (full step) | GN \|dz\| | seconds | gauge generator at 2 w tau |
|---|---|---|---|---|---|---|---|---|
| 7.0 (control) | 31 | 1.396e-10, 1.396e-10 | +4.5459e-18, -1.7568e-17 | 7.8890e-15 | **-7.9596e-18** | 4.3802e-08 | 15 | cos 1.724e-08 ok, sin 3.948e-08 ok |
| 10.5 (first control) | 31 | 2.098e-11, 2.098e-11 | +2.5269e-14, -2.8222e-14 | 4.2644e-12 | **-3.5212e-08** | 8.3941e-04 | 15 | cos 8.831e-07 ok, sin 2.150e-06 FAIL |
| 14.5 | 55 | 1.113e-10, 9.085e-10 | +1.2465e-10, +1.8403e-10 | 2.2397e-10 | **-1.2432e-01** | 1.7116e-01 | 66 | cos 1.628e-07 ok, sin 4.183e-07 ok |
| 15.0 | 55 | 2.921e-11, 7.186e-10 | -8.5369e-11, +2.0732e-10 | 2.3783e-10 | **+2.8808e-01** | 4.1334e-01 | 53 | cos 4.287e-07 ok, sin 8.925e-07 ok |
| 15.5 | 55 | 9.740e-11, 5.233e-10 | -1.2424e-10, +1.7677e-10 | 2.1655e-10 | **+1.2088e-01** | 1.7402e-01 | 47 | cos 1.099e-06 FAIL, sin 1.713e-06 FAIL |
| 16.0 | 55 | 1.502e-10, 4.671e-10 | +1.1152e-10, -1.3924e-10 | 1.7853e-10 | **+6.0441e-02** | 9.9041e-02 | 61 | cos 2.271e-06 FAIL, sin 2.499e-06 FAIL |
| 16.5 | 55 | 1.592e-10, 4.705e-10 | -8.3988e-11, -1.8200e-10 | 2.0080e-10 | **+3.4416e-02** | 7.6172e-02 | 43 | cos 4.165e-06 FAIL, sin 3.039e-06 FAIL |

(The two weakest non-null vectors are the first two of the weak band: indices 0 and 1 at D 7.0 (no null band), 20 and 21 at D 10.5, 52 and 53 at k_c 55. The tau-translation generator's check is ok at every state: 7.4e-15, 6.5e-11, 1.6e-11, 1.7e-11, 2.1e-11, 5.9e-11, 1.5e-10; its control and the planted check pass at every state.)

## Acceptance, stage 1

1. **Control: PASSES at D 7.0.** The Gauss-Newton |dDelta| is **7.96e-18** (<= 1e-8; the full step, valley's line "Gauss-Newton step |dz| 4.3802e-08, dDelta -7.9596e-18"; 16 weak vectors below 1e-8). The first control, D 10.5, failed it (3.52e-8; it is past the onset of the weak selection, ELL.md section 6, and is kept as the scan's first point).
2. **D 16 reproduces #1105: PASSES.** U_w^T F (+1.1152e-10, -1.3924e-10) against (+1.116e-10, -1.392e-10): 0.07% and 0.03% apart (<= 1%); the pair's s/s_max 1.502e-10 and 4.671e-10 (the issue's 1.5e-10 and 4.7e-10); |F| 1.7853243545e-10, steps 2565, equal to the record's.
3. **The first D at which |dDelta| > 1e-6:** all five k_c 55 states are above it, by 4 to 5 orders and more: |dDelta| 1.24e-1 (D 14.5), 2.88e-1 (15.0), 1.21e-1 (15.5), 6.04e-2 (16.0), 3.44e-2 (16.5): so the lowest D scanned, **D 14.5**, is the first, and the onset in the k_c 55 family lies below it (not resolved). The two k_c 31 controls are below 1e-6 (D 7.0: 7.96e-18; D 10.5: 3.52e-8); the onset lies between D 10.5 (k_c 31) and D 14.5 (k_c 55), and the two k_c differ, so this scan does not locate it at one k_c.
   Along the k_c 55 states |dDelta| is not monotone in D (sign -, +, +, +, +; 0.124, 0.288, 0.121, 0.060, 0.034); the pair's s/s_max stays within 2.9e-11 to 9.1e-10 at every k_c 55 state, and its U_w^T F is 1e-10 to 2e-10, with |F| 1.8e-10 to 2.4e-10.

**The gauge check's exit 1 at h = 2 w tau** (the report's exit code is 1 at D 10.5, 15.5, 16.0 and 16.5, 0 at D 7.0, 14.5 and 15.0) is the known failure reported in #1105 (comment 7229260535: 2.3e-6 and 2.5e-6 at D 16, from the generator's part above k_c; here 2.271e-6 and 2.499e-6 at D 16.0), not one of #1109's bars.

## Amendment: stage 1b (2026-11-28 01:34 UTC, coordinator's order after #1109's stage 1 table; written before the runs)

Stage 1b puts the onset of the weak selection in **one k_c family each**, instead of between k_c 31 and 55: the same four commands per state (`run_state.sh`'s sequence: jac with `--pin`, svd, report, valley `--ts=1e-3`, each under `timeout 3600`, 2 threads, nice 10), the same push rule, beside #1101 R3 and #1111 stage 1 (3 threads). A state whose `jac` does not print "the record system" (or exits non-zero) is **skipped and logged**, and the scan goes on (no stop).
Reported per state: k_c, D, the two weakest non-null s/s_max, U_w^T F, |F|, the full Gauss-Newton dDelta, seconds; and per family the first D with |dDelta| > 1e-6 (bar 3's measure: the full step). Posted on #1109, pushed, reported to the coordinator. The jac and svd npz files stay on the machine.
The inputs (all read from `origin/main`, written to `in/`, each blob checked against the order's prefix: 0 mismatches; `list_1b.tsv` is the list the driver reads), in this order:

| tag | k_c | D | record (raw path, blob prefix) | state (raw path, blob prefix) |
|---|---|---|---|---|
| k31_D8.0 | 31 | 8.0 | `I810-mac/out/l1kc31s810.jsonl` 21f83e6b | `I810-mac/out/sol_l1kc31s810_D8.0000.npy` 1607d324 |
| k31_D9.0 | 31 | 9.0 | `I810-mac/out/l1kc31s810.jsonl` 21f83e6b | `I810-mac/out/sol_l1kc31s810_D9.0000.npy` 6cf9c62e |
| k31_D11.0 | 31 | 11.0 | `I1025-mac/out/l1kc31r1025.jsonl` e5a87ec5 | `I1025-mac/out/sol_l1kc31r1025_D11.0000.npy` f3190aa8 |
| k31_D11.5 | 31 | 11.5 | `I1025-mac/out/l1kc31r1025.jsonl` e5a87ec5 | `I1025-mac/out/sol_l1kc31r1025_D11.5000.npy` 0dd6388f |
| k31_D12.0 | 31 | 12.0 | `I1025-mac/out/l1kc31r1025.jsonl` e5a87ec5 | `I1025-mac/out/sol_l1kc31r1025_D12.0000.npy` e6a1cd54 |
| k31_D12.5 | 31 | 12.5 | `I1025-mac/out/l1kc31L1025.jsonl` 2f251d0e | `I1025-mac/out/sol_l1kc31L1025_D12.5000.npy` c7fa42ba |
| k31_D13.0 | 31 | 13.0 | `I1025-mac/out/l1kc31L1025.jsonl` 2f251d0e | `I1025-mac/out/sol_l1kc31L1025_D13.0000.npy` cc9fcaae |
| k31_D13.5 | 31 | 13.5 | `I1025-mac/out/l1kc31L1025.jsonl` 2f251d0e | `I1025-mac/out/sol_l1kc31L1025_D13.5000.npy` 63b8d7d9 |
| k31_D14.0 | 31 | 14.0 | `I1025-mac/out/l1kc31L1025.jsonl` 2f251d0e | `I1025-mac/out/sol_l1kc31L1025_D14.0000.npy` 19785b0b |
| k47_D10.5 | 47 | 10.5 | `I1025-mac/out/l1kc47r1025.jsonl` 9237f140 | `I1025-mac/out/sol_l1kc47r1025_D10.5000.npy` 31379cc6 |
| k47_D11.0 | 47 | 11.0 | `I1025-mac/out/l1kc47r1025.jsonl` 9237f140 | `I1025-mac/out/sol_l1kc47r1025_D11.0000.npy` 8a01271a |
| k47_D11.5 | 47 | 11.5 | `I1025-mac/out/l1kc47r1025.jsonl` 9237f140 | `I1025-mac/out/sol_l1kc47r1025_D11.5000.npy` 4090cd96 |
| k47_D12.0 | 47 | 12.0 | `I1025-mac/out/l1kc47r1025.jsonl` 9237f140 | `I1025-mac/out/sol_l1kc47r1025_D12.0000.npy` 034efc9e |
| k47_D13.5 | 47 | 13.5 | `I1025-mac/out/l1kc47L1025.jsonl` fd96857d | `I1025-mac/out/sol_l1kc47L1025_D13.5000.npy` f581080e |
| k47_D14.0 | 47 | 14.0 | `I1025-mac/out/l1kc47L1025.jsonl` fd96857d | `I1025-mac/out/sol_l1kc47L1025_D14.0000.npy` 56cc0051 |
| k47_D14.5 | 47 | 14.5 | `I1025-mac/out/l1kc47F1025.jsonl` 6ca9d422 | `I1025-mac/out/sol_l1kc47F1025_D14.5000.npy` 05c15737 |
| k47_D15.0 | 47 | 15.0 | `I1025-mac/out/l1kc47F1025.jsonl` 6ca9d422 | `I1025-mac/out/sol_l1kc47F1025_D15.0000.npy` abfc6128 |
| k47_D16.0 | 47 | 16.0 | `I1025-mac/out/l1kc47F1025.jsonl` 6ca9d422 | `I1025-mac/out/sol_l1kc47F1025_D16.0000.npy` b7059fab |

## Results of stage 1b (2026-11-28 01:34:58 - 01:41:37 UTC, 18 states in 6.6 min: 10-39 s each at k_c 31 and 47; each state's four commands as in stage 1)

By script (`table_1b.py`, from each state's `report_*.log`, `valley_*.log` and `run_*.log`; the tables are `table_1b.md`). **No state was skipped:** every `jac` printed "the record system" (|F| and steps equal to the record's) with the pin of its state and record blobs. The k_c 31 family joins stage 1's D 7.0 and D 10.5, the k_c 55 family is stage 1's five states.
The jac and svd npz files stay on the machine (not pushed); the logs, the `rep_*.json` and the tables are pushed.

**The onset, per family** (the first D with the full Gauss-Newton |dDelta| > 1e-6):

| k_c | last D below 1e-6 | first D above 1e-6 | note |
|---|---|---|---|
| 31 | 10.5 (3.5212e-08) | **11.0 (1.2610e-06)** | D 7.0 7.96e-18, D 8.0 1.34e-15, D 9.0 5.35e-13 below |
| 47 | 10.5 (4.8801e-08) | **11.0 (1.6907e-06)** | the lowest k_c 47 D is 10.5 |
| 55 | none (the lowest scanned is D 14.5) | 14.5 (1.2432e-01) | the onset below D 14.5 is not resolved in this family |

**Both families whose scans reach the onset put it between D 10.5 and D 11.0** (the scan step is 0.5; a log-linear interpolation of the two bracketing points gives the 1e-6 crossing at D 10.97 for k_c 31 and D 10.93 for k_c 47, `onset_calc.py`). The onset is the same to the scan's resolution in the two families.

Comparisons at common D, by script (`onset_calc.py` on `table_1b.md`):

- k_c 47 against k_c 31, six common D: |dDelta| ratio 1.386 (D 10.5), 1.341 (11.0), 1.324 (11.5), 1.213 (12.0), 1.180 (13.5), 1.185 (14.0). The k_c 47 value is 18% to 39% larger, and the gap narrows with D. Same sign at all six.
- k_c 55 against k_c 47: D 14.5 -1.2432e-01 and -1.2159e-01 (2.2% apart), D 16.0 +6.0441e-02 and +5.8732e-02 (2.9% apart). **At D 15.0 they differ by a factor 3.93** (+2.8808e-01 and +7.3309e-02), where the k_c 47 state's weak pair is at s/s_max 1.021e-11 and 2.733e-11, 11 and 15 times below the first value at D 14.5 (1.140e-10) and at D 16.0 (1.550e-10).
- Growth of |dDelta| in D (orders of magnitude per unit D between consecutive scanned D): k_c 31 2.2 (D 7-8), 2.6 (8-9), 3.2 (9-10.5), 3.1 (10.5-11), 1.4 (11-11.5), 3.3 (11.5-12), 1.7 (12-12.5), 1.1 (12.5-13), 0.6 (13-13.5), 0.7 (13.5-14); k_c 47 the same from 3.1 at D 10.5-11 down to 0.75 at D 13.5-14. The growth slows beyond D 12, and |dDelta| is 3.45e-2 at D 14 (k_c 31), 4.09e-2 (k_c 47).
- Sign: the k_c 31 and k_c 47 values are positive at D 11 to 12 and negative at D 13.5 and 14 (k_c 31: D 12.5 and 13.0 negative too); k_c 47 and k_c 55 change sign between D 14.5 (negative) and D 15.0 (positive), k_c 47 staying positive at D 16.

The records differ along the k_c 31 family (D 7 to 9 from `I810-mac`, D 10.5 to 12 from the `r1025` run, D 12.5 to 14 from the `L1025` run; the k_c 47 family: `r1025` D 10.5 to 12, `L1025` D 13.5 and 14, `F1025` D 14.5 to 16), so a change of trend at a record boundary (D 12 to 12.5 at k_c 31) is not separated here from the dependence on D.

**Gauge check, exit 1 of `report`** (the known failure at h = sin 2 w tau of #1105, not one of #1109's bars): k_c 31 at D 10.5, 11.0, 11.5, 13.0, 13.5, 14.0; k_c 47 at D 15.0 and 16.0; none at the other states.

## Tables of stage 1b (by script, `table_1b.py`; the same text is `table_1b.md`)

**k_c 31**

| D | s/s_max, two weakest non-null | U_w^T F (two) | \|F\| | Gauss-Newton dDelta (full step) | seconds | report exit |
|---|---|---|---|---|---|---|
| 7.0 | 1.396e-10, 1.396e-10 (idx 0, 1) | +4.5459e-18, -1.7568e-17 | 7.8890e-15 | **-7.9596e-18** | 15 | 0 |
| 8.0 | 2.393e-11, 2.393e-11 (idx 2, 3) | -1.9050e-15, -1.7623e-15 | 1.8358e-14 | **+1.3431e-15** | 14 | 0 |
| 9.0 | 1.997e-11, 1.997e-11 (idx 8, 9) | +7.2982e-16, -7.9595e-16 | 3.8128e-15 | **+5.3518e-13** | 11 | 0 |
| 10.5 | 2.098e-11, 2.098e-11 (idx 20, 21) | +2.5269e-14, -2.8222e-14 | 4.2644e-12 | **-3.5212e-08** | 15 | 1 |
| 11.0 | 2.221e-11, 2.221e-11 (idx 22, 23) | -2.1539e-13, -1.0416e-13 | 1.2600e-11 | **+1.2610e-06** | 12 | 1 |
| 11.5 | 3.795e-11, 3.817e-11 (idx 24, 25) | +4.0238e-13, +1.3563e-12 | 1.8229e-11 | **+6.4140e-06** | 10 | 1 |
| 12.0 | 1.568e-11, 1.572e-11 (idx 24, 25) | -1.5472e-12, -1.1675e-12 | 2.5343e-11 | **+2.9802e-04** | 11 | 0 |
| 12.5 | 6.148e-11, 6.931e-11 (idx 26, 27) | +2.3122e-13, -6.1226e-12 | 1.0949e-10 | **-2.0760e-03** | 10 | 0 |
| 13.0 | 3.014e-11, 3.382e-11 (idx 26, 27) | +6.6164e-13, -7.7540e-12 | 1.9302e-10 | **-7.0114e-03** | 10 | 1 |
| 13.5 | 1.454e-11, 1.737e-11 (idx 26, 27) | -9.2143e-12, -8.3872e-12 | 2.3726e-10 | **-1.4698e-02** | 10 | 1 |
| 14.0 | 1.083e-11, 3.989e-10 (idx 27, 28) | -4.7458e-12, -1.2641e-10 | 2.4183e-10 | **-3.4504e-02** | 11 | 1 |

first D with |dDelta| > 1e-6 in the k_c 31 family: 11.0

**k_c 47**

| D | s/s_max, two weakest non-null | U_w^T F (two) | \|F\| | Gauss-Newton dDelta (full step) | seconds | report exit |
|---|---|---|---|---|---|---|
| 10.5 | 2.097e-11, 2.098e-11 (idx 36, 37) | -3.2468e-14, +3.5903e-14 | 3.7735e-12 | **-4.8801e-08** | 32 | 0 |
| 11.0 | 2.221e-11, 2.221e-11 (idx 38, 39) | -3.0705e-13, +2.2626e-14 | 1.6353e-11 | **+1.6907e-06** | 34 | 0 |
| 11.5 | 3.802e-11, 3.821e-11 (idx 40, 41) | -5.4365e-13, -1.7610e-12 | 2.2723e-11 | **+8.4950e-06** | 31 | 0 |
| 12.0 | 1.572e-11, 1.576e-11 (idx 40, 41) | +2.5311e-12, +2.5942e-13 | 3.0696e-11 | **+3.6150e-04** | 39 | 0 |
| 13.5 | 1.380e-11, 1.759e-11 (idx 42, 43) | +6.9591e-12, -4.3176e-12 | 2.4963e-10 | **-1.7340e-02** | 33 | 0 |
| 14.0 | 3.987e-10, 1.124e-09 (idx 44, 45) | +1.4982e-10, +1.8309e-10 | 2.3689e-10 | **-4.0904e-02** | 35 | 0 |
| 14.5 | 1.140e-10, 9.067e-10 (idx 44, 45) | +1.2474e-10, +1.8843e-10 | 2.2788e-10 | **-1.2159e-01** | 34 | 0 |
| 15.0 | 1.021e-11, 2.733e-11 (idx 43, 44) | -7.9930e-11, +7.8457e-11 | 2.4268e-10 | **+7.3309e-02** | 32 | 1 |
| 16.0 | 1.550e-10, 4.722e-10 (idx 44, 45) | -1.1052e-10, +1.2749e-10 | 1.6893e-10 | **+5.8732e-02** | 30 | 1 |

first D with |dDelta| > 1e-6 in the k_c 47 family: 11.0

**k_c 55**

| D | s/s_max, two weakest non-null | U_w^T F (two) | \|F\| | Gauss-Newton dDelta (full step) | seconds | report exit |
|---|---|---|---|---|---|---|
| 14.5 | 1.113e-10, 9.085e-10 (idx 52, 53) | +1.2465e-10, +1.8403e-10 | 2.2397e-10 | **-1.2432e-01** | 66 | 0 |
| 15.0 | 2.921e-11, 7.186e-10 (idx 52, 53) | -8.5369e-11, +2.0732e-10 | 2.3783e-10 | **+2.8808e-01** | 53 | 0 |
| 15.5 | 9.740e-11, 5.233e-10 (idx 52, 53) | -1.2424e-10, +1.7677e-10 | 2.1655e-10 | **+1.2088e-01** | 47 | 1 |
| 16.0 | 1.502e-10, 4.671e-10 (idx 52, 53) | +1.1152e-10, -1.3924e-10 | 1.7853e-10 | **+6.0441e-02** | 61 | 1 |
| 16.5 | 1.592e-10, 4.705e-10 (idx 52, 53) | -8.3988e-11, -1.8200e-10 | 2.0080e-10 | **+3.4416e-02** | 43 | 1 |

first D with |dDelta| > 1e-6 in the k_c 55 family: 14.5

## Amendment: stage 1c, the pair at the threshold, k_c 127, D 23.0 (2026-11-28 01:46 UTC, coordinator's order of 01:45 UTC with its 01:46 correction; written before any run)

Folder `c/`. Worktree `~/Source/choptuik-1109` at 49664990 (`i1101_weakdir.py` blob 8709abbd, `d18_secant.py` blob eb1396ad), `~/venv-314/bin/python`, run from `solver/matter`, 2 threads per process (OPENBLAS/OMP/VECLIB = 2), `nice -n 10`; #1111's three runs and #1101 R3 keep priority. J at k_c 127 is about 8350 unknowns (0.6 GB; the SVD about 2 GB): the jac and svd npz stay on the machine, none pushed.

**Input** (R0, `origin/main`, written to `c/in/` and blob-checked: 90d3e6556817066dadb8ac8988f8b6661473a66e and d1a3a641ab9c9e53c2cc76e0170b1956e266346a, as ordered): state `I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy`, record `I1101-dh170/in/l1kc127k070w2.jsonl` (kappa 0.7, u0 0.04, Ks 30, |F| 3.1949266444e-10, 4179 steps, Delta 1.1743225027439044).

**Commands** (REC, STATE are the two `c/in/` files; `c/` paths below are in this folder):

```
python3 i1101_weakdir.py jac REC STATE 23.0 c/jac_r0.npz --pin=90d3e655,d1a3a641          (timeout 7200)
python3 i1101_weakdir.py svd c/jac_r0.npz c/svd_r0.npz                                      (timeout 3600)
python3 i1101_weakdir.py report c/jac_r0.npz c/svd_r0.npz 23.0 r0=REC:STATE --out=c/rep_r0.json   (timeout 3600, mine)
python3 i1101_weakdir.py valley c/jac_r0.npz c/svd_r0.npz REC STATE 23.0 --ts=1e-3,1e-2,1e-1 --save=1e-2:c/sol_w01_D23.0000.npy,1e-1:c/sol_w10_D23.0000.npy --refreeze=1   (timeout 7200, mine)
```

then three roots at once, 2 threads each, timeout 14400 each (the order's 01:46 correction: `i1101_weakdir.py root` takes only chord states, since it reads STATE.map.json; `d18_secant.py run` instead, as #1105 did; valley --save writes sol_X.npy and its stub sol_X.jsonl):

```
python3 d18_secant.py run REC STATE 23.0 0.0 0.1 c/root_r0.jsonl --tol=1e-6 --maxev=20 --b12=fast --pin=90d3e655,d1a3a641      (the control)
python3 d18_secant.py run c/sol_w01_D23.0000.jsonl c/sol_w01_D23.0000.npy 23.0 -0.1 0.2 c/root_w01.jsonl --tol=1e-6 --maxev=20 --b12=fast
python3 d18_secant.py run c/sol_w10_D23.0000.jsonl c/sol_w10_D23.0000.npy 23.0 -0.3 0.4 c/root_w10.jsonl --tol=1e-6 --maxev=20 --b12=fast
```

`run` is refused (exit 2) unless both ends are robust with opposite signs: then the bracket is widened once, by 2x each way about its centre (half-width doubled: r0 (-0.05, 0.15), w01 (-0.25, 0.35), w10 (-0.65, 0.75)), appended to the same output file, and said so in the report. A second refusal is reported, not widened again.

**Bars** (the order's, written before the runs):

1. `jac` prints the record system (|F| and steps equal to the record's, pin of both blobs); otherwise stop and report.
2. **Control:** the det-linear root of R0 (`lam_lin` of `root_r0.jsonl`'s last record) is within **1e-5** of **0.045967998** (dh170's); otherwise stop the other two roots and report.
3. Reported: the full Gauss-Newton dDelta at D 23 (valley's line at t = 0), each saved state's dDelta, |F| and root, and root - root(R0).
4. Reading, for information: dh170's kappa-0.7 roots give d lambda_1 / dD = (-0.0419082 - 0.045968)/0.125 = -0.703 per unit D, so a root shift r moves the k_c 127 zero by about r/0.703 in D.

The gauge check's exit 1 of `report` is the known failure of #1105, not a bar. Posted on #1109, pushed here (logs, JSON, the saved sol_w01 and sol_w10 states and their stubs if under 90 MB; no jac or svd npz), reported to the coordinator.

## Amendment: stage 1d, the Gauss-Newton step at two more threshold states (2026-11-28 02:38 UTC, coordinator's order of 02:38 UTC; written before any run)

Folder `d/`. Purpose: to see whether stage 1c's full Gauss-Newton dDelta of -1.96e-2 (R0, k_c 127, kappa 0.7, one weak vector at s/s_max 4.25e-11) holds across k_c and kappa. jac, svd, report and valley only, no roots. Worktree `~/Source/choptuik-1109` at 49664990 (`i1101_weakdir.py` blob 8709abbd), `~/venv-314/bin/python`, from `solver/matter`, 2 threads per process (OPENBLAS/OMP/VECLIB = 2), `nice -n 10`, both states at once, each command under `timeout 7200`. Stage 1c's roots and #1101 R3 keep priority. R2's J has 8351 steps, so about twice R0's jac time (442 s) is expected. The jac and svd npz stay on the machine.

**Inputs** (`origin/main`, written to `d/in/`, blob-checked against the order's prefixes: 0 mismatches):

| tag | k_c | D | kappa | state (raw path, blob) | record (raw path, blob) | record steps, \|F\| |
|---|---|---|---|---|---|---|
| kc135 | 135 | 23.0 | 0.7 | `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy` cd134e2c | `I1025-win2/kc135_d23/l1kc135win2d23.jsonl` bc295fbc | 4441, 3.1834404599e-10 |
| r2 | 127 | 23.0 | 0.35 (R2) | `I1101-dh170/in/sol_l1kc127k035w2_D23.0000.npy` 25ba3a91 | `I1101-dh170/in/l1kc127k035w2.jsonl` 9111bfca | 8351, 3.1242366894e-10 |

**Commands** (X = the tag; REC, STATE the `d/in/` files):

```
python3 i1101_weakdir.py jac REC STATE 23.0 d/jac_X.npz --pin=STATEBLOB,RECBLOB
python3 i1101_weakdir.py svd d/jac_X.npz d/svd_X.npz
python3 i1101_weakdir.py report d/jac_X.npz d/svd_X.npz 23.0 X=REC:STATE --out=d/rep_X.json
python3 i1101_weakdir.py valley d/jac_X.npz d/svd_X.npz REC STATE 23.0 --ts=1e-3
```

**Bars:** each `jac` prints the record system (otherwise that state is skipped, and said so). Reported per state, beside R0's stage 1c line (one weak vector at s/s_max 4.25e-11, U_w^T F -1.0446e-10, |F| 3.1940e-10, full Gauss-Newton dDelta -1.9568e-02, 510 s): the weak band's s/s_max below 1e-8 and just above it, U_w^T F, |F|, the full Gauss-Newton dDelta (valley's line), seconds. The gauge check's exit 1 of `report` is not a bar (known: #1105; and the h = cos 0 control at k_c 127). Posted on #1109 with stage 1c's results when both are in, pushed here, reported to the coordinator.

## Results of stage 1c (jac, svd, report, valley; the roots are still running) and stage 1d (2026-11-28 03:00 UTC)

By script (`d/table_d.py`, from each state's `rep_*.json` and `valley_*.log`; the same text is `d/table_d.md`). Stage 1c's R0 ran 01:47:03 - 01:55:33 UTC (jac 442 s, svd 41 s, report 5 s, valley 22 s; total 510 s); stage 1d's two states ran 02:39:06 - 02:51:23 (k_c 135, 737 s) and - 02:58:22 UTC (R2, 1156 s, jac 1076 s). All three `jac` printed the record system (steps equal to the record's; |F| on this machine against the record's: R0 3.1940e-10 against 3.1949e-10, k_c 135 3.1881e-10 against 3.1834e-10, R2 3.1233e-10 against 3.1242e-10). The jac and svd npz stay on the machine. In each table the weak band is the report's (s/s_max in [1e-11, 1e-5)); "below 1e-8" is the set valley takes its Gauss-Newton step on; U_w^T F is in the report's order (index from the smallest singular value; valley prints the vectors below 1e-8 in the reverse order).

| state | k_c | kappa | steps | \|F\| | weak below 1e-8 (s/s_max) | U_w^T F on them | weak above 1e-8 | U_w^T F on them | \|F\| weak part | full GN dDelta | GN \|dz\| | s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r0 | 127 | 0.7 | 4179 | 3.1940e-10 | idx 125 4.254e-11 | -1.0446e-10 | idx 126 2.690e-08, idx 127 2.691e-08 | -2.775e-13, +7.502e-14 | 1.045e-10 | **-1.9568e-02** | 2.7768e-02 | 510 |
| kc135 | 135 | 0.7 | 4441 | 3.1881e-10 | idx 134 4.031e-09, idx 135 4.032e-09 | +8.5432e-14, +1.1319e-15 | idx 136 9.135e-06 | +1.041e-15 | 8.545e-14 | **-9.1231e-12** | 4.1761e-08 | 737 |
| r2 | 127 | 0.35 | 8351 | 3.1233e-10 | idx 125 2.362e-11 | +9.6448e-11 | idx 126 1.511e-08, idx 127 1.512e-08 | +2.223e-12, -6.833e-13 | 9.648e-11 | **-1.8064e-02** | 2.5565e-02 | 1156 |

Field names as the report prints them (the unknown's part: d, c0, the node fields p m c q, mS aS qS, Delta). Weak vector composition (right: field shares and Delta's share, the two largest nodes, tau-harmonic bands [k 0], [1-3], [4-7], [8-15], [16-31], [32-] (HBANDS of i1101_weakdir.py), the three largest harmonics; left: the two largest blocks, fields, harmonics):

| state | idx | s/s_max | U_w^T F | right: fields (three largest), Delta share | right: nodes | right: tau-harmonic bands | right: top harmonics | left: blocks; fields; harmonics |
|---|---|---|---|---|---|---|---|---|
| r0 | 125 | 4.254e-11 | -1.0446e-10 | Delta 0.497, p 0.187, m 0.186; Delta 0.497 | x4 0.0587, x5 0.0585 | 0.0375 0.189 0.213 0.0493 0.0136 0.0005 | 5 0.13, 1 0.115, 7 0.0812 | 11 0.5, 12 0.5; q 0.655, p 0.165; k 1 0.981, 2 0.017 |
| r0 | 126 | 2.690e-08 | -2.7750e-13 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0687, 119 0.0334 | 11 0.344, 12 0.344; m 0.726, q 0.231; k 127 0.961, 125 0.0383 |
| r0 | 127 | 2.691e-08 | +7.5018e-14 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0686, 119 0.0332 | 11 0.344, 12 0.344; m 0.726, q 0.231; k 127 0.961, 125 0.0383 |
| kc135 | 134 | 4.031e-09 | +8.5432e-14 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 135 0.809, 133 0.0684, 127 0.0327 | 11 0.347, 12 0.347; m 0.72, q 0.23; k 135 0.962, 133 0.0363 |
| kc135 | 135 | 4.032e-09 | +1.1319e-15 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 135 0.809, 133 0.0683, 127 0.0326 | 11 0.347, 12 0.347; m 0.72, q 0.23; k 135 0.962, 133 0.0363 |
| kc135 | 136 | 9.135e-06 | +1.0414e-15 | d 0.424, p 0.237, m 0.216; Delta 0 | centre 0.436, x11 0.088 | 0.0032 0.478 0.0806 0.392 0.0435 0.0023 | 1 0.327, 3 0.146, 13 0.134 | 0 0.802, 1 0.126; q 0.971, a 0.0164; k 1 0.969, 6 0.0063 |
| r2 | 125 | 2.362e-11 | +9.6448e-11 | Delta 0.499, m 0.186, p 0.185; Delta 0.499 | x4 0.059, x5 0.0588 | 0.0367 0.186 0.215 0.0496 0.0137 0.0005 | 5 0.131, 1 0.111, 7 0.0816 | 11 0.5, 12 0.5; q 0.656, p 0.165; k 1 0.981, 2 0.0164 |
| r2 | 126 | 1.511e-08 | +2.2226e-12 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0687, 119 0.0334 | 11 0.339, 12 0.339; m 0.751, q 0.236; k 127 0.962, 125 0.0374 |
| r2 | 127 | 1.512e-08 | -6.8328e-13 | d 1; Delta 0 | centre 1 | 0 0 0 0 0 1 | 127 0.808, 125 0.0686, 119 0.0332 | 11 0.339, 12 0.339; m 0.751, q 0.236; k 127 0.962, 125 0.0374 |

Controls (the check passes when its value is small; a control must read >= 1e-3, else it did not fire):
- r0: tau generator 2.249e-10, tau control 2.758e-03 (fired); cos(0 w tau) 2.252e-10; cos(2 w tau) 3.999e-07; sin(2 w tau) 4.798e-07; cos(0 w tau) control 1.150e-04 (DID NOT FIRE)
- kc135: tau generator 1.658e-11, tau control 4.806e-04 (DID NOT FIRE); cos(0 w tau) 1.677e-11; cos(2 w tau) 4.231e-08; sin(2 w tau) 4.764e-08; cos(0 w tau) control 2.003e-05 (DID NOT FIRE)
- r2: tau generator 1.245e-10, tau control 1.527e-03 (fired); cos(0 w tau) 1.245e-10; cos(2 w tau) 2.214e-07; sin(2 w tau) 2.656e-07; cos(0 w tau) control 6.366e-05 (DID NOT FIRE)

**Reading, by script from the table's digits:**

- R2 (kappa 0.35) against R0 (kappa 0.7), both k_c 127, D 23.0: the same structure. The vector at idx 125 has Delta's share 0.499 and 0.497, its left vector sits in blocks 11 and 12 (0.5 each) in tau-harmonic k = 1 (0.981 in both). Its s/s_max is 2.362e-11 against 4.254e-11, its U_w^T F +9.6448e-11 against -1.0446e-10, and the **full Gauss-Newton dDelta -1.8064e-02 against -1.9568e-02 (R2/R0 = 0.923, 7.7% smaller)**. The pair above the cut (idx 126 and 127, pure `d`, harmonic 127) is at 1.511e-08 against 2.690e-08.
- **k_c 135 (kappa 0.7) has no such vector.** Its weak band is a pair at s/s_max 4.031e-09 and 4.032e-09 (pure `d`, harmonics 135 and 133, left vector in blocks 11 and 12) and a third vector at 9.135e-06 with no Delta share (d 0.424, p 0.237, m 0.216; left vector in block 0, harmonic 1). The pair's U_w^T F is +8.5432e-14 and +1.1319e-15, and the **full Gauss-Newton dDelta is -9.1231e-12**: 4.7e-10 of R0's. R0's -1.96e-2 does not hold across k_c: the Delta-bearing weak vector of k_c 127 is not in k_c 135's weak band.
- Dropping from k_c 127 to k_c 135 changes the weak band's U_w^T F by three orders (1.0e-10 to 8.5e-14), |F|'s weak part 1.045e-10 to 8.545e-14 of |F| 3.19e-10 (R0) and 3.19e-10 (k_c 135).

**Controls that did not fire** (a control must read >= 1e-3; the real checks, below it, pass at all three states: tau generator, h = cos 0, cos 2 w tau and sin 2 w tau all <= 1e-6). Not #1109 bars; they bear only on the gauge check, not on J, the SVD or the Gauss-Newton step (the coordinator's reading):

| state | control | value | needs |
|---|---|---|---|
| R0 (k_c 127, kappa 0.7) | h = cos 0 | 1.150e-04 | >= 1e-3 |
| k_c 135 (kappa 0.7) | tau generator | 4.806e-04 | >= 1e-3 |
| k_c 135 (kappa 0.7) | h = cos 0 | 2.003e-05 | >= 1e-3 |
| R2 (k_c 127, kappa 0.35) | h = cos 0 | 6.366e-05 | >= 1e-3 |

The tau generator's control fired at R0 (2.758e-03) and at R2 (1.527e-03). The report's exit code is 1 at all three states (these controls).

## Results of stage 1c's roots: the control fails bar 2, the other two roots stopped by the gate (2026-11-28 03:29 UTC)

By script (`c/roots_summary.py`; its output is `c/roots_summary.txt`, with every evaluation). The three roots ran 01:55:33 - 03:28:18 UTC (`c/run_c.log`), `--tol=1e-6 --maxev=20 --b12=fast`, brackets as ordered (no bracket was refused, no widening). The control, `root_r0`, ended at 03:28:18 (5565 s, 12 evaluations); the gate then stopped `root_w01` and `root_w10` (SIGTERM, rc 143; 11 evaluations each, no root record), as bar 2 says.

| root | state | evaluations | status | det-linear root | final robust bracket |
|---|---|---|---|---|---|
| r0 (control) | R0 | 12 | **nonrobust** (not robust at 0.04559167577503611, dln 0.276 > 0.1) | **0.045592888377014425** | [0.04484430241611344, 0.04560583793715152], width 7.6154e-04 |
| w01 | `sol_w01` (t 1e-2, 4179 steps) | 11, stopped | no root record | | [0.04413872351675394, 0.045490313638722434], width 1.3516e-03 (the robust sign-change bracket of the records so far) |
| w10 | `sol_w10` (t 1e-1, 4182 steps) | 11, stopped | no root record | | [0.0421002183739478, 0.04677662180360061], width 4.6764e-03 |

**Bar 2 (control: root(R0) within 1e-5 of dh170's 0.045967998): FAIL.** The control's det-linear root is 0.0455929, **3.7511e-04 below** dh170's value, and dh170's value is outside the final robust bracket (the hybrid sign is -1 at 0.04560583793715152 and at every larger lambda evaluated, up to 0.1). Bar 3's reading (the roots' shifts and the verdict against #1109's bounds) is not made: with the control failing the order stops it.

Reported as is, from `roots_summary.txt`:

- The hybrid sign of R0 is monotone: +1 at 0, 0.025, 0.0415, 0.0448443 and 0.0455917 (the last not robust), -1 from 0.0456058 on. The float64 sign is not: +1, +1, +1, **-1** at 0.0448443, +1 at 0.0455917, 0.0456058 and 0.0457597, -1 from 0.0474178 on. The two disagree at 0.0448443, 0.0456058 and 0.0457597 (the hybrid is -1 where the float64 is +1 at the last two); dh170's 0.045968 lies between 0.0457597 and 0.0474178, where this machine's float64 sign changes, not where its hybrid sign does.
- dln grows as lambda nears the hybrid root: 1.23e-05 (0.0448443), 5.22e-05 (0.0457597), 6.26e-04 (0.0456058), 2.76e-01 (0.0455917); about 8.8e-09 / |lambda - 0.045592| (an observation of the three numbers, not a fit).
- w01: the hybrid sign is -1 at 0.0454903 and above, +1 at 0.0441387 and below; its float64 sign is +1 up to 0.05 and -1 at 0.2. w10: hybrid and float64 signs agree at every evaluation (+1 up to 0.0421002, -1 from 0.0467766).
- The records' code: `d18_secant.py` blob eb1396ad and `i1101_weakdir.py` 8709abbd (the worktree at 49664990); `--b12=fast` (ell_fastdd's block 12, the order's choice), `mode_matrix_fast` for blocks 0-11, float64, Accelerate BLAS on macOS.
