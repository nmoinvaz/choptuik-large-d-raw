# I1098-mm5/horizon300: D 300's horizon question, Moebius against u with exact 1/k (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's D 300 horizon check, relayed by coordinator t5. Wave 1 of `../fix/` left the Moebius horizon (a 8, ks 600) **+3.23341e-21** above the u horizon (ks 306) on fastmul5 (f350aa62:
lane-precision reciprocals, the Moebius series' relaxed products). Each run re-solves one of wave 1's two converged states with one horizon parameter changed (`tools/variant_state.py`) by
`release_ls --harm 13 --kmax 13`, the qq Jacobian, the octo-double residual, tol 1e-48; its `rls.log` ends with "h13's change", Delta's change from that state.

## Bars, written before the runs (2026-11-26 13:51 UTC; relayed by the coordinator)

- If Moebius at a 8, ks 600 is right, then ks 800, a 16 and a 4 (each at ks 600 and 800), and the relaxed sums off, each move Delta by **< 1e-23**.
- If u's truncation at ks 306 makes the gap, then u ks+200 and ks+400 both move about **+3.2e-21** toward Moebius, and agree within 1e-23.
- If u's own rounding makes it, they move **< about 1e-22** and do not approach Moebius.
- The horizon whose family stays within 1e-23 is the right one. If the Moebius family spreads by more than 1e-23 itself, report that spread.

Reported: each run's "h13's change" line and the three verdicts (by script).

## Runs (8 re-solves in 3 rounds of up to 3; 3 threads each, nice 10, 1 h cap each; HP_EXACT_RECIP=1, qq, od, tol 1e-48, --harm 13 --kmax 13)

| round | runs (folder name = variant of the state it starts from) |
|---|---|
| 1 | u_ks+200 (from D300_u_base), mob_ks=800 (from D300_mob_base), mob_relax0 (D300_mob_base unchanged, HP_HORIZON_RELAXED=0) |
| 2 | u_ks+400, mob_mob16 (a 16), mob_mob16,ks=800 |
| 3 | mob_mob4 (a 4), mob_mob4,ks=800 |

## Tools and inputs

- `tools/variant_state.py` blob 19b05a5a70e1b6e49f700e176a4d86c265a0ea48 and `tools/horizon300.sh` blob d44d211d5060ae7e2b4260d75569b68047f01b42 (from `I1098-mac-a/tools/` at raw 1f56fa49; verified with `git hash-object --no-filters`).
- States: `../fix/D300_u_base/release_ls_h13_D300.0000.npz` and `../fix/D300_mob_base/release_ls_h13_D300.0000.npz` (wave 1's outputs). Kernel: `~/Source/fastmul5-site`, code `~/Source/choptuik-fastmul5/hp` (f350aa62).
- Command (detached): `bash tools/horizon300.sh <fix>/D300_u_base/release_ls_h13_D300.0000.npz <fix>/D300_mob_base/release_ls_h13_D300.0000.npz <this folder>`.

## Results (2026-11-26 14:42 UTC)

All eight runs rc 0 (`<name>/run.log`), 13:51:18-14:27:39 UTC, kernel `~/Source/choptuik-fastmul5/hp` + fastmul5-site (`kernel.txt`). "h13's change" is the log's line; the changes are by script from the logs' digits (mpmath).

| run | h13's change | what the log shows |
|---|---|---|
| u_ks+200 (ks 306 -> 506) | **-7.612e-24** | outer 0 step -7.612e-24 (target |F| 6.00e-48 -> 1.57e-68), outer 1 released |
| u_ks+400 (ks 306 -> 706) | **-7.612e-24** | the same; ks+200 minus ks+400 = **0.0** |
| mob_ks=800 | +0.000e+00 | released at outer 0 with no step: target |F| 1.21e-53 at the new ks |
| mob_relax0 (relaxed sums off) | +0.000e+00 | released at outer 0: target |F| 1.08e-57 |
| mob_mob4 (a 4, ks 600) | +0.000e+00 | released at outer 0: target |F| 1.21e-53, harmonic-13 step 8.80e-28 |
| mob_mob4,ks=800 | +0.000e+00 | released at outer 0: target |F| 1.21e-53, step 8.80e-28 |
| mob_mob16 (a 16, ks 600) | no end line | outer 0: all six trials 'inner NOT converged in 6 steps' (|F| 1.7e-20 ... 1.08e-20 against 1.09e-25), no step accepted, 1918 s; the run ends unreleased with Delta unchanged |
| mob_mob16,ks=800 | **-4.809e-13** | outer 0 -4.81e-13, outer 1 +9.046e-17, outer 2 released (target |F| 5.41e-55) |

Wave 1 left the Moebius horizon (a 8, ks 600) **+3.23341e-21** above the u horizon (ks 306).

Verdicts against the bars:
- **u's truncation at ks 306 is not the gap.** u ks+200 and ks+400 move -7.6e-24 each, not about +3.2e-21 toward Moebius, and agree to 0.0 (within 1e-23).
- **u's own rounding, as the bar words it: yes.** They move below 1e-22 (-7.6e-24) and do not approach Moebius (they move away).
- **The Moebius family at a 8 / a 4 and ks 600 / 800, and the relaxed sums off, stay within 1e-23** of the a 8, ks 600 state (all +0.000e+00: each was already a solution of the changed system to |F| 1.2e-53 or less, so the first-order shift is below about 6e-34 at the full system's D 300 gain of about 5e19).
  **a 16 does not**: at ks 800 it moves Delta by **-4.809e-13**, and at ks 600 its inner solves do not converge. The Moebius family spreads by 4.8e-13 through a 16, an under-resolved horizon (at a 16 the series needs more than ks 800).
- Both the u family (ks+200, ks+400) and the Moebius family at a <= 8 are stable within 1e-23 themselves; **neither moves toward the other**, so the +3.23e-21 gap between them is not explained by either one's discretization (ks, a) or by the relaxed sums.
- A coincidence to look at: mob_ks=800, mob_mob4 and mob_mob4,ks=800 have the same target |F| (1.21e-53) and the same harmonic-13 step (8.80e-28) to three digits, though they change different parameters.
