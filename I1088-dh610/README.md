# I1088-dh610: form S in hp (#1088 Track A), its validation and its conditioning against form A, on dh610

Machine: dh610 (Fedora 45, i7-12700, 20 threads), Python of `~/Source/venv-i1058` with a release build of branch
`wip/large-d-form-s` (hp/src/form_s.rs) unpacked into `~/Source/choptuik-large-d-1088a/site` on `PYTHONPATH`, 8 threads
at nice 10, systemd user units `i1088a-*`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
The runs ran in `~/Source/choptuik-large-d-1088a/` (the branch fetched as a tarball); their files were copied here from
the Mac, which pushed this folder.

- `run_val.sh`: the validation and the conditioning table (its logs: `check.log`, `check_flux.log`, `planted.log`,
  `planted_step.log`, `cond.log`), on the M = 32 full-system states of hp/data/states (D 16.76 to 27.04, and 50.01)
  and the chain states at D 100 and 200 (`T138-win2/`) and 245.56 (`I966-dh370/ks_chain3b/`).
