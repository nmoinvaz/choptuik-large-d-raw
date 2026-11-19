# I1009-dh170: cache-ordered f64 Jacobian fill and chunked dmat_apply, x86 checks and timings on one Linux build

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1009 (#998 step 1; coordinator's hc 2026-11-19).

## Setup

- hp `perf/cauchy-cache-chunks` at **76fdcbc9** in a new worktree `~/Source/choptuik-large-d-ccc`; its `[patch.crates-io]` takes multidouble's branch `perf/dmat-apply-chunks`
  (`MatLane::dmat_apply` in chunks of 8 columns), so one build carries both changes. A new venv `~/Source/venv-ccc` (uv, 3.14.10, seeded with pip because `hp/build.sh` calls it;
  the issue's command does not say `--seed`). Nothing here touches `~/Source/choptuik-large-d-935/.venv`, which #949's near_null lanes import.
- Build: `hp/build.sh` with `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6`, nice 15, under `/usr/bin/time -v` (`build1009.sh`, `build.log`),
  with a **memory watchdog** (`MemAvailable` every 2 s into `mem1009.log` every 30 s; the build's process group is killed if it falls under 2 GB, the issue's rule, with the top
  processes by resident size logged). Beside it run #949's two near_null lanes and #996's two 180-digit jobs (about 2 GB together).
- Inputs: the committed bytes of raw origin/main (`raw_commit.txt`), extracted into `~/scratch1009/raw` = $RAW: `T81/ref_main.json`, `T81/scaled_main.json`,
  `anm-mac/jets_inputs/`, and the M 320 state `T100-win2/states/lowDhm_x0.000157-0.975_D3.0444_M320.npz`.

## Checks and pass criteria, written before the build

| # | check (from `hp/` of the worktree) | pass |
|---|---|---|
| 1 | `cargo test --profile release-dev --lib cols_` | all pass, including the control tests (`COLS_MUT_ULP`: one ulp of p_1 in one lane must make the coefficients and the Jacobian differ) |
| 2a | `python3 highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` | exit 0, 72 of 72 outputs bit-identical |
| 2b | `highm_check.py scaled --compare=$RAW/T81/scaled_main.json` | exit 0, 22 of 22, its control fires |
| 2c | `highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` | exit 0, 28 of 28 |
| 2d | the same with `--mutate=kappa` | exit 1 |
| 3 | `python3 dump_ctx.py $RAW/T100-win2/states/lowDhm_x0.000157-0.975_D3.0444_M320.npz ctx320.bin`, then `FILE=ctx320.bin RUSTFLAGS="-C target-cpu=native" CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6 cargo test --release --lib bench_fill -- --ignored --nocapture` at `THREADS=1` and `THREADS=4` | runs; the bench compares the lane-vector and the field-wide form bit for bit inside one binary (its own check must hold); the seconds per step of both forms and their ratio are reported either way |
| 4 | multidouble at `perf/dmat-apply-chunks` (6dfd5b0): `cargo test --release --features mutate --test field f64_matrix` and the `dmat_f64` bench | the test passes and its control `mutate::DMAT_CHUNK` fires; the bench ratio is reported |

Acceptance (the issue's): every bit check identical with its control firing. A timing ratio below 1 on x86 is a finding, not a failure. `ctx320.bin` is input, re-made by the command, not committed.
Not in the issue's steps, so not claimed: that the 6-job build stays under 2 GB free next to the other jobs; the watchdog says.

## 2026-11-19 07:07 UTC, first build attempt stopped by the watchdog (`build.log`, `mem1009.log`)

The build started 06:51:50 UTC (6 jobs, nice 15, LTO off, 16 codegen units; worktree `~/Source/choptuik-large-d-ccc` at 76fdcbc9, venv `~/Source/venv-ccc`). At 07:05:37 UTC, 14 minutes in, the watchdog
read `MemAvailable` 2015 MB, under the issue's 2 GB, and killed the build's process group (exit 143, minimum 2015 MB). The cause is one process: `rustc --crate-name _hpkernel` was at **26.7 GB resident** and
still growing; the other jobs on the machine together held about 2 GB (the two 180-digit #996 amplitude runs 0.34 and 0.29 GB, two near_null reads under 0.1 GB each, the desktop and the Claude processes
about 1.5 GB). `MemAvailable` fell from 28.4 GB at the start to 2.0 GB in 14 minutes. The earlier hp builds on this box, run with nothing else heavy beside them, peaked at 29.2 GB (#935) and 29.4 GB (#958), both with 10 jobs; at #958's peak the system had 31.0 GB used and 0.95 GB available. So, if 6 jobs
lowers the final compile's peak only a little,  the final `_hpkernel` compile needs about the same: **this build cannot meet the 2 GB rule on a 31 GB machine, with or without the other jobs**. Nothing after the build
was run (checks 1 to 4). No file of any other job was touched; the 935 venv was not used.
