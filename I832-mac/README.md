# I832-mac: the horizon rows' linear range in Delta against D, and the chart with e_Delta weak (D 200-253.7)

Machine: the Apple M5 Mac (`mac`), agent xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/832.

Code: branch `wip/xf-832` from main 75f94140, 12af59c5 (`hp/delta_range.py`) and d89143c9 (`reduced_cubic.py curve
--weak_delta`). Build: main 3c35f0c's hpkernel (i599/site2). 3 threads, nice 10 (`run.sh`).

## Part 2: the linear range in Delta (`delta_range.log`, `delta_range.csv`, `rate_832.log`)

- **The estimator.** Per state, the pinned system is built as octo_corrector.pinned_o builds it. The octo-double
  residual is evaluated at z +- d e_Delta, d = 1e-16 .. 1e-36, with the horizon data held. Per horizon field (p, m, a,
  4th), the odd part / 2d is S and the even part / 2d^2 is C, max norms over the field's M rows.
- **The range.** r = S/C at the smallest d, the move where the linear and quadratic terms are equal.
- **The resolution check.** A field is resolved when S and C at the two smallest d agree within 10%. The state's r is
  the smallest over its resolved fields.
- **The selftest** (`delta_range_selftest.log`) recovers the planted s 1e32 and c 1e58 within 1e-3, and flags a cubic
  above s as not resolved. Its control `--mutate=evenone` fails (`delta_range_selftest_evenone.log`).

| D | 200.0 | 210.5 | 215.0 | 226.13 | 230.13 | 234.13 | 237.76 | 241.96 | 245.64 | 248.02 | 249.87 | 251.30 | 252.61 | 253.73 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r | 1.76e-24 | 3.29e-25 | 1.70e-25 | 3.87e-26 | 2.39e-26 | 1.52e-26 | 1.03e-26 | 6.71e-27 | 4.72e-27 | 3.79e-27 | 3.21e-27 | 2.84e-27 | 2.54e-27 | 2.31e-27 |

States: I215-win/chain_d6 (200.0), I215-win/chain_d10 (210.5), I19-win2/crawl (215.0), I603-win2/chain (the rest);
every one is a solution of its pinned system (max|F| 1.7e-34 to 5.5e-20).

**ln r falls by 0.119 per unit of D over the 14 states.** It is 0.142 at D <= 230 and 0.088 at D >= 245, and the
neighbour rates fall smoothly from 0.160 to 0.083 (`rate_832.log`). That is against #805's 1.44, the weak pivot's
rate, and 0.34, 13.6's pole law for a_h (notes/HORIZON_RADIUS.md). The range shrinks more slowly toward the front
and does not track the weak pivot. At 252.61 it is 2.54e-27, consistent with #828's three-point fit of
2.37e-27 (p rows) at P(z0).

`delta_range_dps15.log` is the first run. It parsed D_str at mpmath's default 15 digits: on main before #831,
pinned_o parses at the caller's precision. So every state with a long D_str read max|F| of 6e25 to 1e31, and was not
resolved. The script now sets 60 digits.

## Part 1: the chart with e_Delta among the weak directions

**The plant** (`curve_planted_wd*.log`). Its truth is `chart_truth`, an independent Newton solve of the chart's
square system at 400 digits.

| run | result | exit |
|---|---|---|
| `curve_planted_wd` (`--elim=1 --weak_delta=1 --plant_t=1e-12,...,1e-8`) | PC1 worst point error 1.0e-55 (bound 1e-3), every solve converged; PC2's orders reported only | 0 |
| `curve_planted_wd_w0` (`--mutate=w0`) | PC1 5.0e+41 | 1 |
| `curve_planted_regress` (plain `curve planted`) | 1.3e-48, as before | 0 |
| `curve_planted_wd_curvet` (on CURVE_T, before `--plant_t`) | PC1 1.7: CurvePlanted's rows 0-3 turn nonlinear above \|x\| 1e-7, which this chart's ray reaches at t ~ 1e-7 | 1 |
| `curve_planted_wd_p2` (`--plant_t`, before the predictor's linear term) | the rays stop at 1e-10: w - w0 is linear in t in this chart, and the quadratic predictor missed by 10 t | 1 |

The real runs follow.
