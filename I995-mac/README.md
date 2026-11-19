# I995-mac: adaptive winding counts of the M = 1 and M = 3 selection multipliers, searching for excited echoing zeros

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/995.
Code: `solver/inner_stokes/argcount.py` on branch `wip/excited-zeros` of choptuik-large-d at 22835e34 (from main 005b99f3),
`/Users/nathan/venv-314/bin/python`, nice 10, 2 worker processes.

## Criteria (the issue's, fixed before the first count, 2026-11-19 01:31 UTC)

- The counter's selftest passes, and its two mutations fail (nosplit misses a close pair of opposite sign, conj flips every sign).
- The known zeros are found: M = 1 at (A, w/w_inf) = (2.5421480, 0.7769940), M = 3 at (2.7264759, 1.0156031).
- A planted factor (A - A0) + 2i (w/w_inf - wf0) is counted: one more zero of sign +1 at (A0, wf0) = (1.7, 2.1).
- Any further zero at M = 1 must reappear at M = 3 within the shift the known zero shows (A 2.542 -> 2.726,
  w/w_inf 0.777 -> 1.016). A zero that does not is reported as an M = 1 artefact of truncation, not as a solution.
- Every count reports the winding of the whole box's boundary, the sum over the leaf cells (which must agree), and
  every cell left unresolved (an edge piece below 1e-5 with a phase step still >= 0.5 rad, or a failed evaluation).

## Runs

- M = 1 over A 0.5-6, w/w_inf 0.2-3 (base grid 22 x 28), then the same with the planted factor (cache reused).
- M = 3 in boxes around the known zero and around each M = 1 candidate's shifted position. The full M = 3 box is a
  runner job (about 7.5 s a point).

## Results

- `m1/count_M1_full.json`, `m1/leaves_M1_full.jsonl`, `m1/points_M1.jsonl` (18643 points), `logs/m1_full.log`: the
  first M = 1 count at r1 = 0.3, 01:31-04:09 UTC on 2026-11-19. **Not usable as a count:** boundary winding 0 and leaf
  sum 0, but 397 of 2635 leaf cells unresolved, among them 51 of the 55 cells of nonzero winding and the known zero's
  cell. R_1 computed along the r1 = 0.3 path jumps between nearby w/w_inf (A 0.5123456, w/w_inf 2.351404 to 2.351410),
  the same to 7 digits at rtol 1e-12, 1e-13 and 1e-14, and absent along the r1 = 0.25 path. Being diagnosed (#995).
