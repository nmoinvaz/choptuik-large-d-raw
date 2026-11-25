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
