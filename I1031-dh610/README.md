# I1031-dh610: hp's cols_ cargo test at main 5d0a96e6 (multidouble 4.9.1), with and without target-cpu=native

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1031, the
`cols_` step that the coordinator moved here (comment of 2026-11-19 18:56 UTC; the bump is on main as 5d0a96e6 since
2026-11-20 00:12 UTC and the issue stays open for this test), run after #1003's K 49 ended (06:19:27 UTC on 20 Nov).

Code: a new worktree `~/Source/choptuik-large-d-1031` of main at 5d0a96e6 (detached; `hp/Cargo.lock`: multidouble 4.9.1,
multishoot 3.3.0), not the branch commit 6266a213. Venv `~/Source/venv-ccc` activated for the Python the crate links against
(no hpkernel is built or imported here). Nothing a live job imports is touched.

Commands, from `hp/` of that worktree, `CARGO_BUILD_JOBS=6`, nice 10, as a user unit with an alert-only memory log:

1. `cargo test --profile release-dev --lib cols_ -- --nocapture` with no RUSTFLAGS (multidouble's portable backend, Sse2).
2. the same with `RUSTFLAGS='-C target-cpu=native'` (the AVX2 backend of this CPU), as #1009's dh610 run did.

Expected, from #1009 (dh610, 76fdcbc9, multidouble 4.9.0-era): exit 0 in both, `test result: ok. 2 passed`, `333000 entries
compared, none differ` in `cols_coeffs_bitwise`, and in `cols_jacobian_bitwise` every tile's line reading `0 of N entries
differ (parallel: 0); control: K differ` with K > 0 (22 lines, the control `COLS_MUT_ULP`, which perturbs one ulp and must be
seen). Any run that fails, differs, or shows a control line with K = 0 is reported with its size and place.

## Files

| file | what |
|---|---|
| `common1031.sh`, `run1031.sh`, `watch1031.sh` | paths, the two runs and the summary, the build's memory sampler |
| `cols_test.log`, `cols_test_native.log`, `mem_cols_test*.log`, `memlog_1031.log`, `summary_1031.txt` | the two runs' output (no RUSTFLAGS; target-cpu=native), the samplers and the driver's summary |
| `check_logs1031.py`, `check_logs_1031.txt` | the recount of the two logs and its failing controls (`--mutate=differ`, `--mutate=control`, both exit 1) |

## Result, 20 Nov 07:20 UTC

Both runs exit 0 (no RUSTFLAGS 1237 s, target-cpu=native 1873 s, loaded: #1033's 8 threads, #1021's jobs). Each log: `test result: ok. 2 passed`, `333000 entries compared, none differ`, and 22 control
lines, each `0 of N entries differ ...; control: K differ` with K from 61 to 1895 (`check_logs_1031.txt`: PASS, and with a first line changed to `3 of` or K 0 it fails). Backends: all 22 lines
`backend::Sse2` without RUSTFLAGS, `backend::Avx2` with native. The unit's memory peak was 11.3 GB (journal), not the 24 GB expected for a compile. Two defects in my scripts, not in the check: `summary_1031.txt`'s
column "tile lines" reads 9 instead of 22 (its regex counts only lines with `(parallel: 0)`; `check_logs1031.py` recounts), and `watch1031.sh`'s process-tree sampler read 0 MiB (its `pgrep` list), so `mem_cols_test*.log`
hold only MemAvailable (minimum 51.5 GB and 46.3 GB from 56.3 GB at the start).
