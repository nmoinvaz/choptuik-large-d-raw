# I788-mac: Borel-Pade sums of P1's noisy coefficients against the corrected zero law (K = 40, 60, 80, 100)

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/788 (pre-registration in the issue's comments, 20:01 UTC).

Code: `solver/harmony/stokes/stokes_bp.py` (with stokes_series.py, stokes_lines.py, zerolib.py), branch wip/i788
(venv-314: Python 3.14.7, mpmath 1.3.0, python-flint 0.9.0), run from `solver/harmony/stokes/`.

## Files

- `checks.log`: `selftest` (e^{ax} - c e^{bx}: its 10 zeros in the region to 1e-20, winding 10; exit 0) and its
  control `--mutate=coarse` (h = 2: none found; exit 1); `exact` (the order-3 law on P1's exact arm: e = 0.0117, as
  #773; exit 0).
- `run.log`, `sums.jsonl`: `run --K=40,60,80,100` (one record per sum: zeros, winding, arm, zero errors, x0_hat, e).
- `verdict.log`: `verdict --out=sums.jsonl` (exit 3: K = 100 does not suffice).
- Post hoc, not part of the test: `posthoc_noise.jsonl` with `posthoc_noise_first.log` (stopped at a singular Pade
  system of the noise-free data, m = 46), `posthoc_noise.log` (noise 0, 1e-20, 1e-17 at K = 100) and
  `posthoc_noise_K60_80.log` (noise 1e-17 at K = 60, 80).

## Results (pre-registered)

| K | P1 sums, entered | e1 of the entered P1 sums | C: abs(x0_hat - (x0 + 1)) | control fires | decisive |
|---|---|---|---|---|---|
| 40 | 8, 5 | 5.13-6.12 | 4.34-4.50 | no | no (the control K = 40 must fail: it does) |
| 60 | 11, 10 | 4.19-5.22 | 2.80-3.70 | no | no |
| 80 | 14, 12 | 1.20-2.91 | 0.67-3.28 | no | no |
| 100 | 17, 16 | 2.13 | 0.97-0.98 | no | no |

Verdict: K = 100 does not suffice. Eight sums failed the argument-principle check (count against winding) and did
not enter (sums.jsonl, "complete": false).

Median errors of P1's arm zeros over the entered sums:

| K | x1 | x2 | x3 | x4 | x5 | x6 |
|---|---|---|---|---|---|---|
| 40 | 4.4e-11 | 1.2e-6 | 1.2e-3 | 0.22 | 5.1 | 12 |
| 60 | 4.6e-12 | 4.1e-10 | 3.3e-8 | 5.0e-5 | 8.2e-3 | 0.42 |
| 80 | 2.2e-12 | 1.5e-10 | 1.5e-8 | 5.3e-7 | 1.2e-4 | 1.5e-2 |
| 100 | 3.9e-12 | 8.2e-11 | 7.6e-9 | 9.3e-7 | 2.0e-4 | 2.4e-2 |

## Post hoc: the noise, not K, sets the floor at K >= 80

P1's sums at K = 100 with other noise levels (same seeds; "every sum" means every sum that enters):

| noise | sums entered | e1 | median error of x5, x6 |
|---|---|---|---|
| 0 | 11 of 17 (6 Pade systems singular) | 0.0117 | 3.5e-25, 1.4e-24 |
| 1e-20 | 15 of 17 | 0.0116 | 2.0e-10, 2.5e-8 |
| 1e-17 | 17 of 17 | 0.0108-0.0117 | 2.0e-7, 2.5e-5 |
| 1e-14 (the test) | 16 of 17 | 2.13 | 2.0e-4, 2.4e-2 |

At noise 1e-17: K = 60 gives e1 3.0-5.7 and K = 80 0.06-5.3 (not every sum within 0.15). The zero errors at K = 100
scale with the noise (x6: 2.5e-8, 2.5e-5, 2.4e-2 at 1e-20, 1e-17, 1e-14) and are the same in every sum.
