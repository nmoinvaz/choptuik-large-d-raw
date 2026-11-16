# I875-mac: #852's horizon contraction from the re-converged root at D 240.1244

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/875

Code: hp/step_spread.py at main 2283596e (`--steps`), on main 3c35f0c's hpkernel, from the wip/xf-874 worktree. One
process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: #874's
`I874-mac/anm_pin3_D240.1244_u2.npz` in `truth_system`. Runs in `queue.sh` order, after I857-mac's queue.

Done: 2026-11-16 03:20 to 04:38 UTC. C1 to C3 pass; C4 is reported below.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes (the unperturbed dΔ at #874's state, from `I874-mac/check_u2.json`) | the unperturbed step changes |
| C2 | `gain.py --selftest` passes (a planted quadratic gain passes; one with #852's linear gain 9.306e3 fails), and `gain.py` on #852's `steps_D240.json` FAILS (it does: gain 9.3060e3 at 1e-96) | the check misreads a planted case or passes #852's |
| C3 | the prediction, at the first step: gain e_1 / e_0 below 1 at 1e-96 and above 1 at 1e-90, and gain / rel at 1e-90 within 10% of 7.5556e92 | any of the three fails |
| C4 | reported: the unperturbed path's own steps from #874's state, and e_2 | (the floor) |

## Result

From #874's re-converged root, the first Newton step's gain on an m_h, a_h move is purely quadratic. gain / rel is
7.5556e+92 at rel 1e-90 and at 1e-93, #852's excess to −6.086e-06 of it. At 1e-96 the gain is 1.9861e-03, below 1,
where e_1 is the step's own floor. #852's gain less #875's is +9.3060e+03 at all three rels, so #852's linear gain of
9.306e3 was the stored truth's offset, its cross term, and none of it is left at the root.

## Acceptance

| # | verdict | numbers (logs and `tables.md`) |
| --- | --- | --- |
| C1 | pass | `--ref` equal: the unperturbed dΔ 5.744294532362707e-103 (`steps_u2.log`) |
| C2 | pass | `gain_selftest.log` PASS (the planted quadratic gain passes, the one with 9.306e3 on top fails at 1e-96 and on gain / rel); `gain_ctl852.log` FAILS (gain 9.3060e+03 at 1e-96, gain / rel +1.232e+01 off) |
| C3 | pass | gain 1.9861e-03 at 1e-96 (< 1), 7.5556e+02 at 1e-90 (> 1); gain / rel at 1e-90 7.5556e+92 against 7.5556e+92, −6.086e-06 (within 0.1) |
| C4 | reported | the unperturbed path's steps 1.5634e-99 and 2.8286e-99 of max\|z_h\| (max\|F\| before them 5.4062e-94, 4.5783e-94; 6.6719e-94 at u_2); e_2 3.0684e-99, 8.8728e-100, 1.3679e-99 at rel 1e-90, 1e-93, 1e-96 |

## Readings (`tables.py`, `tables.md`)

- **The quadratic part.** e_1 / e_0² is 7.5556e+92 at rel 1e-90 and 1e-93. At 1e-96 it reads 1.9861e+93, because
  e_1 there, 1.9861e-99, is the size of the unperturbed path's own steps (1.5634e-99, 2.8286e-99), not of the move.
- **The second step.** Every path is at the floor after it: e_2 is 3.0684e-99, 8.8728e-100 and 1.3679e-99, the size
  of the unperturbed path's steps. At 1e-90, where the first step grew the move 755 times, the second removed it.
  `step_spread` reads 1e-90 as "does NOT contract" because e_1 > e_0, as the issue expects there.
- **The cross term.** #852's gain from the stored truth less #875's from u2 is +9.3060e+03 at rel 1e-90, 1e-93 and
  1e-96, the same at each rel to the printed digits. So the truth's offset adds a gain linear in the move and
  independent of rel, as −J⁻¹F''(·, d0) does, and the quadratic part is the same from both starts. #857 found the
  same split for a Δ move (I857-mac, +8.324447e-02 of the move).
- **The code.** These runs used #874's code (wip/xf-874, main 2283596e and 28763c87), which reads u2 with held values
  recomputed from u2 itself. They differ from the truth's by at most 1.767e-100 (I874-mac/check_u2.json); #884, which
  changes this, is deferred.

## Discrepancies

None against the criteria.

## Recommended tasks

None.

## Files

- `queue.sh`, `run.sh`: the runs, in order. `steps_u2.json`, `steps_u2.log`: the step_spread run.
- `gain.py`: the C2 and C3 check, with `--selftest`. `gain.log`, `gain_selftest.log`, `gain_ctl852.log`.
- `tables.py`, `tables.md`: the readings above, from the JSONs (`python3 tables.py`).
