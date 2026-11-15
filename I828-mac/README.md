# I828-mac: the reduced map at s0_D252's truth with the horizon data eliminated (D 252.6)

Machine: the Apple M5 Mac (`mac`), agent xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/828.

Code: branch `wip/xf-828` (from main 78687d7c), worktree /Users/nathan/Source/choptuik-large-d-828. Build: main
3c35f0c's hpkernel (i599/site2), as #816 and #823. One process, 3 threads, nice 10 (`run.sh`).

## The new solve

`reduced_cubic.py curve ... --elim=1` runs curve on the system with the horizon data eliminated (`Elim`). The
unknowns are the base system's but m_h and a_h (2M), and the rows its rows but the horizon block's m and a rows (2M,
rows 4MK+M .. 4MK+3M). F(p) is the base's residual on the other rows at z0 + p, after the horizon data have been
projected, i.e. solved from the m and a rows at fixed other unknowns. On a real start this is ElimO's projection,
Reseeder.project at the point's quad-double rounding followed by `--reseed_o` (3) octo-double corrections. The
reduced Jacobian is the Schur complement, so a solve is the full LU's solve of [r; 0] with the horizon unknowns
dropped, and a transposed solve is the full LU's transposed solve of [s; 0] with the m and a rows dropped. The start
is P(z0), and the LU is refactored there.

The plant (`HorizonPlanted`) is CurvePlanted with two horizon unknowns and two horizon rows inserted, gains 1 and
1e37. Its rows vanish, and its main rows reduce to CurvePlanted's, on the projected manifold. A term
E mu G^2 d h in the main rows, zero on the manifold, is what the full system's strong solve cannot follow.

## Plan and criteria (posted before the real run)

https://github.com/nmoinvaz/choptuik-large-d/issues/828#issuecomment-6891188413. Judged on the real start:

- **R1.** g(0)'s strong solve converges: curve's chord at c = 0 from w0 and from w0 (1 + 1e-5) keeps |dw| < 1e-40 |w0|.
  |g(0) - U^T F(P(z0))| is reported against |B a|.
- **R2.** #823's criterion, by `I823-mac/verdict_823.py`: per ray, a root within |c| <= 1e-4 (every component of g
  changes sign between neighbouring grid points), or none, or undecided.
- **E1.** The largest max|F| on the m and a rows over every projected point is below 1e-20 |B a|.
- **E2.** The reduced Newton step at P(z0) has a Delta part within 1e-3 of ElimO's +1.100878e-5 (#823's proj_shift).

## Runs

| run | result | exit |
|---|---|---|
| `curve_planted_regress` (`curve planted`, the unchanged path) | PC1 worst point error 1.3e-48, as on #823 | 0 |
| `curve_planted_elim` (`--elim=1`) | PC1 1.3e-48 (bound 1e-3), PC2-PC4 pass; the plant's manifold check 0.0 | 0 |
| `curve_planted_elim_w0` (`--mutate=w0`) | PC1 7.3e+56, PC2 FAIL | 1 |
| `curve_planted_elim_noelim` (`--mutate=noelim`) | g(0)'s chord NOT converged: \|dw\| 2.8e-8 against \|w0\| 7.21e-33 | 1 |
| `curve_planted_elim_hrows` (`--mutate=hrows`) | g(0)'s chord NOT converged: \|dw\| 1.6e+3 | 1 |
| `verdict_selftest`, `verdict_selftest_any` | `I823-mac/verdict_823.py --selftest` PASS; `--mutate=any` FAIL | 0, 1 |

The first four `curve planted` runs were first launched with the options as one argument (zsh does not split an
unquoted parameter), so they ran plain `curve planted`; they were run again with the options split, and these logs
are the second runs.
| `curve_elim_dps50` (07:39-07:57 UTC, killed) | reseed's import set mpmath to 50 digits, so P(z0)'s 1.7e-65 move of a_h was rounded to 0, the LU stayed at z0 (pivot 7.09e-29) and the reduced step was the unprojected +3.311085e-8; fixed in 77351cbe (curve now fails unless it ends at 140 digits) | killed |
| `curve_elim` (07:58-08:22 UTC) | below; R1 FAIL, E1 FAIL, E2 pass (`judge_curve_elim.log`) | 1 |
| `diag_828` (08:25-09:03 UTC) | w0 by block, the Delta scaling, the production projection at P(z0) + w0 (below) | 0 |
| `fit_delta` | s, c and s / c per horizon field; the third move predicted within 2 for all four | 0 |

