# I1021-dh610: boxes 11-31 of #1021's M = 3 recount at xi1 0.17 (argcount 068913b4, --m3fix --retry)

Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021.

Inputs from I1021-mac/split/ (run_dh610.sh, leaves_b*.jsonl, points_M3_r0.17_in.jsonl) and I1021-mac/m3/points_M3_r0.2.jsonl.
One folder per job, b11-15 b16-20 b21-25 b26-31. xfchecks merges them into I1021-mac's records.

`logs/rss_762034.log`: resident size of the b21-25 job's one growing spawn worker (pid 762034), every 5 min from 16:54 UTC (every 30 s before), with the unit's MemoryCurrent; its first line says what each column is.
Caches `b*/points_M3_r0.17.jsonl` are rewritten by argcount after each whole batch of points, so they lag the computation.

Box 21-25 was stopped at 17:49:09 UTC (the coordinator's order, after xfchecks found the stuck point) and rerun from 17:50:10 UTC at wip/argcount-m3-bounds 728f59c7 (worktree `~/Source/choptuik-1021-cap`, unit `i1021-b2125`, no MemoryMax; `I1021-mac/split/rerun_b21-25.sh`) from the same 617-line cache. Its log is `logs/recount_b21-25_728f59c7.log`, its selftests `logs/selftest_728f59c7.log`, its memory log `logs/memlog_1021_b2125.log`. `logs/recount_b21-25.log` (empty) is the first job's, at 068913b4.

Box 21-25 was stopped again at 20:07:02 UTC (the 728f59c7 rerun, noise cap 1e2, 48 new points in its cache; its log `logs/recount_b21-25_728f59c7.log` is kept) and rerun from 20:07:24 UTC at wip/argcount-m3-bounds 998fd290 (noise cap 1e7; worktree `~/Source/choptuik-1021-cap7`, unit `i1021-b2125b`, no MemoryMax; `I1021-mac/split/rerun2_b21-25.sh`, `--retry`, so the points the 1e2 cap left without value are computed again) from the cache of 665 lines. Its log is `logs/recount_b21-25_998fd290.log`, its selftests `logs/selftest_998fd290.log`, its memory log `logs/memlog_1021_b2125b.log`. `logs/rss_b26-31_762039.log` samples two growing workers of the b26-31 job (068913b4).

Box 26-31's 068913b4 job was stopped at 20:11:33 UTC (the coordinator's order; cache 767 lines, 150 new points; its log `logs/recount_b26-31.log` is empty) and rerun from 20:11:50 UTC at 998fd290 (noise cap 1e7, `--retry`, unit `i1021-b2631`, no MemoryMax, `I1021-mac/split/rerun2_box.sh ... 26-31`). Its log is `logs/recount_b26-31_998fd290.log`, its selftests `logs/selftest_998fd290_b26-31.log`, its memory log `logs/memlog_1021_b2631.log`. `logs/rss_workers_1021.log` lists every 10 min the workers of the two jobs still on 068913b4 (b11-15, b16-20) as parent/pid:RSS:cpu minutes.

Box 11-15's 068913b4 job ended exit 0 at 00:26:01 UTC on 20 Nov (35 551 s of recount), which wrote the `end` line of `run_dh610.sh` to `logs/exits.txt`; the b21-25 rerun at 998fd290 was still running then. Its count file is `b11-15/count_M3_cand_r0.17_fix_b11-15.json` and its leaves `b11-15/leaves_M3_cand_r0.17_fix_b11-15.jsonl`. Units `i1021`, `i1021-b2631` and `i1021-b2125b` (running) were the three that held the jobs.

Box 21-25's 998fd290 rerun ended exit 0 at 03:05:47 UTC on 20 Nov (25 101 s of recount, 6 h 58 min wall and 17 h 16 min CPU from the start at 20:07:24 UTC on 19 Nov, `--procs=3`; the journal gives the unit's memory peak as 251 MB), which `logs/exits.txt` records as `b21-25 998fd290 exit 0`; unit `i1021-b2125b` has ended, and all four jobs are done. Its count file is `b21-25/count_M3_cand_r0.17_fix_b21-25_998fd290.json`, its leaves `b21-25/leaves_M3_cand_r0.17_fix_b21-25_998fd290.jsonl` (122 leaves, 10 not resolved) and its cache `b21-25/points_M3_r0.17.jsonl` (1042 lines, 377 of them the rerun's; a point without value is a record with `re` nan). The log `logs/recount_b21-25_998fd290.log` has 377 point lines (8 without value) and, last, the count's summary line.

Follow-ups of boxes 21-25's unresolved cells (the coordinator's hc message of 20 Nov, 03:15 UTC) are in `b21-25-fu/` (its README first): argcount 6da7da7b, steps 2, 1, 3, with the working cache and every row.
