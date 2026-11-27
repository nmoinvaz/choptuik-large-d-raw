# I1098-mm5/ladder/D4000: D 4000's M 32 stages on fastmul7, chord-free (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 21:30 UTC): D 4000's M 32 stages (the jump, the ks gate, h5..h11, h13) on fastmul7, in the second 6 threads that free up: D 2231 takes the first, as already queued; of D 360m48 and D 747, whichever ends second frees these.
The M 48 tail to kmax 31 is a later job.

```
bash <ladder>/tools3/d4000_mm5.sh        # detached, from the ladder folder
```

`tools3/d4000_mm5.sh` (raw ad818d784 `I1098-mac-a/tools/mm5/d4000_mm5.sh`, blob db0549a846de95a541e8781a73ebe132c5cec5f3, verified) runs `tools3/tools3_check.sh` first (blob fa8071b15ae0e882e4b6ec471cf49b588656f506; it writes `tools3/ladder_point2.sh` from blob 8802fb2699aad3b73a9cab94cea5f4431e830bc2 and checks all seven tools3 files by blob: the check printed 7 "ok" lines, exit 0, `tools3/check.log`),
then checks the two inputs by blob (S1000_D1000_base6_h13 48db1b6cf09ca4feebd9ca5a0976ec8154711635, D2000_base6_h13 b897ba43adb46653785b362d2ae6a2f712fdd8db) and runs `ladder_point2.sh 4000 260 6 <ladder>/D4000 S1000 D2000 48 31`.
Settings: fastmul7 (Python `~/Source/choptuik-fastmul7` at d40a9c62, kernel `~/Source/fastmul7-site`), **chord-free** (`INNER_CHORD=0`), kc 260, **KSBAR=1e-70**, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 6017**, gated by the octo-double `ks_gate.py` (steps of 200 until the residual change at ks + 200 is at most KSBAR),
`STOP_AFTER=rls13` (the point ends after its M 32 stages; the h13 state is left for a tail elsewhere). The jump fits in 1/n to the two inputs. Output in `<ladder>/D4000` (`jump/`, `rls/`, `rls13/`, `run.log`; its last act writes "job rc N").

## Bars, written before the run (coordinator's order)

