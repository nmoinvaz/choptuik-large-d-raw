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

## Result

Every `run` of the two scripts that ran exits 0 (25 in all: `cover_ray` of part a, and 24 of part b), apart from the three
row runs of the race in part a, which `run876b.sh` reran. Every control gives its stated verdict in its log (the 6 of part
b, and the 19 lines of `mutations_M`). The whole of part b took 1 h 18 min 46 s (00:03:13 to 01:21:59 UTC), 1 h 25 min 50 s
from the first start.

| part | result on Windows x86-64 | against the stored file and the Pi |
|---|---|---|
| 6b1(3) covering | check PASS: 183 tiles, 579 polar rectangles, 461 links; the control with tile (11, 0) dropped FAILS with 182, 576, 458; c1check True and its `nov` control outside: True | #849's counts; the logs equal the Pi's except seconds; the rows' JSON differ in their numbers (worst relative 1.9e-2 against the stored x86 rows, 3.6e-4 against the Pi's) |
| step (i), M = 3 | `usys_M`, `fpm_check_m1`, `fpm_M3`, the diag run, the table and data runs all exit 0 | the JSON differ from the stored files by 2.3e-14 at most |
| lemma S, M = 3 | scan and box run pass (contraction 0.8252, Lambda 0.2923) | 3.4e-14 at most |
| 6a(3) at the certificate's box | rho_6a = 4.128e-02 < 1: True | the stored 0.04134615071 +/- 5.3e-13, ours 0.04127932156 +/- 4.95e-12 (0.16%); assembled from upper bounds |
| D, mutations | `disc_M` True, `mutations_M --all`: ALL VERDICTS AS EXPECTED: True | verdicts equal the Pi's; `jump_swap_M3` underflows at t = 0.06813978 against the Pi's 0.06811420 |
| M = 5 | tables, sector (Lambda 0.2979), scan, 6a(5) at p^ rho_6a = 0.2133 < 1, partial, coords (3.249, False) and swap controls fail as stated, `bfloat` 8.71e-08 and its `w` control 226, macm3's B (0.2121) and the Pi's B (0.2125) pass | logs equal the stored ones; JSON within 6.0e-13; B's midpoints equal the Pi's in all 722 strings, its radii differ up to 24% |

Discrepancies, not fixed:
- The race in `run876.sh` (above): its three row runs failed at once; `run876b.sh` corrected it.
- rho_6a differs from the stored value at M = 3 (0.04128 against 0.04135) and from the Pi's at M = 5 (0.2133 against 0.2125);
  an upper-bound assembly, as AGENTS.md says of builds.
- B's radii for M = 5 differ from the Pi's and macm3's by up to 24%, the midpoints not at all.
- The rows' JSON of the covering differ in the numbers other than timings from the stored x86 rows (worst relative 1.9e-2, in
  the `F0` and radius entries of the discs) and from the Pi's (worst 3.6e-4), and `ray.json` differs in 18169 of its 25721
  leaves from the Pi's (18159 of them arb ball strings), while the check's counts and verdicts are the same.
