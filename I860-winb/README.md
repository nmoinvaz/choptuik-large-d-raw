# I860-winb: Theorem A's certificates at M = 1, 3 and 5 reproduced on Windows x86-64

Machine: winb (Surface Laptop 4, Windows 11). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/860. The commands
are the issue's, from `solver/proof/` of the worktree `choptuik-i860` at main f182be24, run by `run860.sh` (one chain, with
box5 started first in the background, so two processes at most, below-normal priority). Each run writes `<name>.log`, and
`exits.txt` has each run's exit code and wall time (UTC). The Pi's folders I843-rpi5, I844-rpi5 and I847-rpi5 are read from
a separate worktree of raw main fc6db14b.

```
commit f182be24 (f182be244dd652d0d14c80db8920d97b428bfd23)
python-flint 0.9.0 FLINT 3.6.0 numpy 2.5.4 mpmath 1.3.0 scipy 1.18.1
Windows-11-10.0.26200-SP0 AMD64 python 3.14.10 uv-made venv venv-choptuik-314
PYTHONUTF8=1 (logs are UTF-8 as on the Pi)
CPU: 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz, 4 cores, 8 threads
RAM: 31.8 GB
```

## Part A(M = 1) (22:36:42 to 22:46:02 UTC)

Every run exits 0 (13 of 13). The Krawczyk test passes in all three runs of `validated_int.py krawczyk 1e-9`, with the
Pi's two margins to every printed digit: 7.925e-10 and 9.247e-10 on this machine's own enclosures (`vi_test_own`), on the
stored x86 ones (`vi_test_stored`) and on the Pi's (`vi_test_pi`).

| run | exit | wall (s) | Pi wall (s) | against the Pi's log |
|---|---|---|---|---|
| certify_M1 | 0 | 0.68 | 0.52 | identical |
| certify_M1_pm | 0 | 99.6 | 95.9 | differs, see below |
| residual_poly 0.08 | 0 | 0.47 | 3.2 | identical to its `residual_poly_008.log` |
| fixed_point | 0 | 0.36 | 0.32 | identical |
| fixed_point_box | 0 | 0.56 | 0.47 | identical |
| fixed_point_sector | 0 | 0.40 | 0.32 | identical |
| fixed_point_008 | 0 | 0.56 | 0.44 | identical |
| krawczyk --xi1=0.3 | 0 | 17.1 | 16.5 | one printed digit |
| vi_point | 0 | 220.0 | 285.1 | the radii differ, see below |
| vi_box | 0 | 218.2 | 280.8 | only the seconds, in the log; the radii in the json differ |
| vi_test_own | 0 | 0.29 | 0.19 | the radii in 3 lines, in the last printed digit |
| vi_test_stored | 0 | 0.28 | 0.19 | identical |
| vi_test_pi | 0 | 0.28 | | margins 7.925e-10, 9.247e-10 |

