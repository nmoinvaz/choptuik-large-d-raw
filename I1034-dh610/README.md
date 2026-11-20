# I1034-dh610: runner checks for PR #1041 (fast product for the series' middle terms) at main 9980cd93

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1034; steps 1-6 of the coordinator's comment 7019891857.
PR #1041 is merged (main 17ae55bf); the coordinator's hc messages moved the code head to 9980cd93 (main after #1047: fastmul's edge cases and checks, fastmul's direct route at
e2 != 0, timing fields in driver.newton_step; both checksums unchanged: fast series 30acdab9851616fb, split 1 a0aada9b8fe95419), and added #1040's check after the build (raw `I1040-dh610/`).

Code: a new worktree `~/Source/choptuik-large-d-1034` detached at 9980cd93, a new venv `~/Source/venv-i1034` (uv, Python 3.14, `requirements.txt`). Nothing a live job imports is touched.
RAW is `~/Source/choptuik-large-d-raw` (live clone; inputs not in it come from origin/main by `git archive`, no pull). The machine is shared with #1033 run 5 (8 threads) and #1021's jobs
(about 6 processes), so every wall time below is loaded.

Order run (cheapest first; the coordinator's numbering in brackets), each under a cap of 3 times its estimate by `timeout` on its exact pid, nice 10:
0. venv and worktree check; 1. `hp/build.sh` (est. 31 min, 24 GB) [1]; #1040's `step_timing_check.py` twice (a few minutes) [#1040]; 2. `cargo test --profile release-dev --lib split_ -- --nocapture`
then `fastmul_planted` (est. 18 min each) [2]; 5. `highm_check.py` ref, scaled, jets and `jets --mutate=kappa` (est. 10 + 40 + 5 + 5 min) [5]; 3. `series_split_check.py` at
`I608-dh610/restart4_d6/anm_pin3_D253.3382.npz`, `--split 2`, then `--mutate 31` (est. 60-90 min each) [3]; 4. the same at `I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz` (est. 90 min each) [4];
6. `anm_run.py` chain step at `--series_split` 0, 1, 2 from the leg08 state (est. 70-90 min each) [6]. Exits are in `exits_1034.txt`, one summary line per step in `summary_1034.txt`.

## Files

| file | what |
|---|---|
| `common1034.sh`, `run1034.sh` | paths and the driver (the commands are in it) |

## Step 2 result (20 Nov 08:39 UTC) and an added run

`step2_split` exit 0 (1223 s: compile and tests, 3 passed, 2 ignored: `bench_split`, `split_file`), `step2_fastmul_planted` exit 0 (16 s, 1 passed). The printed checksums are NOT the expected ones: split series' checksum 072e4ce86c49682c (expected
a0aada9b8fe95419), fast series' checksum 69ffd7e54fcf9637 (expected 30acdab9851616fb, the Mac's `I1034-mac/logs/v5_split_fast_accuracy.log`). Every other printed figure is identical to the Mac's (worst d_fast / threshold 2.11e-4, 5879
products, max_frac 3.81e-5, controls 2.21e123 and 2.14e123). `cargo test` ran without RUSTFLAGS, so on multidouble's portable Sse2 backend, not the Avx2 one `hp/build.sh` uses; `step2b_native.sh` (added, same commit) repeats it with
`RUSTFLAGS='-C target-cpu=native'`. `split_tests.rs`'s `synth()` builds its inputs with libm `tan`, `sin` and `cos`.

## Step 6 (third attempt, `run1034_step6c.sh`, `--D_max 300`, OUT `step_s<S>_dmax300`) and the closing summary, 20 Nov 10:22 UTC

The issue's command as written failed twice (relative OUT refused by raw_out.py; then, with an absolute OUT, a no-op run because `--D_max` defaults to 200 below the state's D 237.527): `step6_chain_s*.log`, `step6b_chain_s*.log`.
Third attempt: `--series_split` 0, 1, 2 all exit 0 (955, 916, 800 s); the series saved in 280, 237 and 158 s; each step accepted at a 0.5 to D 238.026970387 with Delta 1.686998214543 (formula diff -1.5e-06), moved 2.4e-35, corrector 211, 215 and 184 s.
`cmp_step6_1034.py` (`compare_step6_states.txt`, control `compare_step6_states_control.txt`): the accepted base `anm_pin3_D238.0270.npz` of step 1 is byte-identical to step 0's, step 2's differs in z3 to z7 (3461 to 5840 bytes each; z0 to z2 equal); the series files differ in `meta`
only for step 1 (timings) and in z2 to z7 for step 2. Memory peaks (journal): unit i1034 26.8 GB (the build and the checks), i1034b 11.2 GB, i1034c 205 MB, i1034d 1.5 GB.
