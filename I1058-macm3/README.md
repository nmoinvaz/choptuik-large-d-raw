# I1058-macm3: hp at main 7ca74dd5 (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0) built on macm3, and the stored-reference checks

Machine: macm3 (Apple M3, 24 GB, macOS), runner macm3b. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058

Worktree `~/Source/choptuik-large-d-1058` detached at 7ca74dd51e2faf1d2cc0d955b2551af79c64ec2b, new venv `~/Source/venv-macm3-1058` (Python 3.14.3).
The build runs beside #1008's run2 (anm_run pid 98367, venv-macm3-main, untouched). Low-memory recipe `CARGO_PROFILE_RELEASE_LTO=false
CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=2`, nice 19, under caffeinate. `build_1058.py` started `hp/build.sh` at 18:10:21 UTC
and sampled the build's process tree every 30 s into `mem.log`. Its first version also stopped the build if the data volume had under 3 GiB free
or the system's free memory was under 8% twice in a row. The coordinator ruled at 18:1x UTC that no watcher may stop a process for memory or disk,
so at 18:17:43 UTC I stopped that driver by its exact pid (it never fired, and the build's process group was not signalled) and attached
`watch_1058.py`, which only appends to `mem.log` and sends `hc` alerts at under 3 GiB free disk or under 8% free memory. The build's exit status
is therefore read from build.log (the import line `hpkernel <isa> multidouble <isa>` that build.sh prints last), not from the driver.

## Results

Build of hp at main 7ca74dd51e2faf1d2cc0d955b2551af79c64ec2b on macm3, 2026-11-20, `hp/build.sh` in a new venv with the low-memory recipe `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=2`, nice 19 under caffeinate, beside #1008's run2 (untouched, on venv-macm3-main).

| machine | venv | hp / libs | build | memory | ref | scaled | jets | jets --mutate=kappa |
|---|---|---|---|---|---|---|---|---|
| macm3 (Apple M3, 24 GB) | `~/Source/venv-macm3-1058` (Python 3.14.3, worktree `~/Source/choptuik-large-d-1058` at 7ca74dd5) | multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0, Python package `8c4360ac` | ran to its import line (exit read from the log), 1907 s (31.8 min), 18:10:21 to 18:42:17 UTC | largest process 11.23 GiB, process tree 10.97 GiB | exit 0 (PASS: 72 outputs bit-identical) | exit 0 (PASS) | exit 0 (PASS: 28 outputs bit-identical) | exit 1 (FAIL: 28 of 28 outputs differ) |

- Build: `pip uninstall -y multidouble` first (not installed in the new venv), then `hp/build.sh`: 1907 s wall (31.8 min), user 2248.05 s, sys 68.81 s; started 18:10:21 UTC, process group gone 18:42:17 UTC. The exit status is read from build.log (build.sh's last line is the import line), because I replaced the build's driver mid-build when the coordinator ruled that no watcher may stop a process for memory or disk.
- Memory: `time -l` maximum resident set size of the largest process 11.23 GiB; sampled peak of the process tree 10.97 GiB (64 samples, 30 s apart); lowest system free memory 48%, lowest free disk 11.12 GiB during the build. No alert fired. rustc 1.99.1.
- Import: `hpkernel neon multidouble neon` (Python 3.14.3); `_hpkernel` `.so` sha1 a2de9b1ad744; rustc 1.99.1 (58cf8f9c3 2026-10-13), maturin 1.16.0.
- pip's direct_url of multidouble 5.1.0: `{"subdirectory": "python", "url": "https://github.com/nmoinvaz/multidouble", "vcs_info": {"commit_id": "8c4360ac0be804d081faeea524e5c1c6e2fffaaa", "requested_revision": "8c4360ac0be804d081faeea524e5c1c6e2fffaaa", "vcs": "git"}}`. It names 8c4360ac0be804d081faeea524e5c1c6e2fffaaa.

The four checks, one after the other, nice 19, the default 2 threads:

| check (from `hp/`, `python3 highm_check.py ...`) | exit | wanted | result | wall s | peak process tree GiB |
|---|---|---|---|---|---|
| `ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` | 0 | 0 | PASS: 72 outputs bit-identical | 150 | 0.64 |
| `scaled --compare=$RAW/T81/scaled_main.json` | 0 | 0 | PASS; control (scale wrong at order 7, M = 192): Newton step differs: fires | 1173 | 0.97 |
| `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` | 0 | 0 | PASS: 28 outputs bit-identical | 241 | 0.26 |
| `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa` | 1 | 1 | FAIL: 28 of 28 outputs differ | 241 | 0.26 |

Pass: 0 differing rows. `ref` and `jets` print `PASS` with every output bit-identical, `scaled` prints `PASS` (22 outputs at M 192 and 256 bit-identical, its control fires), and the control `jets --mutate=kappa` exits 1 and prints `FAIL: 28 of 28 outputs differ`, as wanted. The stored files are the raw repository's `T81/ref_main.json`, `T81/scaled_main.json` and `anm-mac/jets_inputs/jets_inputs.json` (sha1 prefixes a2c359d8145b, 2d938c93b3a0, ee008fc8d8c5). During the four checks (60 samples) the largest tree was 0.97 GiB, system free memory never under 80%, free disk never under 11.28 GiB, and run2 was alive at every sample (yes). Alerts sent: 0.



## Results at main 8179068d (the new target; files in `at_8179068d/`)

The target moved from 7ca74dd5 to main 8179068d at 20:18 UTC (#1058 comment 7049678470: `Solver.plan_auto` and `Solver.set_exact_recip`, hp/src last changed at 14b2e4c4). The 7ca74dd5 results above stay as they ran. Worktree `~/Source/choptuik-large-d-1058b` detached at 8179068d, new venv `~/Source/venv-macm3-1058b`. Drivers: `at_8179068d/build_1058b.py` (alert only from the start) and `at_8179068d/checks_1058b.py`.

Build of hp at main 8179068da460fe6be81312602e4c9987d17d73a3 on macm3, 2026-11-20, `hp/build.sh` in a new venv with the low-memory recipe `CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`, `CARGO_BUILD_JOBS=2`, nice 19 under caffeinate, beside #1008's run2 (untouched, on venv-macm3-main).

| machine | venv | hp / libs | build | memory | ref | scaled | jets | jets --mutate=kappa |
|---|---|---|---|---|---|---|---|---|
| macm3 (Apple M3, 24 GB) | `~/Source/venv-macm3-1058b` (Python 3.14.3, worktree `~/Source/choptuik-large-d-1058b` at 8179068d) | multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0, Python package `8c4360ac` | exit 0, 1864 s (31.1 min), 20:23:18 to 20:54:23 UTC | largest process 11.84 GiB, process tree 11.41 GiB | exit 0 (PASS: 72 outputs bit-identical) | exit 0 (PASS) | exit 0 (PASS: 28 outputs bit-identical) | exit 1 (FAIL: 28 of 28 outputs differ) |

- Build: `pip uninstall -y multidouble` first (not installed in the new venv), then `hp/build.sh`: exit 0, 1864 s wall (31.1 min), user 2193.91 s, sys 64.85 s (`time -l`); started 20:23:18 UTC, ended 20:54:23 UTC. The driver `build_1058b.py` only samples and alerts: `hc` at under 3 GiB free disk or under 8% free memory, no signal to any process.
- Memory: `time -l` maximum resident set size of the largest process 11.84 GiB; sampled peak of the process tree 11.41 GiB (62 samples, 30 s apart); lowest system free memory 48%, lowest free disk 11.35 GiB during the build; run2 alive at every sample (yes). rustc 1.99.1.
- Import: `hpkernel neon multidouble neon` (Python 3.14.3); `_hpkernel` `.so` sha1 6d8213c28d71; rustc 1.99.1 (58cf8f9c3 2026-10-13), maturin 1.16.0.
- pip's direct_url of multidouble 5.1.0: `{"subdirectory": "python", "url": "https://github.com/nmoinvaz/multidouble", "vcs_info": {"commit_id": "8c4360ac0be804d081faeea524e5c1c6e2fffaaa", "requested_revision": "8c4360ac0be804d081faeea524e5c1c6e2fffaaa", "vcs": "git"}}`. It names 8c4360ac0be804d081faeea524e5c1c6e2fffaaa.

The four checks, one after the other, nice 19, the default 2 threads:

| check (from `hp/`, `python3 highm_check.py ...`) | exit | wanted | result | wall s | peak process tree GiB |
|---|---|---|---|---|---|
| `ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` | 0 | 0 | PASS: 72 outputs bit-identical | 180 | 0.80 |
| `scaled --compare=$RAW/T81/scaled_main.json` | 0 | 0 | PASS; control (scale wrong at order 7, M = 192): Newton step differs: fires | 1204 | 1.00 |
| `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` | 0 | 0 | PASS: 28 outputs bit-identical | 241 | 0.28 |
| `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa` | 1 | 1 | FAIL: 28 of 28 outputs differ | 241 | 0.25 |

Pass: 0 differing rows. `ref` and `jets` print `PASS` with every output bit-identical, `scaled` prints `PASS` (22 outputs at M 192 and 256 bit-identical, its control fires), and the control `jets --mutate=kappa` exits 1 and prints `FAIL: 28 of 28 outputs differ`, as wanted. The stored files are the raw repository's `T81/ref_main.json`, `T81/scaled_main.json` and `anm-mac/jets_inputs/jets_inputs.json` (sha1 prefixes a2c359d8145b, 2d938c93b3a0, ee008fc8d8c5). During the four checks (62 samples) the largest tree was 1.00 GiB, system free memory never under 80%, free disk never under 13.97 GiB, and run2 was alive at every sample (yes). Alerts sent during the build and the checks: 0.
