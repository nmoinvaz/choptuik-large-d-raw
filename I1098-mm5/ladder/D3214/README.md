# I1098-mm5/ladder/D3214: D 3214's full point by recipe v2's amendment 2 (the L-20 last node, the downward ks gate) on fastmul7, chord-free, to the M 48 tail at kmax 23 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 11:10 UTC): D 3214's full point, moved here from win2 (unreachable since its 10:25 UTC reboot), into the 6 threads D 2828 freed:

```
TC=0934a63e4 bash tools3/d3214_mm5_v2.sh        # detached, from the ladder folder
```

`tools3/d3214_mm5_v2.sh` (raw 0934a63e4 `I1098-mac-a/tools/mm5/d3214_mm5.sh`, blob 2e6271527feffe2bcda6f08cae1061ab791f7679, verified and read; the first version, ea28badf6 blob 8c756b91, is `tools3/d3214_mm5.sh`: see the first attempt below). It writes its tools from raw TC into **`tools5/`** (not `tools4/`: D 8000's running bash reads `tools4/ladder_point2.sh`), checks `ladder_point2.sh` (e0cf5880), `ladder_new.sh` (3039e5b9) and `hold_timeouts.sh` (b9a711ca) by blob, checks fastmul7's `hp/ks_gate.py` (3b3bfc60's, blob a91c7363), writes the three sources from their blobs into `../inputs`
(#1088's lastnode states at D 2828.4271, 4000 and 5656.8542: 52f878b7, f06d04d5, 127bbb58) and starts `hold_timeouts.sh` beside it on `D3214/` (cap 57600 s per stage). All of it was pre-flighted before the start (every blob read from raw and hashed).

Stages (`tools5/ladder_new.sh`): the guess by `form_s_lastnode.py guess` (degree 2 in 1/n from the three sources, which bracket D 3214, carried to the last node **x_l 0.7058552367160431**, the largest source's own fifth node, its true L = 20 node; L = 11.36 here, by script), the jump from it (degree 0, held, the Moebius horizon a = max(8, n/400) = **8.03**, start ks = ceil(1.5 n) + 20 = **4838**, kc 250),
then `ladder_point2.sh` with the downward gate (`--down 1 --step 100 --ks0 3850`, 1.2 n rounded to 10), KSBAR 1e-64, h5..h11, h13, the M 48 tail to **kmax 23** and the k* stage (no STOP_AFTER), as D 2828 ran. fastmul7 (d40a9c62, kernel `~/Source/fastmul7-site`), chord-free, kc 250, 6 threads. Output in `D3214/`; the last act writes "job rc N" to its `run.log`.

## Bars, written before the run (coordinator's order)

- The jump converges (its kc+20 line |dF| 0 or below its bar 1e-25), and the downward ks gate passes (log the ks it settles on and its octo-double change). h5..h13 are each released.
- The M 32 -> 48 shift (the h13 re-converge at M 48) is about 1e-25 or less. The tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23 released with a pending dDelta at most about 1e-26 and no step: no turn. `kmax_rule.py` on the tail's `release_ls.jsonl`: **exit 0**.
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Pilot: report the guess's max |F| per block, the jump's time and end, the gated ks and h5 outer 0's time. Reported: the final Delta, each stage's time, the ks used, the k* stage. Times from `date -u`.

## First attempt (2026-11-27 11:10 UTC, `attempt0_x_l_error/`): the guess refused its x_l

`tools3/d3214_mm5.sh` (raw ea28badf6, blob 8c756b91) had x_l = 0.7058552367050799, the L = 20 node computed from D rounded to 5656.8542 (n = 5654.8542: L 19.99999999999939 by script). The source `lastnode_D5656.8542.npz` is the state of the exact D (4000 sqrt 2), whose own fifth node is **0.7058552367160431** (1.0963e-11 larger), so the x_l lay inside it and
`form_s_lastnode.py` refused: "x_l 0.7058552367050799 lies inside the source's fifth node 0.7058552367160431: the path runs outward only", "no guess", **job rc 3 at 11:10:12 UTC** (setup passed; nothing ran; `attempt0_x_l_error/pre.log`, `run.log`). The coordinator's error (it had taken D rounded to 4 decimals); corrected script 0934a63e4 (blob 2e627152; only the constant and a comment differ, by diff), started below with the same bars.
