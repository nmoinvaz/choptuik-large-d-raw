# I713-mac: the octo-double corrector's planted and wall checks with ElimO's projection switch at 0

Machine: the coordinator's Mac (Apple M5, macOS), a subagent of the coordinator. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/713 (recommended by #700, notes/CRAWL.md).

Code: `hp/` of choptuik-large-d branch `wip/i713-subagent` at 00c3963f (main 10bcd936, which has acbc0dfd's `--switch`,
plus one commit: `planted` takes `--reseed_o K` and `--reseed_start pred`, `wall` takes `--reseed_start pred`, as
anm_run.py's options of the same names). Kernel: the i599/site2 build of main 3c35f0c (exact freeze projector), the one
I644-mac and I674-mac used, on `PYTHONPATH`; Python `/Users/nathan/venv-314`. Every run from `hp/` with
`OPENBLAS_NUM_THREADS=1 nice -n 10`, 3 threads, one run at a time. RAW below is the root of a worktree of this
repository at bfd2a893. Each `<name>.log` ends with `exit N`.

## Why the switch-0 runs project with the chain's re-seeder

ElimO's projection is the quad-double polish of the horizon data, put back with parts 4 to 7 zero, unless the
re-seeder also corrects them in octo-double (`--reseed_o K`, `Reseeder.refine_o`). With the switch at 1e-15 the last
iterates are not projected, and the octo-double Newton corrects the horizon data itself. With the switch at 0 every
point is projected, so the projection's own residual is a floor of the corrector. #603's chain projects with
`--reseed_q 1 --reseed_o 3 --reseed_start pred` (chain_nsr), whose rung residual reaches about 1e-80 (notes/CRAWL.md 8).
So the switch-0 runs use `--reseed_o 3 --reseed_start pred`, the chain's projection, whatever the pilot shows. The pilot
measures the floor of each projection at a converged point (information; it changes no criterion).

The accept test is each check's default (`own`, no strong chord). The chain's own flags (natural test, `--od_strong 4`)
at switch 0 are #714's A/B.

## Runs and criteria (fixed before the first run)

| name | command (`octo_corrector.py` unless named) | pass |
|---|---|---|
| pilot | `pilot_floor.py RAW T138-win2/chain_o/anm_pin3_D200.0000.npz I644-mac/planted_own.npz` | information: max\|F\| at I644's converged point (expected 6.52e-49, a reproduction check), and at its projection with reseed_o 0 and 3 |
| ref_D200 | `planted RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --threads 3 --out RAW/I713-mac/ref_D200` (switch 1e-15, reseed_o 0, ladder, own; both halves) | C0: the octo-double half reproduces I644-mac/planted_own: 6 steps, pinned max\|F\| 6.52e-49, Delta 1.695088752463841744241523971202762929113 to all 40 digits, projections u0q 2, ladder 2, skipped 3, and its per-step \|F\| and \|dz\| as printed. The quad-double half is the D 200 reference of C1. |
| s0_D200 | `planted RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --threads 3 --switch 0 --reseed_o 3 --reseed_start pred --qd 0 --Delta_ref REF200 --out RAW/I713-mac/s0_D200` | C1: exit 0, i.e. converged with pinned octo-double max\|F\| below 1e-40 and \|Delta_od - REF200\| at most 1e-30 |
| s0_D200_mo | s0_D200 with `--mutate_offset qd` | must exit 1 |
| s0_D200_m10 | s0_D200 with `--mutate 10` | must exit 1 |
| ref_D252 | `planted RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --reseed_o 3 --reseed_start pred --out RAW/I713-mac/ref_D252` (switch 1e-15; both halves) | information: the references of C2 |
| s0_D252 | `planted RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --switch 0 --reseed_o 3 --reseed_start pred --qd 0 --Delta_ref REF252 --out RAW/I713-mac/s0_D252` | C2: exit 0, as C1 |
| s0_D252_mo | s0_D252 with `--mutate_offset qd` | must exit 1 |
| s0_D252_m10 | s0_D252 with `--mutate 10` | must exit 1 |
| s0_wall | `wall RAW I603-win2/chain_nsr/pred_pin3_D254.4381.npz --threads 3 --switch 0 --reseed_o 3 --held_o 1 --reseed_start pred --out RAW/I713-mac/s0_wall` | C3: exit 0, i.e. pinned octo-double max\|F\| below 1e-36 |
| s0_wall_mo | s0_wall with `--mutate_offset qd` | must exit 1 |
| s0_wall_m10 | s0_wall with `--mutate 10` | must exit 1 |

**The Delta reference (REF200, REF252).** The issue's reference is the quad-double corrector's Delta from the same start
(ElimQ, newton_qd, tol 1e-45, 12 steps; ElimO's switch does not enter it). It is a valid reference to 1e-30 when that
run's last Newton correction, max\|dz\| of its last record, is at most 1e-31. At D 192 it stalled at 7.87e-24, 4.2e-14
from the octo-double root (#468), and the chain's quad-double corrector stalls past D 193.77 (notes/OCTO_DOUBLE.md 5.1),
so it may not be valid here. When it is valid, REF is its Delta. When it is not, the issue's criterion cannot be met by
any corrector: that is reported as a discrepancy, not as a pass, and REF is the octo-double Delta of the default-switch
run from the same start (ref_D200, ref_D252), which then must itself have converged below 1e-40. The bound stays 1e-30.
Both distances, to the quad-double Delta and to the default-switch octo-double Delta, are reported for every run.

**Controls.** `--mutate_offset qd` takes PinnedO's J^-1 c through the quad-double LU at the point's quad-double rounding;
`--mutate 10` is the kernel's OD_MUT_STATE_QD (the state read in its quad-double part). Each must make its check exit 1.
A control that exits 0 stops the work.

A check that fails stops the work, and the failure is reported as it stands.

**Amendment 1 (21:38 UTC, after ref_D200's octo-double half and before s0_D200).** The quad-double half of ref_D200
took 1990 s for its first step and reached only lam 1/2: |dz| 1.1e-9 where the octo-double step is 2.7e-11, smallest
pivot 2.3e-14 where the octo-double one is 1.7e-12, dDelta +1.14e-9. At that pace its 12 steps take about 6.6 h, so I
stopped it (`ref_D200.log`, exit 143). Its validity is not established. Until a quad-double run alone (`--od 0`) has
finished, REF200 is the octo-double Delta of ref_D200, the fallback above, and the issue's criterion against the
quad-double corrector stays open at D 200, reported as such. ref_D252 runs its octo-double half alone (`--qd 0`) for the
same reason, and its quad-double half runs alone after the switch-0 runs if time allows. No bound changes.

## Results

### pilot (`pilot.log`, `pilot.json`, exit 0, 20:15 to 20:21 UTC)

At I644's converged point on the D 200 planted system, and at its projection by ElimO with the switch at 0:

| point | pinned max\|F\| (octo) | horizon block p, m, a, c | every node block |
|---|---|---|---|
| I644's converged point | 6.519e-49 (I644: 6.52e-49) | 5.1e-50, 9.2e-50, 3.3e-49, 6.5e-49 | at most 3.5e-78 |
| projected, reseed_o 0 (quad-double only) | **1.189e-33** | 9.2e-36, 1.7e-34, 6.0e-34, 1.2e-33 | unchanged |
| projected, reseed_o 3 | 7.442e-52 | 7.3e-52, 1.2e-84, 3.9e-87, 7.4e-52 | unchanged |

The projection with reseed_o 3 took 159 s, its rung max\|R\| 6.03e-34 → 2.28e-69 → 2.31e-77 → 1.24e-84. So with
the switch at 0 and the quad-double projection alone, every iterate carries 1.2e-33 in its horizon rows, seven orders
above the planted check's 1e-40. The setup reproduces I644's converged residual.

### ref_D200, C0 (`ref_D200.log`, `.json`, `.npz`; 20:21 to 21:38 UTC)

**C0: PASS.** The octo-double half took 6 steps to pinned max\|F\| 6.52e-49, with Delta
1.695088752463841744241523971202762929113, which equals I644-mac/planted_own to all 40 digits. Its projections
were u0q 2, ladder 2 and skipped 3, and it took 2294 s. Each step's \|F\|, lam, dDelta and pivots equal I644's log line
for line, and \|dz\| matches to the digits I644 printed (it printed two). The quad-double half was stopped after its
first step (amendment 1), so the log ends `exit 143`.

### s0_D200, C1 (`s0_D200.log`, `.json`, `.npz`; 21:38 to 22:10 UTC, exit 0)

**C1: PASS.** With every point projected (switch 0, reseed_o 3), the corrector converged in 5 steps to pinned max\|F\|
8.12e-54, with Delta 1.695088752463841744241523971202762929111. That is 1.71e-39 from REF200, the default-switch
octo-double Delta. Its projections were u0q 4, ladder 2, skipped 0, and it took 1938 s.

| step | switch 1e-15 (ref_D200) | switch 0 (s0_D200) |
|---|---|---|
| 0 | 3.39e-12 → 1.15e-15 | 3.39e-12 → 1.15e-15 |
| 1 | 1.15e-15 → 2.15e-22 | 1.15e-15 → 2.15e-22 |
| 2 | 2.15e-22 → 9.75e-34 | 2.15e-22 → 6.22e-34 |
| 3 | 9.75e-34 → **4.51e-25** (the trial not projected) | 6.22e-34 → 8.12e-54, converged |
| 4 | 4.51e-25 → 6.52e-49, converged | |

At the default switch, ElimO skipped 3 of its 7 evaluations: the start, five trials and the final point. That fits
the last three being below the switch, step 3's trial among them, though it is inferred from the counts, not logged per
point. Unprojected, that trial keeps the horizon rows' second-order term (#700), and the residual rises by nine orders
before the next step removes it. With every point projected, the same step goes straight to 8.12e-54.

### The stop of 22:40 UTC and the queue

The first run of s0_D200_mo (from 22:10 UTC) died at 22:40 UTC with the session that ran it, after three refused trials
of its first step (lam 1, 1/2, 1/4). Its partial log is kept as `s0_D200_mo_killed.log`. It is not a verdict. From
22:45 UTC `queue.sh` runs the rest of the table, s0_D200_mo again from the start with the same command, then the others
in the table's order, one at a time through run.sh. It does not rerun a run whose log has its `exit` line, takes REF252
from `ref_D252.json`, and stops at the first exit the criteria do not expect (a check 0, a control 1). Its own log is
`queue.log`, one line per run.

### s0_D200_mo, C1's `--mutate_offset qd` control (`s0_D200_mo.log`, `.json`, `.npz`; 22:45 to 00:13 UTC, exit 1)

**Fires: exit 1, as required.** The first step's nine trials (lam 1 to 1/256) were all refused, so the corrector
stopped after one step at the start's max\|F\| 3.39e-12. With the quad-double offset, the step's \|dz\| is 7.71e-3
against the true step's 2.74e-11, and each trial's own correction is far larger still (nan at lam 1, then 3.96e+66
falling to 8.98e+41 at lam 1/256). ElimO's projection failed at all nine trials (`failed` 9, u0q 2). The rerun's
first three trials equal the killed run's to every printed digit. It took 5254 s.
