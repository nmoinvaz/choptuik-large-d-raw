# I889-winb: Theorem A(M = 1)'s lemmas S, 6a and 6b1 reproduced on Windows x86-64

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/889.
The commands are the coordinator's `run889.sh` (in this folder; placed md5 b72725a461111588e45852ca0a10a29c, mine
8e8a817e58fce80edf81c93d831de1fd, only its RAW path line changed), run in Git Bash from `solver/proof/` of the worktree
`choptuik-i889` at main 982723ee, one process at a time at below-normal priority, with the venv `venv-choptuik-314`
(Python 3.14.10, python-flint 0.9.0 with FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0; `env.txt`), `PYTHONUTF8=1`.
The Pi's folder I873-rpi5 is read from a separate worktree of raw main 955e3088. `exits_889.txt` has each run's exit code and
wall time (UTC).

## Result

Every run of `run889.sh` exits 0 (24 of 24; the 21 min 50 s from 01:28:17 to 01:50:07 UTC), and every control gives its
documented verdict in its log. The numbers of the issue:

| item | Windows x86-64 (this run) | stored / the Pi |
|---|---|---|
| lemma S (`sector`) | norm(T0) <= Lambda = 0.1513 < 1, ALL CHECKS PASS | the same; JSON worst relative 1.4e-15 |
| `sector_series` control | lemma S passes: False | False |
| path box, Krawczyk margins | 8.575e-10, 9.717e-10 | 8.562e-10, 9.706e-10 (differs in the 3rd digit, 0.15% and 0.11%) |
| rho_6a on this machine's own box | 0.004220708705 +/- 4.39e-13 | stored 0.004220711508 +/- 1.90e-13; the Pi's 0.004220618728 +/- 2.23e-13 |
| rho_6a on the stored box, on the Pi's box | 0.004220707621 +/- 2.60e-13, 0.004220708705 +/- 4.39e-13 | the Pi on the stored box 0.004220617667 +/- 3.90e-13 |
| `jump_swap` control | fails (underflow at t = 0.08424259629100561), exit 2 | fails (0.08423926215618849) |
| `jump_coords` control | not caught, rho_6a = 0.1222 < 1: True | not caught, as documented |
| covering check on the stored rows and on this machine's own | PASS, 178 tiles, 566, 450 (both) | (178, 566, 450) |
| `cover_sign` control | 0 of 7 discs of row 11 certified | 0 |
| `cover_drop` control | FAIL, 177 tiles, 559, 441, 3 failures | FAIL, the same |

Discrepancies, not fixed:
- The path box's Krawczyk margins, 8.575e-10 and 9.717e-10 against 8.562e-10 and 9.706e-10 (0.15% and 0.11% higher).
- rho_6a differs from the stored value (2.8e-9 absolute, 6.6e-7 relative, own box) and from the Pi's (9.0e-8, 2.1e-5 relative),
  the intervals not overlapping; both below 1, and a bound assembled from upper bounds may differ between builds (AGENTS.md).
- The enclosure radii: `V_rad` 1.0953e-03 against the stored 1.1325e-03 (3.3% lower) and the Pi's 1.1377e-03 (3.7% lower),
  the path point's ball radii 1.06 to 1.20 times the stored (`state_rad` 2.04e-16 against 1.80e-16), the jump's `H_max`
  7.719119720 against the stored 7.719119877 (2.0e-08) and the Pi's 7.719103716 (2.1e-06), the jump's B radius 1.82e-06 against
  the Pi's 1.78e-06, all with the ball midpoints agreeing to 40 characters.
- `jump_swap`'s underflow time differs from the Pi's in the 5th digit, with the same verdict; `cover_control`'s last digits.

## Lemma S, lemma 6a (01:28:17 to 01:41:05 UTC)

Every run exits 0. The controls give their documented verdicts in their logs, read from them (`sector_series` and
`jump_coords` exit 0 by design; `jump_swap` exits 2):

