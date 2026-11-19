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
  the same to 7 digits at rtol 1e-12, 1e-13 and 1e-14, and absent along the r1 = 0.25 path.
- `m1b/lines1.jsonl`, `m1b/lines2.jsonl` (`lines.py`, `anal2.py`): R_1 on lines of w/w_inf at A 0.51, 2.51, 5.01 (and
  5.99) for xi1 0.3, 0.25, 0.2, 0.17, 0.15, with max |Y| on the path. The jumps sit where max |Y| > about 1e2: the path
  passes near a movable singularity of y+. None at 0.17 for A <= 5; at A 5.99 the singularities come inside 0.17, and
  at 0.15 J reaches the double-precision floor (its error is about 4e-16 |Y| at every rtol).
- `m1b/*guard*`: the guard check, A 0.5-0.75, w/w_inf 2.2-2.5. At xi1 0.3 all 8 points have max |Y| > 1e2 (largest
  1.4e5), so no value and 3 unresolved cells; at 0.17 none, and the box resolves.
- `m1b/*pilot_known*`: the known zero's box at xi1 0.17: one zero of sign +1 located at (2.542148, 0.776994), the same at
  0.2.
- `m1b/count_M1_full.json`, `leaves_M1_full.jsonl`, `points_M1_r0.17.jsonl`, `logs/m1b.log` (`run_m1b.sh`, code
  8e770023 of wip/excited-zeros): the count at xi1 0.17 with the guards, 06:52-08:08 UTC. 10 cells of nonzero winding,
  leaf sum -2, 145 unresolved (134 by the rounding floor, at w/w_inf < 1 and A > 2.8; the rest past A 4.75), 14350
  points. The box boundary has points of no value, so its winding is NaN.
- `m1b/count_M1_plant.json`, `leaves_M1_plant.jsonl`: the same with the planted factor at (1.7, 2.1), 08:08-08:16 UTC.
  One more zero, of sign +1, located at (1.700000, 2.100000); the other 10 unchanged; leaf sum -1.
- `run_m1c.sh`, `logs/m1c.log`, `m1b/*_M1_full_r0.2*`, `*_r0.25*`, `*_r0.3*`: the radius ladder, 08:16-08:53 UTC (code
  8cad564f; its waves give the same leaves as 8e770023 on the planted maps and the cached pilot). It recounted the 145
  unresolved cells at xi1 0.2: 15 more zero cells, leaf sum +1, 101 left; at 0.25: none, 89 left; at 0.3: none, 73
  left. The 73 lie at A >= 3.98 (mostly A >= 4.5, area 1.14 of the box's 15.4), all with paths past max |Y| 1e2 at
  0.3: there the rounding floor rises below xi1 0.17 and the singularities come inside 0.2-0.3, so double precision
  does not resolve them.
- `m1b/zeros_M1.md`: the 25 zeros (sum -1) with their locations at each radius. 15 sit at two or three radii within
  1e-5, (3.4077, 0.6150) within 1.6e-4, and 9 at one radius only (6 of them at A >= 4.25).
