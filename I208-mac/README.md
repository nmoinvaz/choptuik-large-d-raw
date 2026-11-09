# I208-mac: lemma 6b1(5) rows 1-8 and 10-16 through CAPD, #189's second validated integrator

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1, build 26A434). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/208. Code: solver/proof/review_189/ of main at 188853c, unchanged
(worktree agent-a1cd434a46c3bedb1, branch wip/i208). capd_m5 was rebuilt there with review_189/build.sh and is byte
for byte #189's binary (sha256 64bbc7a94b926b28d8138a3029e2e55f4113515e4e1000c6f24d43c5dcc90c1b). CAPD 6.1.0 at
commit 37057e5899bccaa6cd5701057b7e6ea5e232ef8b, built with -DCAPD_ENABLE_MULTIPRECISION=ON
-DCAPD_INTERVAL_TYPE=NATIVE, against MPFR 4.2.2 and GMP 6.3.0 (Homebrew), Apple clang 21.0.0. Python:
/Users/nathan/venv-qd (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0, mpmath 1.3.0, numpy 2.5.4). At most 2
processes, nice 10. exits.txt has each run's exit status and wall time, scripts/ the shell scripts that ran everything
(W = the review_189 directory, R = this folder).

## Criteria, written before the runs (2026-11-08 23:35 UTC)

1. **Clean rows.** For each row J in 1-8 and 10-16, capd_m5 c0 with --prec=128 --order=32 --tol=1e-26 (as #189 ran
   rows 0 and 9) runs from inputs/start6b1.txt along inputs/path6b1_rowJJ.txt (ray legs 1..J, then row J's arc with a
   stop at each disc time). It passes when `compare.py b1 b1_rowJJ.log ray.json I39-mac/disc_inputs/row_JJ.json
   --expect=overlap` exits 0. That means every one of the 39 real components overlaps at every stop, the ray legs
   against ray.json "starts" and the discs against the disc inputs' Y0 and w, and the CAPD run did not fail. The count
   of the review's enclosures that lie inside the stored ones is reported and is not a pass criterion.
2. **Sign mutation.** capd_m5 with --sign=-1 (the sign of [[C E] P] in V' flipped) on row 1's full path. It passes when
   `compare.py b1 ... --expect=miss` exits 0, that is, when some component misses. #189's mutations compared ray boxes
   only, so this is also the first mutation of the comparison against the disc inputs.
3. **Determinism.** The ray-stop BOX lines of each clean row equal those of I189-mac/b1_clean.log byte for byte
   (scripts/ray_identity.sh with `same`), since capd_m5 starts a fresh solver on every leg. The mutated row 1's must
   differ (`differ`, the control). Before the runs, on I189's logs, row 9 against b1_clean passed `same` and failed
   `differ`, the mutated first leg passed `differ` and failed `same`, and a request for 10 legs from row 9's log failed.
4. **Inputs.** scripts/prep.sh writes inputs/ from the stored files, and its start set and the paths of rows 0 and 9
   are identical to I189-mac/inputs (they are).

A clean row that fails 1 or 3 is a discrepancy. It is reported, not fixed, and the other rows continue. A mutation that
does not miss would mean the comparison against the disc inputs cannot fail, and is reported the same way.

## Contents

- inputs/: capd_m5's inputs from scripts/prep.sh (review_189/export_inputs.py). start6b1.txt is the C^1 start set of
  I38-macm3/lemma6b1_runs_M5_cert/ray.json sets["0"] at s0 = 405 e^{-3 i pi/4}, and path6b1_rowJJ.txt is row J's path
  (exact binary stop times), for J = 0..16.
- b1_rowJJ.log, cmp_b1_rowJJ.{log,json}, rayid_b1_rowJJ.log: row J's CAPD run, its comparison (criterion 1) and its ray
  identity check (criterion 3).
- mut_sign_row01.log, cmp_mut_sign_row01.{log,json}, rayid_mut_sign_row01.log: the sign mutation on row 1.
- scripts/: prep.sh, b1_row.sh (one row, `J` or `J:sign`), ray_identity.sh, pool.sh (the job list jobs.txt, 2 at a
  time), table.py (the per-row table, saved as table.md). pool.log is pool.sh's output.

## Results (2026-11-09 13:32 UTC)

All 48 runs in exits.txt exit 0. The pool ran from 2026-11-08 23:32 to 2026-11-09 13:31 UTC.

1. **Clean rows: every criterion passes.** All 15 rows pass `compare.py b1 --expect=overlap`. Over their 428 stops,
   16692 of 16692 components overlap the stored boxes, and all 16692 of the review's enclosures lie inside the stored
   ones. At the last disc of rows 1-13 the review's radius is about 1e-18 against stored radii of 3e-16 to 1.5e-15.
   The worst midpoint gap is 1.3e-05 of the summed radii (row 3). The gaps are largest on the outer rows 1-5, beside
   rows 0-2, where #39 found the regenerated radii differing from the stored ones by up to 6%. On rows 10-16 the gap
   is 6.0e-08, set by the ray legs. table.md has the per-row numbers.
2. **Sign mutation: it misses, as it must.** On row 1's 36 stops, 36 of 1404 components overlap. The one component that
   overlaps at each stop is w, which is constant along the flow, so every state component misses at every ray stop and
   at every disc.
3. **Determinism: it holds.** Every clean row's ray stops equal #189's b1_clean.log byte for byte (39 to 624 lines). The
   mutated row 1's differ on 38 of 39 lines.
4. **Inputs: identical to I189-mac/inputs.** That covers start6b1.txt and the paths of rows 0 and 9.

With #189's rows 0, 9 and 17, every row of lemma 6b1(5)'s flow has now been reproduced by CAPD, with every component
overlapping and every enclosure inside the stored one. The disc lemma itself was checked by #39, not here.

With its lid closed from 04:03 UTC, the Mac slept during 04:03-06:23, 07:25-07:41, 08:41-08:55, 09:55-10:26,
11:29-11:41 and 12:42-13:12 UTC, waking only briefly within those times (`pmset -g log`). It stayed awake for about an
hour between them. The runs advanced only while it was awake, so the wall times of rows 3, 11, 4, 5, 10, 6, 7 and 8
(7300-11800 s) include sleep. The CAPD step counts are 287-345 per row.
