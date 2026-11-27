# I1098-mm5/ladder/D6666: D 6666's M 32 stages by recipe v2's amendment 2 (the L-20 last node, the downward ks gate) on fastmul7 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 01:01 UTC): D 6666 queued for D 2828's 6 threads. The script waits by itself for D 2828's "job rc" line in `../D2828/run.log` (every 10 min, at most 14 h; D 2828 started 23:51 UTC, ETA about 9-10 h), then runs detached:

```
TC=c281b00d3dd00ab1a9f9880cb332bf1b14325433 bash tools3/d6666_mm5.sh        # from the ladder folder
```

`tools3/d6666_mm5.sh` (raw c281b00d3 `I1098-mac-a/tools/mm5/d6666_mm5.sh`, blob b931a959c738824bbecdff244e900ad3965dcbe9, verified). After the wait it writes its tools from raw TC into `tools4/` (`ladder_new.sh` 3039e5b9b92dc98280a0e9e52b55f71a00b6165d, `ladder_point2.sh` e0cf58809f062a6791e7d982369be5eaa57d97ad checked in the script, `variant_state.py`, `resample_m.py`, `kstar_*`, `kmax_rule.py`),
writes the three sources from their blobs into `../inputs` (#1088's lastnode states at D 4000, 5657 and 8000: f06d04d5b98e1df5b8040c263ea50d5e882f60f7, 127bbb585763caf0029e903c455cb65dc1907319, 511a1ff828a54aa235775c972082b4a5876274f2; each checked by blob) and installs `ks_gate.py` of wip/large-d-form-s 3b3bfc60 (blob a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7; it takes `--down` and `--ks0`) as `~/Source/choptuik-fastmul7/hp/ks_gate.py`
(that worktree's tracked file, d40a9c62's, is replaced; the records still name d40a9c62 as HP's HEAD). All of it was pre-flighted before the wait (every blob read from raw and hashed), so a failure cannot come after the wait.

Stages (`tools4/ladder_new.sh`): the guess by `form_s_lastnode.py guess` (degree 2 in 1/n from the three sources, carried outward to the last node **x_l 0.7062221251334241** by Taylor steps: D 8000's L = 20 node; L = (n/2) ln(1/x_l^2 - 1) = 16.66 here, by script),
the jump from it (`form_s.py jump`, degree 0, held, the Moebius horizon a = max(8, n/400) = **16.66**, start ks = ceil(1.5 n) + 20 = **10016**, kc 260, dd then qd, it_max 12, `timeout 4h`), then `ladder_point2.sh` (keeps the converged jump) with the downward gate
(`KSGATE_EXTRA="--down 1 --step 100 --ks0 8000"`: from KS0 = 1.2 n rounded to 10 = 8000, stepping up when KS0 fails the bar), KSBAR 1e-64, then h5..h11 and h13 (STOP_AFTER=rls13; the M 48 tail is a later job). fastmul7 (d40a9c62, kernel `~/Source/fastmul7-site`), chord-free, kc 260, 6 threads. Output in `D6666/`; the last act writes "job rc N" to its `run.log`.

## Bars, written before the run (coordinator's order, with D 1291's)

- The guess is built and its max |F| reported (dh610's ratio test for this guess read 3.7e-12; no bar was set for it). The jump converges, and its kc+20 line reads |dF| 0 or below its bar (the jump's discretization bar, 1e-25).
- The downward ks gate passes the bar 1e-64: log the ks it settles on (and its octo-double change). h5..h13 are each released.
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
- Pilot: report the guess's max |F|, the jump's time, the gated ks and h5 outer 0's time. Times from `date -u`.

## Dropped (2026-11-26 02:37 UTC, coordinator's order)

The queued D 6666 is dropped on this machine: **D 6666 moved to dh610, started 02:36:42 UTC.** The waiting `tools3/d6666_mm5.sh` (it was only polling for D 2828's "job rc"; no tools4, no setup, no output beyond this README and `driver.log`) was stopped by exact pid (bash 63250, its `sleep 600` 68448) at 02:37 UTC.
Nothing was installed: `~/Source/choptuik-fastmul7/hp/ks_gate.py` is still the one of d40a9c62. The bars above are not run here.
