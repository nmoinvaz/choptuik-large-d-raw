# I1101-mac-weakdir: the weak direction of the l = 1 system and the order of its RK step error, at k_c 55, D 16

Machine `mac` (Nathan's MacBook, Apple silicon, 10 cores, 32 GB, macOS, Accelerate BLAS), a research subagent of the
coordinator t5. Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1105 (task A) and
https://github.com/nmoinvaz/choptuik-large-d/issues/1101 (task B). Written 2026-11-27 21:40 UTC by the clock.

Code: branch `wip/i1101-weakdir` of choptuik-large-d (from `wip/i1105-u0` at 5b1e38e8), script
`solver/matter/i1101_weakdir.py`; the root scanner `d18_secant.py` of `wip/ell1-kappa-mm` at f56f91d2 (default block
12 `ddm`, no Rust build on this Mac). Python `~/venv-1025dd` (numpy 2.5.4, scipy 1.18.1, multidouble with dd_logdet).
At most 2 processes, 1-2 BLAS threads each, nice 10.

Inputs (blob-checked, `git hash-object --no-filters`), all D 16.0, k_c 55, kappa 0.7, u0 0.04, Ks 30, 2565 steps:

| name | state | blob | record | blob |
|---|---|---|---|---|
| src (continuation) | `I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy` | 94c8b048 | `I1025-mac/out/l1kc55Fb1025.jsonl` | 5be40af4 |
| U40 | `I1105-dh170/step1b/sol_l1kc55u040_D16.0000.npy` | 491eb1e4 | `l1kc55u040.jsonl` | 12a42fc8 |
| U40b | `I1105-dh170/step1c/sol_l1kc55u040b_D16.0000.npy` | 78af2111 | `l1kc55u040b.jsonl` | 15d999a9 |
| U40c | `I1105-dh170/step1c/sol_l1kc55u040c_D16.0000.npy` | 898360c0 | `l1kc55u040c.jsonl` | 4a9c9182 |

All four rebuild as the record system on this Mac (|F| within 1e-2 relative, 2565 steps), and their per-segment step
maps from `freeze_from(z, 0.7)` are identical, so the four are approximate zeros of one discrete system.

## Task A (#1105): the weak direction (files only)

**Disclosure.** Before this README was written I ran an exploratory scratch SVD of the source's Jacobian (87 s) and
projected the three differences on it. What it showed (to be reproduced by the committed script, with the checks
below): 52 singular values below 3e-12 of the largest, a pair at 1.5e-10 and 4.7e-10, a pair at 1.3e-7, then 4.4e-4
and up; the three differences lie in the last four (the 1.5e-10 to 1.3e-7 band); and the residual 1.785e-10 sits in
the left vectors of the 1.5e-10 / 4.7e-10 pair at all four states. The checks and readings below are written after
that look, before the committed script runs.

Checks (each can fail, with a control that must fail):
1. **Planted projection.** On the source's SVD, a planted difference dz = a v_i + b v_j + e w (v_i, v_j two named
   right singular vectors of the weak band, w a unit vector of the strong band, known a, b, e) is recovered:
   coordinates to 1e-10 relative of |dz|, and the weak-band fraction equals sqrt(a^2 + b^2)/|dz| to 1e-10. Control
   (`--mutate=basis`): the projection on the left vectors U instead of V must fail it.
2. **Tau translation.** The generator g (harmonic k of every field rotated by i k, Delta 0) satisfies
   |J_mis g| <= 1e-6 |J| |g| on the mismatch rows (the discrete system is translation covariant up to aliasing), and
   the phase row gives J g = Re d_1. Control (`--mutate=gsign`, the odd fields rotated by -i k): |J_mis g| >= 1e-3
   |J| |g|. Then reported: g's fraction in each band of the spectrum.
3. **Nonlinear valley.** Moving the source along the weakest vector by t (t = 1e-6 to 1e-2) changes |F| by about
   s t, while the same t along a strong vector changes it by about 1e-2 t or more. Reported as measured.

Readings, written before the committed run:
- a difference is "in the weak band" if its fraction in the span of the band's right vectors is at least 0.99.
- the root's sensitivity to each weak vector (from the hybrid determinant at two lambda about the root, if run) is
  compared with the three measured root differences; "explained" means within 30% for each.

