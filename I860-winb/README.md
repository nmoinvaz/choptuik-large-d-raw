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

(parts A(M = 3) and A(M = 5) follow)
