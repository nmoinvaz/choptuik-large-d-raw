# I252-mac: D 55.04 and D 61.03 at M 64, kf 23: determinant checks, counts, and circles at the M 40 and M 48 zeros

Machine: mac (Apple M5, 10 cores, shared). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/252

Code: worktree branch `wip/i252` of the main repository: main 590d88a with #242's rule cherry-picked
(`hp/modecount_wind.py` and `hp/modecount_planted.py` of `wip/i242` 01f6c59 and bc9fd22). Python
/Users/nathan/venv-314/bin/python (hpkernel and modecount_cx as installed, not rebuilt). At most 2 single-thread
processes, `nice -n 10`, `caffeinate -i`.

## Inputs

- `states/modecount_state_D61.0264_M64_kf23.npz`: #141's D 61 M 64 kf 23 state (nodes 0.3 ... 0.7, ks 191, |F| 8.5e-21;
  raw `I141-mac/states/`, 76fbf9b).
- `states/modecount_state_D61.0264_M64_kf23_outer085.npz`: #141's state with the node at 0.85, whose det M failed (the
  control of the determinant check).
- `states/modecount_state_D55.0351_M48_kf23_from_I232.npz`: the D 55 M 48 kf 23 state of #232 (raw
  `I232-macm3/D55/hp_data_after/`, identical to #241's), the start of the D 55 M 64 setup.
- lambda_phys = 2.043532530673195 (D 61.03) and 2.04768412771239 (D 55.04), as the M 40 and M 48 counts.

## Criteria (written before the runs)

1. **D 55 setup.** `hp/modecount_probe.py <D55 M48 state> --M=64 --kf=23 --setup --fmax=1e-15` (resample, fit_nodes,
   Newton then Levenberg-Marquardt). Its gates must pass (both series truncations <= 1e-15, |F| <= 1e-15), or D 55
   stops there.
