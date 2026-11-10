# I259-mac: sums against terms in modecount_cx's series blocks at M 64 (step 1), and the quad-double accumulation

Machine: mac (Apple M5, 10 cores, shared). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/259

Code: worktree branch `wip/i259` of the main repository (from main bfe5fd5). modecount_cx rebuilt there with
`hp/modecount_build.sh`; hpkernel not rebuilt. Python /Users/nathan/venv-314/bin/python. One process at a time, 2
threads, `nice -n 10`, `caffeinate -i`.

Inputs: the states of `I252-mac/states/` at raw 940d3f0c (D 55.04 M 64 kf 23, ks 150; D 55.04 M 48 kf 23 from #232;
D 61.03 M 64 kf 23, ks 191; D 61.03 M 48 kf 23 from #212). lambda_phys = 2.04768412771239 (D 55.04) and
2.043532530673195 (D 61.03).

## Step 1: the measurement (criteria written before the runs)

`scripts/series_acc_probe.py` (its docstring defines every quantity). The new `CSolver.series_matrix(zh, zl, lr, li,
acc)` computes only the series blocks' columns of the mode matrix. acc 0 is the production summation; acc 1 sums each
series' final Horner evaluation in quad-double from the same double-double coefficients. At z = lambda_phys + 0.2
e^{2 pi i/20}, d = 2^-46, per block (centre rows, horizon rows): rel D2 for each acc, the wiring difference, and T, the
largest |tangent term| c_k h^k of the Horner sums, with floor = 2^-106 T / max |M|.

Runs: D 55 M 64, then D 55 M 48 as the control.

1. **Wiring.** At each state the acc 1 matrix differs from the acc 0 one in some series entry, by at most 1e-12 of the
   block's max |M|. If not, the probe is not read.
2. **Control.** At D 55 M 48 both blocks' rel D2 at acc 0 is at most 1e-23 (#252's M 48 level, 3e-25 and 3e-24 at
   D 61). If it fails, the probe is not read as sums against terms; its numbers are reported as measurements.
3. **Reading at D 55 M 64**, per block, with ratio = rel D2 (acc 0) / rel D2 (acc 1):
   - **the final sums dominate** if ratio >= 100 and rel D2 (acc 1) is within 10 times the control's rel D2 (acc 0);
   - **the terms dominate** if ratio < 10 and rel D2 (acc 0) is within 30 times the floor (the size of the stored
     double-double coefficients alone explains it, and no summation of them can go below it);
   - if ratio < 10 but rel D2 (acc 0) is more than 30 times the floor, the coefficients carry more error than their own
     rounding: the recurrence's inner sums (the Cauchy products) are the next suspect, and a variant with those in
     quad-double is run before the verdict;
   - anything else is reported as mixed, with its numbers.

### Step 1 results, acc 0 against acc 1 (2026-11-10 00:45 UTC; `probe/series_acc_D55_M64.*`, `probe/series_acc_D55_M48.*`)

| | D 55 M 64 centre | D 55 M 64 horizon | D 55 M 48 centre | D 55 M 48 horizon |
|---|---|---|---|---|
| max \|M\| of the block | 1.01 | 2.30e8 | 1.01 | 2.30e8 |
| rel D2, acc 0 | 2.70e-19 | 5.08e-22 | 1.40e-24 | 1.46e-24 |
| rel D2, acc 1 | 2.70e-19 | 5.08e-22 | 1.37e-24 | 1.46e-24 |
| ratio acc 0 / acc 1 | 1.00 | 1.00 | 1.02 | 1.00 |
| wiring | 7.2e-21 | 5.3e-29 | 4.5e-26 | 4.3e-32 |
| T | 2.54e11 | 3.90e11 | 1.76e6 | 1.33e8 |
| floor 2^-106 T / max \|M\| | 3.1e-21 | 2.1e-29 | 2.1e-26 | 7.1e-33 |
| rel D2 (acc 0) / floor | 87 | 2.4e7 | 65 | 2.1e8 |

Criterion 1 (wiring) passes at both states and criterion 2 (control at most 1e-23) passes. By criterion 3 the final
Horner sums are not the cause (ratio 1.00), and rel D2 is more than 30 times the floor in both blocks, so the Cauchy
product variant runs before the verdict.

### Step 1b (criteria written before the runs)

