# I1088-mac-a: Track A of #1088, the direct solve at a target D (hp/jump.py), development runs on the Mac

Machine: the Mac (Apple M-series, macOS), `/Users/nathan/venv-314` with the hpkernel build of #1043 (main's kernel of
2026-11-20) on `PYTHONPATH`, 2 threads at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
Code: branch `wip/large-d-jump` of choptuik-large-d, `hp/jump.py` (a4df1196 and later).

Inputs: chain states of `I903-macm3/chain_k135/` and `I966-dh370/ks_chain3b/` (this repository, origin/main at
c30c2766).

- `g250/`: the guess at D 250 from the 28 states with D 226.13 to 245.56 (`jump.py guess`, its command line in
  `g250/cmd.txt`), its log and the eight-part guess (`guess_D250.npz`, the re-seed failed, so its horizon data are
  the ladder's last rung's).
- `probes/`: one octo-double Newton step of the full system from the chain's state at D 245.5586 (`probe2.py`,
  kfreeze None in `probe2.log`, kfreeze 13 in `probe2_k13.log`), and the ladder and its u0 rung on that state
  (`ladtest*.py`; `run_probes.sh` reran ladtest2 to 4 into their logs).

- `probes/` also: `weak_sv.py` (`weak_sv_k13.log`, the Mac's run at D 245.5586), `gauge_test.py` (the last node's c or
  p moved by 1e-12, then the ladder: `gauge_test_c.log`, `gauge_test_p.log`), the u0 rung with the octo-double block
  LU (`ladtest3_o.log`, `ladtest4_o.log`, `run_o.log`), and `slave_test.py` (a_h from the momentum constraint against
  the stored one, `slave_test.log`). `run_u0.sh` was stopped when Track A in form A was stopped (its log says when);
  `u0_tolerance.py` never ran.

- `form_s/`: form S in hp (`hp/src/form_s.rs`, branch `wip/large-d-form-s`), an opt-level-1 build of it
  (`HP_PROFILE`-style profile dev-o1 in hp/Cargo.toml) on `PYTHONPATH`. `run_check.sh` runs `hp/form_s.py check` at D
  16.76-27.04 (`check.log`, the form-S solutions in `states/`), its flux control (`check_flux.log`) and the planted
  check with its control (`planted.log`, `planted_step.log`); `run_check.log` has the times and the reruns of the
  controls after two fixes of form_s.py. `check_D20_before_horizon_q_fix.log` is the first run, before the horizon
  series' q was fixed (38943f4f). `cond_S_D50_mac.log`: form S's conditioning at D 50 on the Mac.

- `form_s/j250/`: the form S jump to D 250 with the 10 weakest no-Delta directions frozen (stopped by hand, the
  frozen subspace changed between LUs); `form_s/j250_held/`: the jump with p1's harmonics 5-13 held at the guess's
  values, converged, its state `jump_s_D250.0000.npz` and `jump_s.jsonl` (its `jump.log` lost its later lines, the note
  at its end says why).

- `form_s/hprobe.py`: the horizon block of form S at the rescaled guesses of D 400 and 1000 and its gain from m_h
  (`hprobe_D400.log`, `hprobe_D1000.log`; the Mac's opt-1 build; the guess's Delta is the fit's here).

- `form_s/mobius_gain.py`: hp's horizon sum (u variable, octo-double) against t2v's float64 recurrence in the Moebius
  variable (wip/large-d-inner ee996ecc, solver/inner_large_d/mobius_s.py) at the D 400 held state and the D 1000 guess,
  and each one's gain from m_h (`mobius_gain_D400.log`, `mobius_gain_D1000.log`).

- `form_s/mobcheck400/`: `form_s.py mobcheck --newton 0` at the D 400 held state (the held system's blocks with the
  u horizon, the Moebius horizon a 8 ks 617, and the control mutate 52; `mobcheck.jsonl`) and `mobsplit.py`'s split of
  the u-Moebius difference (`mobsplit.log`).
- `form_s/hprobe_mob.py`: check 4, the D 1000 guess's horizon gain from m_h with the Moebius horizon
  (`hprobe_mob_D1000.log`, the difference in octo-double; `hprobe_mob_D1000_f64diff.log`, the first run, whose float64
  difference cannot resolve the 1e-30 move).
- `form_s/g2000.sh`: the D 2000 guess's blocks for two fits (`g2000_A.log`, `g2000_B.log`, `g2000_*/`).

- `form_s/mob_f64.py`: t2v's float64 Moebius sum at a state's m_h against its last node, for several a and ks; at the
  D 2000 guess (`g2000_B/`, `mob_f64_g2000_B.log`).
- `form_s/ctl300.sh`: the controls of the stopping rule on Delta's first-order bound at D 300 (`ctl300_b15/`,
  `ctl300_b30/`, `ctl300_s101/` stopped by hand after 3 steps, `ctl300_b30h/`); `form_s/segtest.py`: the Taylor plan's
  truncation seen by form S (`segtest_D300.log`).

