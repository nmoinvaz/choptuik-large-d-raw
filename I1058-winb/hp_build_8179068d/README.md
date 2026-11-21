# I1058-winb/hp_build_8179068d: hp build at main 8179068d on the win laptop, beside the #1025 P4 rows (winb)

Written before the build starts (2026-11-20 21:27 UTC).

Machine: winb, Surface Laptop 4 (i7-1185G7, 4 cores, 8 threads), 31.8 GB, Windows 11, Git Bash; page file system-managed (4.9 GB allocated at the start, commit limit 36.6 GB, 50 GB free on C:).

## Question

Order of the coordinator (#1058, comms, winb): build the hp kernel at main 8179068d on this laptop, beside the P4 rows of #1025 (whose driver is left alone), and measure the build's time, peak commit and page-file growth, and the cost to the P4 rows. Then the four stored-reference checks. The #1058 table (main 7ca74dd5) had said "no hp build on winb" because the Windows build needs about 30 GB; the coordinator asked for it with the low-memory recipe, expecting the laptop to page.

## Plan

| step | what |
|---|---|
| worktree | `C:/Users/nathan/Source/choptuik-i1058-hp`, detached at 8179068da460fe6be81312602e4c9987d17d73a3, made with core.autocrlf=false so build.sh has LF |
| venv | NEW `C:/Users/nathan/Source/venv-i1058` (Python 3.14, requirements.txt); venv-md510 (P4's) is not touched |
| uninstall | `PIP_NO_CACHE_DIR=1 pip uninstall -y multidouble` in the new venv |
| build | `hp/build.sh` with MSVC's link.exe first on PATH (vcvars64, Git's usr\bin last), BelowNormal, `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16` (the low-memory recipe, same bits per #600/#604); the recipe's variables also reach the pip build of multidouble's Python package inside build.sh; CARGO_BUILD_JOBS not set (8) |
| watcher | every 30 s: commit charge and limit, available memory, page file allocated/used/peak, C: free, the biggest rustc's working set and private bytes (`mem_1058.csv`); alert-only, hc to the coordinator if C: free < 10 GB, stops nothing |
| priority | `prio_hp_1058.ps1` sets every descendant of the driver that is not BelowNormal to BelowNormal (build.sh's `nice -n 2` may change a class) |
| checks | from hp/ with the new venv: `highm_check.py ref --compare=RAW/T81/ref_main.json --Ms=48,64,80`, `scaled --compare=RAW/T81/scaled_main.json`, `jets --compare=RAW/anm-mac/jets_inputs/jets_inputs.json`, and `jets --compare=... --mutate=kappa` (must fail); pass is exit 0 and 0 differing rows. RAW is a plain folder by `git show` from raw origin/main (blobs checked with `git hash-object --no-filters`, `prep_raw_1058.log`) |
| P4 cost | the coordinator wants it told if a P4 row takes more than twice the cross-check row's 1.87 h (6722 s) while the build runs; row D 15.5 k_c 63 started 2026-11-20 20:51:02 UTC |

## Starts (2026-11-20, UTC)

| start | driver, log | what happened |
|---|---|---|
| 1, 21:27:19 | `driver_hp_1058.py`, `hp1058_build.log` | Made the venv (9 s), installed requirements.txt (57 s) and ran the uninstall (multidouble not installed, skipped). `hp/build.sh` then exited 1 after 0.4 s with the WSL launcher's text ("Windows Subsystem for Linux has no installed distributions", UTF-16, `hp1058_build_output.log`). Cause: the driver ran `cd hp && bash build.sh`, and in Git's bash `bash` resolved to the WSL launcher in WindowsApps/System32 ahead of `/usr/bin/bash`. Nothing was compiled |
| 2, 21:29:42 | `driver_hp_1058b.py`, `hp1058b_build.log` | Same worktree and recipe, `/usr/bin/bash build.sh`; reuses `venv-i1058` (only requirements.txt in it, checked: no multidouble or hpkernel entries), repeats the uninstall. The watchers (`watch_mem_1058b.ps1`, `prio_hp_1058b.ps1`) were restarted for the new log. The build time counts from 21:29:45 |

The driver also runs the four checks right after the build, so they ran at 23:29:51, before the coordinator's order to run them (00:26 UTC); they were not repeated.

## Result

| item | value |
|---|---|
| worktree, HEAD | `C:/Users/nathan/Source/choptuik-i1058-hp`, 8179068da460fe6be81312602e4c9987d17d73a3 |
| venv | `C:/Users/nathan/Source/venv-i1058`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0, hpkernel 0.1.0, multidouble 5.1.0 |
| toolchain | rustc 1.95.0 (59807616e 2026-04-14), cargo 1.95.0, MSVC 14.51.36231 link.exe first on PATH (checked in Windows and in bash) |
| build | `hp/build.sh` exit 0, 7206 s (120.1 min), 21:29:45 to 23:29:50 UTC; BelowNormal throughout (`prio_hp_1058.log` lists no lift) |
| import | `hpkernel avx512 multidouble avx512` (this CPU has AVX-512); `Solver` has `set_exact_recip` True and `plan_auto` True; `_hpkernel.cp314-win_amd64.pyd` 85 931 008 bytes, sha1 c12c22c38ad7 |
| multidouble direct_url | `{"subdirectory": "python", "url": "https://github.com/nmoinvaz/multidouble", "vcs_info": {"commit_id": "8c4360ac0be804d081faeea524e5c1c6e2fffaaa", ...}}` |

### The four checks (from hp/, `venv-i1058`, BelowNormal, beside P4; the references are raw's `T81/ref_main.json` blob 7fa3eba9, `T81/scaled_main.json` ba9d3f40, `anm-mac/jets_inputs/jets_inputs.json` 0807f73d and its `jets_inputs_inputs.npz` 6e804f1c)

| check | exit | wanted | result | wall s |
|---|---|---|---|---|
| `ref --compare=T81/ref_main.json --Ms=48,64,80` | 0 | 0 | PASS: 72 outputs bit-identical | 128 |
| `scaled --compare=T81/scaled_main.json` | 0 | 0 | PASS; control (scale wrong at order 7, M = 192): Newton step differs, fires | 1054 |
| `jets --compare=anm-mac/jets_inputs/jets_inputs.json` | 0 | 0 | PASS: 28 outputs bit-identical | 218 |
| the same `jets --mutate=kappa` | 1 | 1 | FAIL: 28 of 28 outputs differ | 220 |

DIFFERS lines in the three comparisons: 0, 0, 0 (`checks/`).

### Memory and page file (`mem_1058.csv`, 30 s samples; `mem_stats_1058.py` and `mem_stats_1058.txt`)

| quantity | before the build (21:27:16) | during the build |
|---|---|---|
| commit charge | 23.84 GB (limit 36.58) | peak 42.50 GB at 22:11:09 (limit grew to 45.04 GB at 22:07:36); 34 samples above 40 GB |
| available memory | 14.50 GB | minimum 0.11 GB at 22:06:05; 14 samples under 1 GB |
| page file allocated | 4864 MB | maximum 13 528 MB (+8664 MB), 9726 MB at 23:57:01 |
| page file in use | 454 MB | maximum 8048 MB at 22:08:06 (PeakUsage counter 8098 MB) |
| C: free | 50.06 GB | minimum 39.44 GB at 21:56:57; 44.58 GB at 23:57:01 |
| biggest rustc | none | working set 18.70 GB, private 20.35 GB (4 rustc at 21:30 for the dependencies, then a single rustc from 21:31:06 to 23:28:37, the hp crate; 4 again from 23:28:37 to 23:29:38, the pip build of multidouble) |

The commit charge includes the other session's jobs on this laptop (two pythons of 3 to 7 GB) and P4's row (3 to 4.5 GB), so the build's own share is not separable from this log. `alerts_1058.log` holds no alert (C: free never under 10 GB). No job was stopped.

### Cost to the P4 rows (#1025, `I1025-win/p4/p4_w.log`)

| row | time | note |
|---|---|---|
| cross-check, Fb D 16 k_c 55 | 6722 s (1.87 h), 18:58:54 to 20:51:01 | before the build; the other session's jobs ran beside it |
| D 15.5 k_c 63 | 10 953 s (3.04 h), 20:51:02 to 23:53:40 | the build covered 21:29:45 to 23:29:50 of it (120 of 183 min) and the checks 23:29:51 to 23:53:40; 1.63 times the cross-check, under the coordinator's 2 times bar (13 444 s, 00:35 UTC) |

The two rows are different problems (k_c 55 and k_c 63, 13 and 12 evaluations), so the ratio is an upper bound on the slowdown, not a measurement of it: no k_c 63 row has run alone on this laptop.

Files: `hp1058_build.log` (start 1), `hp1058b_build.log`, `hp1058b_build_output.log` (build.sh's output), `checks/`, `checks_1058.json`, `mem_1058.csv`, `alerts_1058.log`, `prio_hp_1058.log`, the drivers, launchers and watchers, `prep_raw_1058.sh` and its log.
