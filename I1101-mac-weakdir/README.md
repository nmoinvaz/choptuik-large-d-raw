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

## Task A results so far (2026-11-27 22:25 UTC by the clock)

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