- `form_s/guess_probe.py`, `form_s/resonance.py`, `form_s/gain_f64.py`: why the D 2000 jump left the basin: guess
  fits' horizon mismatch (`guess_probe_D2000.log`), the horizon operator's smallest singular value per D
  (`resonance.log`), and the gain from m_h with the coefficient profile at D 1000, 1414 and 2000 (`gain_f64.log`).
- `direct_s.jsonl` (this folder and I1088-dh370, I1088-dh610): one record per converged form-S solve for the tables;
  `form_s/direct_backfill.py` wrote the ones before jump did (`direct_backfill.log`).
- `form_s/zcheck.py`: the z recurrence against the Cauchy sums (run on dh370, I1088-dh370/zcheck/).

- `form_s/zcheck_815287c6_D1000.log`: the z-recurrence check at D 1000 on the Mac's opt-1 build of 815287c6 (the
  Moebius constants in the lane's precision).

- `form_s/gain_x.py`: the horizon sum's gain from m_h against the point it is summed at (x 0.7, 0.8, 0.9, 0.95) at the
  D 2000 solution and the D 2828 guess, and where its coefficients fall below 1e-50 and 1e-70 (`gain_x.log`).
- `form_s/relayout1000/`: `form_s.py relayout` of the lean D 1000 state onto nodes 0.3 ... 0.9 (`relayout.log`, the
  re-solve's `relayout_solve.log`: not converged, Delta's gain 3.5e34 with the double-double Jacobian).

- `form_s/fine1000/`, `fine1000h/`, `fine2200/`, `fine2828/`: `form_s_fine.py jump` (the fine mesh 0.7 -> 0.95, the
  sparse Newton) on the Mac's opt-1 build of 580af314: D 1000 from the lean state (and with its held harmonics), D 2200
  and D 2828 from the held states at 1000, 1414, 2000; `fine_dd.log`, the double-double residual's run.
- `form_s/finedisc.py` (`finedisc_D2200.log`): the fine mesh's truncation at D 2200 (steps halved, ks + 100, kc + 30);
  `form_s/fullcheck.py` (`fullcheck_D2200.log`): the full system (kfreeze 13) at the fine held solution.
