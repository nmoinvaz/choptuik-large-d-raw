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

Files are added as the runs go; each log or script names its command line.
