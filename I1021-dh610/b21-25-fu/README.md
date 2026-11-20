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
