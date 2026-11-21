# I1058-win2: hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0) on win2: a new venv, the build and the stored-reference checks

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058 (Nathan, 2026-11-20 18:04 UTC: "update all machines to latest multi libs"; the coordinator's hc: win2 after the #1034 libm-free test is posted, fat LTO, below-normal priority, about 150 min by the issue, win2b's #1025 job keeps running beside).

## Change of target (the coordinator's hc of 2026-11-20 about 20:20 UTC, read at 20:20 UTC)

The first attempt (target main 7ca74dd5, worktree `D:/choptuik-i1058`, venv `venv-i1058`) started 18:26:57 UTC and was **stopped at about 20:21 UTC by the coordinator's order**, after 1 h 54 min, because Nathan asked at about 20:15 UTC to upgrade all machines to the latest multi libs and repo code, so #1058's target moved to main **8179068d** (#1058 comment 7049678470): "one 5 h build instead of two". No memory pressure was involved (commit 77 GB of 101.5, 21.9 GB available). I killed by exact pid, driver bash first, then the build's bash, nice, maturin, cargo and rustc (listed in `stopped_7ca74dd5/exits_1058.txt`); nothing else was touched. That attempt did not finish (no hpkernel in venv-i1058). Its logs are in `stopped_7ca74dd5/` (build.log, build.times, mem.log, commit.log, exits, the pip logs); its venv and worktree stay unused. Its peak so far: rustc 33.23 GB working set, commit about 77 GB.

## Setup (written 2026-11-20 20:22 UTC, before the restarted build)

| | |
|---|---|
| code | a new worktree `D:/choptuik-i1058b`, detached at main **8179068d** ("EXACT_RECIP: the commands of 3.5's two follow-ups, with their readings (#1043)"), tree `5a6a9479ade15ce0451b00d2b530071e1428b2a5`. Against 7ca74dd5, `hp/` changed in `src/plan_auto.rs` (new, 687 lines: plan_auto), `src/model.rs`, `src/python.rs` (set_exact_recip), `src/recip_tests.rs`, `src/lib.rs`, `src/series_split.rs`, `src/split_tests.rs`, `src/qd_residual.rs`, `python/hpkernel/driver.py`, `reseed.py`, `plan_auto_gain.py` and others (19 files); `hp/Cargo.toml`, `hp/Cargo.lock` and `hp/pyproject.toml` are unchanged: multidouble 5.1.0, multishoot 4.1.0, multisolver 0.2.2, Python package at 8c4360ac0be804d081faeea524e5c1c6e2fffaaa (checked in the files at 8179068d) |
| venv | a **new** `C:\Users\nathan\Source\venv-i1058b` (Python 3.14.10 by `python -m venv`, then the repo's `requirements.txt` of that commit, sha256 prefix 9a539138a26f1a91, unchanged: numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0). Running jobs and their venvs untouched (win2b's #1025 solves use venv-i962) |
| step 1 (the issue's) | `PIP_NO_CACHE_DIR=1 pip uninstall -y multidouble` (a no-op in a new venv, logged), then `hp/build.sh`: fat LTO (the default profile), `CARGO_BUILD_JOBS=8`, `RUSTFLAGS=-C target-cpu=native` (set by build.sh), BelowNormal, `PIP_NO_CACHE_DIR=1`. Log: the time (`build.times`), the peak memory (the alert-only watches' `mem.log` and `commit.log`, 30 s samples, kill nothing) and pip's `direct_url.json` of multidouble (`versions.txt`), which must name 8c4360ac |
| cap | 54981 s (three times this machine's own last fat build, 5 h 5 min at 9980cd93), by the exact root pid of the build's bash (command line checked for `build.sh`), nothing else killed |
| step 2 (the issue's), from `hp/`, one BLAS thread each, three chains | `highm_check.py ref --compare=\$RAW/T81/ref_main.json --Ms=48,64,80`; `scaled --compare=\$RAW/T81/scaled_main.json`; `jets --compare=\$RAW/anm-mac/jets_inputs/jets_inputs.json`; `jets ... --mutate=kappa` (must fail). \$RAW = my raw worktree `D:/choptuik-i935-raw`; the four reference files have equal sha256 in it and in the push worktree (`input_sha256.txt`). As information: `ref --compare=T45-win/scratch/t45/diag/ref_new.json` (win2's own Windows reference) |
| memory triggers | I tell the coordinator if commit passes 99 GB, the page file grows by more than 2 GB, or available memory stays under 1 GB for 5 minutes; stop nothing myself. The attempt before peaked at commit about 77 GB (rustc 33.23 GB) beside win2b's #1025 solves |
| raw | `I1058-win2/` (this folder), pushed at the end; a row posted on #1058: the machine, venv path, build time and memory, the four exits |

## Readings fixed before the build

1. **Build**: `hp/build.sh` exit 0; `hpkernel` imports from venv-i1058b (isa printed); `hp/Cargo.lock` and the `.pyd` strings say multidouble 5.1.0, multishoot 4.1.0, multisolver 0.2.2; **pip's direct_url names 8c4360ac0be804d081faeea524e5c1c6e2fffaaa** (a different commit, or a missing multidouble package, is a failure reported as such).
2. **Checks, the issue's pass rule: 0 differing rows**: `ref` (T81) exit 0 with 72 of 72 bit-identical; `scaled` exit 0, 22 of 22, its control firing; `jets` exit 0, 28 of 28 (the M 32 input line differs by the expected numpy resampling, AGENTS.md); `jets --mutate=kappa` exit 1 with 28 of 28 differing. A difference is reported with its size and where it sits, whether a zero's sign or a NaN's low part; nothing is loosened.
3. The `ref` against the T45 Windows reference is information; a difference there would be reported with the same detail.
4. The exit line of `build.times` is crun's wait on the build's bash; it is a build result only if `hpkernel` imports and `versions.txt` shows the new crates (the stopped #1034 build's "exit 0" was a kill artifact, remembered here).

## Result (written 2026-11-21 01:50 UTC)

**The build at main 8179068d passes: exit 0, pip's direct_url names 8c4360ac, and every stored-reference check has 0 differing rows with its control behaving.**

| item | value |
|---|---|
| machine, venv | win2 (desktop-pc, Core Ultra 7 265K, 20 threads, 95 GB), `C:\Users\nathan\Source\venv-i1058b`, worktree `D:\choptuik-i1058b` at main 8179068d |
| build | `hp/build.sh` fat LTO, `CARGO_BUILD_JOBS=8`, BelowNormal, `PIP_NO_CACHE_DIR=1`: **exit 0, 19007 s = 5 h 16 min 47 s** (20:24:09 to 01:40:55 UTC), cap 54981 s not reached; rustc 1.96.0, maturin 1.16.0 |
| import | `hpkernel` isa **avx2**, multidouble avx2; `hp/Cargo.lock`: multidouble **5.1.0**, multishoot **4.1.0**, multisolver **0.2.2**; the `.pyd` carries the path strings `multidouble-5.1.0` and `multishoot-4.1.0`; `.pyd` sha256 ee09ddfe53c7db0563ef113b6cf650daca869553d8f995832d93e660c2661730 |
| pip's direct_url (multidouble 5.1.0 package) | url `https://github.com/nmoinvaz/multidouble`, subdirectory `python`, **commit_id 8c4360ac0be804d081faeea524e5c1c6e2fffaaa** (requested_revision the same); `pip uninstall -y multidouble` before the build was the expected no-op in the new venv |
| memory (alert-only watches, 30 s samples, 629 samples) | the big rustc peaked at **35.70 GB working set, 36.61 GB private**; **commit peak 80.8 GB** (00:33:40 UTC) of 101.47; **minimum available 18.15 GB**; page file allocation stayed 6144 MB; `alerts.log` never written; none of the coordinator's triggers fired. Nothing else of mine ran beside it |
| `highm_check.py ref --compare=T81/ref_main.json --Ms=48,64,80` | **exit 0**, 72 of 72 outputs bit-identical, 79 s |
| `scaled --compare=T81/scaled_main.json` | **exit 0**, 22 of 22 bit-identical; its control (scale wrong at order 7, M = 192) changes the Newton step: fires; 508 s |
| `jets --compare=anm-mac/jets_inputs/jets_inputs.json` | **exit 0**, 28 of 28 bit-identical, 126 s; only the M 32 input differs from the reference's (`21b5b259...` against `710ec990...`, the expected numpy resampling of AGENTS.md), the M 48 and M 64 inputs are the same |
| `jets ... --mutate=kappa` | **exit 1** as required, 28 of 28 outputs differ, 125 s |
| information: `ref --compare=T45-win/.../ref_new.json` (win2's own Windows reference) | exit 0, 72 of 72 bit-identical, 77 s |

Pass rule of the issue: 0 differing rows. It holds for ref, scaled and jets; the control differs in all 28 rows as it must. Against #1034's run at main 9980cd93 (multidouble 4.9.1, multishoot 3.3.0), whose reference checks passed the same way, the new crates and the hp code up to 8179068d (plan_auto, set_exact_recip, with their flags off by default) moved no bit of what these checks reach; the checks do not reach a code path that those flags switch on. The label `(step 5)` in the first line of `summary_1058.txt` is left over from the script this one was copied from; these are the issue's step 2.

The first attempt (target 7ca74dd5, stopped at 1 h 54 min by the coordinator's order) is in `stopped_7ca74dd5/`.

Files: `build.log`, `build.times`, `versions.txt`, `ref_t81.log`, `ref_t45.log`, `scaled.log`, `jets.log`, `jets_kappa.log`, `summary_1058.txt`, `exits_1058.txt`, `mem.log`, `commit.log`, `input_sha256.txt`, `requirements.txt`, the pip logs, the scripts, `stopped_7ca74dd5/`.