`series_acc_probe.py ... --accs=0,2,3` (`scripts/run_step1b.sh`) at D 55 M 64, then D 55 M 48 as the control. acc 2
also sums every Cauchy product of the two series (`cs`, `cs_w`, `cs_range`) with exact products in quad-double, rounded
once; acc 3 does that and also the series' D f (the d/dtau matrix product, a sum of M products) in quad-double.
Everything else (the stored coefficients, the horizon's periodic LU solves, the products by 1/c0 and the order's
divisions, the sums of the few partial results within one order) stays double-double.

1. Wiring and control as in step 1 (the acc 2 and acc 3 matrices differ from acc 0 by at most 1e-12 of max |M| and not
   by 0; the control's rel D2 at acc 0 at most 1e-23).
2. Reading at D 55 M 64, per block, ratio = rel D2 (acc 0) / rel D2 (acc 2 or 3):
   - **the sums dominate** if, for acc 2 or acc 3, ratio >= 100 and rel D2 is within 10 times the control's rel D2
     (acc 0); the lowest acc that does it names the sums, and it becomes the step 2 fix;
   - **the terms dominate** if ratio < 10 for both acc 2 and acc 3: the error is made in the operations that stay
     double-double (the stored coefficients, the solves, the per-term products and divisions), which quad-double sums
     cannot reach;
   - anything else is mixed, reported with its numbers.

   For the centre block the floor (3.1e-21 at M 64, 2200 times the control's 1.4e-24) already bounds what any summation
   of double-double coefficients can reach, so its "sums dominate" outcome needs the floor estimate to be wrong by that
   factor. It is run anyway, as written.

### Step 1b results at D 55 M 64 (01:30 UTC; `probe/series_acc023_D55_M64.*`)

| | centre | horizon |
|---|---|---|
| rel D2, acc 0 | 2.70e-19 | 5.08e-22 |
| rel D2, acc 2 (Cauchy products in qd) | 2.14e-19 | 3.40e-22 |
| rel D2, acc 3 (also D f in qd) | 6.59e-20 | 1.91e-22 |
| ratio acc 0 / acc 2 | 1.26 | 1.49 |
| ratio acc 0 / acc 3 | 4.10 | 2.66 |
| wiring acc 2, acc 3 | 1.3e-19, 1.5e-19 | 4.8e-21, 1.7e-19 |
| control's rel D2 (acc 0, D 55 M 48, step 1) | 1.40e-24 | 1.46e-24 |

acc 0 reproduces step 1's numbers to all printed digits. Wiring passes. **By criterion 2 the terms dominate:** the ratio
is below 10 for both acc 2 and acc 3 in both blocks. With every sum of the series in quad-double the centre is still
4.7e4 times and the horizon 130 times the M 48 level.

The M 48 control (`probe/series_acc023_D55_M48.*`) passes, with acc 0 equal to step 1's:

| D 55 M 48 | centre | horizon |
|---|---|---|
| rel D2, acc 0 / acc 2 / acc 3 | 1.40e-24 / 1.22e-24 / 4.11e-25 | 1.46e-24 / 1.15e-24 / 6.64e-25 |
| wiring acc 2, acc 3 | 8.2e-25, 5.6e-25 | 1.7e-23, 1.1e-22 |

The quad-double sums gain the same small factors at M 48 (1.1 to 3.4) as at M 64. Their wiring at a single point (up to
1.7e-19 of max |M| for the M 64 horizon at acc 3) is far above the D2 noise. That part of the change is smooth in
lambda. It is the more accurate background (value) series entering the tangent, a fixed error of the background, not
the non-smooth one measured here.

### Step 1c: the horizon's tangent solves (criterion written before the run)

A measurement for the size of the fix, not a fix. acc 4 changes only the horizon series' tangent solves: the 2M x 2M
real form of (omega D + diag kappa_kk + lambda) is factored by multidouble 4.0.0's `QDLu` from the same double-double
entries, and the double-double right-hand sides are solved in quad-double and rounded once. Everything else is acc 0.
Run at D 55 M 64 (`--accs=0,4`). Reading for the horizon block: if rel D2 (acc 4) is at least 100 times below acc 0 and
within 10 times the M 48 level (1.46e-24), its error is made in the dd solves, and the horizon needs only a quad-double
solve, which multidouble 4.0.0 has. If the ratio is below 10, the solves are not the cause and the horizon needs its
terms in quad-double as well. Anything else is mixed. The centre block must not change (it has no solves): its acc 4
rel D2 must equal acc 0's, or the wiring is wrong and the run is not read.

### Step 1c result (01:58 UTC; `probe/series_acc4_D55_M64.*`)

| D 55 M 64 | centre | horizon |
|---|---|---|
| rel D2, acc 0 | 2.70e-19 | 5.08e-22 |
| rel D2, acc 4 (qd tangent solves only) | 2.70e-19 | 3.80e-22 |
| ratio | 1.00 | 1.34 |
| wiring | 0 | 1.1e-22 |

The centre is unchanged with wiring 0, so the run is read. The horizon's ratio is 1.34, so **the solves are not the
cause** either. The horizon needs its terms in quad-double as well.

## Verdict of step 1: the terms dominate

Neither the final sums (acc 1), nor every Cauchy product (acc 2), nor also D f (acc 3), nor the horizon's tangent
solves (acc 4) brings either block within 100 times of the M 48 level. The best is acc 3, at 4.1 times (centre) and 2.7
times (horizon). The centre's error is 65 to 87 times its storage floor at both M, so it scales with the size of the
series' terms. Those terms grow by 1.4e5 from M 48 to M 64 (T 1.8e6 to 2.5e11), and the noise by 1.9e5. Even exact sums
of the stored double-double coefficients leave the centre at the floor, 3.1e-21, which is 2200 times the M 48 level.
The horizon's error is 2e7 to 2e8 times its floor at both M, so it is made in double-double operations on intermediate
quantities larger than the Horner terms, and neither its sums nor its solves are the place. By the rule of #259 step 2
is not done.

## Production path unchanged (criterion written before the run)

`scripts/prod_identity.py` runs `mode_det` at D 55 M 48 at z (step 1's point) with the main checkout's build
(2026-11-08 16:26, sha256 3e485ab9...) and with this worktree's build. The four numbers must be bit-identical at z. The
control compares the main build's numbers at z with this build's at z + 2^-46, which must differ (the comparison can
see a change).

Result (`checks/identity_*`): bit-identical at z and at z + 2^-46, and the control differs. Pass.

## What the fix would take (not started)

The series' terms must be carried in quad-double, with the horizon solves in quad-double too. One part alone does not
help, as acc 4 shows.

- multidouble: a complex quad-double dual lane (quad-double value with a complex quad-double tangent, the twin of `Dc`
  as `Qu` is of `Du`). It needs the `Lane` and `MatLane` impls, the `Fl` helpers (`tan_re`, `tan_im`, `from_vri`, `val`)
  and tests against `Dc` and an mpmath reference. That is about 400 lines (the `Qu` lane is about 250) and an additive
  release, 4.1.0. A PR there first, by AGENTS.md.
- hp: the version bump to 4.1.0, the hpkernel rebuild on the Mac and on Windows, and the bit-identity checks
  (`highm_check.py ref`, `scaled`, `jets`), since modecount_cx builds against hpkernel's pinned multidouble.
- modecount_cx: the centre and horizon series, d/dtau, the horizon solves (multidouble 4.0.0's `QDLu`, ks + 1 factors
  per lambda) and the Horner sums on the new lane, with the inputs promoted and the outputs rounded to double-double.
  The Taylor segments stay double-double (they are at its rounding, #252). About 300 lines.
- Cost: acc 4's quad-double factors and solves alone took the series-only matrix from about 30 s to 51 s at M 64. acc
  3's per-term conversions took 435 s, but a lane with in-place accumulators should be well below that. A rough guess is
  5 to 10 times today's series cost, from about 2 min to 4 to 7 min per M 64 determinant.

## Runs and exits (`probe/exits.txt`, `checks/exits.txt`)

| run | exit |
|---|---|
| step 1, D 55 M 64 and M 48 (acc 0, 1) | 0, 0 |
| step 1b, D 55 M 64 and M 48 (acc 0, 2, 3) | 0, 0 |
| step 1c, D 55 M 64 (acc 0, 4) | 0 |
| production identity, main build and worktree build | 0, 0 |

Code: `wip/i259` of the main repository, commits 79e51cc, 41ef41d and f9aa838 (the diagnostic `CSolver.series_matrix`
and its modes; the production `mode_det`, `mode_matrix` and `test_*` paths unchanged).
