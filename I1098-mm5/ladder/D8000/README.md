# I1098-mm5/ladder/D8000: D 8000's M 32 stages by recipe v2's amendment 2 (the L-20 last node, the downward ks gate) on fastmul7 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 06:31 UTC): D 8000, the ladder's top point, moved here from win2's queue, into D 2231's 6 freed threads, now (no wait):

```
TC=c281b00d3dd00ab1a9f9880cb332bf1b14325433 bash tools3/d8000_mm5.sh        # detached, from the ladder folder
```

`tools3/d8000_mm5.sh` (raw 92fe0208e `I1098-mac-a/tools/mm5/d8000_mm5.sh`, blob a1b357b41cc455ac19d53fb98345b5543d49e6d4, verified and read; it is `d6666_mm5.sh` without the wait). It writes the tools pinned at raw TC c281b00d3 into `tools4/` (`ladder_new.sh` 3039e5b9, `ladder_point2.sh` e0cf5880 checked in the script, the others), writes the three sources from their blobs into `../inputs`
(#1088's lastnode states at D 4000, 5657 and 8000: f06d04d5, 127bbb58, 511a1ff8; at D 8000 the last is the lastnode state itself), and **installs `ks_gate.py` of wip/large-d-form-s 3b3bfc60 (blob a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7; `--down`, `--ks0`) as `~/Source/choptuik-fastmul7/hp/ks_gate.py`** (the install time is in `setup.log`, and noted in `../D4000/README.md`).
It is safe for the running points: the diff of the two versions adds only the downward gate and `--ks0` (read here: the options and defaults of the upward gate are unchanged); D 2828 and D 1549 passed their gates already, and D 4000's tail uses the upward gate.

Stages (`tools4/ladder_new.sh`): the guess by `form_s_lastnode.py guess` (degree 2 in 1/n from the three sources, carried outward to the last node **x_l 0.7062221251334241**, D 8000's own L = 20 node), the jump from it (degree 0, held, the Moebius horizon a = max(8, n/400) = **19.995**, start ks = ceil(1.5 n) + 20 = **12017**, kc 260, dd then qd, it_max 12),
then `ladder_point2.sh` with the downward gate (`--down 1 --step 100 --ks0 9600`), KSBAR 1e-64, h5..h11 and h13 (STOP_AFTER=rls13; the M 48 tail is a later job). fastmul7 (d40a9c62 with that `ks_gate.py`, kernel `~/Source/fastmul7-site`), chord-free, kc 260, 6 threads. Output in `D8000/`; the last act writes "job rc N" to its `run.log`.

## Bars, written before the run (as D 6666's; coordinator's order)

- The guess is built and its max |F| reported (**expect about 1e-16 in every block**; dh610's ratio test read 1.1e-16). The jump converges, and its kc+20 line reads |dF| 0 or below its bar (the jump's discretization bar, 1e-25).
- The downward ks gate passes the bar 1e-64: log the ks it settles on (**expect about 1.09 n, 8700**) and its octo-double change. h5..h13 are each released.
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
- Pilot: report the guess's max |F|, the jump's time, the gated ks and h5 outer 0's time. Times from `date -u`.

### The time limits held (2026-11-27 09:34:45 UTC, coordinator's order)

`ladder_point2.sh` runs h5-h11 under `timeout 6h` and h13 under `timeout 4h`, the tail under `timeout 10h`; D 8000 needs about 9.8 h and 5.8 h for its two stages (D 5555 on dh370 was killed this way at 09:16). `tools3/hold_timeouts.sh` (raw 6267c60b4 `I1098-mac-a/tools/hold_timeouts.sh`, blob b9a711cad555836b1887162281073b955c42ce21, verified and read) was started for `D8000` (`bash tools3/hold_timeouts.sh <ladder>/D8000 57600 <ladder>/D8000/hold_timeouts.log`, detached): it stops (SIGSTOP) each `timeout` process whose command names `D8000/`, continues it when its child exits, and ends a child still running 57600 s (16 h) after its timeout was stopped.
First stop: the rls h5..h11 stage's `timeout 6h` (started about 08:05 UTC) `timeout` pid **95515** stopped at 09:34:45 UTC (child 95516; `hold_timeouts.log`; ps shows the timeout in state T, the child running). Later stages' timeouts of this OUT are caught by its 60-s loop.

## D 8000's M 48 tail, the ladder's last stage (coordinator's order, 2026-11-27 15:13 UTC; armed now, it waits for the M 32 job)

`tools3/d8000tail_mm5.sh` (raw debca1365 `I1098-mac-a/tools/mm5/d8000tail_mm5.sh`, blob 263c54dff12b1fc699027705f9dcc4cb1ef934ae, verified and read), detached from the ladder folder, `WAIT_H=10` by default. It checks `tools3/` `ladder_tail.sh` (322f0995), `kmax_rule.py` (196f12a5), `kstar_stage.sh` (6d29dfc0) and `hold_timeouts.sh` (b9a711ca) by blob (tools3 is read, not written), then waits for "job rc 0" in `run.log` and rls13's h13 state
(`rls13/release_ls_h13_D8000.0000.npz`; h13 outer 0 started 15:10:37 UTC; at most 10 h). Then, into `tail/` (the last act writes "job rc N" to `tail/job.log` and `tail/run.log`), on fastmul7 (d40a9c62), chord-free, **12 threads** (the 6 that D 4000 freed and D 3214's, which end about when D 8000's h13 does; if D 3214's tail is still running then, the machine runs 18 threads on 18 cores):

1. **The ks:** the downward gate put D 8000 at ks 8600 on the M 32 jump state. It is checked on the tail's own start: rls13's h13 state resampled to M 48, set to ks 8600 (a 19.995), then the **upward gate** (`ks_gate.py`, steps of 100, bar 1e-64, the bar D 8000 was run to) from 8600; the tail takes the ks it gates at.
2. `ladder_tail.sh mob` (MT 48 at that ks, h13 re-converged and h15..h23 released, kmax 23, qq, od, tol 1e-48, tol_h 1e-44, ddelta 1e-25), then the k* stage (`kstar_stage.sh`).
3. `kmax_rule.py` on the tail's `release_ls.jsonl`: exit 0, kmax 23 suffices; exit 2, the h25 extension (`release_ls` from the h23 state, `--harm 25 --kmax 25`, qq, od) and the k* stage again into `tail/kstar25`. `hold_timeouts.sh` runs beside it on `D8000/tail` (cap 57600 s per stage).

### Bars, written before the run (as D 4000's tail)

- **The ks gate at the M 48 start passes, or steps up** (log the ks it gates at and its octo-double change).
- The h13 re-converge at M 48 moves Delta by about 1e-25 or less (D 300 +7.3e-26, D 360 +4.8e-26, D 622 +4.6e-26, D 1291 -2.8e-26, D 1549 -3.2e-26, D 2231 -3.8e-26, D 2828 -4.0e-26, D 4000 -4.3e-26).
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23 released with a pending dDelta at most about 1e-26 and no step: no turn. The kmax rule at the end (exit 0).
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Reported: the gated ks, h13's re-converge, the final Delta, each stage's time, the k* stage and the kmax rule's output. Times from `date -u`.

## Result of the M 32 stages (the job ended 2026-11-27 17:58:12 UTC, "job rc 0"; 06:31:39 - 17:58:12, 41193 s = 11 h 27 min)

By script from `run.log`, `pre.log`, `jump/jump.log`, `*/rls.log`, `*/release_ls.jsonl` and `hold_timeouts.log`.

- **The guess:** max |F| per block (double-double) 8.2e-17, 1.0e-16, 9.6e-17, 9.7e-17, 1.1e-16, 5.3e-17, 5.2e-18 (12 s, 1085 Taylor steps, x_l 0.7062221251334241, L 20.000 by script).
- **The jump** (rc 0, 07:54:04): **4856 s** (06:33:08 - 07:54:04): the dd stage 5 iterations of about 735 s (the 5th rejected at |F| 1.977e-22, lam 0, the floor), then 1 qd chord step 1.350e-20 -> 1.812e-26 in 20 s; Delta 1.645190211705390837094174007454207108275; end state od max |F| 1.812e-26; kc+20, ks+200 and steps-halved |dF| all 3.7e-55 (the quad-double check's floor), below the bar 1e-25.
- **The downward ks gate** from ks0 9600 (07:54:04 - 08:05:43, 699 s): **gated ks 8600** (1.075 n; 8600 -> 8700 2.59e-68 met, 8500 -> 8600 2.84e-53 over the bar; the control: Delta + 1e-40 at ks 8600 changes the residual by 1.62e-45, must exceed 1e-64: fires).
- **Stages (wall):** rls h5..h11 **25493 s** (08:05:43 - 15:10:36, 7 h 5 min, past the stage's `timeout 6h`: the held timeout, `rc 124` logged, the h11 state present); rls13 (h13) **10055 s** (15:10:37 - 17:58:12, 2 h 48 min, inside its `timeout 4h`, which was held anyway).

| harmonic | change in Delta (outers) | pending dDelta at release | outer walls (s) |
|---|---|---|---|
| h5 | +4.5166e-10 (o0), -3.6406e-17 | +5.10e-32 (outer 2) | 3760, 2725 |
| h7 | +1.4083e-10 (o0), +1.7742e-18 | +2.88e-33 (outer 2) | 3594, 2716 |
| h9 | -2.6891e-11 (o0), +3.6285e-18 | +6.36e-30 (outer 2) | 4452, 2649 |
| h11 | +4.307e-14 (o0) | +3.93e-20 (outer 1) | 2285 |
| h13 | **+1.5829e-14** (o1; o0 the qd outer floored with no step; o2 -2.4916e-22) | +1.42e-41 (outer 3) | 3206, 3787, 2273 |

- **Delta after h13 (M 32, ks 8600): 1.645190212271047273404497925102653469013** (rls13's last logged Delta); the full system's qd check max |F| 9.93e-56; h13's change +1.583e-14. State `rls13/release_ls_h13_D8000.0000.npz`, blob a40d23db09012cc452651921a81b81e392ae9ee7.
- **Bars:** the jump converges and its kc+20 line is below its bar: met; the downward ks gate passes at 8600: met (expected about 8700: 1.075 n instead of 1.09 n); h5..h13 each released: met. h13 outer 0 (qd) floored above its target (|F| 1.64e-35 against 5.71e-38) and handed to qq (logged); qq outer 1 converged in 4 steps (|F| 2.79e-59); no stop rule hit.
- **The hold on its timeouts:** `hold_timeouts.log`: the 6h rls stage's timeout 95515 stopped 09:34:45, its child ended 15:10:36 (the continued timeout exited 124, which the script only logged); the 4h rls13 timeout 51072 stopped 15:11:06, the child ended 17:58:12; the instance ended itself on the "job rc" line at 17:58:13.
- The M 48 tail script (`tools3/d8000tail_mm5.sh`, armed 15:14:03) starts on this state: its gate, tail and k* stage are the next sections.

## Result of the M 48 tail (the tail ended 2026-11-28 00:06:50 UTC, rc 0; 18:00:32 - 00:06:50, 21978 s, 12 threads)

By script from `tail/job.log`, `tail/rls.log`, `tail/release_ls.jsonl` and `tail/direct_s.jsonl`.

- **The gated ks at the M 48 start: 8600** (`tail/gate/ks_gate.log`: 8600 -> 8700, octo-double change **4.95e-90**, bar 1e-64; a 19.995, kc 260, M 48, fastmul7, chord-free).
- **Tail** (h13 re-converged on M 48, then h15..h23; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | **-4.6064e-26** | +6.01e-31 (outer 1) | 4349 s |
| h15 | -1.2471e-17 | +2.59e-32 | 5408 s |
| h17 | -6.5968e-20 | +3.11e-34 | 3744 s |
| h19 | +1.0315e-22 | +5.54e-27 | 3772 s |
| h21 | +1.3099e-24 | -1.01e-29 | 3751 s |
| h23 | none | **+1.16e-27** (harmonic step 5.85e-16), released at outer 0 | 954 s |

- **Delta of the tail (the state's `Delta_parts` summed at 60 digits): 1.64519021227104726086785096266598692601** (the pendings not in it); total -1.25366e-17 from the M 48 start. State `tail/release_ls_h23_D8000.0000.npz`, blob 39e7a5da07e48e5529364e19ba03078d74c9e60d; od solve max |F| 3.57556e-59, qd check 3.57557e-59;
  Hamiltonian check at the four nodes at most: p 3.9e-32, m 3.9e-32, a 3.1e-32, c 4.7e-30. The record's commit field reads d40a9c62.
- **The kmax rule** (`tools3/kmax_rule.py`, blob 196f12a5, 00:06 UTC): `c19 +1.032e-22, c21 +1.310e-24, r 0.0127 (bar 0.05), the geometric remainder past h21 1.68e-26 (err_tail's, information); h23: 0 steps, pending +1.16e-27: kmax 23 suffices`, **exit 0** (no h25 extension).
- **Bars:** the gate at the M 48 start passes at 8600: met; the h13 re-converge about 1e-25 or less: -4.61e-26, met; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 189, h17/h19 = 640, h19/h21 = 79: met; h21's change 1.31e-24 (at most about 1e-23): met; h23 released with pending +1.16e-27 (at most about 1e-26) and no step, no turn: met; the kmax rule exit 0: met.
  No qq inner solve failed, no line-search trial below lam 1, no floor, no outer step above 3x its harmonic's first. The k* stage started at 00:06:53 (12 threads): its section follows.

### The k* stage (`tail/kstar/`, 00:06:53 - 01:26:55 UTC, 4802 s; `kstar_stage.sh` by the tail script, fastmul7, chord-free, 12 threads) and the end of the point

kfree 15 at the h23 state: gain **2.46139e+30** (the gain solve 910 s), F before 2.99470e-54, **bound before 7.37112e-24** (gain x F), above 1e-27, so **re-converged** (the h15 state, qq, od, tol 1e-62: outer 0 inner converged in 2 steps, |F| 9.14e-93, 2867.5 s, step dDelta +2.59e-32;
outer 1 released with pending -4.50e-53, 968 s for its Newton step): **F after 9.38068e-81; the k* system's Delta moved +2.5889e-32 (from 1.645190212271047260933714217206060026254 to ...085915265); bound after 2.5889e-32.** The full system's qd check 5.70e-56, h13's change +2.589e-32.
`tail/job.log`: "tail rc 0 01:26:55", "kmax_rule rc 0" (the rule's line above), **"job rc 0 01:26:55"**. D 8000's Delta stands at 1.64519021227104726086785096266598692601 (the tail's state at h23; the k* bound after 2.59e-32).
**The whole point:** M 32 stages 06:31:39 - 17:58:12 (41193 s) and the M 48 tail script 17:59:04 - 01:26:55 (26871 s, 12 threads: gate 86 s, tail 21978 s, k* 4802 s): 18 h 55 min (68116 s) from the guess to the end; this was the last stage of the ladder's last point.
The held timeout of the tail (`tail/hold_timeouts.log`: timeout 72007 stopped, its child ended 01:26:55, the timeout continued) is done; the hold instance ended itself on the "job rc" line at 01:27:25.
