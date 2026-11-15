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

## Result: the margins against the Pi's

Every run of the three parts exits 0 and every control exits non-zero by its verdict (no run or control crashed). Each
reproduced margin below equals the Pi's to every printed digit; the discrepancies of the logs are listed under each part.

| item | Windows x86-64 (this run) | the Pi (the issue, or its log) |
|---|---|---|
| M = 1, Krawczyk, own enclosures (`vi_test_own`) | 7.925e-10, 9.247e-10 | 7.925e-10, 9.247e-10 |
| M = 1, stored x86 and the Pi's enclosures | 7.925e-10, 9.247e-10 (both) | 7.925e-10, 9.247e-10 |
| M = 1 reproduction (`m1_rerun`) | REPRODUCED | REPRODUCED |
| M = 3, `krawczyk3` on box3, relative margins | +0.994, +0.997, +0.778, +0.778 | +0.994, +0.997, +0.778, +0.778 |
| M = 3, stored x86 and the Pi's box | the same (both) | the same |
| M = 5, `krawczyk5` on B5, relative margins | +0.996, +0.998, +0.889, +0.889, +0.912, +0.911 | +0.996, +0.998, +0.889, +0.889, +0.912, +0.911 |
| M = 5, hier checks (a) and (b) | True, True | True, True |
| M = 5, stored x86 and the Pi's B5 | the same margins (both) | the same |
| M = 5, `d2check5`, worst abs(dev) / tolerance | 2.59e-07 | 2.64e-07 (stored box), 2.67e-07 (the Pi's) |
| M = 1 and M = 3 reference checks | REPRODUCED (thmA1, AM3) | REPRODUCED |

Discrepancies, in order of size (the details are under each part): `d2check5`'s worst ratio is 2.59e-07 against 2.64e-07
and 2.67e-07 (2% and 3% lower); the non-rigorous Newton search and the box margins printed by `certify_M1_pm` differ from
the 4th digit; the printed contribution matrices of `krawczyk5` differ by up to 19% in small entries; the sha256 of
`fixed_point_M.py` printed in the logs differs because of the CRLF working copy (the repository's blob has the Pi's sha256);
enclosure radii and mpmath enclosures differ in the last printed digits throughout.

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

## Part A(M = 5) (box5 22:36:42 to 23:43:34 UTC, the rest 23:00:00 to 23:43:37 UTC)

Every run exits 0 and every ctrl exits non-zero by its check's verdict, none by a crash (no Traceback in any log). box5
took 4012 s against the Pi's 4924 s, and ran beside the M = 1 and M = 3 parts (two processes). B5 passes the Krawczyk
test (C^2) with the Pi's six relative margins to every printed digit, +0.996, +0.998, +0.889, +0.889, +0.912, +0.911, and
hier.py's checks (a) inside the hull and (b) agreement within 3x its spread are both True; the stored x86 B5 and the Pi's
B5 pass with the same margins on this machine. `controls5` prints CONTROLS ALL AS EXPECTED with the Pi's margins. The
`reference check` prints REPRODUCED for M = 1 (`krawczyk1`, thmA1) and for M = 3 (`krawczyk3m2`, AM3), and NOT REPRODUCED
in the control `krawczyk1_mut`.

| run | kind | exit | wall (s) | Pi wall (s) | verdict line |
|---|---|---|---|---|---|
| box5 | run | 0 | 4012.4 | 4923.6 | steps [2118, 863, 101] (the Pi's) |
| lohner_selftest | run | 0 | 1.5 | 1.7 | SELFTEST2 PASS |
| lohner_selftest_mut (lin2) | ctrl | 1 | 1.5 | 1.6 | SELFTEST2 FAIL |
| box1 | run | 0 | 210.2 | 243.3 | steps [303, 320, 46] (the Pi's) |
| krawczyk1 | run | 0 | 0.27 | 0.24 | margins +1.000, +1.000; reference check (thmA1): REPRODUCED |
| krawczyk1_mut (ref) | ctrl | 1 | 0.29 | 0.24 | reference check (thmA1): NOT REPRODUCED |
| controls1 | run | 0 | 0.28 | 0.24 | CONTROLS ALL AS EXPECTED |
| recheck1 | run | 0 | 0.17 | 0.09 | margins +1.000, +1.000 |
| recheck1_mut | ctrl | 1 | 0.16 | 0.09 | K(X) in int X: False, margins -58856260.588, ... |
| box3m2 | run | 0 | 770.7 | 923.1 | steps [955, 552, 72] (the Pi's) |
| krawczyk3m2 | run | 0 | 0.31 | 0.25 | margins +1.000 (four); reference check (AM3): REPRODUCED |
| controls3m2 | run | 0 | 0.29 | 0.26 | CONTROLS ALL AS EXPECTED |
| d2check3 | run | 0 | 0.29 | 0.24 | True; worst abs(dev) / tolerance 3.46e-10 (the Pi's 3.50e-10) |
| recheck3m2 | run | 0 | 0.23 | 0.17 | margins +1.000 (four) |
| recheck3m2_mut | ctrl | 1 | 0.26 | 0.17 | K(X) in int X: False, margins -69705846.168, ... |
| krawczyk5_stored | run | 0 | 0.32 | 0.27 | margins +0.996, +0.998, +0.889, +0.889, +0.912, +0.911; hier (a), (b) True |
| krawczyk5_pi | run | 0 | 0.30 | | the same |
| krawczyk5 (B5) | run | 0 | 0.36 | 0.22 | the same |
| krawczyk5_mut (hier) | ctrl | 1 | 0.35 | 0.20 | hier.py check (a) False, (b) False |
| controls5 | run | 0 | 0.39 | 0.25 | CONTROLS ALL AS EXPECTED |
| d2check5 | run | 0 | 0.34 | 0.20 | True; worst abs(dev) / tolerance 2.59e-07 |

Differences from the Pi's logs (listed, not fixed):
- `d2check5`: the worst abs(dev) / tolerance is 2.59e-07 against the Pi's 2.67e-07 and the stored box's 2.64e-07 (the issue's
  numbers), the worst relative deviation 6.49e+01 as the Pi's; the enclosure radii it prints are 1.0e+22 against 1.2e+22.
  `d2check3`: 3.46e-10 against 3.50e-10, and the enclosure radii 3.8e+07 and 3.9e+07 against 3.9e+07 and 4.6e+07.
- `krawczyk5`, `krawczyk5_mut`: the printed matrices of contributions to |K_i| / w_i differ in 56 entries, by up to 19%
  in the small ones (1.86e-07 against 2.30e-07, 1.25e-08 against 1.32e-08) and by 0.1% or less in the large (1.95e-04,
  3.17e-04 equal); the margins and the hier checks are identical. `krawczyk3m2`: 18 entries, up to 14% (1.63e-08 against
  1.40e-08); `krawczyk1`: the enclosure radii, up to 8% (2.31e-15 against 2.12e-15). On the Pi's B5, `krawczyk5_pi` is
  identical to the Pi's own `krawczyk5.log`, line for line.
- The ray lines of `A_M2_box_M5_1e-10.log`: 72 printed radii differ, by up to 7% (V0 and W radii; 9.93 against 10.7 on one
  line); the step counts are the Pi's (2118, 863, 101).
- `A_M2_box_M5_1e-10.json` (7104 leaves, the same keys as the Pi's and the stored x86 box): four numeric leaves differ
  (`sec`, `start/sec`, `start/eta` by 3e-13 relative, `start/eta_der`), and of 2004 ball strings the midpoints differ within
  their first 40 characters in 593 (against the Pi's B5), 667 (against the stored x86 B5) and 693 (the Pi's against the
  stored), so the Windows box is as close to the Pi's as the Pi's is to the stored one. The sha256 of `fixed_point_M.py`
  recorded in it is a44e6c92eac010eb (CRLF working copy), as in the M = 3 part.
- `recheck1`, `recheck3m2`: the mpmath enclosures differ from the 11th to the 14th digit; the margins agree.
- Wall times: box5 81%, box3m2 83%, box1 86% of the Pi's.
