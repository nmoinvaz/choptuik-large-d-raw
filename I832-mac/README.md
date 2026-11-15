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

## Part 1: the real start (s0_D252, #823's dz0_truth.npz, 3 threads)

| run | result | exit |
|---|---|---|
| `curve_wd` (`--elim=1 --weak_delta=1 --g0_only=1`, 11:20-11:36 UTC) | sigma of B 4.62e-32 .. 1.26e-31 and **0.249** (the e_Delta direction); a's e_Delta part 1.11e-20, \|B a\| 2.76e-21; \|w0\| 2.17e-19. g(0)'s chord: first \|dw\| 2.25e-20 above its bound 1e-3 \|w0\|, stopped. max\|F\| on the eliminated rows 1.65e-20. **R1 FAIL, E1 FAIL** (`judge_curve_wd.log`) | 1 |
| `curve_wd_free` (`--weak_delta=1 --g0_only=1`, horizon data free) | \|w0\| 2.25e-19; first \|dw\| 2.86e-13, as #823's 2.76e-13; **R1 FAIL** (`judge_curve_wd_free.log`) | 1 |
| `diag_832` (11:40-12:04 UTC) | below | 0 |
| `judge_selftest` | judge_832.py's three planted records: pass, fail, fail | 0 |

**Why** (`diag_832.log`). In this chart w0's Delta part is 6.7e-115, so Delta does not move. Its blocks (max|.|) are
the centre 3.64e-20 and nodes 0-4 1.01e-20 to 1.66e-20. With the horizon data held:
- The centre part moves the held p rows by 3.58e-20. That is the start's residual, and the strong move is meant to
  remove it.
- The last node's part moves the horizon m rows by 1.65e-20. Every other block leaves the m and a rows alone.

**The m and a rows cannot be re-solved cheaply.** Re-solving them needs m_h to move by 1.65e-20 and a_h by 1.95e-23,
and the response along that correction is quadratic:
- The fast chord's one step from P(z0)'s block lands at max|F[hrows]| 4.89e-4, against 1.65e-20 before it. That is
  the even part of the response along the step, 4.894e-4 at eps 1, the same at eps 1e-3 and 1e-6.
- The production projection at P(z0) + w0 needed its ladder (459 s). The u0 rung from the point's own data and its
  quad-double polish both failed (|R| 6.2e6, then 5.1e-20 after 8 steps). The ladder's 7 rungs converged (4.6e-26),
  and 3 octo-double corrections took the rows to 7.25e-79.
- In (4) of the diagnostic, the "odd part / eps 1.144" is an artifact. It used only the leading double of the octo
  solve's dh, and a_h's gain of about 1e37 turns that truncation into an O(1) residual. The chord, which uses all eight
  parts, agrees with the even part.

**With the ladder's projection the first strong step works.** At the projected P(z0) + w0:
- the reduced residual's max is 4.1e-22, against 3.58e-20 at P(z0), so the held p rows' residual is removed;
- |U^T F_red| is 2.757e-21, 1.0 |B a|, so g is unchanged by the step;
- the eliminated rows read 7.25e-79.

The system with Delta weak and the horizon data eliminated is therefore not the obstruction. The obstruction is the
projection: m_h moves of 1e-20 lie far outside the u0 rung's Newton basin, about 1/G in m_h, which is HORIZON_RADIUS's
pole law in another unknown. Only the ladder follows them, at 459 s a projection.

## Discrepancies

1. delta_range's first run (`delta_range_dps15.log`) parsed D_str at 15 digits through pinned_o, #831's trap. Every
   I603 state then read 6e25 to 1e31 and none was resolved. The script now sets 60 digits, and #831's branch makes
   pinned_o parse at 60 digits whatever the caller's precision.
2. In the e_Delta chart, CurvePlanted's own ray (CURVE_T) is outside that plant's design: PC1 1.7. The planted check
   uses --plant_t 1e-12 .. 1e-8. Its PC2 (orders 4 and 5) belongs to CurvePlanted's own chart and is reported, not
   judged, in this chart.

## Recommended tasks

1. **g(0) with the ladder's projection at every residual.**
   - What: `curve ... --elim=1 --weak_delta=1 --elim_fast=0 --g0_only=1` at s0_D252.
   - Why: through the ladder, the first strong step lowers the reduced residual 100-fold with g unchanged.
   - Acceptance (can fail): R1 as here, the kept |dw| below 1e-40 |w0| from both starts; the log gives |dw| per step.
   - Estimate: about 460 s a projection, 10 to 20 projections, 1.5-3 h at 3 threads. Depends on #832.
2. **A projection that follows m_h moves of 1e-20 cheaply.**
   - What: the ladder warm-started from the last projected point's inner rungs, or Newton on the full system's m and
     a rows with their block refactored each step and a damped start.
   - Why: the fixed-block chord fails at P(z0) + w0, and the ladder takes 459 s.
   - Acceptance (can fail): at P(z0) + w0 it reproduces the ladder's horizon data (m_h 1.65e-20 and a_h 1.95e-23
     moved) to 1e-60 relative, in under 60 s; its control (the fixed block) fails as above.
   - Estimate: 2-3 h.
