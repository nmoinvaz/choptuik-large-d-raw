# I106-mac: the RT prototype at the resolution of arXiv:2611.07007 (40 x 80) at D 20-60, against hp, and its growth in D

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/106
Code: main b4d401f of nmoinvaz/choptuik-large-d (solver/rt/, #145's code) and branch wip/i106 (the fit script
solver/rt/rt_trunc_fit.py), worktree agent-abc971b3baa37717c; the reading is section 12 of notes/RT_FORMULATION.md
there. python-flint 0.9.0, numpy 2.5.4, Python 3.13.15 (/Users/nathan/venv-qd/bin/python, MULTIDOUBLE_SITE as #145).

## The grid of Ecker, Ecker and Grumiller (EEG) against rt_run.py's NtxN

EEG (arXiv:2611.07007v1, Sec. III) expand each field as sum g_nm exp(i n t / 2 + i m theta), theta = arccos xi, on
(t, xi) in [0, 4 pi] x [-1, 1], with N_Fourier = 40 and N_Chebyshev = 80, and count 40 * 80 * 2 * (1/4 + 1/2 + 1/2 +
1/2) = 11,200 real unknowns. The infrastructure is RT's (arXiv:1203.3766v1, Sec. 1.3 and 3), whose "number of Fourier
indices, 0 <= m < 250" and "number of Chebyshev indices, 0 <= n < 750" count non-negative indices, the negative ones
following from reality and evenness in theta. So 40 x 80 is 0 <= n < 40 (each 2 pi periodic field keeps the even n,
frequencies 0..19 of exp(i k t); omega_4, antiperiodic, keeps the odd n, frequencies 1/2..39/2) and 0 <= m < 80
(Chebyshev degrees 0..79, in xi itself, no map).

rt_run.py's NtxN is N_t collocation points in t on [0, 2 pi) and the N + 1 Chebyshev-Gauss-Lobatto points
xi_j = cos(pi j / N), with N odd (rt_model.RT asserts it, so that xi = 0, where the equations are divided by xi, is not
a point). Its unknowns are L = 3.5 N_t (N + 1) + 1. So EEG's 40 x 80 is `--grids 40x79`: L = 11,201 = EEG's 11,200
plus mu, the same polynomial degree (79) in xi, the same frequencies in t (0..19 and 1/2..39/2), the same odd-in-xi
halving of omega_1, the same independent equations ((1 + P) Omega_1^+, Omega_2^+, Omega_3^+, Omega_4^+), the same phase
condition Re(omega_4^-)_{1,0} = 0, no boundary rows, and Delta from Eq. (3). 40x80 itself (N even) is not supported.

What differs and cannot be matched by any NtxN:
- Projection. EEG truncate in coefficient space: products are exact convolutions, and the residual's retained
  Fourier-Chebyshev coefficients are set to zero (a Galerkin projection). rt_run.py collocates: the residual vanishes at
  the 40 x 80 points, so its truncation error carries aliasing that EEG's does not.
- Division by xi. rt_model divides the collocated equations by xi pointwise (RT's S); RT's coefficient-space S is the
  regularized left inverse (f - f(0)) / xi; EEG do not state theirs.
- The Nyquist mode. On an even N_t, each periodic field carries a cosine at frequency 20 (its t derivative set to zero),
  which EEG's index set does not have.
- Arithmetic and path: arb at 192 bits with an f64-preconditioned GMRES (#105), from D = 20 in steps of about 1 with a
  cubic predictor, against EEG's GMP dyadic Newton from D = 4 in steps of 1/2 with a linear predictor. With roots not
  unique along the weak direction (#145), the path can matter.
So the nearest grids on both sides in N, 40x77 and 40x81, are run too, as the local sensitivity of Delta to N.

## Criteria, written before the main runs (not changed afterwards)

Solver and options for every solve (as #145): `rt_run.py --solver mp` (192 bits) with `--max_products 250
--refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4`, `--newton_tol 1e-40` below D = 54 and `1e-36` from
D = 54.996085. A root counts when its record has ok true (max|F| below newton_tol, or a stall within 1e6 of it under
--patient). An unconverged solve may be restarted once from its last saved state; a step that does not converge then
is reported as failing. Delta_hp is the double-double row of hp/data/delta_all.csv (Delta_q0 + Delta_q1, err 1e-16 to
2e-15); differences are taken in arb from the records' 30-digit Delta_str.

1. **Control (can fail).** 32x121 at D = 20.043653 (start: I105-mac/cont/cont_32x101_D20.0437_32x101.npz) and at
   40.020065 (start: I145-mac/cont/cont_32x101_D40.0201_32x101.npz), and 32x101 at 60.001952 (start:
   I145-mac/fol/fol_32x121_D60.0020_32x121.npz), each converged and within 1e-9 of Delta_hp (`--tol 1e-9`, exit 0).
2. **Delta(40x79) - Delta_hp at the three D (the measurement).** At D = 20.043653, 40.020065 and 60.001952, two
   starts each: A, the 40x79 continuation of this folder (from the I105-mac 32x81 state at 20.043653, resampled), and B,
   the 32x101 states named in 1 (at 20.043653 and 40.020065) and I145-mac/cont/cont_32x101_D60.0020_32x101.npz,
   resampled. Both must converge. The value quoted is A's, with |A - B| beside it (the two-start spread, a lower
   bound on how far the grid leaves Delta undetermined). If |A - B| exceeds 10% of |Delta(40x79) - Delta_hp|, the value
   is quoted as the range of the two.
3. **The growth in D.** The continuation A lands on the hp rows nearest each integer from 21 to 60 (cont/README
   lists them), giving delta(D) = Delta(40x79) - Delta_hp on about 41 points. `rt_trunc_fit.py` fits ln|delta| by three
   models, E: a + b D (exponential), P: a + b ln D (power), Q: a + b D + c D^2, on the windows [20, 60], [30, 60],
   [40, 60] and [50, 60], using only the points at and above the last sign change of delta. Each of the 12 fits is
   extrapolated to D = 80, 100, 150 and 190. The spread over the 12 is reported as an estimator range (min to max),
   not an error bar; E and P on [30, 60] and [40, 60] are the primary set, whose range is quoted first.
4. **Planted truth first (can fail).** Before it reads real data, `rt_trunc_fit.py --planted` runs synthetic delta(D)
   of known exponential and power growth (1% multiplicative noise) on the same D points through the same code: the
   matching model's rate must come back within 2% and its extrapolation to 190 within a factor 1.5, and the verdict
   rule of 6 must classify planted cases of known class correctly. `--mutate=rate` (the checker expects a rate 10%
   off the planted one) must exit 1.
5. **EEG's departure.** d_EEG(D) = Delta_EEG - Delta_ours from hp/data/delta_published_compare.csv (minus its column
   diff), averaged over the windows 55-65, 90-110, 140-160 and 180-200 (centres 60, 100, 150, 190). Its ± is the
   standard error of the window mean from the rounding scatter (EEG print six decimals), not a bound. Before the runs
   these are +2.1e-7 ± 0.7e-7, +9.4e-7 ± 0.8e-7, +2.8e-6 ± 0.7e-7, +4.1e-6 ± 0.8e-7.
6. **Verdict on truncation, per D.** At D = 60 the measured delta(60.001952) of 2; at 100, 150 and 190 the estimator
   range of 3. "Reproduces" when delta has EEG's sign (positive) and its value or range overlaps [d_EEG / 3, 3 d_EEG];
   "far below" when its upper end is below d_EEG / 10; "far above" when its lower end is above 10 d_EEG; otherwise
   "between". The overall reading is evidence for truncation if "reproduces" holds at 60 and at two of the three
   larger D; evidence against (truncation far below their departures) if "far below" holds at all four; "far above"
   likewise means our collocation at their grid is far less accurate than their published values, so it cannot measure
   their truncation; anything else is reported per D as not decided.
7. **Mutation of the runs (can fail).** `rt_run.py --mutate=coef` at D = 20.043653 on 40x79 from the converged root
   A must move Delta by more than 1e-6 and exit 1.

Exit codes: the 40x79 runs use `--tol 1e-4` (a sanity bound, converged and near hp); the measurement is the number.

## What ran

(filled in as the runs go)
