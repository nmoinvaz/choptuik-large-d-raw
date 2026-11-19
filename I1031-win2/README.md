# I1031-win2: hp on multidouble 4.9.1, the win2 build and its bit-identity checks before the bump goes to main

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session beside win2b's #903 chain and #945's leg. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1031 (the coordinator's hc `nathans-macbook-air-m5-3/t5`, 2026-11-19 after #1028). Depends on #1009 and #1028.

## Setup (written before the build)

| | |
|---|---|
| code | a new worktree `D:\choptuik-i1031`, detached at `origin/chore/multidouble-4.9.1` (6266a213 = main 82f87a33 + one commit: `hp/Cargo.toml`, `hp/Cargo.lock`) |
| venv | a new `C:\Users\nathan\Source\venv-md491` (Python 3.14.10; `python -m venv` + `pip install -r requirements.txt`, uv is not installed here) |
| not touched | #1003's `D:\choptuik-i1003` and #945's checkouts and venvs (venv-i600, `D:\choptuik-i600`, `D:\choptuik-i603r`), `D:\choptuik-i962` and venv-i962 (win2b's ks_chain2), `D:\choptuik-i935` and venv-md482 (read only) |
| build | `run_build.sh`: `hp/build.sh`, the default fat LTO release profile (no `CARGO_PROFILE_*` override), `CARGO_BUILD_JOBS=8`, `RUSTFLAGS="-C target-cpu=native"` (build.sh), BelowNormal, rustc 1.96.0 / cargo 1.96.0 / maturin 1.16.0 |
| memory | `mem_watch.ps1`: available memory (free + standby), free memory and the build's processes' working sets every 30 s into `mem.log`; a line in `alerts.log` when the available memory falls under 6 GB. **Alert only, it kills nothing** (the coordinator's rule); on an alert I tell the coordinator and the other sessions' owners and nothing is stopped without their word. #935's fat build beside other jobs took 250 min and peaked at 34.7 GB working set (35.6 GB private). **Margin at the start (17:28 UTC): 37.1 GB available of 95.5 GB** (other jobs hold about 58 GB), so the expected peak leaves about 1.5 to 2.5 GB, which the watch will show. The standby list is inside that figure, not on top of it (17:34 UTC: available 38.4 GB = free+zero 4.5 + standby 33.9). The page file is system-managed (6144 MB, 70 MB used at the start; the coordinator: 221 GB free on C:), so the commit limit grows instead of an allocation failing |
| commit watch | `commit_watch.ps1` (added 17:35 UTC at the coordinator's hc, alert-only): commit charge, commit limit, page file size and usage, free+zero and standby every 30 s into `commit.log`; an alert in `alerts.log` when commit passes 95 GB or the page file's size grows or its usage rises 512 MB over the start's (#1003's K 49 run beside the build has no resume). The coordinator then revised **what I tell it** (hc 17:5x UTC, after #935's 35.6 GB private peak): commit over **99 GB**, the page file grown by more than **2 GB**, or available memory under **1 GB for more than 5 min**; crossing 95 GB alone is not reported. The watches' own alert lines keep their first thresholds (95 GB, 512 MB, 6 GB), so `alerts.log` holds more lines than were reported. The event stream that applies the revised triggers to `commit.log` and `mem.log` is a scratch script (its planted-log selftest: quiet case silent, commit 99.5 GB, page file +2256 MB by size and +2230 MB by usage and available under 1 GB held each fire, +856 MB and a short dip do not). Nothing is stopped by any of this |
| raw inputs | `$RAW` = `D:\choptuik-i935-raw` (my worktree of the raw-data repository, clean for the three inputs); their sha256 equal the push worktree's (`input_sha256.txt`) |
| the Python package | `hp/pyproject.toml` still pins multidouble's Python package at 482c6835 (4.8.2); the branch changes the crate only. The checks that use `dd_*` helpers run on that package, as every earlier build here |

## Checks and acceptance, fixed before the run (the issue's)

1. `hpkernel` imports from the new venv and the crate it was built from is multidouble 4.9.1 (`hp/Cargo.lock`, and the crate path strings read out of the `.pyd`).
2. **NOT run on win2 (the coordinator's hc, recorded 18:56 UTC: "the cols_ cargo test does not run on win2"; it queues it for dh610 after its K 49 run).** Reason: the compile's peak memory is unknown (24 to 32 GB for the thin builds of #1009 and #962) and #1003's K 49 beside it on win2 cannot resume; `cols_` compares two fill forms inside one build and passed on dh610 for #117's branch (#1009), while the bits 4.9.1's constructor changes could move are what ref/scaled/jets compare. The step as written was: `cargo test --profile release-dev --lib cols_`, whose control `COLS_MUT_ULP` must fire (each `cols_` test prints its control's differing entries and fails when the control differs in none). The command as written has no `RUSTFLAGS`, so it runs multidouble's portable backend; the `target-cpu=native` run (the AVX2 backend, the one the hpkernel build uses) is added as #1009's dh610 run did (`cols_native1009.sh`).
3. `python highm_check.py ref --compare=$RAW/T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80`: exit 0, 72 of 72 bit-identical.
4. `python highm_check.py scaled --compare=$RAW/T81/scaled_main.json`: exit 0, 22 of 22, its control fires.
5. `python highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json`: exit 0, 28 of 28 (the M 32 "input DIFFERENT" line is numpy resampling, expected); and its control `--mutate=kappa`: exit 1.

**Acceptance, as the coordinator narrowed it for win2:** the Python checks (3 to 5), the `cols_` test being dh610's. The issue's: every check identical to its reference with its control firing: the coordinator merges the bump into main. **Any difference:** report each with its size and where it sits, and say whether it is a zero's sign (-0 against +0) or a NaN's low part (what the `DD::new` change produces: a zero low part becomes +0, an infinite or NaN part gives a NaN low part). The bump then waits.

Not in the issue's steps, so not claimed: that the build fits beside the other jobs (the watch says), and any timing.

Logs: `build.log`, `build.times`, `versions.txt`, `mem.log`, `commit.log`, `alerts.log`, `ref.log`, `scaled.log`, `jets.log`, `jets_kappa.log`, `summary_1031.txt`.

## Result (2026-11-19, build ended 21:54:43 UTC, checks done 22:03:52 UTC)

**Build** (`build.times`, `build.log`, `versions.txt`): exit 0, 17:33:06 to 21:54:43 UTC = 4 h 21 min, fat LTO, 8 jobs, BelowNormal, rustc 1.96.0. `hpkernel` imports from `venv-md491` (isa avx2). `hp/Cargo.lock`: multidouble 4.9.1, multishoot 3.3.0, multisolver 0.1.1; the `.pyd`'s crate path strings read `multidouble-4.9.1`, `multishoot-3.3.0`. The Python package (`multidouble` 0.1.0) is at 482c6835 as `hp/pyproject.toml` pins it.

**Memory** (`mem.log` 522 samples, `commit.log` 521, 30 s apart): peak rustc working set 33.71 GB (34.61 GB private); peak commit 95.76 GB (21:18:36); minimum available 3.01 GiB (21:18:02); page file 70 MB used of 6144 MB, at most 72 MB. None of the coordinator's triggers (commit over 99 GB, page file up more than 2 GB, available under 1 GB for 5 min) fired. The watches' own first lines did: `alerts.log` has 78 lines, 76 of available memory under 6 GB and 2 of commit over 95 GB (95.63 GB at 21:17:35, 95.15 GB at 21:34:08), none for the page file. Nothing was stopped. The big rustc (pid 20128) fell from 33.7 GB to 9 GB in the last seven minutes and exited at 21:54:42.

**Checks** (`summary_1031.txt`, run by `run_checks.sh` from `D:\choptuik-i1031\hp`, three chains of one BLAS thread each, BelowNormal, 21:54:45 to 22:03:52 UTC):

| check | expected | got | result |
|---|---|---|---|
| `ref --compare=T45-win/scratch/t45/diag/ref_new.json --Ms=48,64,80` | exit 0, all identical | exit 0, 65 s | PASS: 72 outputs bit-identical |
| `scaled --compare=T81/scaled_main.json` | exit 0, control fires | exit 0, 545 s | 22 of 22 bit-identical; control (scale wrong at order 7, M = 192): Newton step differs: fires |
| `jets --compare=anm-mac/jets_inputs/jets_inputs.json` | exit 0, all identical | exit 0, 120 s | PASS: 28 outputs bit-identical (the M 32 "input DIFFERENT" line is the expected numpy resampling) |
| `jets ... --mutate=kappa` | exit 1 | exit 1, 121 s | FAIL: 28 of 28 outputs differ (the control fires) |

No output differs from its reference, so there is no zero-sign or NaN-low-part difference to classify. **The `cols_` cargo test (step 4, first bullet) was not run on win2**: the coordinator moved it to dh610 (its hc, recorded 18:56 UTC), the compile's peak memory being unknown and #1003's K 49 beside it unable to resume.