## Task B (#1101): the order of the RK step error at k_c 55, D 16

Runs, from U40's state (491eb1e4), in this Mac's worktree of `wip/i1101-weakdir` (`ell_refine.py` as on
`wip/i1105-u0`), one re-solve at a time (2 BLAS threads, nice 10), each then rooted:

```
K35  ell_refine.py l1kc55u040 55 l1kc55k035m 55 1 16 2.2426280416106374 --kappa 0.35 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
K50  ell_refine.py l1kc55u040 55 l1kc55k050m 55 1 16 2.2426280416106374 --kappa 0.5  --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
K25  ell_refine.py l1kc55u040 55 l1kc55k025m 55 1 16 2.2426280416106374 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
K70  ell_refine.py l1kc55u040 55 l1kc55k070m 55 1 16 2.2426280416106374 --kappa 0.7  --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
root d18_secant.py run REC STATE 16 LO HI OUT --tol=1e-7 --maxev=20 --pin=STATE,REC   (block 12 ddm, 1 thread)
```

The first `freeze_from` on U40 gives 2565, 3590, 5124 and 7173 steps at kappa 0.7, 0.5, 0.35 and 0.25. The bracket
of each root starts at (2.238, 2.252); a refused bracket is widened by 0.01 on the side the signs give, once per side,
and said so. Cap per re-solve 4 h.

