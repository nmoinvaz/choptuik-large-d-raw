# I624-macm3: the D 61 share of non-linear mode-matrix entries at M 40 and M 80 (monotone in M, or its own dip?)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, numpy 2.5.4, python-flint 0.9.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main ef466c7 (the build of #612), modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/624 (macm3's #612 recommendation; the coordinator's message of 2026-11-12 23:20 UTC: after #615's runs).

Command, from hp/ of the worktree, as in #612 with only the state and M changed: python3 -u modecount_smooth.py STATE M 23 RE IM --joint, STATE = I252-mac/states/modecount_state_D61.0264_M64_kf23.npz (sha256 179d0bd6...), M 40 and 80, at #584's q1 1.980000+0.749808i and s3 0.132000+2.912795i. setup resamples the M 64 state to M and saves it in hp/data of the worktree (modecount_state_D61.0264_M40_kf23.npz, ..._M80_kf23.npz; none existed before). run_624.sh C (the control, starts after #615's b5 has exited), then P (M 40), Q (M 80), R (M 48 kf 23, my addition: #609's D 61 M 48 used I280-macm3's kf 27 state, so M 48 from the same kf 23 state makes the series M 40, 48, 64, 80 one cut). Control: #612's M 32 D 30 lambda_phys run, 1 non-linear entry at block (0, 0), row 8, column 29, field p (the gate of run_624.sh; tried in I612-macm3/run_612.sh on a good log and five changed ones). Known: M 64 q1 8.51% and s3 17.0% (55,821 entries; #609, #612), M 48 kf 27 q1 0.595% and s3 7.07%.

Written before the run (the issue's). The control passes; each (M, point) share and its blocks are tabled; the summary states whether the D 61 share is monotone in M. A resampling that stalls (setup raises) is reported, not rerun.

## Results (2026-11-12 23:48 UTC; control passes; M40_q1/M40_s3/M48kf23_q1/M48kf23_s3 exit 0, M80_q1/M80_s3 exit 1 (setup's series gate; not retried, the coordinator's message of 2026-11-12 23:27 UTC))

| state | q1 non-linear (of changed): share, centre / horizon | s3 non-linear (of changed): share, centre / horizon | largest abs(d1)/abs(A) q1; s3 |
|---|---|---|---|
| M 40, kf 23 (resampled from M 64 kf 23) | 8 of 128000: 0.00625%, 0 / 8 | 3629 of 128000: 2.84%, 0 / 3629 | 5.7e-18; 2.0e-15 |
| M 48, kf 23 (resampled from M 64 kf 23; added) | 1092 of 184320: 0.592%, 532 / 560 | 12618 of 184320: 6.85%, 2885 / 9733 | 4.2e-16; 9.8e-14 |
| M 48, kf 27 (I280-macm3's state; #609) | 1096 of 184320: 0.595%, 524 / 572 | 13038 of 184320: 7.07%, 2867 / 10171 | 1.4e-15; 6.8e-13 |
| M 64, kf 23 (I252-mac's state; #609) | 27901 of 327680: 8.51%, 18098 / 9803 | 55821 of 327680: 17%, 24366 / 31455 | 5.1e-11; 3.9e-11 |
| M 80, kf 23 | setup refused (series gate) | setup refused (series gate) | -; - |

Shares are non-linear entries among the entries changed by one ulp; centre / horizon are the first and last block of 4M rows (the joint sums to the count in each case, table624.py asserts it). The M 48 and M 64 rows of kf 27 and kf 23 are #609's logs (I609-macm3). The M 40 and M 48 kf 23 states (states/) were made by setup from the M 64 kf 23 state (sha256 179d0bd6...); none existed in hp/data before. The share rises with M over M 40, 48, 64 at both points. M 80: setup's series gate refused both (the log message: RuntimeError: series not converged in this layout (start; M = 80, nodes [0.15, 0.3, 0.4, 0.5, 0.6, 0.7]): centre 6.1e-127 (ratio 0.517 at 0.15), horizon 3.7e-12 (ratio 0.968 at 0.3); more than 1e-15).
