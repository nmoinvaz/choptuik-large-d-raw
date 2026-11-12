# I609-macm3: where the complex mode matrix's assembly stops being smooth in lambda, hp/modecount_smooth.py over M and D

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, numpy 2.5.4, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main 98ee71b (the fix of a879ccc's missing imports; the coordinator's message of 2026-11-12 19:48 UTC), modecount_cx built from 742bb879's source (the coordinator: agrees with main's). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/609.

Command, from hp/ of the worktree, one process per case under caffeinate -is and nice -n 10: python3 -u modecount_smooth.py STATE M KF|none RE IM (the script fixes 4 threads for the matrix assembly). run_609.sh 1 and run_609.sh 2 are two chains of cases; chain 2 starts after the control of chain 1 has passed. Started 2026-11-12 19:50 UTC.

Cases. D 30.0688 (data/states/up6_D30.0688.npz, kf none): M 32, 40, 48, 64, 80 at lambda_phys (2.0797477, 0) and at 0.055758+1.411769i (the first of #473's eight extra positions, as #607 lists them). D 61.03: M 48 kf 27 (I280-macm3/hp_data_after/modecount_state_D61.0264_M48_kf27.npz) and M 64 kf 23 (I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd6...) at #584's q1 1.980000+0.749808i and s3 0.132000+2.912795i. Resampled D 30 states (M != the seed's) are made and saved by setup in hp/data of the worktree.

Written before the run (the issue's). Control: M 32, D 30, lambda_phys: the entries with |d2 - 2 d1| > |d1|/2 are at most 1% of the entries changed by one ulp, else the table is not read (run_609.sh's gate; the gate's awk was tried on logs at 50/5000 (passes), 51/5000 (fails) and an empty log (fails)). Per case: the count, the blocks, the largest |d1|/|A| among the counted entries. Named: the M at which the count first exceeds 1%. The count can be large: #584's s3 at M 64 had 55,821 centre and horizon entries (coordinator, #605), so D 61 M 64 s3 is the positive reference.

## Results (2026-11-12 20:42 UTC; all 15 cases of run_609.sh exit 0, exits.txt; table.md is table609.py's output of the logs)

| case | at | changed by 1 ulp | non-linear | share | rows by block | cols by block | largest abs(d1)/abs(A) |
|---|---|---|---|---|---|---|---|
| ctrl_M32_phys | 2.0797477+0.0i | 81920 | 1 | 0.0012% | [1] | [1] | 2.6e-21 |
| ctrl_M32_physfull | 2.079747703853262+0.0i | 81920 | 1 | 0.0012% | [1] | [1] | 5.7e-21 |
| D30_M32_pos | 0.055758+1.411769i | 81920 | 20 | 0.0244% | [20] | [20] | 2.0e-20 |
| D30_M40_phys | 2.0797477+0.0i | 128000 | 830 | 0.6484% | [830] | [830] | 7.8e-16 |
| D30_M40_pos | 0.055758+1.411769i | 128000 | 2299 | 1.7961% | [2299] | [2299] | 3.9e-16 |
| D30_M48_phys | 2.0797477+0.0i | 184320 | 3966 | 2.1517% | [3966] | [3966] | 1.0e-10 |
| D30_M48_phys_fresh | 2.0797477+0.0i | 184320 | 3921 | 2.1273% | [3921] | [3921] | 5.9e-12 |
| D30_M48_pos | 0.055758+1.411769i | 184320 | 11383 | 6.1757% | [11374     0     0     0     0     9] | [11374     0     0     0     0     9] | 2.4e-12 |
| D30_M64_phys | 2.0797477+0.0i | 393216 | 57 | 0.0145% | [40  0  0  0  0  0 17] | [40  0  0  0  0  0 17] | 2.4e-18 |
| D30_M64_pos | 0.055758+1.411769i | 393216 | 4979 | 1.2662% | [2753    0    0    0    0    0 2226] | [2753    0    0    0    0    0 2226] | 2.6e-17 |
| D30_M80_phys | 2.0797477+0.0i | 614400 | 20539 | 3.3429% | [12340     0     0     0     0     0  8199] | [12340     0     0     0     0     0  8199] | 2.9e-12 |
| D30_M80_pos | 0.055758+1.411769i | 614400 | 46073 | 7.4989% | [15041     0     0     0     0     0 31032] | [15041     0     0     0     0     0 31032] | 3.8e-14 |
| D61_M48_q1 | 1.98+0.749808i | 184320 | 1096 | 0.5946% | [524   0   0   0   0 572] | [524   0   0   0   0 572] | 1.4e-15 |
| D61_M48_s3 | 0.132+2.912795i | 184320 | 13038 | 7.0736% | [ 2867     0     0     0     0 10171] | [ 2867     0     0     0     0 10171] | 6.8e-13 |
| D61_M64_q1 | 1.98+0.749808i | 327680 | 27901 | 8.5147% | [18098     0     0     0     0  9803] | [18098     0     0     0     0  9803] | 5.1e-11 |
| D61_M64_s3 | 0.132+2.912795i | 327680 | 55821 | 17.0352% | [24366     0     0     0     0 31455] | [24366     0     0     0     0 31455] | 3.9e-11 |

Control (the issue's): D 30, M 32, lambda_phys: 1 entry of the 81920 changed by one ulp (0.0012%), passes the 1% limit, at 2.0797477 and at 2.079747703853262 (the coordinator found 1 as well). Positive reference: D 61 M 64 s3 gives 55821, the number of the coordinator's comment on #605.
Non-linear entries sit in the first (centre) and last (horizon) block of 4M rows and columns whenever there are several, never in the middle blocks; at D 30 M 40 and at M 48 lambda_phys they are all in the first block. The script prints rows and columns separately (their lists are equal in every case); their joint was not computed.
First M with more than 1% of the changed entries: D 30 lambda_phys M 48 (M 40 0.65%, but M 64 0.0145% and M 80 3.34%); D 30 at 0.055758+1.411769i M 40 (M 64 1.27%); D 61 q1 M 64 (M 48 0.59%); D 61 s3 M 48. Not monotone in M at D 30.
States: D 30 M 40, 64, 80 and the M 48 of D30_M48_phys_fresh were made by setup in this run (states/, sha256 in state_sha256.txt). The M 48 state used by D30_M48_phys and D30_M48_pos was already in hp/data of the worktree (dated 12:52 UTC, origin not identified); it is in states_aside/. D30_M48_phys_fresh reruns the case with the state made in this run: 3921 against 3966 entries (2.13% against 2.15%), largest jump 5.9e-12 against 1.0e-10; the two states differ by up to 1.1e-14 in zh (same nodes, |F| 9.0060e-18 and 9.0063e-18).
hpkernel/driver.py:149 printed "RuntimeWarning: overflow encountered in square" in the logs that made a state (D30_M48_phys_fresh, D30_M64_phys, D30_M80_phys); the |F| gate of setup (1e-15) passed in all.
The script fixes 4 threads for the assembly; the two chains ran beside #607's four processes.