| run | kind | exit | wall (s) | verdict line (from its log) |
|---|---|---|---|---|
| sector | run | 0 | 1 | norm(T0) <= Lambda = 0.1513 < 1: True; ALL CHECKS PASS: True |
| sector_series | ctrl | 0 | 1 | MUTATION series (one coefficient off by a relative 1e-6): lemma S passes: False (must be False) |
| usys | run | 0 | 0 | rhs mismatch 1.9e-58; SysUD lin encloses the derivative: True |
| path_point | run | 0 | 198 | |
| path_box (h = 1e-9) | run | 0 | 195 | |
| path_krawczyk | run | 0 | 0 | K(X) in int X: True; margins 8.575e-10, 9.717e-10 |
| jump (own box) | run | 0 | 68 | rho_6a = 4.221e-03 < 1: True (0.004220708705 +/- 4.39e-13) |
| jump_stored (the stored box) | run | 0 | 68 | rho_6a = 4.221e-03 < 1: True (0.004220707621 +/- 2.60e-13) |
| jump_pi (the Pi's box) | run | 0 | 68 | rho_6a = 4.221e-03 < 1: True (0.004220708705 +/- 4.39e-13) |
| jump_swap | ctrl | 2 | 99 | backward integration failed (step size underflow at t = 0.08424259629100561): lemma 6a NOT established |
| jump_coords | ctrl | 0 | 69 | rho_6a = 1.222e-01 < 1: True [MUTATION coords], not caught, as documented (A_certify.md 11.6) |
| disc | run | 0 | 0 | generic rhs vs lemma6_usys.SysU.rhs: max mismatch 2.4e-59 |
| cover_check_stored | run | 0 | 1 | tiles glued: 178 (meeting sets: 566 polar rectangles, 450 links); LEMMA 6b_1 CHECK: PASS |

The stored covering passes its check on Windows (178, 566, 450, the issue's numbers). The logs of `sector`, `sector_series`,
`usys`, `disc` and `cover_check_stored` equal the Pi's in every line except seconds (0 differing lines).

Against the stored and the Pi's numbers (listed, not fixed):
- The Krawczyk margins of the path box are 8.575e-10 and 9.717e-10 here, against 8.562e-10 and 9.706e-10 on the Pi (and
  the stored): 0.15% and 0.11% higher, from a different enclosure (`path_krawczyk.log` differs from the Pi's in 6 lines:
  J_D(x^) +/- 3.29e-16 against 9.93e-17, K(X) radii 4.25e-11 and 2.84e-11 against 4.38e-11 and 2.94e-11, and the smallest
  passing sub-box's margins 3.27e-13 against 1.69e-13).
- rho_6a: 0.004220708705 +/- 4.39e-13 on this machine's own box and 0.004220707621 +/- 2.60e-13 on the stored box, against the
  stored 0.004220711508 +/- 1.90e-13 (6.6e-7 and 9.2e-7 relative) and the Pi's 0.004220618728 +/- 2.23e-13 on its own box
  and 0.004220617667 +/- 3.90e-13 on the stored (2.1e-5 relative); the intervals do not overlap. A bound assembled from
  upper bounds may differ between builds (AGENTS.md). The log prints 4.221e-03 on all. `lemma6_jump_pi_box.json`, with
  the Pi's box, has the same rho_6a and H_max (7.719119720160961) as the own-box one to every digit.
- `lemma6_sector_1e-9.json` against the stored one: 28 leaves, 12 differ, worst relative 1.4e-15.
  `lemma6_path_point.json`: 40 leaves, the 32 ball strings' midpoints agree to 40 characters, `state_rad` 2.04e-16 against the
  stored 1.80e-16. `lemma6_path_box_1e-9.json`: 58 leaves, the 50 ball strings' midpoints agree to 40 characters, `V_rad`
  1.0953e-03 against the stored 1.1325e-03 (3.3% lower) and the Pi's 1.1377e-03 (3.7% lower), `state_rad` 5.1990e-10
  against 5.1992e-10 (both).
- `jump.log`: max radius of B 1.82e-06 against the Pi's 1.78e-06; `jump_swap.log`: the underflow at t = 0.08424259629100561
  against the Pi's 0.08423926215618849 (both fail, as required); `path_box.log`: the derivative radii 2.32e-06, 2.76e-04,
  1.10e-03 against the Pi's 2.37e-06, 2.90e-04, 1.14e-03.

## Lemma 6b1 (01:41:05 to 01:50:07 UTC)

`cover_check_stored` (above) checked the stored covering first. Then `cover_ray` (32 s, exit 0; `ray.json` present) and the
twelve rows, one at a time with `row --j=J` (no race, no skip), all exit 0, and `cover_check` passes on this machine's own
ray and rows. The controls give their documented verdicts in their logs:

| run | kind | exit | wall (s) | verdict line (from its log) |
|---|---|---|---|---|
| cover_ray | run | 0 | 32 | ray: 452 steps |
| cover_row_00 to cover_row_11 | run | 0 | 74, 63, 57, 50, 48, 40, 34, 29, 26, 21, 20, 18 | the Pi's: 87, 79, 71, 63, 60, 50, 43, ... |
| cover_check | run | 0 | 0 | tiles glued: 178 (meeting sets: 566 polar rectangles, 450 links); LEMMA 6b_1 CHECK: PASS |
| cover_sign | ctrl | 0 | 19 | MUTATION sign (the fast term V_u = +V/2 in the defect): 0 of 7 discs of row 11 certified (must be 0) |
| cover_drop (tiles 5,6) | ctrl | 3 | 0 | tiles glued: 177 (559, 441); LEMMA 6b_1 CHECK: FAIL (3 failures: tile (5, 7) agreement point not in the meeting set, tile (6, 5) meeting set not connected, point (abs(u) = 128.8, arg = phi_5,6) not covered without tile (5, 6)) |
| cover_control | ctrl | 0 | 8 | control disc at 14 e^(-3 i pi/4): certified True at radius 2 (Lam 0.094) and 3 (0.263), False at 4 (1.113), 4.5, 5.5, 6 and 8 (no contraction) |

`lemma6b1_runs_winb/` is this run's own ray and 12 rows (copied by the script), and `lemma6b1_check_1e-9.json` the check's
output. Against the stored covering (`compare_stored.txt`, the Pi's `cmp873.py` run on copies of these outputs with the run
folder under the name `lemma6b1_runs_rpi5b`, so the tool's "Pi" is this run): the ray has 275 leaves and none differs apart
from timings; the twelve rows have the stored discs (178 in all) and steps (789, 717, 657, 579, 558, 461, 402, 350, 316, 275,
268, 249), their largest Lam agree to 8.8e-16 relative (0.172980, 0.173892, ... 0.438972 in row 11) and their box radii
to every printed digit (ratio 1.000), all ok; the check json has 172 leaves, 6 differ (the ray's seconds, 31.6 against
142.5, and the last digit of Lam, 1.3e-15). Against the Pi's own rows (`compare_pi.txt`): the ray equal, the rows with the same discs, steps and box radii (ratio
1.000), and the check json against the Pi's `lemma6b1_check_1e-9_b.json` differing in the rows' box radius by at most
1.9e-08 relative (row 2) and in Lam by 1.8e-15.

`cover_check`, `cover_sign` and `cover_drop` equal the Pi's logs line for line except seconds; `cover_control` differs in the
last digits of three huge Lam (88560013429184.906 against 88560013429184.938, 309863214888001536000 against
309863214888001798144, 4.353276875460278e42 against 4.353276875460279e42).

