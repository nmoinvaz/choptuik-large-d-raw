# I903-mac-grip: the grip on Δ at the fixed-order chains' bases (orders 142 and 160), at the own order and at ks 200

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/903 (the
coordinator's comment of 2026-11-16 15:43 UTC). xfkappa's chain writes I903-mac, so this measurement has its own folder.

Code: wip/xf-902 at 5e8b08db (`near_null.py --ks`, #902's method), on main 3c35f0c's hpkernel (i599/site2), the build
xfkappa's order-142 chain runs on. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`).
`state.sh TAG STATE` reads a state from choptuik-large-d-raw's origin/main into a separate inputs root (git show, so no
checkout changes), records its blob in `inputs.txt`, runs `near_null.py` at the state's own order and at ks 200, and
then `lift.py` over the folder (`lift.log`).

States: the order-142 chain's bases (xfkappa, I903-mac/chain_fixed, tag k142) and the order-160 chain's from D 200
(dh610, I903-dh610/chain_k160, tag k160; the coordinator's change of 2026-11-16, from a planned order-140 chain), for each target T = 230, 240, 245, 250 and 255 the first stored base with D ≥ T − 1,
as they land. The control is #902's D 60 state, I611-win/kf13_D60_D60.001952.npz (tag ctl, ks 142 and 200). dh610's chain runs on #911's
build (its README), and these readings of its states use the build above; #911's checks found the paths both use
bit-identical to the stored references.

## Method

#902's: at the stored z, with no Newton step, g = 1/‖e_Δᵀ J⁻¹‖₂ from one transpose solve, σ₁–σ₆ by subspace
iteration (`--its=32`, since 16 left a close pair unseparated in #902's C1), the rows check at ks 200 (only the horizon
block may change), and Δ's pinned Newton step printed, not applied.

## Criteria (posted on #903 before the runs)

The reading per base is the lift L = ln g(200) − ln g(own).

| # | criterion | fails when |
| --- | --- | --- |
| G1 | every run's near_null check passes (σ₁ converged to 1e-3, ‖J v₁‖ / σ₁ within 1e-2, z unchanged), and at ks 200 only the horizon block's rows of F and J change, F's there nonzero | a run's check fails, or another block changes |
| G2 | at the first base, `--ks 200 --mutate=ks` (built at the own order) equals the own-order run bit for bit; `lift.py --selftest` passes (planted: a lift of 1 reads small, 5 large; a failed run, a mutation one ulp off and a control off by 0.1 fail) | the override's path changes the system, or a planted case is misread |
| G3 | control, D 60: \|L\| and \|ln σᵢ(200) − ln σᵢ(142)\|, i = 1–4, below 0.05 | either reaches 0.05 |
| R | the coordinator's bar, at each chain's base near D 255: L < ln 10 says the chain's order (142, 160) leaves little of the cut, and the fixed-order fold test is a fair test of it; L ≥ ln 10 says it leaves a large part, and the fold could stay at that order and still move at a higher one | (the reading) |

Reported at every base: L, σ₁–σ₄ at both orders, the Δ mode followed by overlap, Δ's pinned step at ks 200, and the
horizon rows' max|ΔF|.

## Runs

`queue1.sh` ran the D 60 control (15:48–18:32 UTC) and then the order-142 chain's first base past D 229, with the
mutation control (18:42–19:57 UTC). `drive.sh` then runs one pending target of `targets.txt` at a time, in its order,
as each lands, and records it in `done.txt`. `lift.log` is rewritten after every base.

| chain | base D | ln g(own) | ln g(200) | L | Δ mode σ, own → 200 | 1/g² at own: largest share | at 200 | checks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ctl (D 60) | 60.0020 | −19.4641 | −19.4641 | +0.0000 | – | – | – | G3 pass (0.00e+00) |
| k142 | 229.1312 | −35.4817 | −31.6410 | +3.8407 | σ₃ 8.139e-15 → σ₁ 1.707e-14 (ln +0.741) | σ₂ (k3) 0.970 | σ₁ (k1) 0.993 | G1, G2 pass |
| k160 | 229.0000 | −34.1970 | −31.8111 | +2.3859 | σ₃ 1.179e-14 → σ₁ 1.392e-14 (ln +0.166) | σ₂ (k3) 0.873 | σ₁ (k1) 0.986 | G1 pass |

At D 229.13 the order-142 chain's weakest modes are the harmonic-3 pair (σ₁, σ₂ 1.497e-17, 1.515e-17), below the Δ
mode (σ₃ 8.139e-15), and their small Δ shares carry 0.970 and 0.027 of 1/g² (`lift.log`): the grip on Δ at order 142 is the
harmonic-3 pair's. At ks 200 the pair rises to 2.6e-10 and the Δ mode carries 0.993 of 1/g²; the Δ mode itself moved
by ln +0.741 of the lift's +3.8407.

## The p_min question (t5, 2026-11-17 02:20 UTC)

dh610's order-160 chain has p_min, the smallest LU pivot at its bases, falling 12 to 18 times per unit D from D 228
(1.5 before). Is that the wall's weak direction arriving (order 135's at that D, and order 130's near D 250) or a new
direction from the series at order 160?

### Runs

`queue2.sh` runs the lines of `q2.txt` one at a time (`one.sh`: near_null.py as above, six vectors saved). It covers
dh610's bases D 227 to 231 at their order 160, macm3's order-135 bases D 227.13 to 231.13 at order 135, and the order-160
state at D 229 summed to ks 200 (the same z). `pmin_cmp.py` compares the vectors. `series_order.py` reads where each
vector lives by horizon-series order.

### Criteria (written before the results)

- Same direction as order 135's weak direction: `|v₁(160) · v|` ≥ 0.9 for an order-135 vector v at the same D, and the
  same identity, meaning Δ share and top harmonic. New direction: no order-135 vector above 0.5. Calibration: the
  overlap of order 160's v₁ at D d with D d − 1, and of order 135's Δ mode at d with d − 1.
- The series' own: at D 229 the vector's σ at ks 200 on the same z is above 100 σ(160), or its top-tenth share by
  series order is above 0.5 (`series_order.py`, written before the runs: above 0.5 top orders, below 0.01 not). The
  wall's: σ at ks 200 within a factor 3 of σ(160), and the top-tenth share below 0.01.
- Checks: every near_null run passes its check (σ₁ converged, ‖J v₁‖/σ₁ within 1e-2), and at ks 200 only the horizon
  rows change. `series_order.py`'s linearity check passes, and its control `--mutate=eps` fails. Its selftest passes
  (`series_order_selftest.log`).

Amended at 03:59 UTC, after order 160's D 229 run showed its two weakest as a near pair (σ₂/σ₁ 0.995) and before any overlap with
order 135 or 150 was computed: for a pair, the overlap is read on the span of the other order's two smallest, √(o₁² + o₂²),
since any rotation within a degenerate pair is as good a basis. Added at the coordinator's request: dh170's
order-150 bases D 226 and 227 (`I903-dh170/chain_k150`), whose p_min fell 11 times from D 226 to 227, with v₁(150)
against order 160's six at D 229 and order 135's at D 227.13, and their series content by order.

### series_order.py failed, and what replaces it (04:11 UTC)

`series_order.py`'s criterion is void. Its linearity check failed on order 135's and order 142's D 229.13 states. The
top-tenth share went from 0.9997 at e = 1e-12 to 0.198 at e = 1e-14 for order 135's σ₁ (`so_k135_D229.1312_ks135.log`,
`so_k142_D229.1312_ks142.log`). On order 160's D 229 state its control `--mutate=eps` did not fire: e = 1e-31, below
resolution, still read 1.000 (`so_k160_D229.0000_ks160_muteps.log`). The cause is in the logs. At t = u0/σ = 1.2,
the base series' own terms at u0 grow with the order, with norm 8.06 at order 0 and 1.71e9 at order 160 on order 160's
state (6.79e2 at order 135 and 2.54e4 at order 142 on theirs). So any change, even rounding, lands in the top orders,
and every vector, the σ₅ and σ₆ ones included, reads "top orders". The measure cannot separate directions there. Its
readings are kept in the folder and not used.

In its place, `series_profile.py` prints the series' own term norms at u0 by order (per field), at the state's order
and at higher ones on the same z. Its check: the coefficients up to the smaller order agree bit for bit between two
orders. Its control `--mutate=order` must fail. D 60 (Δ's grip unchanged from ks 142 to 200 there) is the case where
the terms should fall. Whether a weak direction is the truncation's is read from the ks 200 run at D 229 on the same
z: it is the series' if σ there rises above 100 σ(160), and the wall's if it stays within a factor 3.

### series_profile.py: the double-double terms are not the series (04:41 UTC)

Its check passed on all seven states, with the coefficients up to the smaller order bit for bit equal between orders.
Its control fired: `--mutate=order` reads NOT equal, FAIL. At D 60 the terms at u0 fall 0.55 per order (8.2 at order
0, 9.4e-37 at 140, 2.4e-51 at 200). At D 226 to 229 the double-double terms grow past order ~50, reaching 1.7e9 at order
160 and 3.5e11 at 200 on order 160's D 229 state, with similar profiles at orders 135, 142 and 150 (`sp_*.log`).
These terms cannot be the series'. On order 142's D 229.13 state, near_null's octo-double F changed by only 6.82e-22
in the horizon rows from order 142 to 200 (`nn_k142_D229.1312_ks200.log`). If orders 143 to 200 held terms of 5e3 to
1e11, as the double-double profile says, F would change by that much. The likely reading is that the double-double
recursion grows rounding with the order, about 1.7 per order from order ~100 at these D. That would make the
double-double horizon series wrong past order ~100 here, and with it `series_order.py`. `dd_vs_od.py` tests this.
It compares the double-double residual's horizon rows with the octo-double ones at the same converged z (order 160 at
D 229, at orders 160 and 200), with D 60 as the control where the two must agree.

### Results so far (04:54 UTC)

`pmin_table.py` (`pmin_table.log`): every base at its own order. The overlap is v₁ on the span of order 160's two
smallest at D 229, and the falls are per unit D from the same chain's base before.

| order | D | p_min (LU pivot floor) | weak pair σ₁ (harmonic) | fall per unit D | Δ mode σ (Δ share) | fall per unit D | overlap with order 160's pair at D 229 |
|---|---|---|---|---|---|---|---|
| 135 | 229.1312 | 8.10e-18 | 3.958e-20 (k3) | – | 1.016e-17 (0.94) | – | 1.000 |
| 142 | 229.1312 | 4.05e-15 | 1.497e-17 (k3) | – | 8.139e-15 (0.97) | – | 1.000 |
| 150 | 226.0000 | 2.92e-13 | 2.408e-15 (k3) | – | 6.310e-14 (0.85) | – | 1.000 |
| 150 | 227.0000 | 2.74e-14 | 1.443e-16 (k3) | 16.7 | 3.998e-14 (0.87) | 1.58 | 1.000 |
| 160 | 228.0000 | 1.25e-13 | 8.269e-16 (k3) | – | 2.724e-14 (0.87) | – | 1.000 |
| 160 | 229.0000 | 8.85e-15 | 5.406e-17 (k3) | 15.3 | 1.179e-14 (0.75) | 2.31 | 1.000 |

At every base the two weakest vectors are the harmonic-3 pair (p1 and m_h k3, Δ share 4e-5 to 2e-4), the same direction
at orders 135, 142, 150 and 160. Across each chain's collapse step the pair falls 16.7 (order 150, D 226 to 227) and
15.3 times (order 160, D 228 to 229), while the Δ mode falls 1.58 and 2.31 times. Order 160's v₁ at D 229 overlaps
0.965 with the harmonic-3 vector of #902's order 130 at D 253.80 and 0.077 with that state's Δ mode (`pmin_cmp.log`).

`dd_vs_od.py` on order 160's D 229 state (`dv_k160_D229.0000.log`): the double-double residual's horizon rows read
1.164e9 at order 160 and 2.868e12 at order 200, and the octo-double ones 8.557e-4 at both. The double-double horizon
series is wrong there by more than 1e9, which confirms the reading above. The octo-double 8.557e-4 is F itself, not F
minus the held offset c. `dd_vs_od.py` now prints F − c as well, and reruns after the ks 200 run (`dv2_*`). The D 60
control failed on a missing plan (KeyError 'segs', `dv_ctl_D60.log`) and reruns with a new plan, as near_null.py makes.

### The coordinator's question on dh610's stop at D 234 (read only, 05:00 UTC)

The question: is the double-double horizon series what stopped `chain_k160` at D 234? Read from `I903-dh610/chain_k160.log`
and `run903c.sh` (raw ff5dd9f6), and the code at main 80b944ff, which contains dh610's 423bd22d. No code was changed.

- The flags: `--corrector od --tol_od 1e-60 --reseed 2 --reseed_q 1 --reseed_o 3 --reseed_start pred --od_strong 4
  --od_accept natural`, with `--ks 160 --keep_plan 1`.
- The double-double measures are in the log and do not decide acceptance. Every "predicted |F|" is double-double:
  `anm_run.py` sets `Fp = rnorm(spn.residual(ph, pl))`, giving 7.14e9 at D 232, 1.07e10 at 233, 1.65e10 at 234 and
  1.10e11 at 235. So is the corrector's returned |F|, `correct()`'s `Fc = rnorm(spx.residual(z8[0], z8[1]))`, the
  "double-double |F| of its first two parts", 1.3e10 and 1.4e10 at D 233 and 234 against octo-double 9.5e-92 and
  3.4e-78. These are the same rounding as `dd_vs_od.py`'s 1.164e9 on the D 229 state. With `--corrector od` an attempt is
  accepted on the octo-double convergence (`accepted = conv`), so the "stall accepted" in those lines is only a label.
  The same `Fp` gates the re-plan, `if Fp <= 1e-6: plan`, which cannot pass at these D.
- The 7.89e9 at the a = 0.5 start is octo-double, not double-double. `octo_corrector.chord_strong` prints
  `s.residual_o` at z + d, with s the `ElimO`, after its attempted projection. It falls as λ² over the trials: 7.89e9,
  2.17e9, 5.55e8 down to 2.18e6 at λ = 1/64, and 2.00e-27 at λ = 1/128, where the projection succeeded. It is a real
  residual, after a full first step of |dz| 1.18e-14 from a start already at |F| 1.79e-33.
- The projection reads the double-double horizon rows in its first stage. `ElimO.project` calls `reseed.Reseeder.project`,
  which runs a double-double Newton at u0 first: `Reseeder.invert` on `Solver.residual`. At D 235 that stage sat at its
  floor at every trial, for example "u0 rung 1 its, |R| 1.87e+10 -> 1.87e+10". It then passes double-double data
  (parts 2-3 zero) to the quad-double polish, `polish_q`, which uses `residual_q` and `jacobian_q` and no double-double.
  The polish did not converge in 8 steps, for example 1.54e6 to 7.80e1 at λ = 1/64. The re-seed ladder,
  `Reseeder.reseed` (`targets`, then `invert` per rung, then `polish_q` at u0), is double-double up to its last rung, and
  it failed after 8 rungs.
- `--reseed_o 3` was set. `refine_o` ran on the a = 0.5 start's re-seed (2.53e-26 to 2.44e-39) and not inside the
  corrector's projections. At a = 1 the re-seed's first failed stage was the quad-double polish from the prediction's
  own data (`--reseed_start pred`), at |R| 1.82e-5 after 8 steps, not a double-double stage. The start's projection then
  failed, and `StartNotProjected` stopped the attempt.

Reading: the double-double series did not stop the chain by itself. The stop is the first full step's octo-double
residual of 7.9e9, which the projections could not repair. In each of them the first stage is a double-double Newton
that can no longer converge at these D, and the quad-double polish after it starts from double-double-rounded data.
Whether a projection without the double-double stage, from the point's own four-part data and with `refine_o`, would
repair these trials is not tested. dh610 saved the predictions before their re-seed (`pred_pin3_D234.5000.npz`,
`pred_pin3_D235.0000.npz`), and they would be the test's inputs.

### The order-200 test and the F − c rerun (05:18 UTC)

`nn_k160_D229.0000_ks200` passes its check, and only the horizon rows change: max|dF| 1.62e-22, max|dJ| 4.49e41. On the
same z at order 200, order 160's harmonic-3 pair (5.406e-17, 5.381e-17) is order 200's σ₂ and σ₃ (4.223e-14,
4.345e-14). The overlaps on that span are 0.961 and 0.990, and the pair rose 781 times. The Δ mode moved from 1.179e-14
to 1.392e-14, a ratio of 1.181 at overlap 0.982, and is order 200's σ₁ (`pair200.log`). By the criteria above, the pair
is the series' own (above 100 times) and the Δ mode is the wall's (within 3).

`dd_vs_od.py` with F − c (`dv2_k160_D229.0000.log`): on order 160's D 229 state the octo-double F − c horizon rows read
1.505e-91 at order 160, the chain's convergence, and 1.622e-22 at order 200, the series' tail. The double-double ones
read 1.164e9 and 2.868e12. So the 8.557e-4 of the first run was the held offset c. The D 60 control (`dv2_ctl_D60.log`)
agrees in double-double and octo-double to every printed digit at orders 100 and 200, horizon 1.086e-10. That is not
a converged residual, since the state stores no plan and a new one is made. The double-double horizon series is
right at D 60 and wrong by more than 1e9 at D 229.

For the grip queue, `lift.log` now has k160's first base, D 229 (target 230): L = +2.3859, with the Δ mode σ₃
1.179e-14 at order 160 and σ₁ 1.392e-14 at order 200 (ln +0.166).

### Recommended tasks (the p_min question)

1. **Horizon series in octo-double.** What: an hpkernel accessor for the horizon (and centre) series in eight parts,
   beside `Solver.series`, and `series_profile.py` and `series_order.py` rerun on it for the D 226-234 states of orders
   135-160. Why: the content of a direction by series order cannot be read in double-double past D ~226, where the
   double-double terms grow from rounding (1.16e9 in the horizon rows at D 229 against 1.5e-91 in octo-double).
   Acceptance: the eight-part coefficients up to order K agree with the double-double ones where those are right (D 60,
   to 1e-30 relative), the eight-part sum at u0 reproduces `residual_o`'s horizon rows at D 229 to 1e-80, and a
   control that drops the last order must fail that. Depends on: this task.
2. **A projection without the double-double first stage.** What: `reseed.Reseeder.project` (used by
   `octo_corrector.ElimO` under `--reseed 2`) and the re-seed ladder start with a double-double Newton on
   `Solver.residual` (`Reseeder.invert`). At D ≳ 226 its horizon rows are rounding, so it stalls at its floor (|R|
   1.87e10 at D 235) and hands double-double data to `polish_q`. Test a projection that starts `polish_q` from the
   point's own four-part data, followed by `refine_o`, on dh610's `pred_pin3_D234.5000.npz` and `pred_pin3_D235.0000.npz`
   and the a = 0.5 trial points. Why: dh610's order-160 chain stopped at D 234 with every projection failing.
   Acceptance: the new projection converges (octo-double F − c below 1e-60) at λ ≥ 1/64 trials where the current one
   fails, and the current one still fails there (control). Depends on: this task, and on dh610's stored predictions.
3. **The double-double measures in anm_run.py.** What: "predicted |F|" (`Fp = rnorm(spn.residual(ph, pl))`), the
   corrector's returned `Fc` and the re-plan gate `if Fp <= 1e-6` are double-double, and read rounding at D ≳ 226
   (1.1e11 at D 235). Report quad- or octo-double measures, or label these, and decide the gate on one that is right.
   Why: the logs read "stall accepted" at |F| 1e10 for steps that converged to 1e-78, and the plan is never remade at
   these D. Acceptance: at D 229, order 160 the reported measure equals `residual_o` − c's (1.5e-91) within 10 times,
   and a control that reverts to the double-double measure reads above 1e8. Depends on: this task.

### Correction (the coordinator, #937): refine_o does run inside the corrector's projections

Above I wrote that `refine_o` "ran on the a = 0.5 start's re-seed and not inside the corrector's projections". That
is wrong for projections that succeed. `octo_corrector.ElimO.project` returns `with_horizon(z, zp, rs)` unless the
projection failed, and `with_horizon` runs `rs.refine_o` whenever `rs.od > 0` (`--reseed_o 3`). At D 235 the
projections at λ ≥ 1/64 all failed, so they did not run it. dh610's log prints `rs.last_o` only at the start. #937
logs it per projection (`I937-mac/`).

### The Δ mode falls fast from D 229, order-converged (06:50 UTC)

The coordinator's word at 05:31 UTC dropped four rows (order 135 at D 228.13, 227.13 and 230.13, and order 160 at D 227)
and added order 200 at D 231 and order 160 at D 230. All of these runs pass their checks.

`fold_rate.log` (the Δ mode is the vector of largest Δ share, harmonic 1, Δ share 0.75 to 0.87):

| D | order 160 σ | fall per unit D | order 200 σ (same z) | order 200 / order 160 |
|---|---|---|---|---|
| 228 | 2.724e-14 | – | – | – |
| 229 | 1.179e-14 | 2.31 | 1.392e-14 | 1.181 |
| 230 | 7.899e-16 | 14.9 | – | – |
| 231 | 5.908e-17 | 13.4 | 9.042e-17 | 1.530 |

At order 200 the fall from D 229 to 231 is 12.4 per unit D. The criterion for the wall's, within 3 between orders 160
and 200, holds at D 229 and at D 231. So the wall's weak direction falls 12 to 15 times per unit D from D 229, at
the two orders alike, where it fell 2.3 times from D 228 to 229. Caveats: these are order-160 roots read at order 200
without a Newton step, and the ratio between the orders grows from 1.18 to 1.53. Order 135's Δ mode falls 2.1 times
per unit from D 229.13 to 231.13 (1.016e-17 to 2.218e-18, `pmin_table.log`). It sits 1160 times below order 160's at
D 229 and 27 times below at D 231, so order 135 is not converged for this mode.

The pair keeps falling 15.3 to 15.4 times per unit at order 160 (D 228 to 231), and at order 200 on the D 231 state it
rises 1214 times, with v₁ on order 200's pair span at 0.950 (`pair200_D231.log`). So it is the truncation's at D 231
too. For the grip queue, `lift.log`'s k160 D 231.0000 gives L = +2.9247.
