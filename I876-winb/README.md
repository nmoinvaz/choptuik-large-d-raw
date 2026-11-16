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

(the rest of the M = 3 set and the M = 5 set follow)
