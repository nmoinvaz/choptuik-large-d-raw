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
