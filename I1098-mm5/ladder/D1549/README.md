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

## Result of the tail, cut at h23 by the kmax rule (2026-11-27 08:05:00 UTC; 04:05:29 - 08:05:00, 14371 s)

By script from `tail/run.log`, `tail/rls.log` and `tail/release_ls.jsonl`.

- **h13 input:** dh170's chord-free h13 state (blob 014ac56f84b516d4348aefb2ada7d4048ce633c6, verified by the chain), the Moebius horizon a 8 at **ks 2941** (dh170's octo-double gate), M 32 resampled to M 48, fastmul7 (d40a9c62), chord-free, 6 threads, KMAX 31 in the chain.
- **The kmax rule at h23** (`tools3/kmax_rule.py`, blob 196f12a5; run 08:04:53 UTC): `c19 +1.850e-22, c21 +2.422e-24, r 0.0131 (bar 0.05), the geometric remainder past h21 3.21e-26 (err_tail's, information); h23: 0 steps, pending +1.98e-27: kmax 23 suffices`, **exit 0**. As written before the run, the tail's `release_ls` python was then killed by exact pid
  (75484, 08:05:00 UTC, 25 s into h25 outer 0; the h23 state `tail/release_ls_h23_D1549.0000.npz` existed, blob 6d4ba9cc1665567c7f0abe35cf7336b4dcc9201e); `ladder_tail.sh` wrote "rc 143" and went on to the k* stage (`tail/kstar/`, started 08:05:00). There is no `direct_s.jsonl` (the tail was cut before its end record): the Delta below is the last accepted step's Delta in `tail/release_ls.jsonl`.

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | **-3.2257e-26** | -4.34e-32 (outer 1) | 2568 s |
| h15 | -1.7935e-17 | +3.28e-32 | 3114 s |
| h17 | -1.0057e-19 | -1.63e-36 | 3068 s |
| h19 | +1.8496e-22 | +4.82e-36 | 2550 s |
| h21 | +2.4217e-24 | -1.65e-31 | 2496 s |
| h23 | none | **+1.98e-27** (harmonic step 2.87e-15), released at outer 0 | 547 s |

- **Delta of D 1549 (the state at h23; h23 took no step): 1.650580020480835511811831563687484386494** (40 digits as logged; h23's pending not in it); total -1.80352e-17 from the M 48 start. Wall (the machine at 18-24 threads on 18 cores): tail 14371 s.
- **Bars:** the h13 re-converge at M 48 about 1e-25 or less: -3.23e-26, met; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 178, h17/h19 = 544, h19/h21 = 76 (D 1291: 177, 520, 77); h21's change 2.42e-24 (at most about 1e-23): met; h23 released with pending +1.98e-27 and no step, no turn: met; the kmax rule exit 0: met.
  No qq inner solve failed, no line-search trial below lam 1, no outer step above 3x its harmonic's first, no floor.

### The k* stage (`tail/kstar/`, the chain's `ladder_tail.sh` ran it on the h23 state; 08:05:00 - 08:14:51 UTC, 591 s; `kstar_stage.sh` blob 6d29dfc0225a2eff0be932cb849e656c190a0b6e, fastmul7, chord-free)

kfree 15 at the h23 state: gain 2.703635e+22, F before 1.57819e-53, **bound before 4.26685e-31** (gain x F), below 1e-27: **no re-converge** (reconv false). The chain then ended its D 1549 step ("D 1549 tail rc 0 08:14:51").
