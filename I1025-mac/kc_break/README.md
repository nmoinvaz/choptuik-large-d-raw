# I1025-mac/kc_break: where lambda_1's branch stops being k_c-stable, the k_c 55 and k_c 63 hybrid scans side by side at D 18.3125

Mac (Apple silicon, 10 cores), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written before the run, 2026-11-22 02:56:36 UTC.

## The coordinator's task (hc, 2026-11-22 about 02:55 UTC)

lambda_1's branch is k_c-stable through D 18.25 (k_c 55 minus k_c 63: 1.3e-4 at D 17.75, 9.4e-4 at 18.125, 1e-4 at 18.25; comments
7071508693, 7072529186, 7072669877). At D 18.5 it is not (k_c 55 has a complex pair near 1.684). Find where it breaks: D 18.3125.

## Run (`lane_kcb.sh`), the two k_c side by side, 4 BLAS threads each, nice 10, 8 h caps (timeout 28800 s)

| k_c | state | record line | blob (state, record) |
|---|---|---|---|
| 63 | `../d18/sol_l1kc63Wm1025_D18.312500.npy` (the leap) | `../d18/l1kc63Wm1025.jsonl`, D 18.3125: F 2.78658965e-10, 2496 steps | d8bbd43b, 08f4dbf3 |
| 55 | `../out/sol_l1kc55F1025_D18.312500.npy` | `../out/l1kc55F1025.jsonl`, D 18.3125: F 2.77055501e-10, 2179 steps | 3ee23e86, 0fb77df8 |

Each: `d18_hybsign.py REC STATE 18.3125 LAMS OUT` (blob e089207a), the system check first (exit 3 if the state does not rebuild its
record), **lambda 1.62 to 1.80 at 0.01 (19 points)**, the hybrid sign with the noise test (1e-15 on blocks 0-11, 2 seeds) and the float64
sign beside it. Solver code 505d8399 (worktree checked by the lane).

## Reading, fixed now (the coordinator's)

The k_c 55 root's det-linear estimate within 0.01 of the k_c 63 root's means **stable at D 18.3125**; no k_c 55 root there, or one further
off, means **it breaks by D 18.3125**. Report any ln|det| minimum without a sign change, with a dip fit.

Reader: `../d18/d18k2_read.py` (blob 52f31e53, unchanged; selftest 5 planted cases PASS, --mutate=tol and --mutate=dip FAIL,
`../d18/d18k2_read_selftest.log`). Its "k_c-stable there" is this reading's "stable at D 18.3125", and its "k_c-dependent at this D" is
"breaks by D 18.3125". Made exact (mine, as in (m)): the k_c 63 robust change against the nearest robust k_c 55 change by det-linear
estimate; a change touching a non-robust point gives no reading; if k_c 63 has no robust change in the window, no reading (the coordinator
rules); unmatched k_c 55 changes are listed. The dip fit, over the minimum and up to two points each side:
ln|det| = c + s (lambda - lambda_min) + ln|(lambda - a)^2 + beta|; beta > 0 a complex pair a +- i sqrt(beta), beta < 0 two real roots.
Orientations are listed in each state's own signs only (no sign convention across k_c).

## Started

lane_kcb.sh started 02:56:59 UTC. System checks passed: k_c 63 |F| 2.7865896510e-10, 2496 steps; k_c 55 |F| 2.7705550051e-10, 2179 steps,
each equal to its record.
