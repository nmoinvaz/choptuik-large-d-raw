# I961-dh370: #955's rounds, #956's tangent_from and the split series on the merged head 40f4b4a5, one Linux build, one chain step

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, avx2). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/961

Worktree `~/Source/choptuik-large-d-961` at branch `perf/series-par-at` 40f4b4a5 (main add322ff plus #955), fresh venv. Build: `hp/build.sh`
with `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=6`, nice 10. T = 10 threads at nice 10.
The memory watcher only logs and alerts, it never stops anything.

Files are added as the run goes (build961.sh, build.log, run961.sh, exits_961.txt, mem961.log, one log per line of the issue).

## Results so far (interim, 2026-11-18 15:30 UTC)

Build: exit 0, 32 min 44 s, peak RSS 24.08 GB, `hpkernel avx2 multidouble avx2`, multidouble 4.9.0, multishoot 3.3.0, multisolver 0.1.1,
Python package multidouble 482c6835 (`build961.txt`, `build.log`, `mem961_build.log`).

| line | result | numbers |
|---|---|---|
| 1 `cargo test --release --lib oseries_` | pass, 3 tests, 1 ignored | 8 min 37 s compile, tests 919 s; controls 9600 rows, horizon round 3200, centre round 4224, kept series not moved 1.001e0 |
| 2 jet_by_order_check, 10 threads, `--save` | PASS | by order 316.9 s (#957 on 954eadcb: 721.3 s), jets 1650.5 s, ratio 5.21; 24 of 24 orders the same bits, 6 of 6 with the hook; all four controls fired |
| 2 jet_by_order_check, 4 threads, N 12, `--compare` | PASS | 12 of 12 orders the same bits, 12 of 12 as saved by the 10-thread run; round control against the saved series differs at orders 2 to 6 |
| 3 `--tangent_from 1` at ST | PASS | formed twice 316.3 s, moved 196.9 s (ratio 1.61), agreement max 1.0e-46, rho 6.55e-35 (bound 6.71e-32), control rho 1.2e29 |
| 3 `--tangent_from 1` at ST2 | PASS | formed twice 316.4 s, moved 197.0 s (1.61), agreement max 6.7e-46, rho 1.38e-36 (bound 1.41e-33), control rho 2.7e29 |
| 3 `--tangent_from 3` at ST | PASS | formed twice 316.4 s, moved 198.8 s (1.59), agreement max 3.2e-48, rho 6.55e-35, control rho 3.5e29 |
| 4 series_split_check | PASS | default 317.1 s, split 304.5 s (ratio 1.04), d_split 0 at every order, control 1.1e84 times the threshold |

Scripts: `run961.sh` (the stage list), `build961.sh`, `delta_cmp961.py` (line 5's Delta test, with `selftest`), `push961.sh`.
