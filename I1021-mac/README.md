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
