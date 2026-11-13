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
