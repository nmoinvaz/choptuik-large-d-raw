# I612-macm3: the non-smooth entries' joint position (modecount_smooth.py --joint), and D 30 between M 48 and M 80 and at the other #473 positions

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, numpy 2.5.4, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main ef466c7 (the coordinator's message of 2026-11-12 20:46 UTC), modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/612 (my #609 recommendations 1 and 2).

Command, from hp/ of the worktree, one process per case under caffeinate -is and nice -n 10: python3 -u modecount_smooth.py STATE M KF|none RE IM --joint (the script fixes 4 threads for the assembly). run_612.sh 1 and run_612.sh 2 are two chains; chain 2 starts after the control of chain 1 has passed. Started 2026-11-12 20:48 UTC. Part 2's runs carry --joint too (its extra lines leave the first lines of the output unchanged).

Part 1: D 61 M 64 kf 23 (I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd6...) at s3 0.132000+2.912795i (55,821 non-linear entries in #609), and D 30 M 80 at lambda_phys 2.0797477 (20,539 in #609, with the M 80 state of #609's run, copied to states/). Part 2: D 30 (data/states/up6_D30.0688.npz, kf none) at M 56 and 72 at lambda_phys and at 0.055758+1.411769i (#609's #473 position, position 1); and M 64 at #473's eight upper-half positions in #607's order (1 0.055758+1.411769i, 2 3.871717+0.105316i, 3 4.285793+0.551490i, 4 4.656327+1.390362i, 5 0.847147+4.333559i, 6 1.057045+2.913917i, 7 1.978326+3.721021i, 8 4.070967+2.532063i).

Written before the run (the issue's). Part 1: the joint sums to the count (55,821 and 20,539). The M 32 control (D 30 M 32 lambda_phys) gives its one entry at block (0, 0), row 8, column 29, field p (run_612.sh's gate: that line, the count 1, the rows' field list [1 0 0 0], and the first joint row starting with 1; tried on a good log (passes) and on five logs with the column, the count, the block, the field and an empty log changed (each fails)). Part 2: the M 32 control passes (at most 1% of the changed entries), each point's share is tabled at every M, and whether the M 64 dip holds at all eight positions or only at lambda_phys is stated.

## Decisions (the coordinator's message of 2026-11-12 22:26 UTC)
Part 2 at M 56 and M 72 cannot run (hpkernel's M list: 8, 16, 32, 40, 48, 64, 80, 96, 128, ...; ValueError at hpkernel/driver.py:94, logs P2_M56_*.log and P2_M72_*.log). Decided: M 96 at lambda_phys and position 1 in its place; M 48 and M 80 at positions 2 to 8 (14 cases, cached states) so that the M 64 dip is read at all eight positions. run_612b.sh (chains X, Y, Z, started 22:27 UTC) runs them, with position 1 at M 48 rerun as well (the M 48 state in hp/data is now the one made in #609's run, sha256 5bea0e2c...). The cases are named P3_*.

## Results (2026-11-12 23:02 UTC; all cases of run_612.sh and run_612b.sh exit 0 except P2_M56_*, P2_M72_* and P3_M96_*, which exit 1 with the ValueError of hpkernel (M list) and modecount_cx (lib.rs:723, M in 16, 32, 40, 48, 64, 80))

Part 1 (P1_*.log, joint612.py): D 61 M 64 s3 55821 entries, blocks (0, 0) 24366 and (5, 5) 31455; D 30 M 80 lambda_phys 20539, blocks (0, 0) 12340 and (6, 6) 8199; the M 32 control gives its one entry (block (0, 0), row 8, column 29, field p). In all 26 logs of this folder the joint sums to the count with no entry off the diagonal and none in a middle block.

Part 2 (table612.py). From I609-macm3's logs: lambda_phys at M 40, 48 (the rerun on the state made in that run) and 64; position 1 at M 32, 40 and 80. From this folder: lambda_phys at M 32 (the control) and 80 (P1), position 1 at M 48 (the state made in I609's run: 11427 entries, against 11383 on the earlier state) and 64, positions 2 to 8 at M 48, 64 and 80:

| point (D 30) | M 32 | M 40 | M 48 | M 64 | M 80 | M 64 below M 48 and M 80 |
|---|---|---|---|---|---|---|
| lambda_phys | 1 (0.00122%) | 830 (0.648%) | 3921 (2.13%) | 57 (0.0145%) | 20539 (3.34%) | yes, factor 147 |
| 1 0.055758+1.411769i | 20 (0.0244%) | 2299 (1.8%) | 11427 (6.2%) | 4979 (1.27%) | 46073 (7.5%) | yes, factor 4.9 |
| 2 3.871717+0.105316i | - | - | 3894 (2.11%) | 76 (0.0193%) | 12760 (2.08%) | yes, factor 107 |
| 3 4.285793+0.551490i | - | - | 3041 (1.65%) | 14 (0.00356%) | 11999 (1.95%) | yes, factor 463 |
| 4 4.656327+1.390362i | - | - | 3056 (1.66%) | 8 (0.00203%) | 12414 (2.02%) | yes, factor 815 |
| 5 0.847147+4.333559i | - | - | 7202 (3.91%) | 129 (0.0328%) | 32208 (5.24%) | yes, factor 119 |
| 6 1.057045+2.913917i | - | - | 5660 (3.07%) | 36 (0.00916%) | 19523 (3.18%) | yes, factor 335 |
| 7 1.978326+3.721021i | - | - | 5804 (3.15%) | 47 (0.012%) | 13541 (2.2%) | yes, factor 184 |
| 8 4.070967+2.532063i | - | - | 3235 (1.76%) | 5 (0.00127%) | 12786 (2.08%) | yes, factor 1.38e+03 |

M 64 is below both M 48 and M 80 at lambda_phys and at all eight positions. M 56, 72 and 96 cannot run: hpkernel takes M in 8, 16, 32, 40, 48, 64, 80, 96, 128, ... but modecount_cx in 16, 32, 40, 48, 64, 80.
