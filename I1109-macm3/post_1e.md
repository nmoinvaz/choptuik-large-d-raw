#1109 stage 1e on macm3: nonlinear elimination at k_c 127, D 23.0 from R0, runner t5-macm3, 2026-11-28 08:36 UTC. Raw: `I1109-macm3/` (`ne/`, `ne_root.*`), raw-data commit c8be27192.

**Reading (b): the elimination stops at outer 1, the zero is not reached; the root of its last iterate (dDelta -2.4468e-03) is 0.040317475, -5.2742e-03 from 0.0455917, which is 2.75 times the linear estimate 0.785 x dDelta = -1.9208e-03.** The iterate's robust bracket is [0.0396709, 0.04032159856405092], so its root shift lies between -5.9208e-03 and -5.2701e-03, at least 2.74 times the linear estimate. The run ended exit 4 (last point not robust), as w01 and w10 did.

### Step 1: nonlinear elimination (`i1101_weakdir.py ne ... --outer=6`; output `ne.out`, table `ne_summary.txt` by `ne_summary.py`)

| outer | |U_w^T F| | Delta | dDelta from R0 | |F| | steps | J and SVD s | Gauss-Newton dDelta | fraction taken |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.0453e-10 | 1.174322502744 | +0.000000e+00 | 3.1959e-10 | 4179 | 498 | -1.9581e-02 | - |
| 1 | 1.0420e-10 | 1.171875672643 | -2.446830e-03 | 3.1513e-10 | 4183 | 737 | -1.9686e-02 | 0.125 |

Trial fractions (chord |F| first to last; |U_w^T F| and Delta after the chord steps):
- outer 0 fraction 1.0: chord 2.56e-04 .. min 1.11e-09 .. 6.20e-08 -> 1.4258e-07; |U_w^T F| 2.8063e-11; dDelta -1.953535e-02; steps 4228
- outer 0 fraction 0.5: chord 6.37e-05 .. min 3.03e-10 .. 3.12e-10 -> 3.1871e-10; |U_w^T F| 5.4430e-11; dDelta -9.778637e-03; steps 4201
- outer 0 fraction 0.25: chord 1.59e-05 .. min 3.11e-10 .. 7.29e-10 -> 1.3057e-09; |U_w^T F| 7.9518e-11; dDelta -4.892191e-03; steps 4190
- outer 0 fraction 0.125: chord 3.97e-06 .. min 3.14e-10 .. 3.14e-10 -> 3.1513e-10; |U_w^T F| 9.2043e-11; dDelta -2.446830e-03; steps 4183

|U_w^T F| ratios outer k / outer k+1: 1.003; stop line: True; reading: (b)

