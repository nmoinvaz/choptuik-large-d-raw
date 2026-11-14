# I770-mac: winding counts of the D = infinity perturbation determinant of the axion-dilaton (kappa = 1) inner CSS

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/770
Code: `solver/matter/css_inner_pert.py` of choptuik-large-d. `count`, `root` and `det` from main 3e096e26, `check` from
wip/xf-kappa 7dc93151 (its kappa != 0 error metric, now on main), and `locate` from wip/xf-770 (queue 3: a first version
without a determinant cache, stopped; queues 4, 5: the version of commit 48a549f2). Notes: matter/CSS_STABILITY.md 1.6
on wip/xf-770 75f4b4ea.

| file | what |
|---|---|
| `pilot.sh`, `pilot.log` | the pilot: `check 1`, the secant roots from 2.1 and 1.1 at settings A, B, C, det M at conjugate points, box B at setting A |
| `check_k1.jsonl` | `css_inner_pert.py check 1` (PASS): exact modes' series, M singular at lambda = 0, 1, 2 |
| `roots_k1.jsonl` | lambda = 2 and 1 by secant at settings A, B, C |
| `conj_k1.jsonl` | det M at 1.3 +- 2.1i and 0.7 +- 6.5i, settings A and B (det M(conj lam) = conj det M(lam)) |
| `queue1.sh`, `queue1.log`, `counts_k1.jsonl` | winding counts of boxes A, B, S, C and the wide box W (0.05 < Re < 8, \|Im\| < 3 omega) at settings A and B |
| `controls_k1.jsonl` | box B with a zero planted at 3 + 1i, and with `--mutate=nometric` |
| `queue2.sh`, `queue2.log`, `diag_k1.jsonl` | the diagnostics of W (counted 0 with 6 starting samples per edge): the strip 5 < Re < 8 in two pieces, C and W with K = 24; queue 5's counts at setting B |
| `queue3.sh`, `queue3.log`, `strip_root_k1.jsonl` | a secant from the strip's centre (not converged), `locate`'s planted control (2.3 + 6.1i, found exactly at A and B), the first `locate` of the strip (stopped at 17:17, 4x slower without a cache) |
| `queue4.sh`, `queue4.log`, `locate_k1.jsonl` | `locate` of the strip's lower half: the zero 7.7410972542 + 3.7686870595i at settings A and C, not converged at B |
| `after4.sh`, `queue5.sh`, `queue5.log` | at setting B: the zero's box (0) and W with K = 24 (2) |

## Results (kappa = 1, omega_inf = 3.1998939020, eps = 1/4)

| box | region | expected | A | B | determinants (A, B) |
|---|---|---|---|---|---|
| A | 0.05 < Re < 0.9, \|Im\| < omega - eps | none | 0 | 0 | 124, 124 |
| B | 0.9 < Re < 5, \|Im\| < omega - eps | lambda = 1, 2 | 2 | 2 | 132, 132 |
| S | 0.05 < Re < 5, omega - eps < Im < omega + eps | none | 0 | 0 | 68, 68 |
| C | 0.05 < Re < 5, omega + eps < Im < 3 omega | none | 0 (K = 24: 0) | 0 | 52 (192), 52 |
| W, K = 6 | 0.05 < Re < 8, \|Im\| < 3 omega | lambda = 1, 2 | 0 (wrong) | 0 (wrong) | 344, 304 |
| W, K = 24 | the same | lambda = 1, 2 | 4 | 2 | 480, 408 |
| strip, lower | 5 < Re < 8, \|Im\| < omega - eps | | 0 | | 48 |
| strip, upper | 5 < Re < 8, omega - eps < Im < 3 omega | | 1 | | 66 |
| artefact box | 6.5 < Re < 8, 2.95 < Im < 4.61 | | 1 (locate) | 0 | |

| control (setting A) | result |
|---|---|
| zero planted at 3 + 1i, box B | 3 (from 2) |
| `--mutate=nometric`, box B | 1 (from 2) |
| `locate` with a zero planted at 2.3 + 6.1i | found exactly at A and B; M not singular there (1.4e-6) |

Exact modes: `check 1` PASS; secant lambda = 2 - 1.2e-12 / -8.2e-13 / -1.2e-12 and lambda = 1 + 6.7e-13 / -6.4e-13 /
+3.5e-13 at A / B / C; det M(conj lam) = conj det M(lam) to 2.0e-12.

The strip zero 7.7410972542 + 3.7686870595i: at A and C (r1 = 0.3) to 1.1e-13; at B (r1 = 0.25) the secant from it
does not converge and its box counts 0. An artefact of the jump at r1 = 0.3.

## Recommended tasks

1. Count with starting samples per edge scaled to the edge's length. What: `css_inner_pert.py count` and
   `complex_css.py boxes` start each edge at K = 6 samples whatever its length (`complex_css.py locate` at 4); make the default a sample per 0.25
   of edge, as #781's counter does. Why: on W (edges 7.95 and 19.2) the K = 6 count missed whole turns at both
   settings (0 against 4 and 2). Acceptance (can fail): the new default counts W at kappa = 1 as 4 (A) and 2 (B), the
   K = 6 count still gives 0 as the control, and every box quoted in matter/CSS_STABILITY.md and
   matter/COMPLEX_CRITICAL.md 2 recounts to its quoted number. Depends on: #770.
