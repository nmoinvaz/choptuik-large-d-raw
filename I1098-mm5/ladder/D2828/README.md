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
