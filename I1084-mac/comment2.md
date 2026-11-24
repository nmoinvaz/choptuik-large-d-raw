**Progress** (Mac, 2026-11-24 17:57 UTC). Branch `wip/value-mp-floor` at d2a126e1: d598b328 (value_mp: the guarded skip of the criterion above, and the free retry of a failed step) and d2a126e1 (`value_mp_floor_check.py`).

**Old code on p2 and p3** (same method as p1; raw 110637ab cache lines 3828 and 3792): the same pattern as p1.

| point | precision | floor steps (max\|r\| before → after, Jacobian, result) | refreshes at the floor: \|dJ\|/\|J\|, fresh step vs stale step |
|---|---|---|---|
| p2 | 34 | 2.34e-20 → 5.46e-20 chord FAILED; 2.34e-20 → 2.07e-20 fresh **accepted**; 2.07e-20 → 3.52e-20 fresh FAILED | 1.7e-7: bits differ (40, 2902 ulps); 3.4e-15: same bits |
| p2 | 42 | 2.65e-28 → 2.73e-28 chord FAILED; the same step again after the refresh, FAILED | 5.0e-15: same bits (the same residual is computed twice) |
| p3 | 34 | 6.60e-20 → 1.90e-20 chord (0.29); 1.90e-20 → 1.82e-20 fresh **accepted**; 1.82e-20 → 2.64e-20 fresh FAILED | 3.7e-7: bits differ (19, 2492 ulps); 5.7e-15: same bits |
| p3 | 42 | 1.97e-28 → 3.22e-28 chord FAILED; the same step again after the refresh, FAILED | 7.3e-15: same bits |

Calls [19, 13], [19, 8], [19, 8] and 892, 790, 861 s for p1, p2 and p3. At all three points the first floor refresh of the first precision (Jacobian from the start) changes the step, and its fresh step is accepted. Ending the first precision there would change v, R and r. Every other floor refresh gives the stale step's bits.

**Check (c)**, `value_mp_floor_check.py` (planted residual: a smooth map with a known zero plus noise drawn from the bits of v, run through `value_mp.solve`, `value_v` and `zero_mp.newton` unchanged, with and without the floor stop). It passes with exit 0. On the eight value_v runs at M = 3 and 5 the rows are identical, there are 10 skipped refreshes, and the calls drop from 260 to 193. The solve from a far Jacobian is identical, and the guard refused 2 skips there. zero_mp's M = 5 walk gives identical rows. Controls: `--mutate=off`, `tau-low`, `tau-high` (FLOOR_TAU inf) and `keepj` each exit 1. `zero_mp.py selftest` exits 0 and `--mutate=sign` exits 1, as before (zero_mp.py is unchanged and its selftest does not call value_mp).

**Side note (not part of this task).** The Mac's old-code rows differ from dh610's cached rows for the same keys, by |ΔR|/|R| 9.7e-5 (p1), 3.9e-4 (p2) and 3.2e-13 (p3), all far above sig (about 1e-17). The cache stores the key rounded to 12 decimals (`argcount.mp_batch` writes `A=k[0]`), while `value_mp` ran at the walk's float point. That is the likely cause (unverified), so the old-vs-new comparison uses the Mac's own old-code runs.

New-code runs on p1–p3 and the M = 5 centre are running.
