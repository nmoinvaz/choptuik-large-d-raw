# I697-dh370: the horizon series' transient past order n/2, the solution's or the M = 32 grid's? (the dh370 run of #697)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/697 (recommended by #693, raw I693-mac/).
Code: choptuik-large-d main at f40deb4a (hp/horizon_radius.py as merged for #693), worktree `choptuik-large-d-685`, the venv of `choptuik-large-d-614` (the 3c35f0c build).
State: `I603-win2/chain_nat/anm_pin3_D253.8043.npz` (the newest D of I693-mac/states.txt, "D 253.80"), read in place.

## What is run, and the criteria written before any M = 48 run

1. M = 32, quad-double, orders to 300: `horizon_radius.py run` as for #693's long runs (`--precs qd --kmax 300`), at this state. The transient's peak t_peak (the max over fields and lanes of |c_k u0^k|, orders 100 on; as in `long_growth`) must reproduce I693-mac's stored value for the same state to 1e-3 relative, at the same order.
2. M = 48, quad-double, orders to 300: the same code with the horizon data (m_h, a_h, Delta) resampled from the 32-point half grid to the 48-point one by zero-padding their harmonics (the trigonometric polynomial of harmonics below 32 evaluated at 48 points, summed in mpmath and split into eight parts), and D, the layout of the two-node solver and kt = kc = 4 as in `Series.solver2`. The terms are stored as float64 sums of the quad-double parts, so no agreement below about 1e-16 relative can be tested. Amended before the first M = 48 run, with this reason: the criterion first written (orders 1 to 20 equal to 1e-24) cannot be met in that storage. The low orders at M = 48 against M = 32 are therefore reported, not judged: for orders 1 to 20 and the harmonics j <= 15 of each field, the largest |b48 - b32| relative to the order's largest term. The resampling's own controls are below, and the planted check of `horizon_radius.py selftest` (and its `--mutate drop_term`, which must fail) is run first.
3. Verdict by the issue's rule: with t_peak(48) / t_peak(32), the two M's agree if the ratio is within a factor 2 (the transient is the solution's) and differ if it is more than a factor 10 (the grid's); between, the ratio is reported as it is. The order of the peak is reported with it.
Controls of the new code (`m48_697.py`): the resampling at M = 32 to M = 32 returns the data to 1e-60 relative (its parts summed in mpmath), the 32 -> 48 -> 32 round trip does too, and a resampling with one harmonic's coefficient scaled by 1 + 1e-6 (`--mutate scale_h`) must change the M = 48 terms at order 1 by about that amount.

## Result: the first step is met, the M = 48 comparison cannot be made from M = 32's data

Step 1 (M = 32): my quad-double run to order 300 at D 253.8043 equals I693-mac's stored terms bit for bit (all 301 x 4 x 32 entries; peak 8.0255e-14 at order 211, identical). The selftest passes (`selftest.log`, exit 0) and its `--mutate drop_term` fails (`selftest_drop_term.log`, exit 1). The issue's "7.3e-14 at M = 32" is the peak at D 253.7313 (7.2796e-14); at D 253.80 it is 8.0e-14 (`peaks_693.txt`).

Step 2 (M = 48): the resampled data give a series that departs from M = 32's from order 8 and grows to 2e67 by order 300 (`m48/run_M48.log`, `m48/run_M48_qd.npy`), so there is no transient peak to compare.

| order | 1 | 5 | 8 | 10 | 15 | 20 | 40 | 100 | 200 | 300 |
|---|---|---|---|---|---|---|---|---|---|---|
| max\|b\| at M = 32 | 4.42e-02 | 8.20e-07 | 4.66e-10 | 5.81e-12 | 1.32e-14 | 5.04e-17 | 6.06e-26 | 1.02e-26 | 4.87e-14 | 2.72e-23 |
| max\|b\| at M = 48 | 4.42e-02 | 8.20e-07 | 4.66e-10 | 4.35e-10 | 3.68e-06 | 6.62e-03 | 6.14e+06 | 1.51e+20 | 3.99e+43 | 2.12e+67 |

The two agree to 3e-16 (the f64 storage) through order 5 in the harmonics j <= 15, and the M = 48 series then equals the M = 32 one with a_h scaled by 1 + 1.14e-22 (`delta_equivalence.txt`: delta_eff = 1.12e-22 to 1.14e-22 at orders 10 to 40, from the response at delta = 1e-16, which is linear). So the resampled data are not a solution of the M = 48 discrete equations, they are off by about 1.1e-22 in the direction the series sees, and the mass mode's gain (G = 0.7^-250 near 1e39) and 13.6's pole law turn that into the growth.
The control `--mutate=scale_h` (first harmonic of m_h times 1 + 1e-6) moves the order-1 terms by 1.01e-06 (`resample_controls/scale_h_control.txt`); the resampling returns the data to 1e-140 relative at M -> M and M -> 48 -> M (`m48/run_M48.log`), and the M = 32 -> 32 path through the new code gives the stored terms bit for bit (`resample_controls/id_M32.log`).

What a comparison needs: the M = 48 horizon data would have to satisfy the M = 48 discrete equations in a_h to far below 1e-22. At order 211 the M = 48 series' own response is 3.5e46 for an error of 1.14e-22, so 3.1e68 per unit of a_h error; the M = 32 peak is 8.0e-14, so an error below 2.6e-82 keeps its response under the peak and 2.6e-85 reads the peak to 1e-3. That needs the full M = 48 base at D 253.8 polished in octo-double (about 1e-120 relative precision). The octo-double kernel is M = 32 only (AGENTS.md).

## Files

| file | what |
|---|---|
| `run697_m32.sh`, `phases.log`, `selftest*.log`, `long_m32.jsonl`, `long_m32.log`, `coef_m32/` | step 1: the selftest, its mutation and the M = 32 series to order 300 |
| `m48_697.py`, `m48/`, `m48_mutate/`, `resample_controls/` | the M = 48 series from resampled data, its controls |
| `delta_m32.jsonl`, `delta_m32.log`, `coef_delta/`, `delta_equivalence.txt` | the M = 32 series with a_h scaled by 1 + delta, and the equivalent delta of the M = 48 growth |
| `peaks_693.txt` | the transient peaks of I693-mac's quad-double runs from D 253.07 |
