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

- `check_kc31.log`, `check_kc55.log`, `check_kc87.log`, records in `check.jsonl` (scripts/run_checks.sh, ellrs
  bd424726): check 1, `ell_b12rs.py check --threads=6,1 --controls=1`, the Rust block against `DDEll.mode_matrix(only=[12])`
  in one process. k_c 31 at lambda 2.87, k_c 55 at 1.775 and k_c 87 at 0.895 are bit for bit on 6 and on 1 thread
  (15010, 46426 and 115194 entries). The controls fail at every state: nolam (tangents without lambda) and harm (the
  top odd harmonic dropped from the tau operators). The same lines carry the timings (check 4).
- `rs_build_compare.log` (scripts/rs_dump.py): ellrs a3dfcc5b against the blocks of bd424726 in `rsref/`, bit for bit
  at k_c 55 and 87.

## scan/
`scripts/run_scans.sh` (ellrs bd424726): check 2, `d18_secant.py scan` with `--b12=rust` and with the default
(`ell_ddm`), at three lambda per state, one within 1e-3 of the state's root. The roots are 1.7733012 at k_c 55
(SPEED_ELL1.md's refinement) and 0.8945878 at k_c 87 (matter/ell1_roots.csv). Logs and records `scan_kc<k_c>_<b12>.*`.

`compare.log` (scripts/compare_scans.py): every field of the two scans' records is equal at all six lambda, ln|det|
to the last bit: PASS at k_c 55 and 87. Its control, `--b12=rust --mutate=nolam` at k_c 55
(`scan_kc55_rust_nolam.*`), flips the sign at 1.77 and 1.7733 and moves ln|det| by 130: FAIL, as it must.
`scan_kc55_rust_harm.log` is the same run with the harm control, which stops in dd_logdet at a singular pivot (the
dropped harmonic's rows of block 12 vanish).

## rsref/
ellrs bd424726's block 12 (tangents and end values) at k_c 55, lambda 1.775 and k_c 87, lambda 0.895, the references
of `rs_build_compare.log`.

## profile/
`profile_b12.py` (via `run_profile.sh`): one ellrs evaluation's time by kind (Ozaki slicing, f64 products, level sums,
LU, elementwise), per RK4 stage, beside one DDEll.rhs stage in Python on the same shapes. matrixmultiply's products,
6 threads: `profile_kc55_t6.log`, `profile_kc87_t6.log`. With scipy's dgemm (Accelerate; ellrs a3dfcc5b) on 1
and 6 threads: `profile_kc*_t*_dgemm.log`. Records in `profile.jsonl`.