**Bars, written before the runs.**
1. Each re-solve: |F| <= 5e-10, steps within 2% of 2565 x 0.7/kappa (K70: exactly 2565).
2. Control: |root(K70) - root(U40)| <= 3e-4 (twice the 1.7e-4 range of #1105 step 1c), with root(U40) = 2.2449017148
   (dh170, Rust block 12). Also: U40 rooted here, as the scanner's control on this Mac, within 1e-6 of 2.2449017148.
3. Readable: the order is read only if |root(K25) - root(K70)| >= 3e-3 (10 x the control bar).
4. Order: p from the least-squares fit root = r0 + A kappa^p over K70, K50, K35, K25. p >= 3.5: RK4's order holds at
   k_c 55, D 16; p <= 2.8: the reduced order of k_c 127 (#1101, p about 2 to 2.8) is reproduced here; between: mixed.
   Also reported: the two three-point ratios and the p each gives.
5. Which segment: from the residual changes of a fixed state when one segment's steps are refined at a time
   (kappa 0.7 to 0.35, 0.175, 0.0875 on that segment only), each segment's RK error and its order. A segment whose
   error has order <= 3 is named a cause of the order reduction.

Predictions (mine, before the runs): bar 1 passes for all four (85%); the control within 3e-4 (60%); readable (70%);
p >= 3.5 (40%), p <= 2.8 (35%), mixed (25%).

## Task A results so far (2026-11-27 22:20 UTC by the clock)

Code `i1101_weakdir.py` at 1d018e31 of `wip/i1101-weakdir` (blob ed6003c1). Logs in `A/`: `jac/` (J of src and U40,
87 s each; J and the SVD, 104 MB each, are not stored: `jac` and `svd` rebuild them), `report_src.log`/`.json` (the
report on src's SVD, with planted states), `report_src_swap.*` (its `--mutate=swap` control), `planted*.log`,
`floor_u40.log`, `valley_u40_refreeze.log` (the states `valley/sol_w*_D16.0000.npy` and their stubs, record-consistent),
`valley_u40.log` (a first run without re-frozen steps; its `sol_v*` states do not rebuild as their own record system),
`locate*.log` (float64 determinant signs).

- Spectrum of J at src: 52 values below 2.5e-12 s_max (the null band); a pair at 1.50e-10 and 4.67e-10 (v52, v53); a
  pair at 1.316e-7 and 1.321e-7 (v54, v55); then 4.40e-4 and up.
- U40 - src, U40b - src, U40c - src lie in the four weak vectors to 0.9999994 or more.
- |F| 1.785e-10 at every state is 1.785e-10 in the weak band (null 5.6e-12, strong 4e-13 to 9e-13); on the pair
  U_w^T F = (+1.116e-10, -1.392e-10) at all four states, with rounding noise 1e-14 to 5e-14.
- Checks: planted projection PASS (control `--mutate=basis` FAIL as it must). Tau translation: |J_mis g|/(s_max |g|)
  5.9e-11 (control 9.7e-3). Gauge h = 1: 2.6e-8 (control 2.2e-3); h = cos, sin 2 w tau: 2.3e-6, 2.5e-6 against the
  1e-6 bar: FAIL, with 4.6e-5 of the generator's node-state norm above k_c (cut by the layout). Single plants of 1e-3
  along v52, v53: FAIL the 1% bar (11% and 6%). Pairs +-eps (added after that failure): v53 0.63% PASS; v52 5.0% at
  1e-3 and 1.3% at 3e-3 FAIL, falling as 1/eps (the noise of U^T F); control `--mutate=swap` FAIL as it must.

## Task A: roots along the valley (written before the runs, 2026-11-27 22:22 UTC by the clock)

Runs, one at a time beside task B (`d18_secant.py run` of f56f91d2, block 12 ddm, 1 thread, tol 1e-7, maxev 20, pins):
U40 on (2.238, 2.252) (also task B's scanner control, bar 2), then the valley states w10 (t = 0.1, Delta +6.05e-3)
on (2.246, 2.266) and w001 (t = 0.001, Delta +6.05e-5) on (2.238, 2.256); the brackets follow the float64 sign
changes of `locate2.log`. A refused bracket is widened once by 0.01 on the side the signs give, and said so.

Reading, with the root scatter of U40, U40b, U40c (range 1.7e-4, #1105 step 1c) as the yardstick:
- |root(w10) - root(U40)| >= 1e-3: the root moves along the valley by more than 5x the scatter, so a stored state's
  root carries where the solver path left it along the pair, not only the system.
- <= 3e-4: the root is insensitive along the valley at the scatter level.
- between: reported as measured. w001 gives the slope near U40 (linear in t if the root is smooth along it).

## Task A: can the pair be pinned? (written before the run)

Before U40's root in the same queue: `i1101_weakdir.py ne` from U40 (nonlinear elimination: per outer step a fresh J
and SVD, the Gauss-Newton step on the pair at fractions 1 to 1/8 with re-frozen RK steps and chord steps on the strong
band; at most 6 outer steps; stops when one cuts |U_w^T F| by less than 2x). Reading:
- |U_w^T F| <= 1e-12 with |F| <= 1.5e-11: the discrete zero along the pair is reachable, so the pair can be pinned by
  solving; its Delta is reported against U40's.
- the run stops with |U_w^T F| >= 5e-11: not reachable this way (the valley bends away), reported as measured.
- between: reported as measured.

## Amendment, 2026-11-27 22:30 UTC by the clock (before the runs it changes)

K35's root (started 22:20 with block 12 ddm, 1 thread) takes 571 s per evaluation (528 s in block 12; the horizon
segment has 1356 steps), so the queue would take about 8 h. For the roots not yet started (U40, K50, K25, K70, w10,
w001): block 12 `--b12=fast` (ell_fastdd, the same double-double block to 4e-25 per d18_secant's docstring) and 2 BLAS
threads; tol 1e-6 for K50, K25, K70, w10 and w001 (the order bar reads differences of 3e-3 and up), 1e-7 for U40 (the
scanner control, bar 2). K35's root keeps its settings. Bars unchanged.
Further amendment, 22:31 UTC by the clock: K35's ddm root was stopped after its first evaluation (kept as
`B/root_l1kc55k035m_ddm_stopped.*`) and restarted with the amended settings (fast block 12, 2 threads, tol 1e-6).

## Results so far, 2026-11-27 23:17 UTC by the clock

**Pinning test (`A/ne_u40.log`, state `A/ne/sol_ne1_D16.0000.npy`).** One outer step from U40: the full Gauss-Newton
step on the pair diverges in the chord steps (|F| 1.7e-6); half of it gives |F| 1.155e-10 with Delta 1.032106 (+0.0304
from U40), its own 2603-step map. At that state the pair is weaker (s/s_max 3.3e-10, 7.5e-11) and the next
Gauss-Newton step is larger (|dz| 0.147, dDelta +0.095). The run stopped by its rule (|U_w^T F| 1.785e-10 -> 1.150e-10,
less than 2x). Reading: not reachable this way; and a state 0.03 above U40 in Delta has a lower |F|.

**Task B re-solves** (`B/`, from U40, `ell_refine.py` 631e5801, 2 threads):

| run | kappa | steps | \|F\| | Delta | Delta - U40 | constraint | lam_gauge | s | state blob |
|---|---|---|---|---|---|---|---|---|---|
| K70 | 0.7 | 2565 | 1.7833e-10 | 1.001713404637 | -2.21e-8 | 1.84828e-4 | 0.83497762 | 770 | f3b84ff6 |
| K50 | 0.5 | 3590 | 1.8650e-10 | 1.001713422184 | -4.54e-9 | 1.84390e-4 | 0.83497782 | 762 | 2e3aa01c |
| K35 | 0.35 | 5124 | 1.8869e-10 | 1.001713421050 | -5.67e-9 | 1.84270e-4 | 0.83497783 | 1432 | 9a05efa5 |
| K25 | 0.25 | 7173 | 1.8936e-10 | 1.001713420785 | -5.94e-9 | 1.84241e-4 | 0.83497783 | 2183 | 80dce58c |

Bar 1 passes for all four. K35's root (`B/root_l1kc55k035m.*`, fast block, 2 threads, tol 1e-6): status nonrobust
(its 8th point, at 2.2489674, has dln 0.43), robust bracket [2.2489585, 2.2496560] with opposite signs, det-linear
2.2489667.

## Task B: which segments move the root (written before the runs, 2026-11-27 23:26 UTC by the clock)

Seen before writing this (`A/coords_all.log`, `B/root_*`): K50, K35 and K25 keep U40's four weak coordinates to 1e-10
(they differ from U40 in the strong band only), K70 moved along the pair (c53 +8.3e-7 from U40's). The roots so far
are U40 2.2449017 (dh170), K50 2.24189 (bracket [2.24188, 2.24208]) and K35 2.24897 ([2.24896, 2.24966]): not
monotonic in kappa.

Queue `q3.sh`, after K70's root, 2 threads: `segerr` on U40 (each segment refined alone, kappa 0.7 down to 0.04375,
its block's mismatch change and local order, and U_w^T of the change); then chord re-solves of U40 (`chord`, strong
band of src's SVD) on four maps, each rooted (`root`, fast block 12, tol 1e-5, bracket (2.238, 2.252)): every segment
at kappa 0.35 (`all`), blocks 0-5 (x < 0.3, `inner`), 6-9 (0.3-0.7, `middle`), 10-12 (0.7 to the horizon, `outer`),
the others at 0.7.

Bars:
1. Control: |root(all) - root(K35)| <= 3e-4 (the chord re-solve stands in for ell_refine's LM). Otherwise the group
   roots are reported but not attributed.
2. Additivity: |sum of the three group shifts - shift(all)| <= 0.3 |shift(all)| + 3e-4 (shift = root - root(U40 here)).
3. A group whose shift is at least half of shift(all), with the same sign, is named as carrying it.

## Roots so far, and one more (written 2026-11-28 00:09 UTC by the clock)

| state | role | root (det-linear) | status | root - root(U40 here) |
|---|---|---|---|---|
| U40 | scanner control (bar 2: within 1e-6 of dh170's 2.2449017148) | 2.2449011058 | tol 1e-7 | 0 (-6.1e-7 against dh170: bar 2 passes) |
| w001 | valley t = 0.001, Delta +6.05e-5, \|F\| 1.785e-10 | 2.2450806634 | tol 1e-6 | +1.796e-4 |
| w10 | valley t = 0.1, Delta +6.05e-3, \|F\| 1.622e-10 | 2.2585867830 | tol 1e-6 | +1.3686e-2 |
| K50 | kappa 0.5 | 2.2418938 (bracket 2.2418807-2.2420845) | nonrobust | -3.0e-3 |
| K35 | kappa 0.35 | 2.2489667 (bracket 2.2489585-2.2496560) | nonrobust | +4.07e-3 |
| K25 | kappa 0.25 | 2.2429520 | tol 1e-6 | -1.95e-3 |

Valley reading (rules above): |root(w10) - root(U40)| = 1.37e-2 >= 1e-3, so the root moves along the pair by 80 times
the 1.7e-4 re-solve scatter. Added now, before it runs (`q4.sh`, after K70's root): the root of the pinning test's
state ne1 (Delta +0.0304, \|F\| 1.155e-10, its own 2603-step map) on (2.24, 2.40), tol 1e-5, reported as measured.
