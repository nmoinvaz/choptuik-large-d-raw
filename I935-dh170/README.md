# I935-dh170: hp on multidouble 4.8.2 on dh170, the build and the reference checks

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/935
(its follow-up on this machine is I936-dh170/).

## Result

| acceptance | verdict | number |
|---|---|---|
| `build.sh` exits 0 | pass | 1:19:31 wall, exit 0 |
| hpkernel import prints its ISA | pass | `hpkernel avx2 multidouble avx2` |
| `ref --Ms=48,64,80` against T81/ref_main.json | pass, exit 0 | 72 outputs bit-identical, 0 differ |
| `scaled` against T81/scaled_main.json | pass, exit 0 | 22 entries bit-identical, 0 differ; its control (scale wrong at order 7, M = 192) fires |
| `jets` against anm-mac/jets_inputs/jets_inputs.json | pass, exit 0 | 28 outputs bit-identical, 0 differ |
| `jets --mutate=kappa` exits non-zero | pass, exit 1 | 28 of 28 outputs differ |

## What ran

- Code: worktree ~/Source/choptuik-large-d-935 at origin/hp/multidouble-4.8.2 (cdb5a6bc). Main d7b59668 (#934 merged) has
  the same code: `git diff cdb5a6bc d7b59668` is empty for hp/src, hp/python, Cargo.toml, Cargo.lock, pyproject.toml,
  build.sh, octo_corrector.py, reseed.py and highm_check.py. Crates in hp/Cargo.lock: multidouble 4.8.2, multishoot 3.2.0,
  multisolver 0.1.1. The Python multidouble package is the commit pyproject.toml names (a93e0896).
- Venv: ~/Source/choptuik-large-d-935/.venv (uv, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0, maturin
  1.16.0, all from requirements.txt). The main checkout's .venv (4.7.0, the #903 chain's build) was not touched.
- Build: `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=10 nice -n 15
  /usr/bin/time -v bash hp/build.sh`, with the venv's bin/ first on PATH (what `activate` does, so that build.sh finds
  maturin; the task's command sets only VIRTUAL_ENV). Nothing else ran. Started 11:27:35 UTC, exit 0 at 12:47:06 UTC.
  Log build.log (and `/usr/bin/time -v` at its end), build.time.
- Cost: cargo's release build 79 min 26 s, wall 1:19:31. Peak resident set of the process (rustc) 29,188,896 kB (27.8 GiB).
  mem.log samples the whole system every 30 s: at most 30,935 MB of 31,968 MB used and 1,781 MB of the 8 GB zram swap, so
  the machine had about 1 GB to spare. The 4.7.0 build with the same recipe took 4832 s and 29,085,548 kB (the I903 setup).
- Checks: checks.sh from hp/ with the new venv's python at nice 10, 12:47 to 13:08 UTC (ref 1.5 min, scaled 15 min, jets
  2 min, jets with the mutation 2 min). The references are the live raw clone's files (T81/ref_main.json,
  T81/scaled_main.json, anm-mac/jets_inputs/jets_inputs.json and its _inputs.npz), equal by cmp to origin/main's at 8afabea9.
  Logs ref.log, scaled.log, jets.log, jets_kappa.log, checks.log (exit lines).
