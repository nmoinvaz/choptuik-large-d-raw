# I611-win: RT's D 50-60 ladders (#404) against hp's quad-double Delta of the uncut problem

Machine win (Surface Laptop 4, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/611 (the coordinator's message `choptuik-large-d/2026-11-12/202829Z-coordinator-9a56.md`; follows #610). Worktree `choptuik-i611` at main f104de5b (`hp/scan_qd.py` with `--kfreeze -1`, 7c15f24; Python only), venv-t151's hpkernel (a build before #523) and multidouble 0.1.0; nothing is built.

## Summary

Seven of the eight own-D quad-double polishes converge; the acceptance (all six polishes converge) is **not met**. The uncut polish at D 60.001952 does not converge (|F| 6.5e-8), and the two polishes at D 54.996085 could not be made: no hp state of that D is kept, `scan_qd.py`'s continuation to it fails on this machine, and an interpolated start fails with its control.

| D | cut's effect (no cut - kf 13) | #404's verdict | against the uncut Delta |
|---|---|---|---|
| 50.007491 | -1.0431e-15 (measured) | falls below 1e-14 at N* = 103 | unchanged, N* = 103, E_uncut = 1.91e-15 |
| 54.996085 | -1.2096e-15 (interpolated from D 54.04 and 55.04) | stops falling at 99 | unchanged, N_s = 99, E_uncut = 3.64e-14 (estimated reference) |
| 60.001952 | not measured | stops falling at 99 | unchanged, N_s = 99, E = 1.80e-12 (against the kf 13 value) |

The cut moves the reference by about 1.2e-15 at D 50 to 55, which is small against every ladder's miss except D 50's best grid (2.95e-15 becomes 1.91e-15).

## Plan, written before the runs (the issue's acceptance)

- Polish hp's states in quad-double with `hp/scan_qd.py`, each with D_END equal to its own D, with `--kfreeze 13` and with `--kfreeze -1` (no cut), each run with its own `--tag` (both runs save as `<tag>_D<D>.npz`):
  `python -u scan_qd.py RAW/I611-win/qd_<tag>.jsonl data/states/<state>.npz <D> --kfreeze K --threads 3 --tag <tag>` (from hp/).
- States: D 50.007491 `hp/data/states/up8_D50.0075.npz` (its own D), D 60.001952 `hp/data/states/up13_D60.0020.npz` (its own D). **D 54.996085: no state of that D is kept** (`hp/data/states` holds the up10 run at 53.7914, 54.0414 and 55.0351; the row of `delta_all.csv` is from the run's records, its `state` column is empty). So `scan_qd.py` continues from `up10_D55.0351.npz` (D 55.035148) to D_END = 54.996085 (one step of 0.039063), and, as a check of the continuation, from `up10_D54.0414.npz` (D 54.041398) to the same D_END; the two must agree.
- Convergence: all polishes converge (max|F| <= 1e-50, or `scan_qd.py`'s accepted stall, reported).
- Per D: the cut's effect (no cut - kf 13), and #404's E(N) re-read against the uncut Delta for every N and both roots: Delta_RT (the 30-digit `Delta_str` of the records in `I404-win/roots`) minus Delta_qd(no cut), in arb. E_uncut(N) is the larger of the two roots' |Delta_RT - Delta_uncut|; the spread of the roots is unchanged.
- Verdict per D, with #404's rule on the uncut reference: the ladder **falls to below 1e-14** when some N* has both roots within 1e-14 of the uncut Delta and a spread below 1e-14 with E_uncut strictly falling up to N* (or N* the first rung); otherwise it **stops falling** at N_s (the first rung whose E is not below the previous rung's). Also the best N's distance from the uncut Delta.
- Controls: a polish at a nearby D must give a different Delta (the continuation check at D 54.996085 from two starts is the cross-check); the D 40.020065 polish of #610 (Delta kf 13 1.88845166449061383795, no cut 1.88845166449061539504) is the reference for how the two runs differ.

## What ran

- `run_611.py` (20:31 to 21:02 UTC, two at a time, 3 threads each, BelowNormal): the own-D quad-double polishes of `up8_D50.0075` (D 50.007491), `up13_D60.0020` (D 60.001952), `up10_D55.0351` (D 55.035148) and `up10_D54.0414` (D 54.041398), each with `--kfreeze 13` and `--kfreeze -1`, tags `kf13_D50`, `kfm1_D50`, `kf13_D60`, `kfm1_D60`, `kf13_D54a`, `kfm1_D54a`, `kf13_D54b`, `kfm1_D54b` (`logs/*.stdout`, `qd_<tag>.jsonl`, the saved states `<tag>_D<D>.npz`). The D 54 runs then went on, as `scan_qd.py` does, to D_END = 54.996085 and **crashed** (below).
- `run_611b.py` (21:03 to 22:19 UTC): the continuation to D 54.996085 again from the converged D 55.035148 states with `--predictor lagrange` (tags `kf13_D54c`, `kfm1_D54c`): both failed, 4527 s.
- `diag/` (22:20 UTC): a small continuation at D 50 (`kf13_D50` state, D_END 50.017491, `--dD 0.01`) with both predictors. The Lagrange one printed its first failure (22:31) and went on halving dD; I stopped it at 22:42 UTC, when I found it still running next to the later jobs and past the thread budget, so its log holds the first attempt only.
- `interp/` (22:35 to 23:04 UTC): polishes from a start interpolated in D to 54.996085, and the w = 0 control of that start (below).
- `probe/` (22:55 UTC): `tangent_probe.py`, which runs `scan_qd.py`'s first tangent step at D 50 with `tangent_q` replaced by a copy of its body that prints whether each array is finite.

## The quad-double polishes (the own-D ones; max|F| <= 1e-50 is the criterion)

| polish (state at its own D) | Delta_qd | max abs F | Newton steps | seconds |
|---|---|---|---|---|
| D 50.007491, kf 13 | 1.8416311332022644415634205832973 | 9.5e-57 | 4 | 220 |
| D 50.007491, no cut | 1.8416311332022633984652163275760 | 4.3e-57 | 6 | 329 |
| D 54.041398, kf 13 | 1.8274556531206565070201730894252 | 5.1e-56 | 4 | 217 |
| D 54.041398, no cut | 1.8274556531206553089696055802166 | 2.2e-56 | 7 | 370 |
| D 55.035148, kf 13 | 1.8242712581939432761374833482553 | 2.6e-56 | 4 | 218 |
| D 55.035148, no cut | 1.8242712581939420660919734166791 | 3.8e-56 | 7 | 376 |
| D 60.001952, kf 13 | 1.8098842580017148218821155282315 | 1.6e-51 | 4 | 218 |
| D 60.001952, no cut | **did not converge** | 6.5e-08 | 6 | 1027 |

Seven of the eight converge. The no-cut polish at D 60.001952 starts from the kf 13 state (|F| 1.94e-23 in the no-cut system), takes a full Newton step of |dz| 1.0e-3 that raises |F| to 6.1e-7 (its dDelta is -1.56e-15, a linear estimate of the cut's effect there that the step itself shows is not valid), and five more steps with step fractions 0.5, 0.25, 0.5, 1 bring |F| down to 6.55e-8, |dz| 4.8e-5, where the sixth finds "no trial step accepted" and stops. Its Delta has moved by -1.4e-11 from the kf 13 value by then (`logs/kfm1_D60.stdout`, `qd_kfm1_D60_attempts.jsonl`; not a value of anything).

**The cut's effect** (no cut - kf 13): D 40.020065 +1.557e-15 (#610, the Mac), D 50.007491 -1.0431e-15, D 54.041398 -1.1981e-15, D 55.035148 -1.2100e-15; D 60.001952 not measured (the uncut polish does not converge). The effect changes sign between D 40 and D 50 and is smooth from 54 to 55 (the two values differ by 1.2e-17).

**The pivots of the Newton matrix** (`pivots_611.md`, read from the polishes' logs; the smallest LU pivot of the last Newton matrix, which for a converged polish is at its own root):

| D | kf 13 | no cut | ratio | no cut, first matrix (at the kf 13 state) |
|---|---|---|---|---|
| 50.007491 | 1.0e-12 | 5.1e-15 | 2.0e2 | 5.1e-15 |
| 54.041398 | 1.8e-13 | 9.9e-17 | 1.8e3 | 1.3e-17 |
| 55.035148 | 1.5e-13 | 3.1e-16 | 4.8e2 | 4.0e-17 |
| 60.001952 | 3.1e-14 | 1.1e-20 (not at a root) | 2.8e6 | 1.7e-21 |

The cut problem's smallest pivot declines smoothly with D; the uncut problem's is two to six orders smaller, and it does not decline smoothly (it depends on the matrix it is read at by a factor of up to 8 at D 55.04, so the table is an order-of-magnitude indicator, not a measurement of a singular value). At D 60.001952 the uncut matrix is as nearly singular as 1e-20 to 1e-21 against a largest pivot of 1.2e7, and Newton from the cut state does not converge. That parallels RT's family of nearly degenerate roots in the same range of D (#404), but this table does not show that the two are the same direction.

## The continuation to D 54.996085 fails on win

There is no saved hp state at D 54.996085 (the up10 run's states kept are D 53.7914, 54.0414 and 55.0351; the `state` column of the `delta_all.csv` row is empty), so `scan_qd.py` continues from a neighbour. With its default predictor (the tangent `driver.tangent_q` while fewer than 3 points are converged) every one of the four runs (kf 13 and no cut, from 55.0351 and from 54.0414) stopped at the first step with `ValueError: singular or non-finite pivot at column 0 (NaN)` (`failed_tangent_predictor/`). With `--predictor lagrange` (one converged point: the predictor is that point, z unchanged) all eight first steps fail, dD = -2.0e-2, -1.0e-2, ..., -1.56e-4 (halved each time, 545 to 565 s each, 4527 s in all), with |F| after the first Newton try 1.77e16, 9.0e13, 8.3e11, 2.6e9, 8.5e7, 1.6e6, 1.6e4 and 5.1e2, and `scan_qd.py` stops at "dD below 0.0001" (`logs/kf13_D54c.stdout`, `logs/kfm1_D54c.stdout`; the two runs print the same |F|, as a predictor error of J dz would). A constant z is expected to fail this way (|F| of 5e2 is 1.6e-4 times the Jacobian's largest pivot, 3e6), and the tangent predictor is the one meant to avoid it. **At D 50, from a converged state, a step of dD = +0.01 gives |F| 4.4e11 with the Lagrange predictor and the same NaN with the tangent one** (`diag/`), so this is not specific to the up10 states. `probe/tangent_probe.py` (output in `probe/tangent_probe.stdout`) shows where the tangent predictor goes wrong at D 50.007491. Every array it builds is finite (z, `residual_q` at D +- 1e-10, dF/dD whose largest first-part entry is 1.8e3, the result of `qlu_solve`), but the tangent t = dz/dD has largest first-part entry **1.87e6**, against at most 4.1e-3 per unit D for the difference of the two polished up10 states (D 54.04 and 55.04). So the predicted point z + dD t is absurd (about 1.9e4 for dD = 0.01) and the next Newton matrix is not finite. That is as far as I took it: I do not know whether the 1.9e6 belongs to the build (venv-t151's hpkernel is a build before #523, on Windows) or to the problem (a Newton matrix with a smallest pivot of 1e-12 and a dF/dD component along it), nor whether `scan_qd.py`'s continuation works on the Mac for these states (the coordinator's #610 used its polish at the state's own D). The own-D polishes need no step in D and work.

**A start by interpolation fails, and so does its control** (`interp/`, tried after the continuation failed; the rule was fixed before the run: converge to max|F| <= 1e-50, and then kf 13 Delta within 1e-16 of the estimate below and the cut's effect within 1e-16 of -1.2096e-15, else report a discrepancy). `interp/make_interp.py` interpolates linearly in D (w = 0.9607) the two up10 states (D 54.041398 and 55.035148, whose z differ by at most 4.1e-3) to D 54.996085, in double precision (the low part `zl` is dropped), and `scan_qd.py` polishes that at its own D, with and without the cut. Both stop at the first Newton step with |F| 8.1e8, "no trial step accepted" (`interp/kf13_D54i.stdout`, `interp/kfm1_D54i.stdout`). I did not find why |F| is this large for a start whose z is within 4.1e-3 of both neighbours.

The same script at w = 0 (`make_interp.py 54.041398`) is the control: a start identical to the up10 D 54.041398 state except for the dropped `zl` (about 1e-17), whose polish from the stored state converged in 4 steps from |F| 5e-24 (`kf13_D54b`). **The control does not converge either**: it starts at |F| 1.77e-8 and after four Newton steps stops at |F| 1.6e-11 with "no trial step accepted" (`interp/kf13_D54i0.stdout`). So a start that is 1e-17 away from a root in z is already outside what this polish reaches, the float64 form of the start cannot be the test, and the failed interpolation says only that the polish needs a start converged to about the double-double floor. A start interpolated in double-double would have the same interpolation error (|F| of order 1e8), so I did not repeat it.

## #404's ladders read against the uncut Delta

Delta_RT is the 30-digit `Delta_str` of `I404-win/roots/*.jsonl`; the references are the quad-double values above (`reread_611.py` -> `reread_D50.txt`, `reread_D54.txt`, `reread_D60.txt`).

**D 50.007491 (measured: both polishes).** E_uncut(N), the larger of the two roots' |Delta_RT - Delta_uncut|, against #404's E_cut(N) (against the kf 13 value):

| N | root a - uncut | root b - uncut | E_uncut(N) | E_cut(N) | spread a - b | passes 1e-14 (uncut) |
|---|---|---|---|---|---|---|
| 99 | -2.22e-14 | -2.22e-14 | 2.22e-14 | 2.33e-14 | +1.12e-18 | no |
| 103 | -1.91e-15 | -1.86e-15 | 1.91e-15 | 2.95e-15 | -4.86e-17 | yes |
| 107 | -6.49e-15 | -6.35e-15 | 6.49e-15 | 7.53e-15 | -1.45e-16 | yes |
| 111 | -5.87e-14 | -6.46e-14 | 6.46e-14 | 6.56e-14 | +5.89e-15 | no |
| 115 | -3.07e-13 | +1.11e-14 | 3.07e-13 | 3.08e-13 | -3.18e-13 | no |
| 119 | -1.34e-12 | -2.62e-12 | 2.62e-12 | 2.62e-12 | +1.28e-12 | no |
| 123 | -1.95e-12 | -3.31e-11 | 3.31e-11 | 3.31e-11 | +3.11e-11 | no |

Verdict unchanged: **the ladder falls to below 1e-14 at N* = 103** (E_uncut = 1.91e-15, spread 4.9e-17; 103 and 107 pass). The best grid's distance is 1.0e-15 smaller than against the cut value, but it is not at the 1e-17 of D 40 (#610): 1.9e-15 remains at 32x103, with the two starts equal to 5e-17, so what is left is the grid's, not the cut's.

**D 54.996085 (ESTIMATED reference; no polish exists at this D).** The kf 13 quad-double Delta is taken as the double-double row of `delta_all.csv` plus the interpolated (quad-double - row) offset (-1.7e-18 at D 54.041398, +1.32e-17 at 55.035148, +1.26e-17 at 54.996085), the uncut one as that plus the interpolated cut effect (-1.2096e-15): kf 13 1.82439433727262601231498961961, no cut 1.82439433727262480274098503228, with an error of about 5e-17. Against it:

| N | root a - uncut | root b - uncut | E_uncut(N) | E_cut(N) | spread a - b | passes 1e-14 |
|---|---|---|---|---|---|---|
| 99 | -3.64e-14 | -1.53e-14 | 3.64e-14 | 3.76e-14 | -2.11e-14 | no |
| 103 | -6.80e-14 | -7.38e-14 | 7.38e-14 | 7.50e-14 | +5.78e-15 | no |
| 107 | +5.44e-12 | -6.19e-13 | 5.44e-12 | 5.44e-12 | +6.06e-12 | no |
| 111 | +8.30e-14 | -6.93e-12 | 6.93e-12 | 6.93e-12 | +7.01e-12 | no |
| 115 | -4.46e-11 | -8.53e-11 | 8.53e-11 | 8.53e-11 | +4.07e-11 | no |
| 119 | -9.89e-12 | -2.33e-10 | 2.33e-10 | 2.33e-10 | +2.23e-10 | no |
| 123 | +5.65e-11 | -1.21e-09 | 1.21e-09 | 1.21e-09 | +1.26e-09 | no |

Verdict unchanged: **the ladder stops falling at N_s = 99**, E_uncut = 3.64e-14, spread 2.11e-14, no grid passes; the cut changes E by 1.2e-15 at most, far below the 1e-14 bound and the 3.6e-14 distance, so no estimate error of 5e-17 can change this.

**D 60.001952 (no uncut value).** Against the kf 13 quad-double value 1.8098842580017148218821155282315 (the dd row of `delta_all.csv` differs from it by -6.9e-17): the same E as #404, **stops falling at N_s = 99** (E = 1.80e-12). The cut effect measured at D 40 to 55 is 1.0e-15 to 1.6e-15 in size; E(99) = 1.80e-12 and the spread 1.45e-12 are more than a thousand times larger, and, whatever the uncut value is, the spread of the two roots (the reference does not enter it) is 1.8e-12 or more at every N, so no grid can pass the 1e-14 test; and E(99) is the smallest rung of the ladder by a factor of 5.8 (1.04e-11 at 119 is the next) against a cut effect of order 1e-15, so N_s = 99 stands. The cut's effect at D 60 is not measured, and the uncut hp problem there is itself nearly singular (above).

## Against the acceptance

- **All six polishes converge: not met.** Seven of the eight own-D polishes converge (D 50.007491, 54.041398, 55.035148 with and without the cut, and D 60.001952 with the cut); the no-cut D 60.001952 one does not (|F| 6.5e-8 after 6 steps, the Newton matrix's smallest pivot 1e-20 to 1e-21). The two polishes at D 54.996085 do not exist: no hp state of that D is kept (#164's README names the double-double row of `delta_all.csv`, not a state, and `hp/data/states` and the raw repository hold none), `scan_qd.py`'s continuation to it fails on win, and a start interpolated from the neighbouring states does not converge (nor does its control).
- **The cut's effect and #404's E(N) re-read at each D:** D 50.007491 measured (both polishes). D 54.996085 ESTIMATED, from the measured effect at D 54.04 and 55.04 and the quad-double offset from the double-double row, with an error of about 5e-17 (the offset is +4.8e-17, -1.7e-18, +1.3e-17 and -6.9e-17 at D 50, 54.04, 55.04 and 60). D 60.001952 against the kf 13 quad-double value only.
- **Verdict per D:** D 50.007491 falls to below 1e-14 at N* = 103 (E_uncut 1.91e-15, spread 4.9e-17; 103 and 107 pass; the best N is 103). D 54.996085 stops falling at N_s = 99 (E_uncut 3.64e-14 against the estimate, spread 2.1e-14; no grid passes). D 60.001952 stops falling at N_s = 99 (E 1.80e-12 against the kf 13 value, spread 1.45e-12; no grid can pass whatever the reference, since every N has a spread of 1.8e-12 or more). Where #404 said the ladder does not fall below 1e-14 (D 54.996 and 60.002) it does not against the uncut Delta either, so far as the estimate and the kf 13 value allow; where it fell (D 50.007), it still falls.

## Controls

The plan's last bullet (a polish at a nearby D must give a different Delta) was not a check that could fail and is not used. What was run:

- **The reread script reproduces its stored output and fires on a moved reference.** `reread_D50_check.txt` is identical to `reread_D50.txt`. `reread_611.py D50 1e-14` adds 1e-14 to both references: E_uncut(103) goes from 1.91e-15 to 1.19e-14, no grid passes, and the verdict becomes "stops falling at 103" (`reread_D50_shift.txt`). With -1e-14 the ladder still falls at 103 but E(103) is 8.14e-15 and the best N moves to 107 (`reread_D50_shiftminus.txt`). So the D 50 verdict is sensitive to the reference at the 1e-14 level, and the cut's 1.0e-15 moves E(103) from 2.95e-15 to 1.91e-15 without changing it.
- **The polishes against each other.** The cut's effect at D 54.041398 (-1.1981e-15) and 55.035148 (-1.2100e-15) agree to 1.2e-17, and the first Newton step's dDelta of each no-cut polish (-1.04e-15 at D 50, -1.20e-15 and -1.21e-15 at D 54.04 and 55.04, `logs/kfm1_*.stdout`) equals the cut's effect to the printed digits, as a linear step from a converged cut state should. All of it is the same code, so it checks the polishes' consistency, not the code.
- **Not run:** the plan's cross-check (the D 54.996085 continuation from two starts must agree) and a second implementation of the polish. The only independent number is #610's D 40 value (the Mac, the coordinator's run), whose cut effect is +1.557e-15, the opposite sign of the effect here.

## Recommended tasks (for the coordinator)

1. **The polishes at D 54.996085 and the uncut polish at D 60.001952, on a machine where `scan_qd.py`'s continuation works.** What: on the Mac or any post-#523 build, first the 4-minute check of this folder (`diag.cmd`: the kf13_D50 state to D 50.017491, tangent predictor, dD 0.01), which must not give a NaN pivot there; if it does, the continuation is broken for these states and not only for win's build. Then `python -u scan_qd.py <raw>/qd_<tag>.jsonl data/states/up10_D55.0351.npz 54.996085 --kfreeze K --threads N --tag <tag>` for K = 13 and -1, and for D 60.001952 the same from `up12_D59.0250.npz` with `--kfreeze -1` (the polish from the kf 13 state does not converge). Why: closes #611's acceptance, which has two missing polishes. Acceptance: max|F| <= 1e-50 or the accepted stall; `reread_611.py` re-run on the measured values, which must agree with the D 54.996 estimate to 1e-16 or the estimate's error is reported. Depends on #611.
2. **Compare the uncut matrix's weak direction with RT's degenerate direction (#404).** What: the uncut hp matrix's smallest pivot falls to 1e-20 at D 60 (table above); take its singular vector and compare it with the null direction of RT's Jacobian at D 54.996 and 60.002. Why: the two codes may be seeing one direction, and this folder shows only that both are degenerate in the same range of D. Acceptance: the overlap of the two vectors, with a planted-truth control (a vector of known overlap through the same code path). Depends on #611 and #404.
