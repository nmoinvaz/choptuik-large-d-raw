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
