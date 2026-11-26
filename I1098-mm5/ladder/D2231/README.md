# I1098-mm5/ladder/D2231: D 2231 full direct solve on fastmul7, chord-free, recipe v2, tail at M 48 to h31 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (20:12 UTC, with the 20:08 amendment; the start waits for 6 free threads: after D 360m48 or D 747, whichever ends first), detached, 6 threads, from the ladder folder:

```
EXTRA="--inner_chord 0" HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site KSBAR=1e-70 bash tools/ladder_point2_651b.sh 2231 250 6 <ladder>/D2231 <ladder>/inputs/D2000_base6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 31
```

`tools/ladder_point2_651b.sh` (raw 12a4068d `I1098-mac-a/tools/ladder_point2.sh`, blob 651bb75f4ee290156c16fb6c6c3ef4bd788d224d, verified; it takes the commit from HP's HEAD, d40a9c62). Inputs: D 2000's fastmul6 base h13 (`../inputs/D2000_base6_h13.npz`, blob b897ba43adb46653785b362d2ae6a2f712fdd8db, equal to raw's) and D 1000's (`S1000_D1000_base6_h13.npz`, blob 48db1b6c).
kc 250, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 3364**, raised by 200 until the ks gate (the octo-double `ks_gate.py`) change is at most KSBAR = 1e-70. fastmul7 = fastmul6 plus the Moebius split fix (c21ba40d); the Python at d40a9c62 defaults to `inner_chord 1`, which floored D 747's h13 qq inner solve, so every inner solve here is chord-free (`EXTRA="--inner_chord 0"`).
Stages (`run.log`): `jump/`, `rls/` (h5..h11), `rls13/` (h13), `tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h31).

**The fastmul7 check outcome** (`../../fastmul7-build/README.md`): `horizon_mp_check.py` (D 300 u h21 state, bar 1e-100, controls 1e-80): at `--ks_mob 800` **FAIL**, Moebius against mpmath 4.647e-70, the series' own truncation at ks 800 (not arithmetic: dh610's scan falls by about 1e16 per 200 orders, raw ae3500937);
at `--ks_mob 1600` **PASS**, 9.742e-129 against the bar 1e-100, the old-split control 1.7e-60 and the m_h control 4.62e-28 both firing. The other six checks passed.

## Bars, written before the run (D 1291's, with the amended stop rule)

- The jump converges and the ks gate passes (log the ks it settles on). h5..h13 are each released, and the tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23.
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Reported: the final Delta, each stage's time, the ks used. Times from `date -u`.

## The tail stops after h25, not h31 (2026-11-26 22:20 UTC, coordinator's change)

D 2000's tail showed the harmonics past 21 no longer matter (h21 +2.07e-24, h23 released with no step, pending +1.74e-27). So D 2231's tail stops after h25:

1. D 2231 runs as started: its tail is one `release_ls` at kmax 31 (`ladder_point2_651b.sh`, blob 651bb75f, `timeout 10h`); the higher harmonics stay at zero until released, so h23 and h25 come out as they would in a kmax-25 run.
2. When `tail/rls.log` shows the "released" line of harmonic 25, and `release_ls_h25_D2231.0000.npz` exists, only that `release_ls` python is killed, by exact pid. The script then writes "tail rc 143" and ends (it has no k* stage in this version).
3. Then the k* stage by hand, detached, 6 threads, from the ladder folder: `HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site INNER_CHORD=0 COMMIT=d40a9c62 bash tools3/kstar_stage.sh <ladder>/D2231/tail <ladder>/D2231/kstar 6` (`kstar_stage.sh` blob 6d29dfc0225a2eff0be932cb849e656c190a0b6e, verified in tools3).
4. **Exception: if h23's release takes a step (pending dDelta above 1e-25), or |c21/c19| (h21's change over h19's) is above 0.05, the run is not killed: h27 runs, and it is reported.**

Reported: h21, h23 and h25's changes or pendings, and the k* result. The final Delta of this point is the state at h25 (the h27..h31 harmonics are zero, as in a kmax-25 run).
