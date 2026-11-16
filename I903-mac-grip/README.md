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

In progress.
