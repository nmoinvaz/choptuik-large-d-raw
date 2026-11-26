# I1098-dh610/mpcheck: independent mpmath checks of form S's octo-double arithmetic (#1098)

Machine: dh610 (Fedora 45, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Kernel: fastmul5 (f350aa62) in `site_x`, with `HP_EXACT_RECIP=1`. The scripts are `hp/taylor_mp_check.py` (d9441ce3)
and `hp/horizon_mp_check.py`. The runners are in `../fix/` (`mpcheck.sh`, `mpcheck_m.sh`, `mpcheck2.sh`,
`mpcheck3.sh`). mpmath works at 150 digits and shares none of the kernel's arithmetic. Both sides use the kernel's
double-double d/dtheta matrices, read exactly, and omega = dd(2 pi)/Delta, so only the arithmetic is compared.

## The Taylor step (`taylor300.log`, `taylor_m.log`)

One step from the last node x_l = 0.7, order kt 36. The control is the kernel with double-double 1/x0 and 1/(k + 1).

| state | M | h | kernel vs mpmath | control |
|---|---|---|---|---|
| D300_full_base | 32 | -0.02 | 1.24e-124 | 2.36e-31 |
| D 1000 M 48 h23 (I1098-mm5/m48_1000) | 48 | -0.00154 | 2.31e-130 | 4.68e-38 |
| D 1000 M 64 h23 step (I1098-mm5/m64_1000) | 64 | -0.00154 | 3.98e-130 | 4.68e-38 |

All three PASS (bar 1e-60; the control must exceed 1e-40). The step, with the slaving solve's refinement, is good to
octo-double at M 32, 48 and 64.

## The horizon values (`horizon300_r1.log`, `horizon300_r0.log`)

These compare the fields at x_l that the horizon series gives from D300_full_base's m_h. mpmath's u series runs to
order 612; its last ten terms are at most 3.5e-71. The kernel's values come from its u series and its Moebius series
(a 8, ks 600). `_r1` has the relaxed products on, `_r0` has them off; the two agree.

- **A script error in these two logs:** their first line "kernel u (ks 306) against mpmath ... 5.4e-17" summed the
  kernel's eight parts at mpmath's default 53 bits. That first call ran outside the 150-digit block. Fixed in the
  next version (`horizon300_v3.log`).
- The scan, which ran inside the block, shows the kernel's u sum agreeing with mpmath's partial sums to 1e-120 or
  better at ks 20 to 306. u's truncation at ks 306 is 2.6e-35.
- The kernel's Moebius values are 1.0e-40 off mpmath's converged sum, the same with the relaxed products on or off.
  p, m and c read 9.97e-41, 8.77e-41 and 4.70e-41.
- The control moves m_h's low part by 1e-30 in the kernel only. It reads 4.6e-28.
