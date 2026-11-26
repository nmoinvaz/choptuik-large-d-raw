# I1098-mm5/ladder/D622: D 622 full direct solve on the Moebius horizon, recipe v2, tail at M 48 to h23 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Command (coordinator's order, 2026-11-26 18:27 UTC; D 622 and D 747 moved from dh370 to this runner), detached, 6 threads, from the ladder folder:

```
KSBAR=1e-64 bash tools/ladder_point2.sh 622 200 6 <ladder>/D622 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

`tools/ladder_point2.sh` (blob da887d7143bf94d45d99fcd168550d0e56437370, verified; the same as D 1291's; the inputs are `../inputs/`, absolute paths because the script changes directory). kc 200, the Moebius horizon a = max(8, (D - 2)/400) = 8,
start **ks = ceil(1.5 (D - 2)) + 20 = 950**, raised by 200 (at most 4 times) until the jump's ks+200 |dF| is at most KSBAR = 1e-64. That check is the quad-double residual's change, whose own floor read 1.2e-45 to 1.8e-45 at D 1291 (`../D1291/README.md`):
the ks the loop settles on is then confirmed by the octo-double gate `hp/ks_gate.py` (raw/main f398e829, in `~/Source/choptuik-fastmul6c`, bar 1e-64, 2 threads) on the jump state, run beside the point.
Stages (`run.log`, each log and state in its folder): `jump/`, `rls/` (h5..h11 to tol 1e-36), `rls13/` (h13 to 1e-48, ddelta 1e-25, octo-double residual), `tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h23, qq, od, tol 1e-48, ddelta 1e-25). fastmul6, Python 478e9d86.

## Bars, written before the run (coordinator's order)

- The jump converges and the ks gate passes (the ks it settled on is logged). h5..h13 are each released.
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change is at most about 1e-23, and h23 is released with a pending dDelta at most about 1e-26: no turn.
- Stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial (D 432's u tail), or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped (amended 2026-11-26 19:01 UTC, coordinator's order; the order first read: any inner solve that does not converge).
- Reported: the final Delta, each stage's time, the ks used; each point is pushed at its end. Times from `date -u`.

## Result (the run ended 2026-11-26 20:13:28 UTC, rc 0; 18:27:30 - 20:13:28, 6358 s)

By script from `run.log`, `*/rls.log`, `*/release_ls.jsonl` and `tail/direct_s.jsonl`.

- **ks used: 1150** (a 8, kc 200, the M 32 stages at ks 1150 and the M 48 tail). The jump loop: ks 950 (ks+200 |dF| 5.9e-58, qd), then ks 1150 (exact 0.0e+00), converged, Delta 1.660501828209608173503366183993855895773; 86 s.
  The ks gate, run by hand on the ks 1150 state with the octo-double `ks_gate.py` (f398e829): **ks 1150 -> 1350: 2.96e-74** (bar 1e-64), `ksgate/README.md`.
- **Stages (wall):** jump loop 86 s; rls h5..h11 1618 s (18:28:56 - 18:55:54; each of h5-h11 released); rls13 (h13, M 32) 864 s (-> 19:10:18; qd Jacobian floored at outer 0 and handed to qq, logged; qq outer 1 converged; h13's change -3.673e-16; qd check max |F| 5.24e-63); tail (M 48) 3790 s (-> 20:13:28).
- **Tail** (`tail/rls.log`, h13 re-converged on M 48, then h15..h23; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge) | +4.5794e-26 | -4.56e-26 (outer 1) | 796 s |
| h15 | -3.1667e-17 | +5.80e-32 | 792 s |
| h17 | -1.795e-19 | -4.77e-33 | 784 s |
| h19 | +4.5905e-22 | +3.85e-34 | 633 s |
| h21 | +5.5361e-24 | -3.14e-28 | 623 s |
| h23 | none | **+2.37e-27** (harmonic step 1.30e-14), released at outer 0 | 160 s |

- **Final Delta (the state's `Delta_parts` summed at 60 digits): 1.660501812395454452123410593519465372918** (h23's pending not in it); total -3.18458e-17 from the M 48 start. State `tail/release_ls_h23_D622.0000.npz`, blob 042eaacf1631cd77470816fc6ceb33ef3adf9555; od solve max |F| 6.59169e-53, qd check 6.59169e-53;
  Hamiltonian check at the four nodes at most: p 7.2e-32, m 7.1e-32, a 2.5e-32, c 3.6e-30. The recorded commit field reads 478e9d86 (the Python used).
- **Bars:** the jump converged and the ks gate passed (ks 1150: yes); h5..h13 each released: yes; the tail falls from h15 by about 1e2 or more per harmonic: h15/h17 = 176, h17/h19 = 391, h19/h21 = 83 (D 432: 182, 308, 91); **h21's change 5.54e-24 (at most about 1e-23): met; h23 released with pending +2.37e-27 (at most about 1e-26), no turn: met.**
  No qq inner solve failed, no line-search trial below lam 1, no outer step above 3x its harmonic's first.
