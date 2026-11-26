# I1098-mm5/ladder/D4000: D 4000's M 32 stages on fastmul7, chord-free (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 21:30 UTC): D 4000's M 32 stages (the jump, the ks gate, h5..h11, h13) on fastmul7, in the second 6 threads that free up: D 2231 takes the first, as already queued; of D 360m48 and D 747, whichever ends second frees these.
The M 48 tail to kmax 31 is a later job.

```
bash <ladder>/tools3/d4000_mm5.sh        # detached, from the ladder folder
```

`tools3/d4000_mm5.sh` (raw ad818d784 `I1098-mac-a/tools/mm5/d4000_mm5.sh`, blob db0549a846de95a541e8781a73ebe132c5cec5f3, verified) runs `tools3/tools3_check.sh` first (blob fa8071b15ae0e882e4b6ec471cf49b588656f506; it writes `tools3/ladder_point2.sh` from blob 8802fb2699aad3b73a9cab94cea5f4431e830bc2 and checks all seven tools3 files by blob: the check printed 7 "ok" lines, exit 0, `tools3/check.log`),
then checks the two inputs by blob (S1000_D1000_base6_h13 48db1b6cf09ca4feebd9ca5a0976ec8154711635, D2000_base6_h13 b897ba43adb46653785b362d2ae6a2f712fdd8db) and runs `ladder_point2.sh 4000 260 6 <ladder>/D4000 S1000 D2000 48 31`.
Settings: fastmul7 (Python `~/Source/choptuik-fastmul7` at d40a9c62, kernel `~/Source/fastmul7-site`), **chord-free** (`INNER_CHORD=0`), kc 260, **KSBAR=1e-70**, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 6017**, gated by the octo-double `ks_gate.py` (steps of 200 until the residual change at ks + 200 is at most KSBAR),
`STOP_AFTER=rls13` (the point ends after its M 32 stages; the h13 state is left for a tail elsewhere). The jump fits in 1/n to the two inputs. Output in `<ladder>/D4000` (`jump/`, `rls/`, `rls13/`, `run.log`; its last act writes "job rc N").

## Bars, written before the run (coordinator's order)

- The jump converges, and its kc+20 line reads |dF| 0 or below its bar (the jump's discretization bar, 1e-25).
- The ks gate passes (log the ks it settles on, and its octo-double change).
- h5..h13 are each released.
- Stop rules: stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped. A qq floor at h13 outer 0 right after an M resample is logged; a floor above 1e-48 at any later outer step stops the run.
- Pilot: report the jump's time, the gated ks and h5 outer 0's time. ETA 6-8 h (14 h worst case). Times from `date -u`.