- Double-precision comparisons (`usys_M` (b)) and the upper-bound agreement of `fpm_check_m1` (1e-21 against the Pi's 8e-18)
  differ as in #860; `jump_swap_M3`'s and `jump5_swap`'s underflow times differ from the Pi's (0.058585 against 0.058526).
- `cover_c1check_mut`, `jump5_partial`, `jump5_swap` and `bfloat_w` exit 0 and are read from their logs, as on the Pi.

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
| cover_check_drop11_0 | ctrl | 3 | 0 | | LEMMA 6b_1 CHECK: FAIL (2 failures: tile (11, 1) agreement point not in the meeting set; point (abs(u) = 26.98, arg = phi_11,0) not covered without tile (11, 0)); tiles 182, 576 polar rectangles, 458 links |

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

## The rest of the M = 5 set (#861's list) (00:46:39 to 01:21:59 UTC)

Every run exits 0 (`fpm_table5`, `fpm_data5`, `sector5`, `scan5`, `jump5`, `bfloat`, `jump5_macB`, `jump5_piB`), and the four
controls give their stated verdicts in their logs (`jump5_coords` exits 2, `jump5_partial`, `jump5_swap` and `bfloat_w`
exit 0, as on the Pi). `jump5_macB` and `jump5_piB` load macm3's and the Pi's B; both pass on Windows.

| run | kind | exit | wall (s) | Pi wall (s) | verdict line |
|---|---|---|---|---|---|
| fpm_table5 | run | 0 | 46 | 49 | TABLE: every recommended configuration holds and every control fails: True |
| fpm_data5 | run | 0 | 107 | 112 | start data M 5, ray 5pi/16 r0 0.0622: value radius 3.9e-10 / 3.9e-07 (the Pi's) |
| sector5 | run | 0 | 5 | 5 | ALL CHECKS PASS (M = 5): True; Lambda = 0.2979 < 1 |
| scan5 | run | 0 | 207 | 206 | last row M 5 rp 0.045 k 30: contraction 0.2490 ok True |
| jump5 (6a(5) at p^, saves B) | run | 0 | 1155 | 1574 | rho_6a = 2.133e-01 < 1: True; 615 steps; max radius of B 3.29e-05 |
| jump5_partial | ctrl | 0 | 3 | 4 | G_slow is 13 x 17: not square; lemma 6a NOT established [MUTATION partial: failure expected] |
| jump5_coords | ctrl | 2 | 3 | 4 | rho_6a = 3.249e+00 < 1: False [MUTATION coords] |
| jump5_swap | ctrl | 0 | 561 | 759 | backward integration failed (step size underflow at t = 0.058584731072187424): lemma 6a NOT established [MUTATION swap: failure expected] |
| bfloat | run | 0 | 12 | 15 | max abs(B_float - mid(B)) / rad(B) = 8.71e-08 from p^ and 0.179 from x^ (inside B: must be below 1) |
| bfloat_w | ctrl | 0 | 12 | 15 | the same ratio 226 [MUTATION w: must exceed 1] |
| jump5_macB (macm3's B) | run | 0 | 3 | 4 | rho_6a = 2.121e-01 < 1: True |
| jump5_piB (the Pi's B) | run | 0 | 4 | | rho_6a = 2.125e-01 < 1: True |

Against the stored files (`cmp861.py` of #861 run on this folder, `compare_stored_M5.txt`): the logs of `fpm_table5`,
`fpm_data5`, `sector5` and `scan5` agree with the stored logs in every printed number (0 differing). The JSON outputs
differ in the last digits: `fixed_point_M_table_M5.json` 80 of 340 leaves, worst relative 6.0e-13 (`eta`);
`fixed_point_M_data_M5.json` 7 of 36, worst 5.5e-13; `lemma6_sector_M5_rp0.08_1e-6.json` 60 of 73, worst 5.1e-13, and three
ball strings differ in their radii only (`F_S` +/- 5.49e+24 against 5.46e+24, `Lambda_plain` +/- 6.85e-12 against 6.90e-12,
`Lambda_diag` +/- 1.02e-11 against 1.01e-11; the tool exits 1 on them, as it did for the Pi's run, `I861-rpi5/compare_stored.txt`).
Against the Pi's: `lemmaS_scan_M5.json` 54 of 189 leaves differ, worst 4.7e-11 (`eta`).

The B of this run against the Pi's and macm3's (`compare_B_winb_pi.txt`, `compare_B_winb_mac.txt`, the Pi's tool
`compare_B_pi_mac.py` with winb's B as its first argument, which it labels "Pi", and the other as "Mac"): 361 entries,
615 steps each, the midpoints identical in all 722 printed strings against the Pi's B and in 718 against macm3's (the others
differ by 5.8e-20 relative, as the Pi's differ from macm3's), no ball disjoint from either, and the radii differ: max radius
3.293e-05 against the Pi's 3.248e-05 (ratio 1.014) and macm3's 3.030e-05 (1.087), the entrywise ratios from 0.87 to 1.24
against the Pi's and 0.92 to 1.27 against macm3's (the Pi's against macm3's: 0.925 to 1.119). rho_6a from this B is 0.2133
([0.2133038157 +/- 4.64e-11]) against the Pi's own 0.2125 ([0.2124578258 +/- 4.08e-11]); the bound is assembled from upper
bounds (AGENTS.md), and both are below 1. `centre_passed.txt` has the same six numbers as the Pi's (the Pi's copy in a CRLF
checkout differs only by its line ending).

