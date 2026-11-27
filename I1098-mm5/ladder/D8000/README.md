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
