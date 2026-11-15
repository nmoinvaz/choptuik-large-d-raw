# I652-mac: the sigma-model kernel sigma_ms continued in D at eta = 1 from D 4 to 10.475, and two starts at D 10.475

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/652.
Code: wip/xf-652 (matter/sigma_ms/run_eta.py's secant in D, chain.py's --eta/--Ds and --start2). Work in progress; the
closing summary will replace this file's status section.

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
- chain_D3.log: restarted from D 5.75 with the secant through 5.5 (--start2), steps of 0.125 to 10, then 10.1, 10.25,
  10.375, 10.475. Running.

seeds/: sigdss_m1up_D10.4746_eta1.0000.npy (the first march's last entry, Delta 1.0340058134612833), the second start's
seed is solver/matter/data/sigdss_sol_m1hi_D10.4750_eta1.0000.npy in the repository (Delta 0.993485962498047).
