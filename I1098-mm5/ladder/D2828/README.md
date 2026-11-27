# I1098-mm5/ladder/D2828: D 2828 full direct solve on fastmul7, chord-free, recipe v2, tail at M 48 to kmax 23 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 23:51 UTC): D 2828 moves to this machine as a full point (dh170's copy is cancelled), into the 6 chain threads that are idle until D 1549's h13 lands (the chain's D 1549 tail then overlaps it briefly, which is fine), beside D 2231 and D 4000.

```
bash <ladder>/tools3/d2828_mm5.sh        # detached, from the ladder folder
```

`tools3/d2828_mm5.sh` (raw de1cf40c4 `I1098-mac-a/tools/mm5/d2828_mm5.sh`, blob 7ce44e16ad8d7886d3a4bd0c854874d95cb2b8af, equal to raw's, verified) runs `tools3/tools3_check.sh` first (7 "ok", `tools3/check3.log`), checks the two inputs (D 2000's fastmul6 base h13 `../inputs/D2000_base6_h13.npz`, blob b897ba43adb46653785b362d2ae6a2f712fdd8db; D 4000's converged jump state
`../D4000/jump/jump_s_D4000.0000.npz`, sha256 d542ecda2fc9...) and runs `tools3/ladder_point2.sh` (blob 8802fb26) `2828 250 6 <ladder>/D2828 D2000 D4000jump 48 23`.
Settings: fastmul7 (Python `~/Source/choptuik-fastmul7` at d40a9c62, kernel `~/Source/fastmul7-site`), chord-free (`INNER_CHORD=0`), kc 250, **KSBAR=1e-64**, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 4259**, gated by the octo-double `ks_gate.py` (steps of 200 until the residual change at ks + 200 is at most KSBAR),
6 threads. Stages: the jump (fitted in 1/n to the two inputs), `rls/` (h5..h11), `rls13/` (h13), `tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h23), then the k* stage by itself (`kstar/`). The last act writes "job rc N" to `run.log`.
After the tail: `python3 tools3/kmax_rule.py D2828/tail/release_ls.jsonl` (blob 196f12a553edce9651fef58ef90353f3c7fb49b4); exit 2 means the h25 extension. ETA about 9-10 h.

## Bars, written before the run (D 1291's, with the amended stop rules; coordinator's order)

- The jump converges and the ks gate passes (log the ks it settles on). h5..h13 are each released.
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23 released with a pending dDelta at most about 1e-26 and no step: no turn. The kmax rule at the end (exit 0: kmax 23 suffices).
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Pilot: report the jump's time, the gated ks and h5 outer 0's time. Reported: the final Delta, each stage's time, the ks used, the k* stage. Times from `date -u`.

### The time limits held (2026-11-27 09:34:45 UTC, coordinator's order)

`ladder_point2.sh` runs h5-h11 under `timeout 6h` and h13 under `timeout 4h`, the tail under `timeout 10h`; D 8000 needs about 9.8 h and 5.8 h for its two stages (D 5555 on dh370 was killed this way at 09:16). `tools3/hold_timeouts.sh` (raw 6267c60b4 `I1098-mac-a/tools/hold_timeouts.sh`, blob b9a711cad555836b1887162281073b955c42ce21, verified and read) was started for `D2828/tail` (`bash tools3/hold_timeouts.sh <ladder>/D2828/tail 57600 <ladder>/D2828/tail/hold_timeouts.log`, detached): it stops (SIGSTOP) each `timeout` process whose command names `D2828/tail/`, continues it when its child exits, and ends a child still running 57600 s (16 h) after its timeout was stopped.
First stop: the tail's `timeout 10h` (started 04:19 UTC) `timeout` pid **76510** stopped at 09:34:45 UTC (child 76511; `hold_timeouts.log`; ps shows the timeout in state T, the child running). Later stages' timeouts of this OUT are caught by its 60-s loop.

## Result of the tail (the tail ended 2026-11-27 10:50:20 UTC, rc 0; the point started 2026-11-26 23:51:33)

By script from `run.log`, `*/rls.log`, `*/release_ls.jsonl` and `tail/direct_s.jsonl`.

- **ks used: 4259** (a 8, kc 250; the jump at ks 4259 converged in 547 s, Delta 1.647558972524858925507238247836385562325, kc+20 and ks+200 |dF| 0.0; the octo-double ks gate: ks 4259 -> 4459 **6.2e-85**, bar 1e-64, the start ks stands).
- **Stages (wall):** jump 547 s; rls h5..h11 10771 s (00:01:17 - 03:00:48); rls13 (h13, M 32) 4725 s (03:00:48 - 04:19:33; h13's change +3.0202e-17, outers +2.4657e-22, -1.9752e-28, released at outer 3 with pending +1.77e-33); tail (M 48) **23447 s** (04:19:33 - 10:50:20, with 18-24 threads on 18 cores).
- **Tail** (h13 re-converged on M 48, then h15..h23; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | **-4.0352e-26** | +2.35e-32 (outer 1) | 4639 s |
| h15 | -1.4717e-17 | +2.67e-32 | 5738 s |
| h17 | -8.0448e-20 | -1.66e-36 | 5189 s |
| h19 | +1.3462e-22 | +3.36e-35 | 3505 s |
| h21 | +1.7518e-24 | -1.73e-33 | 3483 s |
| h23 | none | **+1.50e-27** (harmonic step 1.39e-15), released at outer 0 | 890 s |

- **Final Delta of the tail (the state's `Delta_parts` summed at 60 digits): 1.647558973970246673000322210835632610311** (h23's pending not in it); total -1.47978e-17 from the M 48 start. State `tail/release_ls_h23_D2828.0000.npz`, blob e84608fdeb79087fadb7ff1b9968f01e49c35099; od solve max |F| 1.18264e-55, qd check 1.16685e-55;
  Hamiltonian check at the four nodes at most: p 3.9e-32, m 3.9e-32, a 3.7e-32, c 2.3e-30. The record's commit field reads d40a9c62 (fastmul7).
- **The kmax rule** (`tools3/kmax_rule.py`, blob 196f12a5, run 10:49:59 UTC): `c19 +1.346e-22, c21 +1.752e-24, r 0.013 (bar 0.05), the geometric remainder past h21 2.31e-26 (err_tail's, information); h23: 0 steps, pending +1.50e-27: kmax 23 suffices`, **exit 0**.
- **Bars:** the jump converged and the ks gate passed (ks 4259): yes; h5..h13 each released: yes; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 183, h17/h19 = 598, h19/h21 = 77 (D 1291: 177, 520, 77); **h21's change 1.75e-24 (at most about 1e-23): met; h23 released with pending +1.50e-27 and no step, no turn: met; the kmax rule exit 0: met;**
  the h13 M 32 -> 48 re-converge -4.04e-26 (below 1e-25): met. No qq inner solve failed, no line-search trial below lam 1, no floor, no outer step above 3x its harmonic's first.

### The k* stage (`kstar/`, 10:50:20 - 11:04:40 UTC, 860 s; `kstar_stage.sh` via `ladder_point2.sh` 8802fb26, fastmul7, chord-free) and the end of the run

kfree 15 at the h23 state: gain 7.38006e+24, F before 1.00126e-54, **bound before 7.38938e-30** (gain x F), below 1e-27: **no re-converge** (reconv false). `run.log`: "tail rc 0 10:50:20", "kstar rc 0 11:04:40", "end 2026-11-27 11:04:40 UTC", **"job rc 0 11:04:40"**: the whole point 23:51:33 - 11:04:40, 40387 s (11 h 13 min; the ETA of 9-10 h was for an idle machine, the stages ran at 18-24 threads on 18 cores).
The held timeout of the tail (`tail/hold_timeouts.log`: `timeout` pid 76510 stopped 09:34:45, its child 76511 ended at 10:50:20, the timeout continued) is done; its `hold_timeouts.sh` instance (pid 4172, which only watches `tail/run.log` for "job rc") was ended at 11:05 UTC.
