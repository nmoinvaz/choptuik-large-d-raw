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

## Results (2026-11-18, closing summary on the issue)

| # | check | pass | result |
|---|---|---|---|
| build | `hp/build.sh`, thin recipe | exit 0 | exit 0, 378 min, peak working set 32.29 GB (`build.times`, `mem.log`, `versions.txt`) |
| 1a | `highm_check.py ref` M 48, 64, 80 | exit 0, 72 of 72 | exit 0, 72 of 72 bit-identical (`ref.log`) |
| 1b | `highm_check.py scaled` | exit 0, 22 of 22, control fires | exit 0, 22 of 22, control fires (`scaled.log`) |
| 1c | `highm_check.py jets` | exit 0, 28 of 28 | exit 0, 28 of 28 (`jets.log`) |
| 1d | `jets --mutate=kappa` | exit 1 | exit 1, 28 of 28 differ (`jets_kappa.log`) |
| 2 | `octo_hashes.py` at ks 240 D 229.0509, against dh170's 4.9.0 (and 4.8.2) hashes | reported | 0 of 12 lines differ, both builds, once the CRLF is stripped (`octo_win2_ST.txt`, `diff_win2_dh170*_ST_nocr.txt`) |
| 3 | `jet_by_order_check.py --N 6 --Np 6` | exit 0, controls fire | exit 0, PASS 6 of 6 orders and 6 of 6 with the hook, four controls fired (`jet_by_order.log`) |

`diff_win2_dh170D_ST.txt` and `diff_win2_dh170A_ST.txt` (not written: `run_checks.sh` wrote them under `diff_win2_dh170{D,A}_ST.txt`) hold the raw `diff`, which flags every line because of the CR.
