# I1098-mac-sing: the nearest singularity of Delta(D) in e = 1/(D - 2), from the ladder records and the low-D rows together, with planted checks

Machine: the Mac (macOS, M-series laptop, at most 2 processes at nice 10). Run by a subagent of the coordinator (t5),
2026-11-27. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Code: branch `wip/i1098-sing` of choptuik-large-d, at e8841d12. Run it from `hp/` with `~/venv-314/bin/python`.
- `sing_data.py` gathers the points.
- `sing_core.py` holds the fits and the planted truths.
- `sing_noise.py` measures the rows' scatter.
- `sing_types.py` runs the scans and the calibrations.

Every number below is in a log or a JSON file of this folder.

## Data (`data.json`, `noise_*.log`)

`data.json` (`sing_data.py`, main's readers) holds:
- the 16 ladder records of `I1098-mac-a/ladder_records` (raw 55fd2c13a, D 250-4000, sigma err_sum);
- the qd, dd (err_kind check) and chain_fit rows of `hp/data/delta_all.csv` (d8ed31c0).

`noise_real.log` (`sing_noise.py`) gives each row's deviation from a degree-8 polynomial in e through its 7 neighbours
on each side, itself left out and scaled by the prediction's variance. It also gives the offsets at the junctions
between runs.
- The planted check passes (`noise_planted.log`): T1 plus noise of 5e-17 is recovered within a factor 1.25 in every
  band from D 16 up.
- The control fails as it should (`noise_control_K6H6.log`, degree 6 with 6 neighbours).

Measured scatter (rms) against the table's err (estimates, not bounds):

| rows | table err | rms |
|---|---|---|
| qd, D 67.7-73 | 2.4e-23 | 3.0e-17 |
| dd, D 36-68 | 2e-15 | 3.5e-17 to 5.4e-17 |
| dd, D 16-30 | 1e-16 | 9.8e-17 to 1.2e-16 |
| dd run up6, D 26.9-35.2 | 1e-16, 2e-15 | 70 rows deviate by more than 3e-16, up to 7.7e-15 |
| chain_fit, D 74-200 | 1.4e-15 to 2.8e-11 | 4.7e-17 to 5.4e-17 |

Discrepancies with the table:
- The qd rows' err (2.4e-23) is not their scatter. At D 67.8 they meet the dd rows with an offset of
  +2.2e-17 ± 6.4e-17.
- Run up6 is offset from run up7 by 4.4e-15 ± 2.4e-15 at D 35.2, against an err of 1e-16.
- chain_fit departs smoothly from fits to the other rows (`reach/`), inside its err: −2.1e-13 at D 99, −6.1e-13 at
  D 133, +1.6e-12 at D 199 and −2.4e-11 at D 245.6. The fits' own range there is at most 2.4e-16.

How the fits use the rows:
- They use `sing_core.sigma_eff`: about twice the measured scatter, and the ladder's err_sum.
- Run up6 is left out where marked "x" (e.g. D16x).
- chain_fit is left out of every fit and serves as a check.

## Result

Every ± or range below is the spread of an estimator over fits, seeds or planted truths. None is a bound.

- **Where:** the singular structure nearest e = 0 lies on the negative real axis, at e ≈ −0.055 to −0.059 (n = D − 2
  ≈ −18.3 to −16.9). How it reads depends on the type:
  - **As a branch point**, the quadratic Hermite-Padé forms put it at **e −0.0547** (n −18.3, D −16.3). This holds
    from D ≥ 16 to D ≥ 36. Over the planted branch points the reading falls within −2.0% to +2.6% of the truth, which
    gives e from −0.0558 to −0.0532.
  - **As a string of poles**, the rational fits put its first pole at e −0.0587 to −0.0600. The coordinator's
    ladder-only cluster at −0.0607 is this front pole.
- **The Taylor series in 1/(D − 2)** therefore has radius 0.053 to 0.059, so it converges for D > 18.9 to 20.8. Its
  coefficients a_k up to k = 12 grow as for a radius of 0.0542 to 0.0546.
- **Not an isolated simple pole.** Every planted simple pole whose next singularity is at least 5% further out reads
  differently from the real data on at least one of the tests below. These cover a T1-like background, residue × 0.3
  to 3, positions −0.0547 to −0.061, and a second pole or cut at −0.064 to −0.072. A string of simple poles from
  e −0.059 on does not read differently (section 4).
- **The type is not determined.** Data-matched truths of four kinds reproduce every reading of the real data:
  - a meromorphic pole string, the rational fit [17/4];
  - (1+e/r)^½, (1+e/r)^⅓ and log(1+e/r) branch points at r = 0.0547.

  Each of these fits the real points to χ² ≈ dof (`matched/`). A matched (1+e/r)^−½ truth departs in one reading.
- **Low D:** one rational form in e is accepted on all rows from D 8.25 to 4000 (26 to 36 parameters, `ratscan/real_D8x`).
  The analytic continuation along the positive e axis therefore holds down to D 8.25 at about 1e-15. Only the series
  in 1/(D − 2) stops, near D 19 to 21.

## 1. Rational fits: the front pole and its residue (`ratscan/`, `calib/`)

The fits are [L/M], with M from 2 to 6 and the two lowest accepted L per M. A fit is accepted when χ² ≤ the 0.99
quantile and every |residual| ≤ 4σ.

The front pole of a fit is its pole of least |e| on the negative real axis. Doublets do not count: a pole with residue
below 1e-8, or with a zero within 1% of it.

The statistic is the front residue at M 6 divided by that at M 2 (`drift_stats`). A simple pole keeps its residue
(ratio near 1). The front pole of a cut's string slides toward the branch point and its residue falls (ratio below 1).

The rule was fixed on the planted poles: a ratio from 0.94 to 1.06 reads as a simple pole.

Planted truths are T1 (the README formula, poles at −0.0769 and −0.191) plus one singular part at e −0.061. Its
amplitude matches T1's e⁶ coefficient, scaled by ×0.3 or ×3 where marked. Noise is 1σ_eff (`calib/summary_ratio.txt`):

| truth | D ≥ 16 without up6: ratio (range), read as pole | D ≥ 20 | D ≥ 25 |
|---|---|---|---|
| **real** | **0.46** | **0.48** | **0.35** |
| simple pole | 0.99 (0.99–0.99), 5/5 | 0.98, 10/10 | 0.96, 3/3 |
| pole × 0.3, × 3, at −0.0587 (× 1, × 0.3), at −0.0547 | 0.95 to 1.00, 25/25 | – | 0.99, 3/3 |
| T1 alone | 1.00, 5/5 | 1.00, 10/10 | 1.00, 3/3 |
| (1+e/r)^½ (× 0.3, × 1, × 3) | 0.19, 0.42, 0.53 | 0.41 | 0.41 |
| (1+e/r)^⅓ | 0.50 (0.44–0.67) | 0.48 | 0.40 |
| log(1+e/r) (× 0.3, × 1, × 3) | 0.53, 0.66, 0.72 | 0.60 | 0.57 |
| (1+e/r)^−½ | 0.85 (0.80–0.90) | 0.87 | 0.83 |
| (1+e/r)^{3/2} | 0.29 | 0.25 | 0.59 |
| double pole | 4.55 | 4.57 | 4.51 |
| exp(−¼/(1+e/r)) | 12.4 | 12.5 | 13.3 |
| pole + second pole at −0.064, −0.068, −0.072 | 0.14, 0.58, 0.85 | – | 0.93, 0.80, 0.92 |
| pole + (1+e/r)^½ or log at −0.068 | 0.90, 0.91 | – | 0.88, 0.85 |

- No planted non-pole reads as a pole except one (1+e/r)^−½ × 3 seed (0.94). Every planted isolated pole reads as a
  pole.
- A pole with a second singularity 5–18% further out reads as "not a pole". So this test alone cannot tell a branch
  point from a pair of close poles.
- At D ≥ 36 the test is weaker. The pole truths with less residue or with structure behind them give medians of
  0.81–0.91 (`calib/robust_D36`, read without the doublet filter), and the real data give 0.81 (`ratscan/real_D36`).

## 2. Quadratic Hermite-Padé forms (`quad/`)

The forms are A g² + B g + C = 0 with g = Δ − ref (`sing_core.Quad`). The statistic is the spread, over the accepted
forms, of the discriminant's front simple real zero. The rule was fixed on the planted truths at D ≥ 16: a spread
below 1e-3 reads as a branch point (`quad/summary.txt`).

| truth (D ≥ 16 without up6) | zero e | spread | read as a branch point |
|---|---|---|---|
| **real** | **−0.05470** | **1.8e-4** | **yes** (D ≥ 25: −0.05469, 8.4e-5; D ≥ 36: −0.05466, 1.5e-5) |
| (1+e/r)^½, ⅓, log at −0.061; amplitudes × 0.3 and × 3; at −0.055 | 0.980–1.028 × e0 | 1.2e-5 to 1.1e-3 | 31 of 35 runs |
| (1+e/r)^−½, ^{3/2}, (1+e/r) log(1+e/r); log at −0.055 | – | 1.5e-3 to 1.7e-2 | 0 of 26 |
| every pole truth: simple, at −0.0547, two close poles, pole + cut, double pole, essential, T1 | – | 1.6e-3 to 1.2e-1, or a zero in at most 2 forms | 0 of 52 |

At D ≥ 25 and D ≥ 36 the planted amplitude-1 branch points are no longer detected (spreads 1.1e-3 to 1.0e-2), and no
planted pole is either (0 of 12). The real data still read as a branch point, so the real singular part is more
visible than the planted one.

`quad/position.log` gives the position range in the result above.

## 3. Domb-Sykes on the fits' Taylor coefficients (`taylor/`, `darboux/`)

The accepted fits on D ≥ 16 give a_0..a_12 with relative spreads below 6.4%. On the planted (1+e/r)^½ truth they
match the exact coefficients to k = 14, within the fits' spread.

| k | a_k (median of 10 fits) | relative spread |
|---|---|---|
| 0 | 1.643893745125357513722882 | 2.3e-23 |
| 1 | 10.3752856284539554 | 4.4e-20 |
| 2 | −49.1687374900662836 | 4.5e-17 |
| 3 | 399.18546066508033 | 1.5e-14 |
| 6 | −744013.711050063326 | 9.6e-9 |
| 9 | 2390967761.31 | 1.2e-4 |
| 11 | 584863324154 | 9.7e-3 |
| 12 | −9345850017618 | 6.4e-2 |

- a_0 lies −6.0e-24 from `ladder_fit`'s Δ∞ and +1.1e-23 from `ladder_pade`'s. This is not independent: the ladder
  records dominate a_0.
- The ratios a_k/a_(k−1) fitted as A + B/k give e0 −0.0542 to −0.0546 and α from 0.58 to 0.53 over the windows k 6–9
  to 10–13.
- **This reading of α fails its planted test.** With the T1 background it reads α 0.11 for a square root, 0.15 for a
  log and 0.13 for a simple pole. With the amplitude × 3 it reads 0.36, 0.13 and −0.43. Every data-matched truth reads
  the same 0.545, because the data fix a_k up to k ≈ 11. So it is not used for the type.

## 4. Closure test on data-matched truths (`matched/D16x_s04_*`)

`sing_types.py matched` takes the first accepted form of each kind on the real points (D ≥ 16 without up6) as a
planted truth. Noise is 0.4σ_eff, about the real rows' scatter. Seeds 1 to 3:

| matched truth (χ², dof) | HP zero (spread) | front pole, ratio | Domb-Sykes e0, α |
|---|---|---|---|
| **real** | **−0.05470 (1.8e-4)** | **−0.0587, 0.46** | **−0.0545, 0.55** |
| rational [17/4] (47.7, 100) | −0.05469 to −0.05470 (4e-5 to 1.4e-4) | −0.0590, 0.45 | −0.0545, 0.545 |
| (1+e/r)^½ (12,3,2) (88.0, 103) | −0.05470 to −0.05478 (1.3e-4 to 9e-4) | −0.0589, 0.44 | −0.0545, 0.545 |
| (1+e/r)^⅓ (11,3,3) (117.1, 103) | −0.05386 to −0.05471 (0 to 9.9e-4) | −0.0590, 0.45 | −0.0545, 0.545 |
| log(1+e/r) (10,3,4) (137.7, 103) | −0.05473 to −0.05477 (1e-4 to 1.9e-4) | −0.0589, 0.44 | −0.0545, 0.545 |
| (1+e/r)^−½ (9,3,4) (87.8, 104) | −0.05466 to −0.05467 (7e-5 to 1.7e-4) | −0.0591 to −0.0610, 0.67 to 0.97 | −0.0545, 0.548 |

Every reading is fixed by the data. A meromorphic function with poles from e ≈ −0.059 on, and branch points of
exponent ½, ⅓ or 0 (log) at −0.0547, all reproduce them. Only the (1+e/r)^−½ truth departs, in the front residue
ratio, in all 3 seeds (0.67 to 0.97 against 0.46). So the data at D ≥ 16 and their analytic continuation cannot fix
the type. They mildly disfavor an exponent of −½.

At noise 1σ_eff the Hermite-Padé zero shows in at most one form for these truths (`matched/D16x_s1_partial_*`, a run
stopped early). So these readings need noise near the real scatter.

## 5. How far the analytic form reaches toward low D (`reach/`)

The accepted fits on D ≥ 36 are evaluated below D 36 (median of the fits minus data, and the fits' range):

| D | data − fit | fits' range |
|---|---|---|
| 34.9 (run up6) | +1.5e-14 | 7.9e-15 |
| 25.1 | −3.7e-13 | 4.0e-10 |
| 20.0 | −2.6e-11 | 5.4e-8 |
| 16.0 | −7.5e-10 | 4.6e-6 |
| 12.0 | −3.2e-8 | 1.0e-3 |
| 8.25 | −2.6e-6 | 1.2 |

- The fits on D ≥ 16 without up6 match the rows from D 16 to 4000 within 2.4σ, and miss D 12 by 4.8e-10. The left-out
  run up6 departs from them by up to 4.4e-14 (8.8σ_eff at D 32.1).
- Fits on D ≥ 8.25 are accepted, so the continuation is analytic over e from 0 to 0.16.
- chain_fit, which the fits never see, departs as listed under Data, inside its err.

## Open

- The type: a cut or a pole string, and its exponent. These data cannot settle it. A direct computation at negative
  n (D < 2), approaching n ≈ −18 from n → −∞ (the same e → 0 limit from the other side), could show a fold (Δ′ → ∞,
  a square root) or a pole (Δ → ∞). That works only if the form-S equations make sense for n < 0, which is not
  checked here.
- The 20-point ladder changes only e < 0.004. The position comes from the low-D rows and should not move.

## Commands

Run these from `hp/` of the branch, with RAW a clone of the raw-data repository and S = RAW/I1098-mac-sing:

```
python3 sing_data.py RAW/I1098-mac-a/ladder_records --out=S/data.json
python3 sing_noise.py S/data.json [--planted=5e-17 | --planted=5e-17 --K=6 --H=6]     # exit 1 on a failed planted check
python3 sing_types.py ratscan S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 --Ms=2,3,4,5,6 --extra=1
python3 sing_types.py calib S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 --seeds=1:5 '--truths=pole,sqrt,...'
python3 sing_types.py quadcalib S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 --seeds=1:5 '--truths=...'
python3 sing_types.py calsum S/calib/*.json; python3 sing_types.py quadsum S/quad/*.json
python3 sing_types.py taylor S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 --K=14
python3 sing_types.py darboux S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 '--truths=...'
python3 sing_types.py matched S/data.json --thin_dd=120 --Dmin=16 --drop_runs=up6 --scale=0.4 --types=rat,sqrt
python3 sing_types.py reach S/data.json --thin_dd=120 --Dmin=36 --Ms=2,3,4,5,6 --extra=2
```

Truth names are KIND[@E0][*AMPLITUDE], joined by '+' for a sum (`sing_core.truth_spec`). The kinds are pole, pole2,
sqrt, isqrt, s32, cbrt, log, ulog, ess and T1.
