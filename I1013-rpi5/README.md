# I1013-rpi5: M = 3 winding counts of the selection multiplier, the upper chain of M = 1 zeros (#1013 step 4, #995)

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, aarch64, Python 3.13.7), runner, under the claude-me2 account.
Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1013 (dh610's steps 1 to 3 run there as `I1013-dh610/`; this folder is the coordinator's step 4 box, assigned by message 2026-11-19).
Code: `argcount.py` of xfchecks at fc7dee4d (branch wip/excited-zeros, worktree `~/Source/cl-995`, `solver/inner_stokes/`), venv `~/Source/venv-choptuik` (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0).

## Written down before the runs

Commands (from the coordinator's #1013 comment of 2026-11-19 08:56 UTC; N = 4 here, nice 10), run from `cl-995/solver/inner_stokes`:

```bash
PY=~/Source/venv-choptuik/bin/python; N=4; RAW=<this folder>
$PY argcount.py --selftest                    # exit 0
$PY argcount.py --selftest --mutate=norecount # exit 1
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=3.6,5.1 --wf=0.5,1.3 --nA=6 --nwf=8 --procs=$N --out=$RAW/m3 --tag=M3_upper > $RAW/logs/m3_upper.log 2>&1
nice -n 10 timeout 6h  $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper.jsonl --r1=0.25 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.25 > $RAW/logs/m3_upper_r0.25.log 2>&1
nice -n 10 timeout 6h  $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.17 > $RAW/logs/m3_upper_r0.17.log 2>&1
```

Readings (the issue's, applied to this box):
- **Persistence:** an M = 1 zero persists at M = 3 when an M = 3 zero of the same sign lies within the known zero's shift, |dA| <= 0.2 and |d wf| <= 0.25 (the known zero shifts by +0.184 and +0.239). Each M = 3 zero serves one M = 1 zero, the nearest.
  The M = 1 zeros to compare with are the upper chain of xfchecks' ladder (#995 comment 7004433173, raw `I995-mac` 3b74d753): wf 0.56 to 0.78 at A 3.0 to 4.7 (this box starts at A 3.6, so the zeros of A < 3.6 belong to dh610's step 2).
- **Report:** each step's count line and zero lines, with the unresolved cells and their causes. A box with unresolved cells after the last rung is reported as such, not as a count.
- **Not decided here:** whether a persistent or missing zero decides the selection rule's solution count (the issue's decision); this folder gives the counts.
- dh610's pilot at the known zero (A 2.5 to 3.0, wf 0.8 to 1.2) had 4 unresolved cells at xi1 0.2 and 0.25, all resolved at 0.17 with winding 0 (its comment of 08:59 UTC); the same corner failures (|r_3| above 1e-8, path |Y| above 100) are the thing to watch here.

## Stopped after 56 min of step 1, 2026-11-19 11:27 UTC (my decision; the coordinator confirmed, "stop your diagnosis", and says step 4 reruns with `--m3fix` when #1021 lands)

**Step 1 (the box, 1 h of 4 workers, `m3/points_M3_r0.2_box_noval24.jsonl`):** 24 of the 63 base points computed (A 3.612, 3.862, 4.112 in rings outward from the known zero), **24 of 24 with no value**: every one has |r_3| above the 1e-8 bar (1.5e-7 to 7e17), and 9 of them also have max |Y| above 100 (up to 1e9). About 2 to 5 min per point where the solve fails (15 to 25 s where it converges). Steps 2 and 3 never ran (`logs/driver.log`).
The cached points are renamed `_noval24` so a restart cannot reuse them as NaN.

**Diagnosis (`diag/`, `diag_chain.py`, `diag_scatter.py`, `diag_scatter2.py`; `argcount.f_M3`, one core each, the continuation seeded from the previous converged point's tuned F_3):**

| xi1 | chain along wf 1.0065 from the known zero (A 2.7265, step 0.15) |
|---|---|
| 0.2 | |r_3| 1.9e-10, 4.7e-10, 1.2e-9, 3.8e-9 at A 2.73 to 3.18 (valid, |R| 76 to 2.5e4, sigma 2e-7 to 2e-5), then 4.1e-8, 1.1e-7, 2.4e-7 at A 3.33, 3.48, 3.63 (above the bar). Same at wf 0.8065 (1.9e-8 at 3.33 to 3.9e-7 at 3.63). |
| 0.17 | valid to A 3.03 (2e-9), 1.1e-8 at 3.18, 3.4e-7, 1.5e-6 at 3.33, 3.48; sigma 0.01 to 0.4 there |
| 0.25 and 0.3 | no convergence even at the known zero (|r_3| 195 and 70 at 0.25, 119 at 0.3; max |Y| 5e7 to 1e8) |

So the first box's failure is two things: the formula seed (linear in A, calibrated at A 2.73) is outside the inner solve's basin at A 3.6 (the converged F_3 at A 3.48 is 0.00597 - 0.13686i, the seed's 0.00615 - 0.10931i; a failed point reports the stale input F_3), and the |r_3| < 1e-8 bar is passed only up to A about 3.2 at xi1 0.2.
**One check that the bar can be conservative (A 3.4765, wf 1.0065, xi1 0.2):** 10 solves of `nested.inner` called directly from the base F_3 times (1 + 1e-3 u), all ending at |r_3| 1.4e-8 to 1.3e-7 (above the bar, so `f_M3` would withhold R): the tuned F_3 agrees to 1e-13 (0.0059669154374 - 0.1368590329698i), R = -179034.726 + 1015.571i with relative scatter 1.1e-8 and phase scatter 1.4e-8 rad (the count's phase step is 0.5 rad). That is the reproducibility between inner solves from perturbed starts, not a proof of the value's accuracy (a shared rounding error would not show), and it is one point at a mild xi1. #1021 reports the noise at xi1 0.17 and large A is much larger.
Nothing here is a count or a zero line. No `--seed` from dh610's points was available (their raw is not pushed), and nothing was changed in `argcount.py` (the bar stays 1e-8).
