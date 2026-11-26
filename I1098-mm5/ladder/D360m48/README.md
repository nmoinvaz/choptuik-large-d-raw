# I1098-mm5/ladder/D360m48: D 360's tail at M 48 on fastmul6, the cross-check against dh610's M 32 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 21:02 UTC): a short cross-check that D 360 lacks, D 360's M 48 tail on fastmul6 (about 40 min), run while D 2231 is held for dh610's ks scan. D 2231 waits for it if the scan answers first.

Input: dh610's D 360 M 32 h13 state `I1098-dh610/ladder/D360/rls/release_ls_h13_D360.0000.npz`, copied to `../inputs/D360_rls_h13.npz` (**blob 572bc483fc379317b8c9bf0b64add16431ea4ad3**, equal to raw's).
Tools: `../tools3/` from raw origin/main (`I1098-mac-a/tools/`), blobs verified with `git hash-object`: `ladder_tail.sh` 322f0995ace89827d8265882f2c03defafaa7f1a, `kstar_stage.sh` 6d29dfc0225a2eff0be932cb849e656c190a0b6e, `kstar_gain.py` e74b4fc7464175341dc0b9a77e60507eeccf4363,
`kstar_summary.py` 8e22d799c3822f57919018f60b63beb59bded157, `variant_state.py` 19b05a5a70e1b6e49f700e176a4d86c265a0ea48, `resample_m.py` 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b.

```
MT=48 KS=957 KMAX=23 INNER_CHORD=0 HP=$HOME/Source/choptuik-fastmul6/hp SITE=$HOME/Source/fastmul6-site bash tools3/ladder_tail.sh mob 360 <ladder>/inputs/D360_rls_h13.npz <ladder>/D360m48 6
```

Detached, 6 threads, from the ladder folder; Python 478e9d86 (HP's HEAD, the commit the records name), kernel `~/Source/fastmul6-site`. The Moebius horizon a = max(8, (D - 2)/400) = 8 at **ks 957** (= ceil(1.5 (D - 2)) + 420 = 537 + 420), the state resampled to M 48, h13 re-converged, h15..h23 released
(qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25, --inner_chord 0: the chord-free path of D 432-622, as for every later point), then the k* stage by itself (`kstar_stage.sh`: the bound at kfree 15, re-converged when gain x F > 1e-27).

## Bars, written before the run (coordinator's order)

- The h13 re-converge at M 48 moves Delta by about **1e-25 or less** (D 300: +7.3e-26; D 622: +4.6e-26).
- The final Delta against dh610's M 32 final **1.672499793793157083326890316334382065517** differs by less than **1e-24**. That difference is D 360's `err_xcheck_M`, and it also differs in machine.
- The tail falls as at D 432 (h15 -4.5351e-17, h17 -2.4908e-19, h19 +8.0779e-22, h21 +8.8627e-24, h23 pending +2.24e-28), with no turn at h23.
- Stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
- Reported: both shifts (the h13 re-converge and the final against dh610's M 32), pushed at the end. Times from `date -u`.
