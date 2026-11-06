# T121-win2: the elimination corrector's u0 rung polish with refactoring, at T118's stall (D 152.93)

Machine: win2. Comms entry: 2026-11-06 cloud to win2 (T121).

T118 stopped at D 152.93 because the re-seed's quad-double polish of the u0 rung (hp/reseed.py `invert_q`, the rung
u = 0.3) stopped short of 1e-24 on every attempt (4e-22 to 2e-9). `invert_q` factors the quad-double Jacobian once and
stops at the first step that does not halve the residual. `rung_fix_run.py` runs hp/anm_run.py unchanged with
`invert_q` replaced by a version that refactors the Jacobian when a step does not halve the residual (at most 3 times,
REFACTOR_MAX) and prints every iterate. The same test runs on the Mac (coordinator, scratch).

Superseded before it ran by T122-win2 (comms 2026-11-06, cloud to win2): the stall had a second cause, fixed on main
(effab02), so the chain runs on main without this wrapper. Kept for the record of the test.
