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
