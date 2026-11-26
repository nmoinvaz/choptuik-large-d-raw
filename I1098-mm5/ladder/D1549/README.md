# I1098-mm5/ladder/D1549: D 1549's M 48 tail to kmax 31 on fastmul7, chord-free (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Step 2 of the D 1291 chain (`../D1291/README.md`, `../tools3/d1291_then_1549_mm5.sh`, blob 6893d73ff6f623685fc872d2e68a6a41775345af): D 1549's M 32 stages are dh170's (`I1098-dh170/ladder/D1549/`, chord-free); this runner takes its h13 state
(`I1098-dh170/ladder/D1549/rls13/release_ls_h13_D1549.0000.npz`, copied to `../inputs/D1549_rls13_h13.npz`, blob checked against raw's) once dh170's `run.log` in raw reads "rls h13 rc 0" (a fetch every 10 min, at most 12 h after D 1291's k* stage ends; otherwise this step is skipped with a log line).

```
KS=2941 MT=48 KMAX=31 bash tools3/ladder_tail.sh mob 1549 <ladder>/inputs/D1549_rls13_h13.npz <ladder>/D1549/tail 6
```

fastmul7 (Python d40a9c62, kernel `~/Source/fastmul7-site`), chord-free (`INNER_CHORD=0`), 6 threads. The Moebius horizon a = max(8, (D - 2)/400) = 8 at **ks 2941** (dh170's octo-double gate), the state resampled to M 48, h13 re-converged, h15..h31 released (qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25), then the k* stage by itself (`kstar_stage.sh`: the bound at kfree 15, re-converged when gain x F > 1e-27).
Expected to end about 11:00-12:30 UTC (the order's estimate).

## Bars, written before the run (as for D 622 and D 1291, with the amended stop rules)

- The h13 re-converge at M 48 moves Delta by about 1e-25 or less (D 300 +7.3e-26, D 622 +4.6e-26, D 360 +4.8e-26).
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23..h31 each released with a pending dDelta at most about 1e-26: no turn.
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Reported: the final Delta, each stage's time, the ks used, the k* stage's bound before and after. Times from `date -u`.

## The tail is cut at h23 by the kmax rule (2026-11-26 22:23 UTC, coordinator's order; the chain script is not edited)

kmax 23 is now the recipe (D 2000's h23 needed no step; posted on #1098), and D 1549's tail runs at `KMAX=31` in the chain, so it is cut at h23 by hand, with `tools3/kmax_rule.py` (raw 841dd6a8e `I1098-mac-a/tools/kmax_rule.py`, blob 196f12a553edce9651fef58ef90353f3c7fb49b4, verified):

1. When `D1549/tail/rls.log` shows the "released" line of harmonic 23, run `python3 tools3/kmax_rule.py D1549/tail/release_ls.jsonl`. It prints c19, c21, r = |c21/c19| (bar 0.05), h23's steps and pending, the verdict; exit 0 when kmax 23 suffices, 2 when to extend to h25, 1 when the log lacks h19, h21 and h23's release yet.
2. **Exit 0: the tail's `release_ls` python is killed by exact pid.** `ladder_tail.sh` (322f0995) then runs the k* stage on the h23 state and the chain goes on to D 1291's fastmul7 rerun. **Exit 2: wait for h25's release, then kill.**
3. Reported: h19, h21 and h23's changes or pendings, the rule's output, and the k* result.

Checked before use (every check must be able to fail): on the finished tails of D 747, D 622 and D 360m48 it exits 0 (r 0.0124, 0.0121, 0.0103; h23 pending +2.80e-27, +2.37e-27, -3.47e-27, no step); with `--rmax 0.001` on D 747's log it exits 2 ("extend to h25"); on D 747's log cut before h23 it exits 1 ("not yet").
