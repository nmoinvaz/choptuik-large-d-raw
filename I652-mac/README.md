# I652-mac: the sigma-model kernel sigma_ms continued in D at eta = 1 from D 4 to 10.475, and two starts at D 10.475

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/652.
Code: wip/xf-652 (2ea71e90 run_eta.py's secant in D and chain.py's --eta/--Ds; fb0cbb7d --start2; 1ca6bb23 and
1582125b the adaptive chain in D, --D_from/--D_to/--dD/--dD_min/--dD_max).

## Result (2026-11-15 16:51 UTC)
The chain in D at eta = 1, M = 32, reached D 10.475 from D 4 with every point converged: Delta(10.475) =
1.020104800025154887044162539824771, |F| 1.4e-31, constraint 6.7e-15 (out/sm_eta1_D10.475_M32.npz). Newton did not lose
the branch: from D 8 on, 18 runs failed and each was recovered by halving the step (the smallest 1/128, at D 9.5625).
No start at D 10.475 other than the chain's own secant converges, so the acceptance (two starts converge to one solution,
agreeing to 1e-20) is not met:

| start at D 10.475 | seed | result |
|---|---|---|
| A (starts.log) | sigdss m1up, Delta 1.0340058 (k_c 15) | not converged, \|F\| 3.3e-3, LU pivot 4.7e-10 |
| B (starts.log) | sigdss m1hi, Delta 0.9934860 | not converged, \|F\| 6.2e-5, pivots 3.7e-9 to 6.3e-11 |
| the chain (chain_D4.log) | secant through D 10.4375 and 10.375 | converged, \|F\| 1.4e-31, Delta 1.0201048000 |
| z0 (start_z0.log) | zero-order, the D 10.4375 state | not converged after 16 + 16 steps, \|F\| 2.1e-4 at lam 1/64, pivots 5e-9, Delta 1.0206581 |

The failed starts walk along SIGMA_DSS 6's near-null band (smallest pivots 1e-8 to 1e-11, steps of 5 to 800 along it);
sigdss crossed it with a smoothness prior, which sigma_ms does not have.

Against SIGMA_DSS 5's sigdss values (table.md): -6.8e-5 at D 4 (sigdss's own constraint there 4.8e-2), within 2.4e-6 at
D 5, 5.5, 6, 7 and 8, then +1.8e-4 at D 9 and -2.7e-3 at D 10. The chain's Delta peaks near D 9 (1.0270833) and falls to
1.0201048 at 10.475, between sigdss's two solutions there.

## Build of sigma_ms on this Mac
- Command (from the worktree's root): `FAST=1 CARGO_BUILD_JOBS=4 PY=/Users/nathan/venv-314/bin/python SITE=<scratch>/site
  CARGO_TARGET_DIR=<scratch>/target nice -n 10 matter/sigma_ms/build.sh`, site outside the checkout.
- Python 3.14.7, maturin 1.16.0, rustc and cargo 1.94.0; crates multishoot =1.2.2, multidouble =4.2.1.
- 4:59.83 wall, 377.5 s user; finished 2026-11-15 06:15:45 UTC; `sigmams neon`; wheel
  sigmams-0.1.0-cp314-cp314-macosx_11_0_arm64.whl. Log: build.log.

## Control against #639 (matter/sigma_ms/data/delta_eta.csv, M 32)
- control.log: eta = inf from #639's state, converged at Newton step 0 (a weak test), Delta equal to the csv in all 32
  digits (Delta_hi + Delta_lo; the record's "Delta" string is hi only).
- control7.log: eta = 7 by Newton from #639's secant seed, 5 steps, |F| 3.1e-31, Delta 0.4598093840111041234186738320679644,
  equal to the csv's 0.45980938401110412341867383206796.

## Chains (out/, records out/sm_records.jsonl; take the last record of each tag)
- chain_eps.log: at D 4, eta 4, 3, 2, 1.5, 1.25, 1, each converged (|F| <= 1.3e-30).
- chain_D.log: the first D chain, 4 -> 4.5 from the zero-order seed, did not converge (tag eta1_D4.5_M32's first record).
- chain_D2.log: 4.05 .. 5.75 converged; D 6 (step 0.25) did not (|F| stalled at 5.2e-3).
- chain_D3.log: restarted from D 5.75 with the secant through 5.5 (--start2), steps of 0.125: converged to D 7; 7.125
  failed (stopping). From D 7.0625 (probes.log) 7.125 converges.
- chain_D4.log: the adaptive chain (chain.py --D_to) from D 7.0625 (secant through 7) to 10.475, steps of 0.0625
  halved on a failed run (down to 1/128) and doubled after three successes on the dyadic grid: 117 runs, every point
  converged (|F| <= 4.2e-29, constraint <= 1.2e-14), 18 failed runs recovered by halving.
- start_z0.log: a second start at D 10.475 from the D 10.4375 state alone (zero-order seed): not converged.
- table.md (table.py): every converged point's Delta, |F|, constraint and Newton steps, with sigdss's values.

seeds/: sigdss_m1up_D10.4746_eta1.0000.npy (the first march's last entry, Delta 1.0340058134612833), the second start's
seed is solver/matter/data/sigdss_sol_m1hi_D10.4750_eta1.0000.npy in the repository (Delta 0.993485962498047).
