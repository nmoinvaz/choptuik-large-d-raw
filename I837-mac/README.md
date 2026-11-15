# I837-mac: planted solves the chain's own system at an eight-part chain state

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/837.

Code: branch `wip/i837` at 1b359232 (on main f44991d5), worktree /Users/nathan/Source/choptuik-large-d-837:
`octo_corrector.truth_system` (used by planted, proj_shift and step_spread), `pinned_o(segs=...)`, an eight-part
`plant_start`. Build: main 3c35f0c's hpkernel (i599/site2). 3 threads, nice 10, one job at a time (queue.sh).

## Plan and criteria (written by 2026-11-15 10:53 UTC, before the queue)

For an eight-part state (`has_o`), `truth_system`'s default builds its chain's system: the state read in eight parts
(`load_o`), the held harmonics held at its own coefficients in eight parts (`band_coeffs(exact=True)`, as
anm_run.py --held_o 1, which #603's chain ran with), and its stored plan (`meta["segs"]`, the 61 steps #603 kept). A
four-part state keeps the old system. Each change has a control that restores the old behaviour: `--read 4`,
`--held float` and `--plan state`.

1. **The truth's residual** at I603-win2's 252.6135 and 240.1244 is at most 1e-55 (3.58e-20 and 2.2e-20 before).
   `step_D252`, `step_D240`: planted --rel 0 --qd 0 --tol 1e-100 --save_dz0, whose start line prints it.
2. **The first Newton step's Delta part from the truth** is below 1e-40. The same runs: --tol 1e-100 forces the
   step, and --save_dz0 prints its dDelta and stops.
3. **The controls**, each with the other two changes in place, must fail bar 1 (residual above 1e-55) at both D:
   `ctl_read4_D*`, `ctl_heldfloat_D*`, `ctl_planstate_D*` (--od 0 --qd 0, the start line only).
4. **The four-part states** reproduce their recorded start lines: T138-win2's 200.0000 (#713's s0_D200: truth
   9.75e-29, start 3.39e-12; and its first step, recorded as |dz| and dDelta in its "on 0" line), T129-win2's 180.5246
   (#504, #523, #555: truth 2.83e-30), I13-win's 192.0000 (#468: truth 7.06e-29, start 3.39e-12).

Pilot (before this plan was written, 10:44–10:51 UTC, `pilot_D252.log`, at d73b4028): at 252.6135 the truth's
residual is 5.5519e-92, and the corrector stops at once as converged (tol 1e-40), so no step was taken. Hence --tol
1e-100 in item 2.
