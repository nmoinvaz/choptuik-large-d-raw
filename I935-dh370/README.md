# I935-dh370: hp on multidouble 4.8.2 on dh370, the build and the reference checks

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/935

- Code: worktree `~/Source/choptuik-large-d-935` at origin/main 043834d9 (contains d7b59668, `hp/Cargo.toml` pins multidouble =4.8.2).
- Venv: `~/Source/choptuik-large-d-935/.venv`, Python 3.14.10 (the interpreter of venv-i800), made with `python3.14 -m venv` and
  `pip install -r requirements.txt` because uv is not installed on this machine. `venv-i800` is untouched.
- Build: `build935.sh` (low-memory recipe: no LTO, 16 codegen units, 10 jobs, nice 15, `/usr/bin/time -v`), log `build.log`,
  system memory every 30 s in `mem.log`, start and exit lines in `exits_935.txt`.

## Results (2026-11-17, built 13:04:08 to 13:37:28 UTC, checks 13:37:40 to 13:52:43 UTC)

Build: `build935.sh`, exit 0 in 33 min 20 s wall (cargo's own "Finished" 32 min 52 s), 2618.6 s user, 132% cpu. Peak resident set of the largest
process 24 055 484 kB (24.06 GB, `time -v`). System-wide used memory (`mem.log`, every 30 s) went from 4.2 GB before the build to 27.4 GB at
its peak (13:09:08), so the build's own part was about 23.2 GB. Crates: multidouble 4.8.2, multisolver 0.1.1, multishoot 3.2.0. The import
`import hpkernel, multidouble` prints `hpkernel avx2 multidouble avx2` (i7-8700, no AVX-512); `isa.log`.

`checks935.sh`: ref, scaled and jets side by side, `OMP_NUM_THREADS=1`, nice 10, from `hp/` of the worktree with its `.venv`.

| check | exit | result |
|---|---|---|
| `ref --compare=T81/ref_main.json --Ms=48,64,80` | 0 | 72 outputs bit-identical, 0 differ |
| `scaled --compare=T81/scaled_main.json` | 0 | 22 outputs bit-identical, 0 differ, its scale control fires |
| `jets --compare=anm-mac/jets_inputs/jets_inputs.json` | 0 | 28 outputs bit-identical, 0 differ |
| same `jets` with `--mutate=kappa` (must fail) | 1 | 28 of 28 differ |

Same entries and hashes as #934's dh610 logs (`I934-dh610/jets.log`, `jets_mutate_kappa.log`). Files: `build.log`, `mem.log`, `isa.log`,
`ref.log`, `scaled.log`, `jets.log`, `jets_mutate_kappa.log`, `exits_935.txt`.

Difference from the issue's commands: uv is not installed on dh370, so the venv was made with `python3.14 -m venv` (the uv-managed 3.14.10
that `venv-i800` uses) and `pip install -r requirements.txt`; the build had the venv's `bin` on PATH for `maturin`.