- The jump converges, and its kc+20 line reads |dF| 0 or below its bar (the jump's discretization bar, 1e-25).
- The ks gate passes (log the ks it settles on, and its octo-double change).
- h5..h13 are each released.
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Pilot: report the jump's time, the gated ks and h5 outer 0's time. ETA 6-8 h (14 h worst case). Times from `date -u`.

## D 4000's M 48 tail (coordinator's order, 2026-11-27 02:38 UTC; armed now, it waits for the M 32 job)

`tools3/d4000tail_mm5.sh` (raw 1d67f29d4 `I1098-mac-a/tools/mm5/d4000tail_mm5.sh`, blob 426becc2c62b85aabdd02ff8f81aceda46bef1e9, equal to raw's, verified and read), detached from the ladder folder, `WAIT_H=8` by default. It checks `tools3/` `ladder_tail.sh` (322f0995), `kmax_rule.py` (196f12a5) and `kstar_stage.sh` (6d29dfc0) by blob, then waits for "job rc 0" in `run.log` and the rls13 h13 state (`rls13/release_ls_h13_D4000.0000.npz`; at most 8 h, so the M 32 job's ETA, about 06:30-07:00 UTC from the pace so far, fits).
Then, into `tail/` (the last act writes "job rc N" to `tail/job.log`), on fastmul7 (d40a9c62), chord-free, 6 threads:

1. **The ks:** dh610's downward gate put D 4000 at ks 4717 (raw `I1098-dh610/ksdown`: 4717 -> 4817 changes the octo-double residual by 5.01e-75 at the M 32 jump state, 4617 -> 4717 by 2.92e-52). That gate was measured on the jump state, so it is checked on the tail's own start: rls13's h13 state resampled to M 48 and set to ks 4717 (a 9.995), then the **upward gate** (`ks_gate.py`, steps of 100, bar 1e-70, the bar D 4000 was run to) from 4717; the tail takes the ks it gates at.
2. `ladder_tail.sh mob` (MT 48 at that ks, h13 re-converged and h15..h23 released, kmax 23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), then the k* stage.
3. `kmax_rule.py` on the tail's `release_ls.jsonl`: exit 0, kmax 23 suffices; exit 2, the h25 extension (`release_ls` from the h23 state, `--harm 25 --kmax 25`, qq, od) and the k* stage again into `tail/kstar25`. A second "extend" is logged, not run.

### Bars, written before the run (as D 2828's tail, plus the gate at the M 48 start)

- **The ks gate at the M 48 start passes, or steps up** (log the ks it gates at and its octo-double change).
- The h13 re-converge at M 48 moves Delta by about 1e-25 or less (D 300 +7.3e-26, D 360 +4.8e-26, D 622 +4.6e-26, D 1291 -2.8e-26, D 2231 -3.8e-26).
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23 released with a pending dDelta at most about 1e-26 and no step: no turn. The kmax rule at the end (exit 0).
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Reported: the gated ks, h13's re-converge, the final Delta, each stage's time, the k* stage and the kmax rule's output. Times from `date -u`.

### The fastmul7 `hp/ks_gate.py` replaced at 2026-11-27 06:31:39 UTC (D 8000's setup, coordinator's order)

`d8000_mm5.sh` installed `ks_gate.py` of wip/large-d-form-s 3b3bfc60 (blob a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7, adds `--down` and `--ks0`) over `~/Source/choptuik-fastmul7/hp/ks_gate.py` (d40a9c62's) at 06:31:39 UTC (`../D8000/setup.log`). The tail's upward gate (`ks_gate.py ... --bar 1e-70 --step 100 --tries 6`) runs this version when the M 32 job ends: the diff of the two versions adds only the downward gate and `--ks0`, the upward path is unchanged. The records of the tail then say HP's HEAD d40a9c62 with this one file newer.

## Result of the M 32 stages (the job ended 2026-11-27 07:13:27 UTC, "job rc 0"; 2026-11-26 22:18:19 - 07:13:27, 32108 s)

By script from `run.log`, `jump/jump.log`, `*/rls.log` and `*/release_ls.jsonl`.

- **ks used: 6017** (a 9.995, kc 260, the start ks, by the octo-double gate from the start ks (the version of d40a9c62): ks 6017 -> 6217 octo-double change **2.0e-89**, bar 1e-70). The jump converged in **1292 s** (22:18:19 - 22:39:51; guess from D 1000 and D 2000, degree 1; the double-double stage floored at 3.206e-13 after 5 iterations and handed to the quad-double stage, as designed), Delta 1.646485791335516559835686890768024038029; its kc+20 line |dF| 1.7e-46 (ks+200 and steps halved the same value: the quad-double check's floor), below the bar 1e-25.
- **Stages (wall):** jump 1292 s; rls h5..h11 19371 s (22:40:37 - 04:03:28); rls13 (h13) 11399 s (04:03:28 - 07:13:27). Every harmonic released; no qd floor, no failed inner solve, no outer step above its harmonic's first (the steps fall by orders of magnitude from outer to outer).

| harmonic | change in Delta (outers) | pending dDelta at release | outer walls (s) |
|---|---|---|---|
| h5 | +2.8957e-9 (o0) then -2.4843e-16, +1.2422e-29 | +2.55e-53 (outer 3) | 2053, 1605, 1220 |
| h7 | -3.0447e-11 (o0), +8.4596e-20 | -1.24e-36 (outer 2) | 2429, 1862 |
| h9 | -6.4932e-13 (o0), -5.3388e-23 | -3.11e-37 (outer 2) | 2412, 1808 |
| h11 | +4.9143e-15 (o0), -1.5632e-24 | -1.53e-33 (outer 2) | 1823, 1773 |
| h13 | **+6.0075e-17** (o0), +6.3353e-24, -8.6407e-27, -6.9803e-32 | -4.04e-36 (outer 4) | 3789, 3002, 2213, 1603 |

- **Delta after h13 (M 32): 1.646485794200099314649352330795089174085** (rls13's last logged Delta); h13's change +6.0075e-17; the full system's qd check max |F| 1.34e-46 (the quad-double floor at this D; the od residual at h13's release 6.17e-49).
- **Bars:** the jump converges and its kc+20 line is below its bar: met. The ks gate passes at 6017 (2.0e-89): met. h5..h13 each released: met. No stop rule hit.
- The M 48 tail script (`tools3/d4000tail_mm5.sh`) started 07:13:31 UTC on this state; its gate and tail results are in `tail/` and the section above.

### The time limits held (2026-11-27 09:34:45 UTC, coordinator's order)

`ladder_point2.sh` runs h5-h11 under `timeout 6h` and h13 under `timeout 4h`, the tail under `timeout 10h`; D 8000 needs about 9.8 h and 5.8 h for its two stages (D 5555 on dh370 was killed this way at 09:16). `tools3/hold_timeouts.sh` (raw 6267c60b4 `I1098-mac-a/tools/hold_timeouts.sh`, blob b9a711cad555836b1887162281073b955c42ce21, verified and read) was started for `D4000/tail` (`bash tools3/hold_timeouts.sh <ladder>/D4000/tail 57600 <ladder>/D4000/tail/hold_timeouts.log`, detached): it stops (SIGSTOP) each `timeout` process whose command names `D4000/tail/`, continues it when its child exits, and ends a child still running 57600 s (16 h) after its timeout was stopped.
First stop: the tail's `timeout 10h` (started 07:14 UTC) `timeout` pid **90867** stopped at 09:34:45 UTC (child 90868; `hold_timeouts.log`; ps shows the timeout in state T, the child running). Later stages' timeouts of this OUT are caught by its 60-s loop.