Run 07:39:05 to 08:00:46 UTC, exit 0, 1301 s, OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6, nice 10, RSS 6.3 GiB at the first J and SVD (one sample). The record system was reproduced at the start (|F| 3.1959e-10 against 3.1949e-10, 4179 steps). The saved iterate `ne/sol_ne1_D23.0000.npy` has |dz| 3.4733e-03 against R0 (Delta alone 2.4468e-03; dDelta from the state files' `z[-1]`).

By the rule the fraction with the smallest final chord |F| is taken: fraction 0.125 (|F| 3.1513e-10). Fraction 1.0 cut |U_w^T F| to 2.8063e-11 (3.72x) at dDelta -1.9535e-02, but the chord on the strong band diverged (|F| minimum 1.11e-09, final 1.4258e-07). Fraction 0.5 ended at |F| 3.1871e-10 (+1.1% against the one taken) with |U_w^T F| 5.4430e-11 (1.92x), after a chord that stalled at 3.03e-10 and drifted up. Outer 1's |U_w^T F| is 1.0420e-10, 1.003x below outer 0's: the elimination's own stop.

### Step 2: root of the iterate (`d18_secant.py run ... --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2`, RAYON_NUM_THREADS=2, `ne_root.jsonl`)

Bracket from the order's formula: centre 0.0455917 + 0.785 x dDelta = 0.043670938370651294, LO 0.0396709, HI 0.0476709 (+-0.004); the run used (0.0396709, 0.0476709). No exit 2, nothing widened.

| iterate | evaluations | exit | status | final robust bracket (width) | det-linear root | root - 0.0455917 | Brent end | seconds |
|---|---|---|---|---|---|---|---|---|
| ne1 | 6 | 4 | nonrobust | [0.0396709, 0.04032159856405092] (6.507e-04) | 0.04031747487157126 | -5.274225e-03 | 0.04032159856405092 | 1922 |

Evaluations (lambda, hybrid sign, float64 sign, dln, robust, seconds):

0.0396709 +1 +1 1.36e-05 R 338; 0.0476709 -1 -1 1.82e-06 R 322; 0.04112819028938678 -1 -1 1.03e-05 R 321; 0.04037853034139323 -1 +1 1.40e-04 R 336; 0.04032159856405092 -1 +1 1.93e-03 R 333; 0.04031715064433497 +1 +1 2.54e+00 NOT robust 272

### Reading

| item | value |
|---|---|
| outer steps run; stop | 2 (outer 0, outer 1); stop line printed: True |
| |U_w^T F| outer 0 -> outer 1 | 1.0453e-10 -> 1.0420e-10 (bar (a): >= 2x per step to <= 1e-12) |
| dDelta of the iterate from R0 | -2.4468301011e-03 |
| root - 0.0455917 | -5.274225e-03; robust range -5.9208e-03 to -5.2701e-03 |
| linear estimate 0.785 x dDelta | -1.920762e-03 |
| root shift / dDelta | 2.156 (w01 0.7868, w10 0.7838; robust range 2.42 to 2.15) |
| w10 for comparison (t = 0.1, 4182 steps) | dDelta -1.956e-03, root - 0.0455917 -1.5330e-03, ratio 0.784; here 1.25x the dDelta, 3.44x the shift |

### Failed or disagrees

- The order's comparison reads "root - 0.0455917 with -0.785 x dDelta"; the bracket formula and the w01/w10 ratios (+0.787, +0.784) have the other sign, which I used: +0.785 x dDelta = -1.9208e-03. With the order's sign the figure would be +1.9208e-03, opposite to the root shift -5.2742e-03.
- |dz| 3.4733e-03 and |dDelta| 2.4468e-03 give dDelta / |dz| = 0.7045; the weak vector at index 125 has Delta share 0.497 in mm5's report (comment 7232733432), sqrt 0.705: the displacement is mostly along that vector (I did not project it; no SVD was saved). w10 is mm5's valley state at t = 0.1 (-1.956e-03, 4182 steps) and the iterate here is the elimination's t = 0.125 step (-2.447e-03, 4183 steps): both are Gauss-Newton moves along the weak vector followed by chord steps on the strong band (I did not compare the two codes' details). dDelta grew 1.25x and the root shift 3.44x (w10 -1.5330e-03, here -5.2742e-03). I do not explain it.
- Exit 4: the last det-linear point (lambda 0.04031715064433497, dln 2.54) was not robust; its hybrid sign +1 is not trusted. Taken at face value the root lies in [0.04031715064433497, 0.04032159856405092].
- The float64 sign is +1 at 0.04037853 and 0.0403216 where the hybrid sign is -1 (as for w01 and r0); the hybrid sign is the one used.
- Nothing was pushed or posted from this Mac.

### Recommended tasks

- **Root versus t along the valley: t = 0.1 (control), 0.11, 0.125.** What: `i1101_weakdir.py valley --ts=0.1,0.11,0.125 --refreeze=1 --save=...` on R0's `jac` and `svd`, then `d18_secant.py run` on each saved state. Why: w10 (t = 0.1) has root shift / dDelta 0.78 and the 0.125 iterate 2.16, a 3.4x larger shift for a 1.25x larger dDelta; the middle point shows where it changes. Acceptance: the t = 0.1 root lies in w10's robust bracket [0.0439440, 0.0440614] (it must, if the valley reproduces w10; otherwise the states differ and the comparison is withdrawn); the three roots, each with exit 0 or 4, give shift / dDelta. Depends on: R0's `jac` and `svd` files (mm5's stay on its machine, #1109 comment 7232733432; here `jac` takes about 500 s).
