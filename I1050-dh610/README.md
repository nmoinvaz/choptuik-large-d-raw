# I1050-dh610: bit identity of hp on multishoot 4.0.0, multidouble 5.0.0 and multisolver 0.2.1 (PR #1050), against dh610's 9980cd93 build

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Pull request https://github.com/nmoinvaz/choptuik-large-d/pull/1050 (branch `chore/multishoot-4.0.0`, head 1c02b15b when this was written), the coordinator's order of
20 Nov 2026 (about 09:55 UTC): after #1034's step 6 ends (so its timings stay clean), a new worktree at the branch head, a new venv `~/Source/venv-i1050`, `hp/build.sh`, then #1034's step 5 commands unchanged,
and a row-by-row comparison with the step 5 outputs of the 9980cd93 build on the same machine (`../I1034-dh610/step5_*.log`): they must be bit-identical.

Between 9980cd93 and 1c02b15b the hp tree differs only in the PR's three files (`git diff --stat 9980cd93 1c02b15b -- hp`: `hp/Cargo.toml`, `hp/Cargo.lock`, `hp/src/lib.rs`), so the two builds differ in the three
pins and one import. Not moved by the PR: `hp/pyproject.toml`'s multidouble Python package commit (the driver's helpers), `matter/sigma_ms`.

Code: a new worktree `~/Source/choptuik-large-d-1050` detached at the branch head (recorded in `exits_1050.txt`), a new venv `~/Source/venv-i1050` (uv, Python 3.14, `requirements.txt`). Nothing a live job imports is touched.
RAW is `~/Source/choptuik-large-d-raw`; T81 and anm-mac inputs are the same files as for #1034's step 5.

Steps, one at a time, nice 10, each under timeout (3 x its estimate) on its exact pid, from `hp/`:
1. `hp/build.sh` (est. 31 min, 24 GB; cap 93 min), then the import check (`hpkernel.isa()`, `multidouble.isa()`, the lock's versions).
2. `python3 highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` (est. 1 min; exit 0), `scaled --compare=$RAW/T81/scaled_main.json` (est. 8 min; exit 0, its control fires),
   `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` (est. 2 min; exit 0), and the same with `--mutate=kappa` (exit 1). The wall times of #1034's runs on the 9980cd93 build were 51, 453, 97 and 96 s.
3. `compare1050.py` of each log against `../I1034-dh610/step5_*.log`: every row (M, name, hash, verdict) and every verdict line must be equal; timings and the header are ignored. Its controls: the old log against itself passes,
   and with `--mutate` (one hash digit changed in the new log) it fails (exit 1).

## Files

| file | what |
|---|---|
| `common1050.sh`, `run1050.sh`, `compare1050.py` | paths, the driver, the row-by-row comparison |
