# I876-winb: Theorem A's M = 3 lemma set and the rest of the M = 5 set on Windows x86-64

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/876.
The commands are the coordinator's scripts `run876.sh` and `run876b.sh` (in this folder), run in Git Bash from
`solver/proof/` of the worktree `choptuik-i876` at main 2d631290 (it contains 7fefa82e), with the venv `venv-choptuik-314`
(Python 3.14.10, python-flint 0.9.0 with FLINT 3.6.0, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0; `env.txt`), at below-normal
priority, `PYTHONUTF8=1`. The inputs of the M = 5 part (`I103-macm3`, `I184-macm3`, `I861-rpi5`) are read from a separate
worktree of raw main 07169c6f. `exits_876.txt` has each run's exit code and wall time (UTC); lines of `run876b.sh` start with
`876b`. In both scripts only the RAW path line was changed (WT and PY were already this machine's): `run876.sh` as placed has
md5 e02b5615aa6313ea4f9e0723315eca63 and mine 882667266ce869fafd70a69acbdc475d; `run876b.sh` as placed has md5
17dd718e3041297c032009cb40782083 and mine ee82eb0c42b72bf8316ac54fffe4b320.

## The race in run876.sh (a discrepancy of the script, not fixed in it)

`run876.sh` started the three row runs beside `cover_ray`, but the rows read `lemma6b1_runs_M3_winb/ray.json`, which the ray
run writes, so they failed at once (the logs are kept as `part_a_failed_cover_rows_a.log`, `..._rows_b.log`,
`..._row11.log`, each ending in `FileNotFoundError: ... lemma6b1_runs_M3_winb\\ray.json`):

```
876 cover_ray start (run) 2026-11-15 23:56:09 UTC
876 cover_rows_a start (run) 2026-11-15 23:56:09 UTC
876 cover_row11 start (run) 2026-11-15 23:56:09 UTC
876 cover_rows_b start (run) 2026-11-15 23:56:09 UTC
876 cover_rows_a exit 1 wall 0 s (run) 2026-11-15 23:56:09 UTC
876 cover_rows_b exit 1 wall 0 s (run) 2026-11-15 23:56:09 UTC
876 cover_row11 exit 1 wall 0 s (run) 2026-11-15 23:56:09 UTC
876 cover_ray exit 0 wall 202 s (run) 2026-11-15 23:59:31 UTC
```

#849's first pass on the Pi did the same (its rows exit 1 at once, `cover_check` exit 3, rows rerun as the `_b` logs). I
stopped the driver a few minutes in, left the `cover_ray` run going, and it ended with exit 0 after 202 s at
23:59:31 UTC, with `ray.json` present (2320678 bytes; its exit line was still written by the surviving subshell).
`run876b.sh` (the coordinator's correction) then checked `ray.json`, copied it to `ray_from_part_a.json`, ran row 11 and
the two row groups in parallel from 00:03:13 UTC, and continued as `run876.sh` from `cover_check` on. Nothing else ran
between.

## Covering of lemma 6b1(3) at the certificate's box, tag `_winb` (00:03:13 to 00:29:00 UTC)

All of `cover_row11`, `cover_rows_a`, `cover_rows_b`, `cover_check` and `cover_c1check` exit 0. The two controls give their
verdicts in their logs.

| run | kind | exit | wall (s) | Pi wall (s, #849 `_b`) | verdict line |
|---|---|---|---|---|---|
| cover_ray (run876.sh) | run | 0 | 202 | 263 | |
| cover_row11 | run | 0 | 216 | 255 | |
| cover_rows_b | run | 0 | 1248 | 1504 | |
| cover_rows_a | run | 0 | 1509 | 1829 | |
| cover_check | run | 0 | 1 | | LEMMA 6b_1 CHECK: PASS; ray: 903 steps; tiles glued: 183 (meeting sets: 579 polar rectangles, 461 links) |
| cover_c1check | run | 0 | 18 | 17.3 | C1 PLANTED TRUTH: every point inside its set: True |
| cover_c1check_mut (nov) | ctrl | 0 | 18 | 17.3 | MUTATION nov: every off-centre point outside: True (must be True); every off-centre point prints OUT |
| cover_check_drop11_0 | ctrl | 3 | 0 | | LEMMA 6b_1 CHECK: FAIL (2 failures: tile (11, 1) agreement point not in the meeting set; point (|u| = 26.98, arg = phi_11,0) not covered without tile (11, 0)); tiles 182, 576 polar rectangles, 458 links |

The counts are #849's (183 tiles, 579 pieces, 461 links, and 182, 576, 458 with the tile dropped). `cover_c1check_mut` exits 0 by
design, as on the Pi, and its verdict is the line in its log. The logs of the check, `cover_c1check` and both controls
agree with the Pi's `_b` logs line for line except the seconds printed (`cover_check` and `cover_check_drop11_0` differ in
2 lines each, only in seconds; the other two are identical). `lemma6b1_runs_M3_winb/` is the covering's own rows and ray (`ray.json`,
`row_00.json` to `row_11.json`), and `lemma6b1_check_M3_winb.json` the check's output.

## Step (i), lemma S, D, the mutations and lemma 6a(3) at M = 3 (00:29:01 to 00:46:39 UTC)

Every run exits 0 (the 11 below, and the covering's), and no log has a Traceback besides the three failed rows of the
race. `mutations_M --all` prints ALL VERDICTS AS EXPECTED: True, with each of its 19 lines as stated:

| run | exit | wall (s) | verdict line |
|---|---|---|---|
| usys_M | 0 | 1 | ALL SELF-TESTS PASS: True |
| fpm_check_m1 | 0 | 3 | M = 1 REPRODUCES fixed_point.py: True |
| fpm_M3 | 0 | 1 | fixed point exists and is unique in the ball: True; abs(eta) <= 2.10e-27 |
| fpm_M3_diag | 0 | 2 | fixed point exists and is unique in the ball: True; abs(eta) <= 5.91e-17 |
| fpm_table_M3 | 0 | 14 | `fixed_point_M_table_M3.json` |
| fpm_data_M3 | 0 | 24 | `fixed_point_M_data_M3.json` |
| sector_scan_M3 | 0 | 104 | `lemmaS_scan_M3.json`; the last row M 3 rp 0.045 k 30: contraction 0.1710 ok True |
| sector_M3 | 0 | 2 | ALL CHECKS PASS (M = 3): True (rp 0.1, k 20: contraction 0.8252, Lambda 0.2923) |
| disc_M | 0 | 2 | M = 1 REPRODUCES lemma6b1_disc: True |
| mutations_M | 0 | 528 | ALL VERDICTS AS EXPECTED: True |
| jump3 (6a(3) at A_M_6a_M3_1e-10_in.json) | 0 | 378 | rho_6a = 4.128e-02 < 1: True => all J_D,mu(0.3) = 0 implies psi = 0 (whole jump): True |

`mutations_M` verdict lines (each OK): fp_series_M3, fp_series_M5, fp_cdrop_M3 (the lemma holds: False, must be False), fp_diagpath_M3
(refused), fp_control_r0 (exit 2, fixed point exists: False), fp_m1 (True), usys_label (caught), usys_clean (True),
S_series_M3 (lemma S holds: False), S_control_rp (exit 2, ALL CHECKS PASS: False), disc_m1 (True), cover_check_M3 (PASS),
cover_drop_M3 (exit 3, FAIL with 3 failures), cover_sign_M3 (0 of 12 discs of row 11 certified, must be 0), c1_truth_M3
(True), c1_nov_M3 (every off-centre point outside: True), jump_partial_M3 (G_slow is 9 x 11, not square, caught),
jump_swap_M3 (backward integration failed, step size underflow at t = 0.06813978124409914, caught), jump_coords_M3 (report
only, rho_6a = 8.916e-01 < 1: True, a pilot).

Against the stored files (`solver/proof/lemmas_M_runs/`; the timing fields left out, "worst" the largest relative difference):

| output | leaves | differing | worst | against |
|---|---|---|---|---|
| fixed_point_M_table_M3.json | 285 | 67 | 2.3e-14 (`eta`) | stored |
| fixed_point_M_data_M3.json | 32 | 6 | 2.3e-15 | stored |
| lemmaS_scan_M3.json | 189 | 53 | 3.4e-14 | stored |
| lemma6_sector_M3_rp0.1_1e-6.json | 55 | 39 | 1.3e-14 (the 7 ball strings agree to 40 characters) | stored |
| lemma6a_M3_cert.json | 13 | 3 | rho_6a [0.04127932156 +/- 4.95e-12] against the stored [0.04134615071 +/- 5.30e-13] (0.16%, the intervals do not overlap), H_max 11.563 against 11.592 (0.25%), G_slow^-1 max 1.61894 against 1.61932 | stored |
| lemma6b1_check_M3_winb.json | 159 | 33 | 9.0e-03 (the radii of the C1 ray's state sets, 1.27e-08 against 1.26e-08), against the Pi's `_rpi5_b`: 6.7e-06 | stored `_cert`, and the Pi's |

The logs agree with the Pi's #849 logs line for line except seconds in `fpm_M3`, `fpm_M3_diag`, `sector_M3` and `disc_M`
(0 lines), `fpm_table_M3`, `fpm_data_M3` and `sector_scan_M3` (seconds only), and in these:
- `usys_M`: (b) 3.5e-16 (M = 3) and 1.4e-15 (M = 5) against the Pi's 6.1e-16 and 8.7e-16 (a double-precision comparison).
- `fpm_check_m1`: the upper bounds of fixed_point.py and fixed_point_M.py agree to relative 1e-21 here against 8e-18 and 7e-17
  on the Pi.
- `mutations_M`: the seconds, and `jump_swap_M3`'s underflow at t = 0.06813978124409914 against the Pi's 0.06811420060694218
  (both caught).
- rho_6a is assembled from upper bounds (AGENTS.md), so its difference from the stored value is expected of a different
  build; both are 0.041 and below 1.

(the M = 5 set follows)
