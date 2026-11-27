# I1102-mac: the l = 1 mode matrix's double-double block 12 in Rust (ellrs) against ell_ddm.DDEll: inputs, checks, controls, profiles, timings

Machine: Mac (Apple M5, macOS 27), venv-1025dd (Python 3.14.7, numpy 2.5.4 and scipy 1.18.1 on Accelerate), ellrs
built into a private site folder (PYTHONPATH), nice 10, beside other users' jobs.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1102

Code: branch wip/ell1-rust-b12 of choptuik-large-d (from wip/ell1-speed 92b9bf53): solver/matter/ellrs/ (the crate),
solver/matter/ell_b12rs.py (the driver and its check), d18_secant.py's --b12=rust. ell_ddm.py, dss_ell.py and ddnp.py
are unchanged from 92b9bf53.

## in/ (copies, blobs by git hash-object --no-filters)
| file | blob | from |
|---|---|---|
| sol_l1kc31r1025_D10.5000.npy | f07a8984 | I1025-mac/out/ |
| l1kc31r1025.jsonl | e5a87ec5 | I1025-mac/out/ |
| sol_l1kc55F1025_D18.125000.npy | 88ccda5c | I1025-mac/out/ |
| l1kc55F1025.jsonl | 0fb77df8 | I1025-mac/out/ |
| sol_l1kc87Ldh370_D21.062500.npy | f9a592e5 | I1025-macm3/kc87_leg_lambda/21.0625/in/ |
| l1kc87Ldh370.jsonl | 3fb006df | I1025-macm3/kc87_leg_lambda/21.0625/in/ |

## checks/
- `ref_lu_spread_kc31.log` (scripts/ref_lu_spread.py): DDEll's block 12 against DDEll with the transposed f64 LU in
  its periodic solves, k_c 31, lambda 2.87. 22 of 15010 entries are equal, the largest difference is 2.0e-14 of its
  entry and 5.1e-27 of the block's largest entry. So no change of rounding meets 1e-28 per entry; only bit for bit does.

## profile/
`profile_b12.py` (via `run_profile.sh`): one ellrs evaluation's time by kind (Ozaki slicing, f64 products, level sums,
LU, elementwise), per RK4 stage, beside one DDEll.rhs stage in Python on the same shapes. matrixmultiply's products,
6 threads: `profile_kc55_t6.log`, `profile_kc87_t6.log`; records in `profile.jsonl`.
