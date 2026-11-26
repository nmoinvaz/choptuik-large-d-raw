# I1098-mac-a/dmat_ms: hp's d/dtheta matrices against 120-digit values and multishoot PR #67's reference (#1098)

Part of `../`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The question came from multishoot PR #67 (feat/dmat-remainder, d1743b45). hp's mpmath-built matrices are not exactly
antisymmetric and carry noise at entries that are exactly 0. hp's builders work at these precisions: driver.dmat_odd
and form_s.dmat_even make double-double values from 40-digit values, and form_s.dmat_corr makes the f64 remainders
c = D - hi - lo from 80-digit values. The quad- and octo-double lanes apply hi + lo + c; the double-double lanes apply
hi + lo. The Mac checks run the Python of d40a9c62 with mpmath only. Its dmat_odd, dmat_even and dmat_corr are
478e9d86's, unchanged by git diff. The residual check runs on dh610 with 478e9d86's Python.

- `exact_M32_48.log` (`dmat_exact_check.py`): the matrices at M 32 and 48 against 120-digit values.
  - hi + lo is off by at most 1.4e-32 to 2.7e-32, the double-double rounding.
  - hi + lo + c is off by at most 2.75e-49 (M 32) and 1.55e-48 (M 48), about 1e-49 of each row's largest entry.
  - The 40-digit noise is there in hi + lo: the odd diagonal (exactly 0) reads 1.03e-43, and max |D + D^T| of the odd
    matrix is 2.07e-43 (M 32) and 4.59e-41 (M 48). That is 9-11 orders below the double-double rounding of the other
    entries.
  - c removes it: with c the odd diagonal reads 1.27e-60 (the lo part) and max |D + D^T| 2.55e-60.
- `entries_M8_16.log` (`dmat_ms_entries.py`): hp's hi + lo + c against multishoot's reference entries
  (tests/data/dmat_mp.txt at d1743b45, the odd and even grids at M 8 and 16). The sums agree exactly on all 640 entries.
  Some parts differ: the odd diagonals' hi, lo and c, and up to 28 of the even entries' parts. Those are the entries
  where hp's parts carry the 40-digit noise and c cancels it; multishoot flushes such parts to 0.
- `residual_D300.log` (`dmat_ms_check.py` by `dmat_ms_run.sh` on dh610, fastmul6 site_y, 4 threads): the octo-double
  residual of D 300's full base state (kfreeze 13, M 32) with hp's c and again with c' = RN(D_120 - hi - lo).
  - c' equals c on every odd entry and differs by at most 9.7e-122 on the even ones.
  - max |F' - F| is 1.4e-119, and the first-order move of the converged Delta, -g.(F' - F), is 4.4e-108.
  - The control (c' times 1 + 2^-20) moves Delta by 2.07e-38, the 2^-20 share of the double-double term (-2.2e-32 at
    D 300) it should give.
- So the noise does not move Delta at 1e-25. Scaled from the double-double term (+2.7e-23 at D 2000 for errors of
  2.7e-32), the remaining 1.55e-48 gives about 1.5e-39 at D 2000.
- It has no bearing on fastmul7's 4.65e-70 split check. horizon_mp_check.py's mpmath reference reads the kernel's own
  hi + lo + c exactly (taylor_mp_check.kernel_dmats), so the two sides share the operator.
