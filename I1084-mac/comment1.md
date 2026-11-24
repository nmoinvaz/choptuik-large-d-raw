**Floor criterion from data, before the change** (Mac, subagent of t5, 2026-11-24 17:28 UTC)

**Method.** The old code (feat/inner-mp 6b807830, `value_mp.py` and `inner_mp.py` as is) run under wrappers that log every residual call and, at every Jacobian refresh, form the step the previous Jacobian would have taken from the same v (one more `lu_solve`, no residual call) and compare its bits with the fresh step's. Point p1: #1076's cached point A 3.642554027092, wf 0.345236176729 (raw 110637ab, `I1021-dh610/fu022mp_m3mp/m3/points_M3_r0.17.jsonl` line 3763, F_3 start from line 3753), `value_point(..., iters=12)` as `argcount --m3mp` calls it. 892 s, calls [19, 13]. The M = 5 centre is read from the `VALUE_MP_PROGRESS` log of the brief.

**p1 (M = 3), dps 34**, steps after the start (max|r| 1.69 at the float64 F_3):

| step | max\|r\| before → after | ratio | Jacobian | result |
|---|---|---|---|---|
| 1 | 1.69 → 7.79e-7 | 4.6e-7 | fresh | accepted |
| 2 | 7.79e-7 → 6.92e-13 | 8.9e-7 | chord | accepted |
| 3 | 6.92e-13 → 7.88e-19 | 1.1e-6 | chord | accepted |
| 4 | 7.88e-19 → 3.38e-19 | 0.43 | chord | accepted, refresh due |
| 5 | 3.38e-19 → 1.05e-19 | 0.31 | fresh (\|dJ\|/\|J\| 9.5e-7; step 1944 and 126945 ulps from the stale one's) | **accepted**, refresh due |
| 6 | 1.05e-19 → 9.66e-19 | 9.2 | fresh (\|dJ\|/\|J\| 1.6e-14; the stale step's bits) | failed: end |

**p1, dps 42** (start 3.92e-19 with the dps-34 Jacobian): 4.92e-27 (chord, accepted), 1.04e-27 (chord, 0.21, refresh due), 5.32e-28 (fresh, 0.51, **accepted**; \|dJ\|/\|J\| 5.7e-14, the stale step's bits), 1.40e-27 (fresh, \|dJ\|/\|J\| 7.1e-22, the stale step's bits, failed: end).

**M = 5 centre** (log): dps 34: 3.45e-25 → 8.12e-25 (chord, failed), refresh, 8.12e-25 again (fresh, failed: the same value, so most likely the same v to the bit). dps 42: 4.42e-33 → 3.61e-33 (chord, 0.82, accepted), refresh, 1.18e-32 (fresh, failed).

**What this shows**
1. The premise holds at the M = 5 centre (both fresh steps after the floor refresh failed) but **not at p1**: there the fresh step after a floor refresh was accepted twice (dps 34 step 5, dps 42 step 3). At the floor the steps are draws of the rounding noise, and the old solve keeps a lucky one. Ending the solve at the floor without the refresh returns another v, R and r whenever the fresh step would have taken a different v.
2. The floor is not one residual level: about 1e-19 at dps 34 for p1 (A 3.64) and 3e-25 for the M = 5 centre (A 2.73). The M = 5 centre's progress step 1.02e-20 lies below p1's floor, so no 10^-(dps-k) separates floor from progress at both.
3. What decides whether a refresh can be skipped with the result unchanged is whether the fresh Jacobian's step rounds to the same v as the stale one's. At p1 it did for the three refreshes whose stale Jacobian was itself formed at a floor (\|dJ\|/\|J\| 1.6e-14, 5.7e-14, 7.1e-22: 0 ulps apart) and not for the one whose Jacobian came from the start (9.5e-7: 1944 and 126945 ulps).

**Criterion (implemented next).** In a solve whose Jacobian is not used afterwards (the second precision; `single=True` without `want_J`), a due refresh is skipped when the predicted shift between the two steps, \|J⁻¹\|∞ (n·16·max\|r\|_J / h_J + 10·\|J\|∞·max_k \|v_k − v_J,k\| / \|v_k\|) \|dv\|∞ / ulp(v_k), is at most 0.01 ulp. The first term is central-difference noise from the residual at the Jacobian's base point, the second its drift. The stale step then stands for the fresh one, and its failure ends the solve. The first precision keeps every refresh, since its Jacobian starts the second precision and enters sig's dr1. A failed step that is retried to the bit after a refresh costs no call. `--floor=0` or `VALUE_MP_FLOOR=0` runs the old solve, call for call. The result is unchanged unless a rounding boundary falls inside the predicted shift: the probability is at most the shift per component.

**Expected gain.** Small at M = 3: the first precision keeps its refreshes, and whether the second precision's refreshes pass the 0.01-ulp test there is what the runs will show (each refresh logs its predicted shift). The 2(M−1)+1 calls per precision that the issue hoped for at M = 3 are not available without accepting changes in the last digits (info, sig, and R within sig). The M = 5 centre's dps-42 refresh (8 calls) is the case it targets. Old and new runs on three #1076 points and the M = 5 centre follow.
