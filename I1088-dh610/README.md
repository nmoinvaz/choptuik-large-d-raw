# I1088-dh610: form S in hp (#1088 Track A), its validation and its conditioning against form A, on dh610

Machine: dh610 (Fedora 45, i7-12700, 20 threads), Python of `~/Source/venv-i1058` with a release build of branch
`wip/large-d-form-s` (hp/src/form_s.rs) unpacked into `~/Source/choptuik-large-d-1088a/site` on `PYTHONPATH`, 8 threads
at nice 10, systemd user units `i1088a-*`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
The runs ran in `~/Source/choptuik-large-d-1088a/` (the branch fetched as a tarball); their files were copied here from
the Mac, which pushed this folder.

- `run_val.sh`: the validation and the conditioning table (its logs in `out/`: `check.log`, `check_flux.log`,
  `planted.log`, `planted_step.log`, `cond.log`, and the unit's journal), on the M = 32 full-system states of
  hp/data/states (D 16.76 to 27.04, and 50.01) and the chain states at D 100 and 200 (`T138-win2/chain/`,
  `T138-win2/chain_o/`) and 245.56 (`I966-dh370/ks_chain3b/`). The build: the low-memory release recipe
  (`CARGO_PROFILE_RELEASE_LTO=false`, 16 codegen units) of wip/large-d-form-s at 38943f4f, 49 min and 25.6 GB
  (`build2_tail.log`).
- `run_cond_ks.sh` and `out/cond_ks293.log`: the table's D 100 and 200 rows again at ks 293.
- `j400_held/`: the form S jump to D 400 (`run_jump.sh 400 252.5 3 0 0 10 held --held 1 --it_max 8 --kc 180`), converged,
  its state `jump_s_D400.0000.npz`.
- `out/rel400.log`: plain Newton with h5 freed from the D 400 held state (`form_s.py release`), stopped by hand.
- `out/rls300.log`, `out/rls300_release_ls.jsonl`: `form_s.py release_ls` from the D 300 held state (copied from
  dh370), h5 then h7 ... h13; copied while it runs, updated as it goes.
- `out/rls300/release_ls_h13_D300.0000.npz`: D 300 with every harmonic up to 13 free (the full system), the end of
  `release_ls` (`out/rls300.log`, `out/rls300_release_ls.jsonl`).
- `rebuild_mob.sh`: the release build with the Moebius horizon and mobcheck at D 400, queued after the release.
- `out/mobcheck400.log`: mobcheck at the D 400 held state with Newton (checks 2 and 3 of the Moebius port); the
  control's Newton ended in a panic of a trial (fixed in form_s.py 4732b6c9).
- `after_mob2000.sh`: the D 2000 held jump with the Moebius horizon (out/j2000_held_mob/), started 07:34:56 UTC.
- `j2000_held_mob/`: D 2000 from the chain and form-S states up to D 400: three damped steps (lam 1/4, 1/16, 1/16) left
  max |F| at 1.13; stopped by hand.
- `run_j1414.sh`: the stepping stone D 1414 from the form-S states at D 300, 400 and 1000 (out/j1414_held_mob/).
- `j1414_held_mob/`, `j2000_held_mob2/`: the stepping stone D 1414 (from D 300, 400, 1000) and D 2000 (from D 400,
  1000, 1414), held, the Moebius horizon a 8, the lean defaults; `ladder.sh`: D 2828 to 10000 in steps of about
  sqrt(2) in n (out/j<D>_ladder/).
- `j2828_ladder/`: D 2828 from D 1000, 1414, 2000: the guess's horizon block 3.2e5 (bulk 1e-10), no trial in step 0;
  the ladder stopped. `run_relayout.sh`, `out/rl1000.log`: the relayout onto nodes up to 0.9 at D 1000 (not converged).
- `ladder2.sh`: the ladder past D 2000 in steps of 1.1 in D, without the discretization report (out/j<D>_l2/).
- `L10000/`: D 10000 held at L = 20 (x_l 0.706399, a 24.995, ks 13018, 1370 Taylor steps; solvestate from
  I1088-mac-a/form_s/g10000L20/): the double-double floor reached by step 3 (|F| 5.0e-21, bound 2.6e-12), Delta
  1.644930989170800 (the log). Its script records the commit as 91d5bbc5 by mistake: the code is 7671bd89. Stopped
  at 00:02 UTC on 2026-11-26 during it 4 (the log's count), at the floor, so its state was not saved (the loop saved only at the end).
- `L10000q/`: D 10000 again from the same guess at f5eb570f, on the precision ladder: 2 double-double steps, then up
  to 2 with the quad-double residual (double-double Jacobian), to Delta's bound 1e-15; a floor stop (a step cutting
  max |F| by less than 10x) ends each stage; every step's state is saved; the octo-double check (`run_10000q.sh`).
- `rls1000h13/`: the D 1000 release of harmonic 13 from I1088-dh370/rls1000/release_ls_h11_D1000.0000.npz, to the
  full system and its direct_s record, at 96b6ddc9 with each trial printed and each accepted step saved
  (`run_rls1000h13.sh`).
- `L2000/`: D 2000 held at L = 20 from I1088-mac-a/form_s/g2000L20/ on the precision ladder (`run_2000L20.sh`), the
  start of the D 2000 release.
- `L10000q/`: the restart's first dd step (1.2e-8 -> 1.9e-16 in 5775 s on the loaded machine), stopped by
  `chord_switch.sh` at 01:42:50 UTC with its state saved (`lastnode_D10000.0000_step0.npz`); continued as out/L10000c
  (one more dd step, then chord steps with the quad-double residual, 7bf304b1).
- `rls1000h13/`: the D 1000 h13 release with the double-double Jacobian, stopped by hand in outer step 0 (`run.log`):
  the inner held solve stopped at its floor 6.6e-33, above the target residual 9.7e-36, so every trial is rejected.
- `rls1000h13q/`: the same with the quad-double Jacobian (`run_rls1000h13q.sh`, afcf9b0d): outer step 0 9.7e-36 ->
  6.0e-40 (inner solve 4 steps to 2.0e-53), step 1 -> 5.4e-43, step 2 released. The full system's record
  (`direct_s.jsonl`): Delta 1.654240854145891739, -9.91e-11 from Track C (+- 7.8e-10), quad-double check 5.4e-43,
  Hamiltonian check a rows up to 7.8e-25. Its held_to_full_dDelta, +3.74e-14, is the h11 -> full change, since this run
  started from the h11 state; held -> full is +2.020e-10 (against I1088-dh370's held D 1000 record).
- `rls2000/`, `rls2000b/`, `rls2000c/`, `rls2000d/`: the D 2000 release at L = 20 from `L2000/`'s held solve, in four
  runs (the qd residual throughout). rls2000: h5 released, h7 outer 0-1 (4 threads; `run_rls2000.sh`), moved to 10
  threads (`rls2000_switch.sh`). rls2000b: h7, h9 released; h11 with the dd Jacobian stopped by hand, its inner solve
  at the floor 2.7e-28 above the target 4.8e-33. rls2000c (`--jac_by 11:qd,13:qd`): h11 released (+8.5e-14); h13's
  inner solves with the qd Jacobian solved in dd floored at 7.6e-34 to 1.9e-37 above the target 2.5e-37, stopped by
  hand. rls2000d (`--jac_by 13:qq`, the qd Jacobian solved in qd, 51a8e3be): h13 outer 0 2.5e-37 -> 6.9e-49, released
  at outer 1. The full system's record (`rls2000d/direct_s.jsonl`): Delta 1.649074313745289326, the octo-double check
  6.9e-49, the Hamiltonian check a rows up to 3.4e-26, held -> full +3.834e-10 (from --held_delta, L2000's Delta);
  -1.41e-10 from Track C (+- 1.2e-9), -5.6e-13 from the corrected refit's prediction 1.64907431374585 +- 1.50e-11.
