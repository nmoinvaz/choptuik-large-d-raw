# I1025-dh610/repro_d1975: the same ell_refine run from dh170's k_c 87 D 19.75 state with 6 threads instead of 8, to test whether the re-converged state and the root near lambda_1's line reproduce

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 09:11:49 UTC, before any run of this folder. The k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after `../eval_dh170_d1975`, raw 3f130258), in part
"Run your reproducibility test: ell_refine.py from dh170's 352107a8 (k_c 87 to 87, as linRe) with 6 threads instead of 8 (tag l1kc87linRe6), then ell_cond (A = linRe, B = the 6-thread state; and its plant control) and d18_hybsign at 1.32 and 1.33 on the new state (2 procs). Written before (README): if the 6- and 8-thread states differ by about 1e-10 to 1e-9 along such directions and the root moves 2e-4 or more, one regrid at D 19.75 is reproducible only to ~0.002 and that is lambda_1's error bar there; if they agree bit for bit, the move came from the re-convergence itself, not from rounding. Then report, and start nothing else. Raw commit titles: 72 is the bar."

## Why
`../reconv_d1975`: dh170's state (352107a8) became linRe by 16 Levenberg-Marquardt Jacobians of `ell_refine.py` at 8 threads, a move of 4.0279e-10 (L2, Delta included); `../eval_dh170_d1975`: this build reproduces dh170's rows bit for bit, and ln|det| at 1.32 and 1.33 of linRe differs from his by +0.416 and -0.378 (the root near lambda_1's line 1.325410 against linRe's 1.327228, +0.001818), about 1e+09 per unit of |dz|. The printed |F| of dh170's state differs between ell_refine's 8-thread evaluation (3.9876058940e-10) and the single-thread d18 evaluation on both machines (3.9877716759e-10), 4.2e-05 relative; the cause is not tested. This folder asks whether re-running the same LM with another thread count ends at the same state.

## The readings, as numeric rules written before the run (`in/repro_read.py`; its selftest plants each case and its `--mutate` must fail)
x8 = linRe (8 threads, `../reconv_d1975/in`), x6 = linRe6 (this folder). norm dz is the L2 norm of x6 - x8 with Delta's entry included, as `ell_cond.py` prints it.
- **R0, bit for bit:** `numpy.array_equal(x6, x8)` (all 5695 entries): the move from dh170's state came from the re-convergence itself, not from rounding.
- **R1:** 5e-11 <= norm dz <= 2e-09 (the coordinator's "about 1e-10 to 1e-9", a factor 2 either side) and the two-point det-linear root in (1.32, 1.33) of x6 moves from x8's 1.327228 by 2e-04 or more: one regrid at D 19.75 is reproducible only to about 0.002, which is lambda_1's error bar there.
- **R2:** anything else; the numbers are reported (for example norm dz below 5e-11 but not zero, above 2e-09, or in the band with the root moving less than 2e-04).
**Limit of this test:** it reruns once at one other thread count and has no second 8-thread run. A difference between x6 and x8 is either the thread count (rounding order) or run-to-run nondeterminism at the same thread count; a same-thread-count rerun (not ordered) would separate them. A bit-for-bit match says the thread count (and any nondeterminism, in this run) did not matter.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lanes refuse any other blob)
| item | blob |
|---|---|
| dh170's state `sol_l1kc87dh170d1975_D19.7500.npy` and record `l1kc87dh170d1975.jsonl` | 352107a8, 6078a0b4 |
| linRe (8 threads, `../reconv_d1975`) state and record | 4988a55c, 6735329b |
| `d18_hybsign.py` (xfkappa's, unmodified), `kc87_syscheck_1025.py` | e089207a, 6df5d960 |
| dh170's rows `ref_dh170_scan_D19.75_1025.jsonl`; linRe's rows at 1.32 and 1.33 (`ref_linRe_*`); this build's rows of dh170's state (`ref_eval_dh170state_*`, `../eval_dh170_d1975`) | 0336f50f; b1d3f64a, 99d9b463 |
| `repro_read.py` (mine) | in `in_blobs.txt` |
| `ell_cond.py` (branch wip/ell-cond, worktree `~/Source/choptuik-large-d-1025h` at ee2c1dbd) | 1bb7b995 |
`ell_refine.py` is blob 631e5801 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399), python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2); `d18_hybsign.py` runs in `~/Source/choptuik-large-d-1025f` at 505d8399.

## Commands (systemd user units under `systemd-inhibit` with the alert-only memory log)
1. **Re-convergence** (`lane_refine6.sh` via `start_refine6.sh` = unit i1025ad): in `solver/matter` of 1025g, 6 threads (OMP, OPENBLAS, MKL = 6; nothing else differs from `../reconv_d1975/lane_reconv_refine.sh lin`), nice 10, cap 21600 s: `ell_refine.py l1kc87dh170d1975 87 l1kc87linRe6 87 1 19.75 2.1120935738 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. Refuses to start with less than 8 GiB free; the result goes to `in/` (`in_blobs_refine6.txt`). Outputs `ref6/`.
2. **After** (`lane_after6.sh` via `start_after6.sh` = unit i1025ae, started at once and waiting for `ref6/DONE.txt`): the bit-for-bit comparison (logged); (info) `kc87_syscheck_1025.py` on the new state with its two controls; `ell_cond.py` control `--mutate=plant` on (linRe, linRe6) at 8 threads (exit 0 and "plant check: PASS", else the lane stops); then at the same time `ell_cond.py` on (A = linRe, B = linRe6) at 6 threads and `d18_hybsign.py` on linRe6 at 1.32 and 1.33 (2 processes of 1 thread, nice 10, each printing the record system); then `repro_read.py read` into `summary_repro.txt`.

## Acceptance (fixed before the run)
- The ell_refine run exits 0 (the cap is a stop); the ell_cond control exits 0 with PASS (a failing control stops the work and I report it; no bar is loosened); both d18 processes print "the record system" (a "NOT the record system" or a non-zero exit stops the work and is reported).
- Reported: the bit-for-bit result, norm dz and the ell_cond lines, |F| before and after, ln|det| and signs at 1.32 and 1.33 beside linRe's, the two-point roots and their move, and the reading R0, R1 or R2.

## Predictions, registered before the run (information)
- ell_refine exits 0 (95%) in 3000 to 4800 s (60%; the two 8-thread runs took 3748 s and 3652 s side by side; this one runs alone with 6 threads).
- **R0, bit for bit equal: 10%** (the single-thread and 8-thread residuals of one state differ in the fifth digit, which suggests the rounding depends on the thread count; the other side is that OpenBLAS splits gemm along M and N and keeps each element's K-order). **R1: 30%. R2: 60%** (norm dz above 2e-09: 30%; in the band with the root moving less than 2e-04: 20%; below 5e-11 but not zero: 10%).
- The 6-thread record's |F| is within 0.1% of linRe's 3.9854e-10 (80%); the ell_cond control passes (90%); both d18 print the record system (95%), signs -, + at 1.32 and 1.33 (90%).

## Status
- 2026-11-23 09:11:49 UTC: folder, inputs, lanes, selftests and the reading prepared before any run.