2. **Determinant checks** (`scripts/det_check.py`, before each count): det M changes sign between lambda_phys - 0.015
   and lambda_phys + 0.015 in both LUs (hpkernel's real one and modecount_cx's complex one), the two LUs agree in
   ln|det M| to 1e-4 at both points, and their signs agree. The pivot range is recorded. Control: the same check on the
   outer-node state must fail (#141 found the LUs 2.2 apart and no sign change there). If the control passes, the check
   is not used. If a state fails, its count does not run.
3. **Counts.** `hp/modecount_wind.py <M64 state> --kf=23 --h0=0.6 --lam=<lambda_phys> --aLL=-0.096 --aL=0.124
   --fmax=1e-15 --resolve=last` (the fixed left column of #241; a1, a2 and aR chosen by the count as at M 48), with
   #242's alias rule (default pi/2). Reported per box: wind(g), resolved, both mismatch counts (any pass, last pass),
   largest step. An unresolved box is not a count.
4. **Circles** on the M 64 states (`hp/modecount_circle.py`, n0 20, tol pi/4). Each is read only if every step is
   below pi/4 with 0 verification mismatches. A lambda_phys circle (R 0.2) at each D must wind +1 with its zero within
   1e-5 of lambda_phys, or that D's circles are not read.
   - D 61 at the M 48 zeros (#230, kf 23): 1.3065 + 1.4158i, 2.0073 + 0.9727i, 2.5584 + 0.5825i, 3.0196 + 0.0958i.
   - D 55 at the M 48 zeros (#238): 0.1996 + 0.2548i, 0.3189 + 3.3314i, 0.0612 + 3.8526i, and -0.2267 + 4.2800i
     (outside the boxes).
   - D 55 at the M 40 zeros (#231): 0.4773 + 1.4533i (circle), and the moment positions 0.2427 + 0.9252i,
     0.0992 + 4.4804i, 0.3486 + 2.6122i, 0.3603 + 2.1609i, 0.5953 + 5.0393i.
   Reading per position: winding 0 means no zero within R of it at M 64 (absent). A winding >= 1 means a zero within R
   (present), and its M 64 position from the circle is compared with the lower-M one.
5. **Keeps its lambda.** A zero keeps its lambda if its M 64 position lies within 0.01 of its M 48 (or M 40) position,
   a tenth of the smallest shift seen between kf 21 and kf 23 at M 48 (0.054, #230), and present at every M where it
   was looked for. Otherwise it moved, multiplied or vanished.
6. **M 64 extras.** The zeros the count finds are located with `hp/modecount_moment.py` (no new determinants), and
   each located zero with spread below 0.05 is confirmed by a circle (R 0.2, n0 20) as time allows.

modecount_cx: the build of the main checkout (`hp/modecount_cx/build/modecount_cx.cpython-314-darwin.so`, 2026-11-08 16:26,
sha256 3e485ab9a27d6da50135b3fa94d758c922cd080f02d4a07a97e42b0de6136073, the same file #242 uses), copied into the
worktree's build folder, not rebuilt. The first launch (15:22 UTC) imported the crate's source folder instead and every
step exited 1 at once; its logs are in `failed_import/`.

## Redirect (coordinator, 2026-11-09 15:55 UTC)

After #250 both slots run circles: D 61 in one (`scripts/run_circles_D61.sh`), D 55 in the other
(`scripts/run_circles_D55.sh`), each with its lambda_phys control. Both full M 64 counts (`scripts/run_count_D61.sh`, and
the D 55 count of criterion 3) are held until the circles are in; the coordinator decides where they run.

Rebalanced at 16:30 UTC (D 55 has 11 circles, D 61 has 5): the shell of `run_circles_D55.sh` was stopped during its
lambda_phys circle, which ran on. `scripts/run_circles_D55_part1.sh` waits for it, gates on it, and runs the M 48 circles
and three M 40 circles. `scripts/run_circles_D55_part2.sh` runs the other three M 40 circles in the D 61 slot after the
D 61 circles, under its own tag (`D55.0351_M64_kf23_b`, its own cache), if the D 55 gate passed. The circles, their
order and their parameters are unchanged.

## Both lambda_phys gates fired (17:26 and 17:28 UTC)

| D | winding | max step | zero located | distance from lambda_phys | circle's own estimate |
|---|---|---|---|---|---|
| 61.03 | +1 | 0.342 rad | 2.043995 - 0.000281i | 5.4e-4 | 1.1e-3 |
| 55.04 | +1 | 0.334 rad | 2.047662 - 0.000005i | 2.3e-5 | 1.4e-5 |

Both exceed the 1e-5 of criterion 4, so no position circle ran (`run_circles_D55_part1.sh` and `_part2.sh` stopped at the
gate; the D 61 script likewise). `scripts/circle_spectrum.py` (cache only) gives the Fourier coefficients of ln h on each
circle: past k = 3 to 4 they sit on a white floor at every |k|, about 5e-3 at D 61 and 1e-4 at D 55, where the M 48 and
M 40 lambda_phys circles of D 55 (#238, #231) have about 3e-7 and 1e-7. A floor of e in a_-1 moves the zero by about
R e. The criterion is not loosened (coordinator, 17:40 UTC).

## Smoothness probe (criteria written before the runs)

`scripts/smooth_probe.py`: five modecount_cx determinants per state. A = the change of ln|det M| from x0 = lambda_phys -
0.015 to x0 + 1e-9 i (it should be O(1e-18); a large A means the li != 0 path, the 2M x 2M horizon solves, changes det M
by itself). B = |f(z + 2d) - 2 f(z + d) + f(z)| with f = ln det M, z the lambda_phys circle's second base point and
d = 1e-7 (it should be about 1e-13). The probe passes (smooth) when A < 1e-6 and B < 1e-6. Runs: D 61 M 64 and D 55
M 64, and as its control the D 61 M 48 kf 23 state of #212 (`states/modecount_state_D61.0264_M48_kf23_from_I212.npz`),
which must pass, since its lambda_phys circle located the zero to 5.5e-7 (#230). If the control fails, the probe is not
read.

## Matrix check (criterion in the script's docstring, written before its runs)

`scripts/matrix_cr.py`: the complex mode matrix (modecount_cx `mode_matrix`, no LU) at x0, x0 + eps and x0 + i eps,
eps = 1e-9. Each entry is analytic in lambda, so M(x0 + i eps) - M(x0) = i (M(x0 + eps) - M(x0)) to O(eps^2). Passes when
the largest departure is at most 1e-6 of the largest real difference. A failure names the row blocks (centre, segments,
horizon) and fields where the complex path departs. Run on D 55 M 64 first. The D 61 M 48 state is its control, which
must pass.

Further diagnostics, each with its reading in the script's docstring before its runs: `scripts/cdet_sensitivity.py` (the
LU on M, on M^T and on M with 1e-30 entry perturbations; its random-matrix control used 1e-20, which the f64 summation of
ln|u_kk| in clu_logdet cannot meet, 8.7e-12, so its numbers are measurements, not a passed test), `scripts/cdet_equil.py`
(exact power-of-two equilibration; control passed at 1.5e-11), `scripts/matrix_noise.py` (second differences of the
matrix entries at steps 2^-40 and 2^-46; `--ks` rebuilds the solvers with another horizon order on the same state).

## Diagnosis results (18:20 UTC)

| test | D 61 M 48 (ks 127) | D 55 M 64 (ks 150) | D 61 M 64 (ks 191) |
|---|---|---|---|
| probe A: ln\|det\| change x0 -> x0 + 1e-9 i | 9.5e-7 | 2.7e-4 | 1.7e-2 |
| probe B: second difference of ln det, d 1e-7 | 3.6e-5 | 8.6e-4 | 1.7e-2 |
| matrix analytic across the axis (departure / real difference) | 8e-8, pass | 8e-8, pass | not run |
| LU of M^T against M, ln det | 25 | 6.6 | 35 |
| M with 1e-30 entry perturbations, ln det | 5e-5 ... 6e-4 | 2e-5 ... 4e-5 | 5e-4 ... 8e-4 |
| equilibrated, 1e-30 perturbations | | 4e-2 ... 7e-2 | |
| entry error, centre block | 3e-25 | 3e-19 | 5e-20 |
| entry error, segments | <= 2e-28 | <= 2e-28 | <= 2e-28 |
| entry error, horizon block | 3e-24 | 5e-22 | 2e-21 |

The probe's control (D 61 M 48) failed its B criterion (1e-6), so the probe is not read as a pass or fail. Its numbers
are measurements. The matrix check's JSON write failed on a numpy bool (fixed afterwards), and its logs are the record.
The JSON of `matrix_cr_D55_M64` and `matrix_cr_D61_M48_control` is missing for that reason.

## Restated gate (option (c), Nathan via the coordinator, 18:30 UTC; written before any circle under it)

Reason: the cause of the fired controls is measured. The M 64 series blocks carry non-smooth entry error (table above),
which limits positions to about R x the ln h floor, while windings are unaffected. The science criterion, "keeps its
lambda" (criterion 5), is 0.01. The original gate (zero within 1e-5 of lambda_phys) **fired at both D** (17:26 and 17:28
UTC, `D55/gate_phys.log`, `D61/gate_phys.log`), and that result stays on record.

**New gate** (`scripts/gate_phys_v2.py`): the lambda_phys circle winds +1 with every step below pi/4 and 0 verification
mismatches, and its located zero lies within 3 times the circle's own estimate and within 1e-3 of lambda_phys. If either
D fails it, the circles stop and are reported. The controls are the same circles, replayed from their caches (no new
determinants), then gated.

**Circles** (n0 20, tol pi/4), one slot per D:
- D 61, M 48 zeros (#230, kf 23): 1.306478 + 1.415783i, 2.007279 + 0.972720i, 2.558385 + 0.582474i (R 0.2), and the
  pair 3.019571 +- 0.095819i by one circle on the axis (R 0.2, winding 2 if present).
- D 61, M 40 moments (#231, macm3, 17:23 UTC): 2.7626 + 0.6308i and 2.9141 + 1.5885i (spreads 7.5e-3 and 6.8e-3; R 0.2),
  1.98 + 1.20i and 1.83 + 0.49i (spreads 0.11 and 0.20; R 0.3), 0.032 + 3.086i (R 0.2).
- D 55, M 48 zeros (#238): 0.19957 + 0.25475i, 0.31895 + 3.33140i (R 0.2), 0.06118 + 3.85263i (R 0.3), -0.226688 +
  4.280040i (R 0.2).
- D 55, M 40 zeros (#231): 0.477308 + 1.453280i, and the moments 0.24271 + 0.92524i, 0.09923 + 4.48036i, 0.34863 +
  2.61221i, 0.36031 + 2.16089i, 0.59532 + 5.03932i (R 0.2).

Reading: as criteria 4 and 5. For a winding of +1 the located zero is reported with the **measured position noise** as its
error bar: the lambda_phys control's distance from lambda_phys at that D (5.4e-4 at D 61, 2.3e-5 at D 55; about 1e-3 and
2e-5), named as such, beside the circle's own estimate. "Keeps its lambda" stays: within 0.01 of the lower-M position.
The full M 64 counts stay held.
