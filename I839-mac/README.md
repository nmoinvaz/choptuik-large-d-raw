# I839-mac: #713's planted test at s0_D252 (D 252.6135) in the chain's own system

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/839.

Code: main 4617f876 (with #837's `truth_system`), worktree /Users/nathan/Source/choptuik-large-d-839 (`wip/i839`,
no changes). Build: main 3c35f0c's hpkernel (i599/site2). 3 threads, nice 10, one job at a time (queue.sh).

## Plan and criteria (written by 2026-11-15 12:00 UTC, before the queue)

planted at I603-win2's 252.6135 from #713's offset start (--rel 1e-12: the centre data and the nodes but the last
moved by 1e-12 relative), in the chain's own system (#837: truth residual 5.55e-92):

- **arm A**, #713's flags: `--threads 3 --switch 0 --reseed_o 3 --reseed_start pred --qd 0` (own test, it_max 12,
  tol 1e-40);
- **arm B**, the same plus `--full_drop 1e-2` (#836);
- seed 1 for both arms, then seed 2 (queue.sh). Each gets `--Delta_ref` = the truth's Delta from all eight parts,
  1.68453445011892229445312904531756908899422197089059690341775, so that planted's own (a) judges both bars.

**Bars, per arm and seed:** pinned max|F| below 1e-40 within 12 steps, and |Delta - Delta_truth| <= 1e-30. Otherwise
the step where it stops, with its trials. Where both seeds of an arm converge, they agree in Delta to 1e-30.
`verdict_839.py DIR` reads the four JSONs and states each verdict. Its selftest passes on planted records, and its
control `--mutate=bar` (the Delta bar at 1e-20) fails: verdict_selftest*.log, run before the queue (exit 0, exit 1).

Estimate: a few hours per arm (#713's s0_D252 took 2–6 h). The hourly posts follow the queue.

## Change of plan (2026-11-15 16:07 UTC, the coordinator's reply)

By step 4, every lam-1 trial of A_s1 had point max|F| 1e14–1e18, far above full_drop's 1e-2 of |F|. So B_s1 would take
every step as A_s1 did, bit for bit. The coordinator agreed: A_s1 runs out its 12 steps, then A_s2 runs. A B arm runs
only when its A run had a lam-1 trial within 1e-2 of |F|. queue.sh was stopped at 16:07 UTC while A_s1 kept running,
and queue2.sh took over at 16:08 UTC.

`b_needed.py A_LOG` makes that decision from the A run's log (exit 0: B needed). Its selftest passes on planted log
lines, and its control `--mutate=bar` (the drop at 1e-5) fails: b_needed_selftest*.log (exit 0, exit 1). On real logs
(b_needed_real.log), it says needed for I777-mac/stopped_s0_D252 (step 3's lam-1 trial at 4.3e-4 of |F|) and for
I713-mac/s0_D252 (step 11, 3.6e-17), and not needed for A_s1 through step 4 (closest 5.5e27 of |F|).

`table_839.py NAME` gives the closing summary's per-step table from NAME.json and NAME.log: Delta − truth before
each step (the summed lam·dDelta, since the offset leaves Delta at the truth), max|F|, |dz|, the smallest pivot,
pivot/|dz| and the accepted lam. It also fits the lam-1 trials' point max|F| against |dz| (exponent free, then 4) and
the smallest pivot against |dz|. Its check compares the summed Delta moves at the end with planted's own Delta − truth
(relative 1e-6). The selftest passes on a planted run. The controls `--mutate=lam` (step 0's lam taken as 1) and
`--mutate=power` (planted trials at exponent 3) fail: table_selftest*.log (exit 0, 1, 1).

## Stopped (2026-11-15 20:26 UTC, the coordinator's word), superseded by #854

A_s1 was stopped by its PIDs at 20:26:58 UTC while on step 9 (exit 143). Its log up to then is A_s1_at_stop.log, and
A_s1.log is the same plus the stop lines. queue2.sh was stopped first, so A_s2 never started. No B run was made, since
b_needed said A_s1's lam-1 trials never came within 1e-2 of |F|. A_s1 wrote no JSON, so the per-step table
(A_s1_table.txt, `table_839.py A_s1`, exit 1 because its check against planted's own Delta needs the JSON) comes from
the log's step lines. Those carry 3 digits, and the pivots 2.

**Result:** A_s1 did not converge in 9 accepted steps (0–8): max|F| went from 3.40e-12 to 1.16e-13. Delta moved away
from the truth, although the offset leaves Delta at the truth's value. Delta − truth reached −2.127e-12 after step 8,
heading for −2.203e-12. At every step, the Delta already moved plus the remaining |dz| equals step 0's |dz| (2.203e-12)
to 3–4 digits, so the iteration's target in Delta was fixed from step 0 onward.

| step | Delta − truth before | max\|F\| | \|dz\| | smallest pivot | pivot/\|dz\| | accepted lam | minutes |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 3.40e-12 | 2.20e-12 | 2.0e-14 | 0.0091 | 1/8 | 60 |
| 1 | −2.750e-13 | 2.97e-12 | 1.93e-12 | 1.5e-14 | 0.0078 | 1/4 | 45 |
| 2 | −7.575e-13 | 2.23e-12 | 1.45e-12 | 1.1e-14 | 0.0076 | 1/4 | 46 |
| 3 | −1.120e-12 | 1.67e-12 | 1.08e-12 | 5.7e-15 | 0.0053 | 1/2 | 31 |
| 4 | −1.660e-12 | 8.36e-13 | 5.42e-13 | 2.9e-15 | 0.0054 | 1/2 | 33 |
| 5 | −1.931e-12 | 4.18e-13 | 2.71e-13 | 2.2e-15 | 0.0081 | 1/4 | 61 |
| 6 | −1.999e-12 | 3.13e-13 | 2.03e-13 | 1.6e-15 | 0.0079 | 1/4 | 65 |
| 7 | −2.050e-12 | 2.35e-13 | 1.53e-13 | 8.1e-16 | 0.0053 | 1/2 | 34 |
| 8 | −2.126e-12 | 1.17e-13 | 7.63e-14 | 7.9e-16 | 0.0104 | 1/64 | 117 |
| after 8 | −2.127e-12 | 1.16e-13 | 7.51e-14 | | | | |

The smallest pivot fell with |dz|: by a factor 25 while |dz| fell by 29. A fit gives pivot = 4.1e-3·|dz|^0.98, but
pivot/|dz| scatters from 0.0053 to 0.0104. The largest pivot stayed 1.2e36.

**The lam-1 law:** at all nine steps, the full-step trial point's max|F| (quad-double, at the point's four-part
rounding, before its projection) was 5.302e64·|dz|^3.9996 (exponent free, max deviation 0.18%). With the exponent
fixed at 4, it is 5.3587e64·|dz|⁴ (max deviation 0.19%). Shorter trials follow it only at step 0 (ratio 1.000 at lam
1/2 and 1/4). At later steps they lie above it, by up to 2.6e8 at step 8's lam 1/32.

**Step 8's trials** (lam 1 to 1/32 refused, each projection failing, lam 1/64 accepted): the points' max|F| rose as lam
fell, 1.81e12 at lam 1, then 1.29e14, 2.76e14, 3.73e14, 4.28e14 and 4.57e14 for lam 1/2 to 1/32. For lam 1/2 to 1/32
that is P0·(1 − lam)^q with P0 = 4.83e14 and q = 1.91 (max deviation 1%; with q fixed at 2, P0 = 4.93e14 and 4.6%). So
a trial point near lam 0 does not approach the reported |F| (1.17e-13). The reading (from the code, checked by the
coordinator): under ElimO, newton_od keeps the unprojected trial point as its iterate (`zt = z + lam d`, line 393 at
4617f876, and `z, st = zt, stt`). Its |F| and step come from ElimO.newton_o at that point's projection, with the
projection's displacement carried into d. A short trial therefore sits near an unprojected point whose residual is
about 5e14, and its projection, started from that point's own horizon data (`--reseed_start pred`), fails. The u0
quad-double polish cut |R| by 4087–4115× in its 8 iterations at every failed projection (steps 0, 4, 5, 8).