- `form_s/tc_1414_2200_2420.json`, `tc_run.log`: Track C at D 1414, 2200, 2420 (main's hp/track_c.py --targets).

- `form_s/t2/`: T2, the held guess's horizon block over its other blocks at D 2828.4271 with the last node at 0.700,
  0.703, 0.705, 0.70677, 0.709 (`form_s_lastnode.py ratio --parts 2`, double-double; the octo-double control at 0.700 is
  I1088-dh610/out/t2/); `form_s/t2g/`: the same at x_c for D 4000 and 5657; `form_s/fine2420/`, `hyb2420/`: the fine mesh
  at D 2420 (valid false) and the hybrid's failed guess (the series at 0.7 from the fine m_h reads 1.7e3).

- `form_s/g10000/`, `g10000L20/`, `g2828L20/`, `g4000L20/`, `g5657L20/`: guesses saved by `form_s_lastnode.py guess` for
  the solves on dh610 and dh370 (`solvestate`): the last node at x_c (g10000) or at L = 20.
- `form_s/g2000L20/`: the D 2000 guess at L = 20 (x_l 0.703559, a 8, ks 2618) from the held states at D 1000
  (I1088-dh370/j1000_lean), 1414 (I1088-dh610/j1414_held_mob) and 2200 (I1088-dh610/j2200_l2), degree 2 in 1/n; the
  command line is in `guess.log`'s README entry: `form_s_lastnode.py guess OUT --D 2000 --states_s <those three>
  --xl 0.7035589258590665 --mob 8 --ks 2618 --threads 2` (96b6ddc9).
- `form_s/g8000L20/`: the D 8000 guess at L = 20 (x_l 0.706222, a 19.995, ks 10418, 1099 Taylor steps) from the L = 20
  states at D 2828 (I1088-dh370/L2828), 4000 (form_s/L4000q) and 5657 (I1088-dh370/L5657q, after its first dd step),
  degree 2 in 1/n (`form_s_lastnode.py guess OUT --D 8000 --states_s <those three> --xl 0.7062221251334241 --mob 19.995
  --ks 10418 --threads 2`, 4f5eaf69); horizon block 7.1e-11, the other blocks 3e-12 to 2e-11 (`guess.log`).
- `form_s/g20000L20/`: the D 20000 guess at L = 20 (x_l 0.706753, a 49.995, 2659 Taylor steps; meta ks 11416, the
  formula value, which solvestate's --ks overrides) from the L = 20 states at D 4000 (form_s/L4000q), 5657
  (I1088-dh370/L5657c, after its chord step: 2.9e-26) and 10000 (I1088-dh610/L10000q, after its first dd step),
  degree 2 in 1/n (`form_s_lastnode.py guess OUT --D 20000 --states_s <those three> --xl 0.7067531041047617 --mob
  49.995 --ks 11416 --threads 2`, 4f5eaf69); horizon block 4.0e-11, the others 1.6e-12 to 1.0e-11 (`guess.log`).
- `form_s/ks_scan/`: the held residual against the horizon order ks (`ks_scan.py STATE KS,...,KSREF PARTS THREADS`, Mac, 2
  threads). D 10000 at its first dd step's state (I1088-dh610/L10000q), double-double (`D10000_step0_dd.log`): ks 4900
  and 5100 differ from ks 13018 by 2.7e-17 (the fast mode, which enters at order n/2 = 4999, not yet summed), 5300 by
  3.2e-29, 5600 and up by 0; one residual takes 12.7 s at ks 6000 against 85.8 s at 13018. A pre-check: the check of
  record is in quad-double at the converged state. D 20000's guess, double-double (`D20000_guess_dd.log`): ks 10100
  differs from 26018 by 3.5e-16, 10400 and up by 0; 41 s at ks 11416 against 282 s at 26018. Bars of the check of
  record at D 10000 (written 02:55 UTC, before it): quad-double residuals of the converged state at ks 5912, 6000 and
  7000 within 1e-25 of ks 13018's in every row; the control ks 5100 must exceed 1e-25. The check of record
  (`D10000_converged_qd.log`, 04:38-04:53 UTC, on L10000c's state after its chord step, max |F| 6.4e-25,
  `D10000_converged_step.npz`): ks 5912, 6000 and 7000 differ from 13018 by 2.0e-46, PASS; ks 5100 by 8.3e-22, the
  control fires. One quad-double residual takes 77.5 s at ks 5912 against 559 s at 13018.
- `form_s/time_res/`: the held residual's time in double-, quad- and octo-double on the D 2000 guess (`time_res.py
  <guess> 2,4,8 2`, 2 threads on the Mac): 2.2 s, 25.5 s, 255 s (`D2000.log`); one double-double Newton step (`time_jac.py
  <state> 2618,1400 2`) at the D 2000 solution: 96 s at ks 2618, 60 s at ks 1400, the same step (`jac_D2000.log`).
- `form_s/check2000/`: `form_s_lastnode.py checkstate` on I1088-dh610/L2000's solve (90945ced): the octo-double check,
  the discretization tails and the Hamiltonian check (`checkstate.log`); the ks controls (`--ks 400, 800, 1050, 1150,
  1400 --check qd --ham 0`, `checkstate_ks*_control.log`): the fast mode enters the Moebius series at order n/2, so
  below it the residual reads 2.7e-19 and ks + 200 changes nothing; at 1050 and 1150 ks + 200 fires (2.7e-19, 3.1e-22);
  from 1400 the residual is the solve's 1.13e-24.
- `form_s/L4000q/`: D 4000's quad-double stage from I1088-dh370/L4000's state (`solvestate --ladder qd --it_max 2`,
  90945ced, 2 threads, 35 min): one step 6.0e-20 -> 7.6e-26, bound 1.3e-18, the octo-double check 7.6e-26, the tails
  (ks + 200, kc + 20: 0; halved steps 5.9e-38; theta's top harmonic 4.2e-18), the Hamiltonian check 9.3e-27; Delta
  1.646485793699952, -6.66e-10 from Track C. Its record's method "lastnode at x_c" is the lastnode layout's old label
  (the same in I1088-dh370/L2828 and I1088-dh610/L2000): x_l is the record's xl, at L = 20 (4f5eaf69 labels it).

Files are added as the runs go; each log or script names its command line.