Differences from the Pi's logs (listed, not fixed):
- `certify_M1_pm.log`: the non-rigorous Newton search and the box margins it prints differ. Its six iterates differ from
  the ninth digit (iterate 1: p = 2.542148047580, 0.776994013630 against the Pi's 2.542148047487, 0.776994013515, and
  |G| 1.20e-07 against 5.99e-08; the last, 2.542148047630 and 4.37e-08 against 2.542148047376 and 1.45e-08), the zero is
  A = 2.5421480476 against 2.5421480474 with w/w_inf 0.7769940137 against 0.7769940136, the singular values of J0 are
  3.027e+02, 8.717e+01 against 3.028e+02, 8.720e+01, and the h = 1e-3 box's edge margins are [0.000973572, 0.001005,
  0.000985995, 0.00101017] against [0.000973135, 0.001004713, 0.00098609, 0.001009959] (differing from the 4th digit; the h =
  1e-5 box's [1e-05, 1.0003e-05, 9.997e-06, 1e-05] against [9.995e-06, 9.999e-06, 9.997e-06, 1e-05]). All margins are
  positive on both, and the run exits 0.
- `krawczyk.log`, line 6: 0.5906 against 0.5905 (the last printed digit of the entrywise max variation of J).
- `vi_point.json`: the midpoints of the four enclosures agree to the 56 digits compared, and the radii differ: 2.656e-19
  and 1.445e-19 against 2.661e-19 and 1.451e-19 (0.2% and 0.4%), the final state radius 2.939e-19 against 2.944e-19, so
  `vi_point.log` and `vi_test_own.log` print ±4.64e-19, ±6.40e-19, ±6.25e-19, ±1.86e-19 where the Pi's print ±4.65e-19,
  ±6.41e-19, ±6.26e-19, ±1.87e-19, and ±7.35e-19, ±8.26e-19 for J_D(x^) where the Pi's print ±7.37e-19, ±8.28e-19.
- `vi_box.json`: the four variational radii differ by up to 1.5e-06 relative (dDp1_rad[1] 3.6560857e-04 against
  3.6560913e-04), the state radius by 3e-09 relative; the printed log lines agree.
- The wall times: vi_point and vi_box take 77% of the Pi's, the others are within 25% of the Pi's.

## Part A(M = 3) (22:46:02 to 22:59:58 UTC)

Every run exits 0 and every ctrl exits non-zero by its check's verdict, none by a crash (no Traceback in any log). box3
passes, and its Krawczyk test gives the Pi's relative margins to every printed digit, +0.994, +0.997, +0.778, +0.778, on
this machine's own box (`krawczyk3`, also `recheck3` by mpmath), on the stored x86 box (`krawczyk3_stored`) and on the
Pi's (`krawczyk3_pi`); `controls3` has the Pi's margins too. The M = 1 reproduction prints REPRODUCED (`m1_rerun`: Krawczyk
passes True, the zero's A and w/w_inf enclosures overlap Theorem A(M = 1)'s), and its control prints NOT REPRODUCED.

| run | kind | exit | wall (s) | Pi wall (s) | verdict line |
|---|---|---|---|---|---|
| sys_selftest | run | 0 | 3.4 | 3.8 | ok |
| sys_selftest_mut (coupling) | ctrl | 1 | 3.3 | 3.3 | `SELFTEST FAIL` (M = 1 step MISMATCH) |
| m1_rerun | run | 0 | 254.9 | 305.3 | `REPRODUCED` |
| m1_mut (m1ref) | ctrl | 1 | 0.3 | 0.2 | `NOT REPRODUCED` (A False) |
| startcheck3 | run | 0 | 13.8 | 13.8 | |
| startcheck3_mut | ctrl | 1 | 14.0 | 13.8 | contains this file's series values: False |
| crosscheck3 | run | 0 | 53.2 | 77.6 | AGREE, worst 8.2e-14 (Pi 6.8e-14) |
| crosscheck3_mut | ctrl | 1 | 52.4 | 77.5 | DISAGREE, 5.5e-06 |
| box3 | run | 0 | 431.4 | 548.1 | 955, 552, 72 steps (the Pi's) |
| krawczyk3 | run | 0 | 0.28 | 0.19 | margins +0.994, +0.997, +0.778, +0.778 |
| controls3 | run | 0 | 0.34 | 0.21 | margins +9.94e-01, +9.97e-01, +7.78e-01, +7.78e-01, and the negative ones as the Pi's |
| krawczyk3_mut (hier) | ctrl | 1 | 0.26 | 0.19 | hier's (a) and (b) False |
| recheck3 | run | 0 | 0.21 | 0.12 | margins +0.994, +0.997, +0.778, +0.778 |
| recheck3_mut | ctrl | 1 | 0.26 | 0.12 | K(X) in int X: False, margins -6970584715.795, -3581188767.700, -2300395.263, -2962748.375 (the Pi's) |
| krawczyk3_stored | run | 0 | 0.28 | 0.19 | the same margins |
| krawczyk3_pi | run | 0 | 0.29 | | the same margins |
| usys_M | run | 0 | 0.87 | 0.70 | ok |
| fpm_check_m1 | run | 0 | 2.4 | 2.4 | True |
| fpm_M3 | run | 0 | 0.71 | 0.65 | |

`A_M_point_M1.json`, `A_M_box_M1_1e-9.json` and `A_M_m1.log` are the m1 rerun's outputs, copied from the worktree.

Differences from the Pi's logs (listed, not fixed):
- The sha256 of `fixed_point_M.py` printed by `startcheck3`, `krawczyk3` and stored in the box json (`start/fpm_sha256`) is
  a44e6c92eac010eb against the Pi's 589e5a810bc50289. This worktree's files have CRLF line endings (`core.autocrlf=true`
  on this Windows machine), and the sha256 of the repository's blob, and of the working copy with the CRs removed, is
  589e5a810bc50289, the Pi's. The logs also print the Windows path of the file.
- `m1_rerun` and `m1_mut`: the zero's enclosures differ in the last digits and radii, A in [2.54214804759635,
  2.54214804763677] (radius 2.02e-11) against [2.54214804759628, 2.54214804763685] (2.03e-11), then (2.46e-12 against 2.47e-12).
- `krawczyk3`, `krawczyk3_mut`: the radii of the enclosures of A, w/w_inf, B3, C3 differ by 1.5% to 2.7% (A 5.69e-13
  against 5.59e-13, w/w_inf 3.07e-13 against 2.99e-13, B3 1.56e-13 against 1.53e-13, C3 8.97e-15 against 8.77e-15), and
  hier's |hier - certified| bound for A and C3 in the last digit (1.15e-11 against 1.14e-11, 1.80e-13 against 1.79e-13).
- `recheck3`, `recheck3_mut`: the mpmath enclosures differ from the 14th digit (A in [2.7264758856303113,
  2.7264758856314488] against [2.7264758856303214, 2.7264758856314387]); the margins agree.
- `controls3`, one margin of C6b: +4.98e-01 against +4.97e-01 (the second of four).
- Double-precision comparisons: `sys_selftest` SysM against inner_np 4.4e-16 (M = 3) and 4.9e-16 (M = 5) against the Pi's
  3.1e-16 and 3.6e-16; `usys_M` (b) 3.5e-16 and 1.4e-15 against 6.1e-16 and 8.7e-16; `crosscheck3` 1.6e-14 and 8.2e-14
  against 1.3e-14 and 6.8e-14 (the same in `crosscheck3_mut` to the last digit).
- `fpm_check_m1`: the relative differences of the upper bounds between fixed_point.py and fixed_point_M.py are lip 6e-51,
  rho 1e-21, selfmap 6e-22 at the point (the Pi: 8e-18, 3e-18, 7e-18) and lip 4e-29, rho 1e-21, selfmap 6e-22 on the box
  (the Pi: 7e-17, 3e-17, 6e-17), and the constants print as equal to relative 1e-21 against 8e-18 and 7e-17.
- The box json (`A_M_box_M3_1e-10.json`): all 1882 leaves have the same keys; 176 ball strings have midpoints equal in
  the first 45 characters and radii that differ in the last digits; the numeric leaves `start/eta` (4.0902588391219086e-64
  against 4.0902588391218884e-64, 4.9e-15 relative) and `start/eta_der` (2.3e-15) differ.
- Wall times: m1_rerun 83%, crosscheck3 69%, box3 79% of the Pi's.

(part A(M = 5) follows)
