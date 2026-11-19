# I1021-dh610: boxes 11-31 of #1021's M = 3 recount at xi1 0.17 (argcount 068913b4, --m3fix --retry)

Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021.

Inputs from I1021-mac/split/ (run_dh610.sh, leaves_b*.jsonl, points_M3_r0.17_in.jsonl) and I1021-mac/m3/points_M3_r0.2.jsonl.
One folder per job, b11-15 b16-20 b21-25 b26-31. xfchecks merges them into I1021-mac's records.

`logs/rss_762034.log`: resident size of the b21-25 job's one growing spawn worker (pid 762034), every 5 min from 16:54 UTC (every 30 s before), with the unit's MemoryCurrent; its first line says what each column is.
Caches `b*/points_M3_r0.17.jsonl` are rewritten by argcount after each whole batch of points, so they lag the computation.

Box 21-25 was stopped at 17:49:09 UTC (the coordinator's order, after xfchecks found the stuck point) and rerun from 17:50:10 UTC at wip/argcount-m3-bounds 728f59c7 (worktree `~/Source/choptuik-1021-cap`, unit `i1021-b2125`, no MemoryMax; `I1021-mac/split/rerun_b21-25.sh`) from the same 617-line cache. Its log is `logs/recount_b21-25_728f59c7.log`, its selftests `logs/selftest_728f59c7.log`, its memory log `logs/memlog_1021_b2125.log`. `logs/recount_b21-25.log` (empty) is the first job's, at 068913b4.
