# I962-win2: the win2 build of main 40f4b4a5 (multidouble 4.9.0, multishoot 3.3.0) and its Windows bit checks

Machine: win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session beside win2b's #903 chain and #945's leg.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/962 (coordinator `nathans-macbook-air-m5-3/t5`).

| | |
|---|---|
| code | worktree `D:\choptuik-i962` of choptuik-large-d, detached at origin/main 40f4b4a5 |
| venv | `C:\Users\nathan\Source\venv-i962`, Python 3.14.10, `requirements.txt` (venv + pip, uv is not installed here; on C: because D: has 29 GB free) |
| raw clone | worktree `D:\choptuik-i935-raw` of `D:\choptuik-large-d-raw`, branch `i745-win2`, pulled to origin/main on 2026-11-18. The live clone is not touched. The four inputs the checks read are sha256-identical in both clones (`input_sha256.txt`) |
| build | `run_build.sh`: `bash hp/build.sh` with `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=4`, BelowNormal, `RUSTFLAGS="-C target-cpu=native"` (build.sh) |
| checks | `run_checks.sh`, 4 threads at BelowNormal, one BLAS thread per process, from `D:\choptuik-i962\hp` |
