# I1021-dh610/b21-25-fu: follow-ups of boxes 21-25's unresolved cells (argcount 6da7da7b, --m3fix --retry)

Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021, started 20 Nov 2026
on the coordinator's hc message (the three recommended tasks of comment 7029152417 as #1021 steps, no new issues).

Code: `solver/inner_stokes/argcount.py` at wip/argcount-m3-bounds 6da7da7b (998fd290 plus the seed fix), worktree
`~/Source/choptuik-1021-seed`, python `~/Source/venv-i1026/bin/python`, nice 10, at most 4 processes in total.
Inputs: the b21-25 job's final files in `../b21-25/` (cache `points_M3_r0.17.jsonl`, 1042 lines, leaves
`leaves_M3_cand_r0.17_fix_b21-25_998fd290.jsonl`, seeds `points_M3_r0.2.jsonl`), unchanged. The working cache here
starts as a copy of that cache.

Steps, in the coordinator's order: step 2 (the sign +1 zero in A 3.7873-3.9123, w/w_inf 0.3065-0.4065), step 1 (the four
points without value and the three boxes whose boundary winding is nan), step 3 (the five unresolved cells of
w/w_inf 0.4065-0.5065). The 10 sigma guard stays: it is the false-acceptance control. A point is valued again from a
different start (radius order, seed neighbour) and a larger right-hand-side bound (`fu_value.py`); one that no variant
values is reported with its cause. A value is taken into the cache only if |R| >= 10 sigma, the continuation accepts it,
and its F_3 is within 0.1 of a valued neighbour's (one sheet, as `sheet_connect.py` of I1021-mac reads it). Then the
step's cells are recounted from that cache with `--retry`.

Files (filled as the steps run; the table is updated at each post):

| file | what |
|---|---|
| `fu_value.py` | values listed points with the variants, applies the guard and the sheet test, appends accepted records; `--selftest` (and its `--break` control), `--retest ... --mutate f3 or lowguard` |
| `run_fu1021.sh` | the driver: `run_fu1021.sh 0 2 1 3` (selftests, then steps 2, 1, 3), writes `exits_fu.txt` and `logs/` |
| `cells_step2.jsonl`, `cells_step1.jsonl`, `cells_step3.jsonl` | the unresolved cells of the b21-25 job's leaves file that each step takes (2, 3 and 5 cells) |
| `points_M3_r0.17.jsonl` | the working cache (copy of `../b21-25/points_M3_r0.17.jsonl`, 1042 lines at the start, appended by the steps) |
| `seeds_b21-25_r0.2.jsonl` | copy of `../b21-25/points_M3_r0.2.jsonl` (seeds, as in the job's `--seed`) |
| `fu_append.py` | appends one point's valued record from another cache to the working cache, with `fu` naming the source; prints |R|/sigma and the |F_3| steps to the four nearest valued neighbours (it does not judge the sheet or the noise cap: the merge does) |
| `exclude_points.txt` | the two points `fu_value.py` does not value (3.6623456, 0.20654321) and (3.6623456, 1.06904321), added 03:18 UTC on the coordinator's word (xfchecks has them valued in other caches); superseded: the coordinator then said to take both from caches, see below |

Records taken from other caches (the coordinator's word, 20 Nov, 03:19 UTC: so that the nan boxes can finish; the merge's noise-cap and sheet checks judge them):

| point | source | taken at | record |
|---|---|---|---|
| (3.6623456, 0.20654321) | `I1021-dh610/b11-15/points_M3_r0.17.jsonl` line 661 (the 068913b4 job, continuation from 0.25) | 03:19 UTC, `logs/append_A3.6623456_w0.20654321.log` | \|R\| 7.15e5, sigma 4.54e3 (157.6 sigma), noise_3 180.3, F_3 -0.0023-0.5336i; |dF_3| to the four nearest valued neighbours 0.063 to 0.087 |
| (3.6623456, 1.06904321) | `I1021-mac/fu_seed/point_3.6623456_1.06904321.jsonl` at raw 8934514e (xfchecks: line 889 of `I1021-mac/fix2931/points_M3_r0.17.jsonl`, 998fd290, `--m3starts=0.2,0.25`, cap 1e7; sha256 dada230ae3a6ace43887503bae5510b85189c1ca854f995d9e314250d00c0c75, checked); a copy is `from_xfchecks_point_3.6623456_1.06904321.jsonl` | 03:20 UTC, `logs/append_A3.6623456_w1.06904321.log` | \|R\| 6.15e5, sigma 2.98 (206 536 sigma), \|r_3\| 1.26e-6, noise_3 3.5e-6, trail 0.2 to 0.17, F_3 0.0055-0.1418i; \|dF_3\| to the four nearest valued neighbours 0.0025 to 0.0078 |
