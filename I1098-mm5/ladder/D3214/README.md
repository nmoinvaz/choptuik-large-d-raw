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

## Result of the point (the job ended 2026-11-27 20:43:14 UTC, "job rc 0"; 11:11:43 - 20:43:14, 34291 s = 9 h 32 min)

By script from `run.log`, `pre.log`, `jump/jump.log`, `*/rls.log`, `*/release_ls.jsonl`, `tail/direct_s.jsonl` and `kstar/`.

- **The guess:** max |F| per block (double-double) 1.1e-12, 1.3e-12, 2.3e-12, 3.8e-12, 6.9e-12, 2.7e-11, 2.0e-17 (3 s, 463 Taylor steps, x_l 0.7058552367160431, L 11.36). **The jump** (rc 0, 11:24:14): 724 s (dd stage 3 iterations of about 155 s, floor 1.146e-24, then a qd chord step 1.506e-23 -> 1.059e-30); Delta 1.647119154482215312701662362353176675330; kc+20 |dF| 1.2e-57, below the bar 1e-25.
- **The downward ks gate** from ks0 3850: **gated ks 3750** (1.167 n; 3750 -> 3850 1.64e-65 met, 3650 -> 3750 1.49e-53 over the bar; the control 6.72e-45 fires).
- **Stages (wall):** rls h5..h11 7528 s (11:25:25 - 13:30:53); rls13 (h13, M 32) 4053 s (-> 14:38:26; the qd outer 0 floored with no step, qq outer 1 converged to 7.08e-50 and took h13's change **+8.7763e-14**, 1.5e3-9.7e3 times the other points': the loose h11 release left a pending +6.60e-14, an untested reading); tail (M 48, ks 3750) **18042 s** (14:38:27 - 19:39:09); k* stage **3845 s** (19:39:09 - 20:43:14).
- **Tail** (h13 re-converged on M 48, then h15..h23; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | **-4.1456e-26** (outers -4.1286e-26, -1.6974e-28) | -3.50e-40 (outer 2) | 4637 s |
| h15 | -1.4283e-17 | +2.73e-32 | 3297 s |
| h17 | -7.7677e-20 | -1.16e-29 | 3323 s |
| h19 | +1.2827e-22 | +8.85e-29 | 2953 s |
| h21 | +1.6318e-24 | +3.19e-26 | 3078 s |
| h23 | none | **+3.33e-26** (harmonic step 1.25e-15), released at outer 0 | 754 s |

- **Delta of the tail (the state's `Delta_parts` summed at 60 digits): 1.647119154952014562939289165487672774203** (the pendings of h13..h23 not in it; their sum is about +6.5e-26); total -1.43607e-17 from the M 48 start. State `tail/release_ls_h23_D3214.0000.npz`, blob 1f6d3006133b2dee87f984dc247dcbe95f98d440; od solve max |F| 5.67822e-58, qd check 5.67822e-58;
  Hamiltonian check at the four nodes at most: p 3.4e-32, m 3.4e-32, a 2.5e-32, c 2.4e-30. The record's commit field reads d40a9c62.
- **The kmax rule** (`tools3/kmax_rule.py`, blob 196f12a5, 19:39 UTC): `c19 +1.283e-22, c21 +1.632e-24, r 0.0127 (bar 0.05), the geometric remainder past h21 2.10e-26 (err_tail's, information); h23: 0 steps, pending +3.33e-26: kmax 23 suffices`, **exit 0**.
- **The k* stage** (`kstar/`; kfree 15 at the h23 state): gain **2.993397e+32** (against 9.6e26 at D 2231, 7.4e24 at D 2828, 2.8e20 at D 4000), F before 2.16868e-51, **bound before 6.49171e-19** (gain x F), above 1e-27, so **re-converged** (the h15 state, qq, od, tol 1e-62; outer 0 inner converged in 2 steps, |F| 2.02e-90, 2300.6 s, step dDelta +2.73e-32;
  outer 1 released with pending -2.41e-46): **F after 4.21776e-78; the k* system's Delta moved +2.7340e-32; bound after 2.7340e-32.** The full system's qd check 4.69e-59, h13's change +2.734e-32.
- **Bars:** the jump converges: met; the downward gate passes (ks 3750): met; h5..h13 each released: met; the M 32 -> 48 shift about 1e-25 or less: -4.15e-26, met; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 184, h17/h19 = 606, h19/h21 = 79: met; h21's change 1.63e-24 (at most about 1e-23): met;
  **h23's pending +3.33e-26 against the bar of about 1e-26 or less: not met literally (3.3x; a third of the release bar 1e-25; no step, no turn)**; the kmax rule exit 0: met. No qq inner solve failed after the logged qd floors, no line-search trial below lam 1, no outer step above 3x its harmonic's first.
- **The first attempt** (`attempt0_x_l_error/`) and the corrected script are above. The hold on its timeouts: the instance ended itself on the "job rc" line.
