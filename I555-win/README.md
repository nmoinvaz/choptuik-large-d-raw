# I555-win: OCTO_DOUBLE 5.3 (a) again at D 180.5 on current main

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/555 (recommended by win in #468; the coordinator's message `choptuik-large-d/2026-11-12/044316Z-coordinator-4a90.md`). Worktree `choptuik-i555` at main 810396bc (hp/ is identical to 14dc3863's: no change under hp/src, Cargo, pyproject or hp/*.py between them), venv-t151's hpkernel (the build of #462), 3 threads per command at BelowNormal, each under `I462-win/run_capped.py` with a cap of 7200 s (the 2 h stop condition).

| name | command (from `choptuik-i555/hp`) | input |
|---|---|---|
| planted | `octo_corrector.py planted RAW T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 --out planted` | T129-win2/chain/anm_pin3_D180.5246.npz (sha256 first 16 66a86e436fcfc4ac, equal to origin's) |
| planted_ctrl | the same with `--qd 0 --mutate_offset qd --Delta_ref <the quad-double Delta of planted>` (notes/OCTO_DOUBLE.md 5.3 (c), as in #468) | the same |

**Criteria (the issue's, as `octo_corrector.py planted` judges them, notes 5.3 (a)).** The octo-double pinned max|F| below 1e-40 and |Delta_od - Delta_qd| at most 1e-30 against the quad-double corrector from the same start; the control must fail. The quad-double side reached its floor near 1e-36 here on 2026-11-06 (5.4 (a): 5.46e-30 after step 2, stopped after 12 steps), which fixes its Delta to 1.2e-34; at D 192.0 it stalls at 7.87e-24 (#468). If it stalls again, that is reported as it stands.

## Results (2026-11-12)

| command | started (UTC) | ended (UTC) | exit | verdict | last line |
|---|---|---|---|---|---|
| planted | 04:45 | 05:06:33 | 0 | **pass** | `(a) PASS: od max\|F\| 6.86e-42 < 1e-40, \|Delta_od - Delta_qd\| <= 1e-30` |
| planted_ctrl (`--qd 0 --mutate_offset qd --Delta_ref`) | 05:07 | 06:05:27 | 1 | fails as it must | `(a) FAIL: od max\|F\| 3.39e-12 < 1e-40, \|Delta_od - Delta_qd\| <= 1e-30` |

**planted.** Start 3.39e-12 (truth 2.83e-30). Octo-double: 5 steps, converged, pinned max|F| 6.86e-42, Delta 1.700531269818162204386381037834122353007, 810 s. Quad-double (ElimQ, newton_qd): 12 steps, **stopped** at its own floor, last max|F| 1.04e-36 (octo-double at the projected point 7.88e-37), Delta 1.700531269818162204386381037834122235155, 454 s. |Delta_od - Delta_qd| = 1.1785e-34, within 1e-30. The octo-double distance from the truth state's Delta is 8.5478e-22 (information).

The run reproduces notes/OCTO_DOUBLE.md 5.4 (a), made on 2026-11-06, in every number it prints. Octo-double: 3.39e-12 -> 5.92e-16 (|dz| 1.0e-12), -> 1.63e-31 (7.7e-16), -> 7.61e-22 (6.8e-24), -> 6.86e-42 (6.4e-34), then converged, 5 steps, 3 projections all u0q. Quad-double: 5.92e-16, 1.30e-26, 5.46e-30, 1.32e-20, 5.30e-27, 1.59e-33, 1.69e-36, then 1.4e-36 to 5.8e-37, stopped after 12 steps, as that table has it (the quad-double side reaches only its floor near 1e-36, not its tolerance 1e-45). Both Deltas equal the record's to all 40 digits (octo-double ...122353007, quad-double ...122235155), 1.18e-34 apart, and the octo-double Delta lies 8.5e-22 from the stored state's, as the record says. The record's octo-double time was 1559 s; here 810 s.

**planted_ctrl.** With the held offset taken through the quad-double LU the first Newton step is |dz| 2.2e-6 where the unmutated one is 1.0e-12, no trial step is accepted (`on 0: |F| 3.39e-12, |dz| 2.2e-06: no trial step accepted, stopping`; 6 failed projections), and the run ends at its start, pinned max|F| 3.39e-12, in 3505 s. |Delta_od - Delta_ref| = 8.5478e-22 equals the distance of the truth state's Delta from the root (no step was taken), so the informative failure is the broken first step. The control is in the 5.3 (c) form (`--qd 0 --Delta_ref` the quad-double Delta of planted), as in #468.

Worktree `choptuik-i555` at main 810396bc: no file under hp/src, Cargo, pyproject or hp/*.py differs from 14dc3863, the code of #468 to #514. Unlike D 192.0 (#468), where the quad-double reference stalls at 7.87e-24, this state's reference reaches its floor near 1e-36, so 5.3 (a) as written is valid here.
