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

## Results (2026-11-15 11:57 UTC)

**planted now solves the chain's own system at an eight-part state.** The truth's pinned residual is 5.5519e-92 at
252.6135 and 1.7135e-66 at 240.1244 (#805: 5.6e-92 and 1.7e-66), and the first Newton step's Delta part is
+5.264596e-82 and -4.376544e-58 (`step_D252.log`, `step_D240.log`, 10:53–11:06 UTC).

| run | read | held values | plan | truth's pinned max\|F\|, 252.6135 | 240.1244 | bar 1e-55 |
|---|---|---|---|---|---|---|
| step (the new default) | 8 parts | eight parts | stored | 5.5519e-92 | 1.7135e-66 | pass |
| control `--read 4` | 4 parts | eight parts | stored | 1.5209e-26 | 1.7585e-28 | fails, as required |
| control `--held float` | 8 parts | floats | stored | 3.5827e-20 | 2.2158e-20 | fails, as required |
| control `--plan state` | 8 parts | eight parts | made at the state | 2.6755e-36 | 6.1479e-36 | fails, as required |

The held-float control alone gives the old residuals exactly (3.5827e-20, 2.2158e-20), so the held values as floats
were their cause. The plan accounts for about 1e-36 and the four-part read for about 1e-26.

**The four-part states are unchanged** (their system is the old one by construction, `four_D*.log`):

| state | recorded start line (truth, start) | now | first step, recorded (#713 s0_D200.json) | now |
|---|---|---|---|---|
| T138-win2 200.0000 (#713 s0_D200's flags) | 9.75e-29, 3.39e-12 | 9.75e-29, 3.39e-12 | \|dz\| 2.7430492042156393e-11, dDelta -9.672282975858525e-13 | equal as doubles |
| T129-win2 180.5246 (#504, #523, #555) | 2.83e-30, 3.39e-12 | 2.83e-30 (2.8253e-30), 3.39e-12 | | |
| I13-win 192.0000 (#468) | 7.06e-29, 3.39e-12 | 7.06e-29 (7.0601e-29), 3.39e-12 | | |

**proj_shift and step_spread share it** (`ss_D252.log`, `ps_D252.log`, 11:14–11:56 UTC): step_spread's unperturbed step
at 252.6135 equals planted's (+5.2645963792835124e-82, exact) and repeats exactly. proj_shift's plain step equals it
too (relative 0), and its projection moves only m_h and a_h. At the chain's root the switch-0 projection (reseed_o 3)
moves m_h by 3.09e-80 and leaves the residual at 2.30e-80 (from 5.55e-92). ElimO's step from the state undoes that move,
so its Delta part equals the plain step's.

## Discrepancies

1. The controls run planted with `--od 0 --qd 0`, which judges nothing and prints "(a) PASS:" (as before). Their
   verdicts are read from the truth's residual line against the bar, not from planted's exit.
2. The four-part reproduction compares start lines at three states and one first step (D 200), not the recorded runs
   in full.
3. At the chain's root the switch-0 projection raises the residual from 5.55e-92 to 2.30e-80. That is a floor for a
   switch-0 run in this system, below the 1e-40 bar, but 12 orders above the root.
4. wall is unchanged: the issue names planted, proj_shift and step_spread, and wall's predictions are saved in four
   parts (--save_pred 1). Whether any eight-part prediction exists was not checked.

## Recommended tasks

1. **The s0_D252 planted test again, in the chain's system.**
   - What: #777's rerun flags (`--rel 1e-12`, seed 1, `--switch 0 --reseed_o 3 --reseed_start pred --full_drop
     1e-6`) at I603-win2's 252.6135, and once at the default switch 1e-15.
   - Why: until now the truth was 3.6e-20 off its system's root. The question #713 asked, whether the octo-double
     corrector reaches 1e-40 from a planted start at D 252.6, has not been asked of a system the truth solves.
   - Acceptance (can fail): planted's own (a), max|F| below 1e-40 and Delta within 1e-30 of the truth's.
   - Estimate: 1–3 h per arm at 3 threads. Depends on #837.
2. **#827 and #830 again at the eight-part states** (the coordinator holds #830's rerun for #837): the Delta step's
   spread under 1e-65 horizon perturbations at the chain's own root. About 2.5 h. Depends on #837.
3. **Eight-part predictions in wall.** Check whether anm_run writes any eight-part prediction, and if so give wall
   the same read. Minutes. Depends on #837.
