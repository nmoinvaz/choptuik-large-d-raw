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

Files are added as the runs go; each log or script names its command line.
