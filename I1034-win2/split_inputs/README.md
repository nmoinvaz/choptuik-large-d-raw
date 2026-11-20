# I1034-win2/split_inputs: #1034's checksum mismatch, check (b): the inputs of the fast and split checksums hashed on win2 (main 1926c1c3)

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1034 (closed at 10:33:55 UTC; this follows the result there, comment 7044472135). Task: the coordinator's hc of 2026-11-20 (read 16:32 UTC): check (b) of my result in a form that runs now. The parent folder `I1034-win2/` holds the first run (main 9980cd93), whose fast and split checksums differed from the Mac's.

## Setup (written 2026-11-20 16:33 UTC, before the run)

| | |
|---|---|
| code | a new worktree `D:/choptuik-i1034b`, detached at main **1926c1c3** ("split_tests: hash the split and fast checksums' inputs (#1034)"), tree `82a176d0936a9795768ec9be59b16c4daffa094f`; it adds `split_tests::split_inputs_hash` (prints `split inputs: libm <h>, state <h>, planted <h>`, FNV-1a of f64 bits: `libm` = the f64 tan, sin and cos values `qd_residual::synth` takes from the platform's libm; `state` = synth's z_0 (zh, zl) built from them by double-double arithmetic; `planted` = split_tests' z_1..z_11). The hp diff 9980cd93..1926c1c3 is `hp/src/split_tests.rs` (+29 lines), `hp/src/lib.rs` (`DotAcc` -> `DDotAcc` alias) and Python/bench files |
| command | from `hp/`: `cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1`, **RUSTFLAGS unset** (multidouble's portable backend on x86-64, as in the first run), `CARGO_BUILD_JOBS=8`, BelowNormal, venv-i1034's PATH (not needed by `--lib`). A new target directory, so a full compile (the first run: 36 min 47 s) |
| cap | 7200 s by the exact root pid of cargo (the command line checked for `cargo`), `taskkill /T /F /PID`, nothing else; estimate about 40 min (compile 37 min, tests about 1 to 2 min serially), times 3 |
| watches | alert-only copies of the #1034 watches (`mem_watch.ps1`, `commit_watch.ps1`, 30 s samples, kill nothing) into `mem.log`, `commit.log`, `alerts.log` here; the coordinator's triggers (commit over 99 GB, page file +2 GB, available under 1 GB for 5 min) are not expected to matter (the first run's test compile peaked at 8.77 GB working set, commit at most 52.4 GB) |
| the Mac's values at the same commit (from the coordinator's hc) | libm `82c612f380d2fcfc`, state `7efba3560fe23d45`, planted `78f7357f4999efc3`, fast `30acdab9851616fb`, split `a0aada9b8fe95419` (the coordinator: the fast and split values equal the Mac's at 9980cd93) |
| win2's values at 9980cd93 (first run) | fast `bfab7c94d50d60b9`, split `19412eac043921aa` |

## Readings, fixed before the run (the coordinator's, applied by `run_inputs.sh` in this order and written as `READING:` in `summary_inputs.txt`)

1. **libm differs** from the Mac's `82c612f380d2fcfc`: the platforms' libm sin/cos/tan differ and the checksums part at the inputs. Expected, not a fault.
2. **libm equal but state differs** from `7efba3560fe23d45`: the double-double integration differs across platforms. A fault, reported at once.
3. **libm, state and planted all equal but fast or split differs**: the kernel's series arithmetic differs. A fault, reported at once.
4. Not in the coordinator's list: libm and state equal but `planted` differs (the planted vectors use `exp2` and octo-double division): reported as such, not called a fault or not.
5. All five equal to the Mac's: reported as such (it would contradict the first run, since the inputs of the first run produced different checksums on this machine).
Check (a), the `target-cpu=native` compile, is not run unless the reading is one of the faults (2, 3 or 4). A run that does not print the five values, or a cap that fires, is a result. No code or threshold is changed.

## Result (written 2026-11-20 17:08 UTC)

**Reading 1: the libm hash differs from the Mac's. Expected, not a fault. The checksums part at the inputs.** `cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1` at main 1926c1c3, RUSTFLAGS unset, BelowNormal: exit 0 (cargo root pid 19668, 2011 s, 16:33:34 to 17:07:05 UTC, no cap), `Finished release-dev in 31m 56s`, **4 passed, 2 ignored (`bench_split`, `split_file`), 38 filtered out, tests 81.13 s** (`cargo_inputs.log`).

| value | win2 (x86-64, Windows) | Mac (aarch64, the coordinator's) | |
|---|---|---|---|
| libm (f64 tan, sin, cos of `synth`) | `55456d7ef2d3396a` | `82c612f380d2fcfc` | **different** |
| state (`synth`'s z_0, built from them in double-double) | `52249698dc35cab9` | `7efba3560fe23d45` | different |
| planted (z_1..z_11) | `78f7357f4999efc3` | `78f7357f4999efc3` | **equal** |
| fast series' checksum | `bfab7c94d50d60b9` | `30acdab9851616fb` | different (as at 9980cd93) |
| split series' checksum | `19412eac043921aa` | `a0aada9b8fe95419` | different (as at 9980cd93) |

Readings 2 and 3 (the faults) need libm equal, so neither applies; check (a) (the `target-cpu=native` compile) is not run.

What this shows and does not. It shows that the f64 tan, sin and cos values that `qd_residual::synth` takes from the platform's libm already differ between win2 (the Windows CRT) and the Mac, and that the state built from them differs too, so the two checksums part at the inputs, before any series arithmetic. The planted vectors (no sin, cos or tan; octo-double division and `exp2`) hash equal, which says the hash function and that arithmetic agree across the two platforms. It does **not** show that the series arithmetic is identical given identical inputs: the checksums cannot say it, since their inputs differ. A libm-free cross-platform check (dump the product's inputs on one machine, replay them on another, compare outputs) would, and I have not written it. The first run's fast and split checksums are unchanged at this commit (`bfab7c94d50d60b9`, `19412eac043921aa`).

A slip of mine: `run_inputs.sh`'s own VALUE and READING lines in `summary_inputs.txt` say "MISSING" and "NO READING" for libm, state and planted, because the script looked for a line starting `split inputs:` and cargo prints it after the test name on the same line (`test split_tests::split_inputs_hash ... split inputs: libm ...`). The correct values and reading are appended there by hand, marked as a correction; the log is untouched.

Memory (alert-only watches, 30 s samples, 65 samples): the compile's rustc peaked at 8.75 GB working set, commit at most 52.35 GB (16:54:14 UTC), minimum available 46.61 GB, `alerts.log` never written, no trigger fired; nothing else of mine ran.

Files: `cargo_inputs.log`, `summary_inputs.txt`, `exits_inputs.txt`, `mem.log`, `commit.log`, `run_inputs.sh`, `lib_inputs.sh`, the two watch scripts.
