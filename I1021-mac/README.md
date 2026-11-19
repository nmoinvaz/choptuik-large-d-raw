# I1021-mac: M = 3 points argcount could not value in #1013's candidates' box, their cause and a way to value them

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021.
Code: `solver/inner_stokes/argcount.py` on branch `wip/excited-zeros-m3` of choptuik-large-d at 068913b4 (from
wip/excited-zeros fc7dee4d), `/Users/nathan/venv-314/bin/python`, nice 10, 2 worker processes.

Inputs, copied from I1013-dh610/m3 (f9e4bea4): `leaves_M3_cand_r0.25.jsonl` (its 32 unresolved cells are the ones
recounted), `points_M3_r0.17.jsonl` (the cache at xi1 0.17; `points_M3_r0.17_I1013.jsonl` is the untouched copy) and
`points_M3_r0.2.jsonl` (seeds and the relocation cache at 0.2).

Criteria (the issue's, fixed before the runs): the selftest and its mutations pass as before; every point valued in
I1013's 0.17 file keeps its record bit for bit; a planted zero (sign +1 at A 3.53, w/w_inf 0.555, inside the cell
A 3.4123-3.6623, w/w_inf 0.5065-0.6065) is counted; the recount of the 32 cells at xi1 0.17 leaves 0 unresolved, or
a cause is named for those left.

Split (proposed 2026-11-19 14:30 UTC, used only on the coordinator's go): the recount had done boxes 0-6 of the 32
(the unresolved cells in file order). `split/points_M3_r0.17_in.jsonl` is the live cache's 617 complete lines at
14:30 UTC (its first 214 lines are I1013's file). Boxes 7-10 (`split/leaves_b07-10.jsonl`) stay on the Mac, and
boxes 11-31 go to dh610 as four jobs (`split/run_dh610.sh`, raw I1021-dh610). Every part starts from a cache that
holds all of I1013's points, and with --retry it computes only points without value, so it never computes a valued
I1013 point again. The parts are merged into one cache, where a later record never replaces a valued one, and then
recounted over all 32 boxes on the Mac at 068913b4 from the merged cache.

Mac part (boxes 7-10, `run_b07-10.sh`): restarted 14:33:17 UTC, ended 19:36:28 UTC with exit 0. Its 432 new points
are all valued by the continuation. Boxes 7-10 resolve with 0 unresolved cells (136 leaves after 44 splits,
`m3/count_M3_cand_r0.17_fix_b07-10.json`). Box 7 holds a zero of sign -1, located at A 3.245478, w/w_inf 0.345851;
the locate at xi1 0.2 did not find it. Bit checks (`argcount_samebits.py`, 3a76a2f9): I1013's 161 valued points and
the split input's 562 keep their records, PASS; the `--mutate=flip` control exits 1.
