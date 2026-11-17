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

### series_order.py failed, and what replaces it (04:20 UTC)

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