## The real run (`curve_elim.log`)

The elimination at P(z0) agrees with #823's ElimO numbers:
- **P(z0).** `Reseeder.project` gave 'u0q' with 3 octo-double corrections (536 s), moving a_h by 1.7e-65 (#823: 1.697e-65). The full system's own m and a rows read 2.30e-80 there, the rung's residual. One chord step with their octo-double block LU took them to 3.08e-92.
- **The step.** The LU pivots at P(z0) are 7.29e-31..1.20e36 (#823: 7.287e-31). The reduced Newton step's Delta part is **+1.100878e-5**, so E2 passes.
- **The basis.** sigma of B is 4.62e-32..1.26e-31, |a| 1.365e-5 (a = 1.282e-5, 1.058e-6, 3.964e-6, 2.291e-6), |B a| 8.30e-37, |w0| 2.17e-19.

**g(0) is not defined with this solve either (R1 FAIL).** At P(z0) + w0 the fast projection left max|F| on the m and a rows at **5.05e14**, and the chord on them did not lower it (E1 FAIL). The reduced residual there is garbage. The chord's first |dw| is 2.1e15, against its bound 1e-40 |w0| = 2.17e-59, and |g(0) - U^T F(P(z0))| is 2.0e51 |B a|. `diag_828.py` follows.

## Why g(0) is not defined: the horizon rows' dependence on Delta (`diag_828.log`, 08:25-09:03 UTC)

`diag_828.py` rebuilt the same system and basis (the same |a|, |B a| and |w0|). It then took three readings:
- w0 by unknown block;
- the full residual at P(z0) + w0 with the horizon data held, for w0 and for each of its blocks alone;
- reseed's production projection at P(z0) + w0.

| move, horizon data held | max\|.\| of the move | change of max\|F\| on the horizon p, m, a, 4th rows |
|---|---|---|
| w0 | 3.6e-20 | 8.11e14, 1.07e14, 5.05e14, 5.24e11 |
| w0's centre part alone | 3.6e-20 | p 3.58e-20, the others 0 |
| one node block of w0 alone | at most 1.6e-20 | at most 1.64e-20 (node 4) |
| w0's Delta part alone | 1.48e-22 | 8.11e14, 1.07e14, 5.05e14, 5.24e11 |
| 1e-3 of it | 1.48e-25 | 8.24e8, 1.22e8, 5.39e8, 1.27e8 |
| 1e-6 of it | 1.48e-28 | 1.46e4, 1.52e4, 6.30e4, 1.26e5 |

**Delta alone moves the horizon rows, and they are linear in it only below about 1e-26.** `fit_delta.py` fits
f = s d + c d^2 through the first two Delta moves and predicts the third within a factor 2 for every field
(`fit_delta.log`; max norms over each field's rows, so the numbers are scales, not one row's derivatives):

| horizon field | s | c | s / c |
|---|---|---|---|
| p | 8.79e31 | 3.70e58 | 2.37e-27 |
| m | 1.01e32 | 4.88e57 | 2.08e-26 |
| a | 2.30e32 | 2.31e58 | 9.98e-27 |
| 4th | 8.55e32 | 1.81e55 | 4.71e-23 |

**No horizon data solve the m and a rows at P(z0) + w0.** Both projections fail there:
- The fast chord went from 5.05e14 to nan in one step.
- The production projection failed after 606 s at every stage:

| stage | its | max\|R\| start, end |
|---|---|---|
| u0 rung, double-double | 1 | 5.05e14, 5.05e14 |
| u0 rung, quad-double polish | 8 | 5.05e14, 1.23e11 |
| ladder, 7 rungs (the last at u 0.3, quad-double) | 9 | 1.74e7, 2.84e-5 |

So the reduced map is not defined at c = 0 with this solve either. The strong correction w0 is the reduced system's own
Newton correction of its strong rows. Its Delta part, 1.48e-22, lies past the horizon block's linear range in Delta
for every field, and the horizon data cannot follow it. The horizon data's freedom, which the elimination removes, is
not what breaks the strong solve.

## Reading (inferred, not shown)

- With the horizon data free (#823) the same w0, of the same size, took max|F| to 8.6e-4. Eliminating the data removes
  their freedom, but not the dependence of the horizon rows on Delta, which is the larger term.
- The slope of about 1e32 and the curvature of about 1e58 fit a horizon series summed near its radius of convergence.
  reseed's docstring places a pole inside u0 past D ~ 249. I have not checked this against the series' radius
  (recommended task 2).

## Discrepancies

1. reseed.py sets mpmath's precision to 50 digits when imported. Every later 140-digit computation in reduced_cubic
   then ran at 50 digits, so P(z0)'s 1.7e-65 move of a_h was rounded to 0 (`curve_elim_dps50.log`, discarded). It is
   fixed for reduced_cubic in 77351cbe. The plant did not catch it, because the plant does not import reseed. Other
   importers of reseed are unaudited (recommended task 3).
2. Real's stored-step check (-J^-1 F(z0) against dz0) read 3.62e-35 in a probe run without OPENBLAS_NUM_THREADS=1. It
   read 3.12e-89 under run.sh, as on #823, with the same build, files and code. Both pass the bound 1e-20, but some step
   of the octo-double path goes through multithreaded BLAS (recommended task 4).

## Recommended tasks

1. **A chart whose strong coordinates exclude Delta.**
   - What: reduced_cubic's strong solve with e_Delta added to the weak directions (V and U each gain one vector, g
     gains one component), or Delta held in the bordered solve, with the horizon data eliminated as here.
   - Why: at fixed Delta the centre and node parts of w0 move the horizon rows by at most 3.6e-20, while its Delta
     part, 1.48e-22, takes them to 8e14 (`diag_828.log`).
   - Acceptance (can fail): a plant with a Delta-like unknown whose rows are as nonlinear as fit_delta's passes, and
     --mutate=w0 fails. At s0_D252, g(0)'s strong solve converges (|dw| < 1e-40 |w0|), or the log names the step where
     it fails.
   - Depends on #828. Estimate: the code first, then about 1 h at 3 threads.
2. **The horizon rows' linear range in Delta along the chain.**
   - What: diag_828's Delta scaling and fit_delta at D 200, 230, 245.6 and 252.6 (states of I603-win2), with the
     horizon series' radius against u0 at each (horizon_radius.py).
   - Why: a linear range of 2.4e-27 in Delta at D 252.6 would explain why Newton's Delta steps there leave the
     horizon block's domain, if it shrinks with D as the radius nears u0.
   - Acceptance (can fail): s / c per D and field, with fit_delta's own check (the third move within a factor 2);
     a trend against the radius, or none.
   - Depends on #828. Estimate: about 30 min per D at 3 threads.
3. **reseed's module-level precision.**
   - What: move reseed.py's `mp.mp.dps = 50` into its command-line functions, and audit its importers for mpmath
     arithmetic after the import (anm_run, octo_corrector, proj_shift, chain_dM, crawl_probe, horizon_radius,
     eq_test, reseed_check).
   - Acceptance (can fail): a check that imports each module and asserts the precision is unchanged; it fails on
     main.
   - Estimate: 1 h.
4. **BLAS threads in the octo-double path.**
   - What: find which call in Real's construction or solve uses multithreaded OpenBLAS.
   - Why: the stored-step check read 3.62e-35 with it and 3.12e-89 without it (discrepancy 2), which bears on #827's
     question.
   - Acceptance (can fail): the check twice in each setting, the same bits within a setting; then the call named.
   - Estimate: 1 h.
