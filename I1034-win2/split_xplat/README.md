# I1034-win2/split_xplat: #1034's cross-platform test on libm-free inputs on win2 (main 7ca74dd5)

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1034 (closed at 10:33:55 UTC; this follows the results there, comments 7044472135 and 7045693325). Task: the coordinator's hc of 2026-11-20 (read 17:51 UTC). Sibling folders: `I1034-win2/` (first run at main 9980cd93) and `I1034-win2/split_inputs/` (check (b) at 1926c1c3: win2's libm hash 55456d7ef2d3396a differs from the Mac's 82c612f380d2fcfc).

## Setup (written 2026-11-20 17:52 UTC, before the run)

| | |
|---|---|
| code | a new worktree `D:/choptuik-i1034c`, detached at main **7ca74dd5** ("split_tests: the split and fast checksums on libm-free inputs (#1034)"), tree `80441d9d753b07c88613e54a418b2c5286966bb5`. Relative to 1926c1c3 (hp): `Cargo.lock`/`Cargo.toml` (#1056's pins: multidouble **5.1.0**, multishoot 4.1.0, multisolver 0.2.2), `pyproject.toml`, `src/qd_residual.rs` (+49: `det_sin`, `det_cos` by Taylor series with +, -, *, / only; `synth_det`), `src/split_tests.rs` (+34: `split_xplat`), the two side crates' manifests. The test `split_xplat` asserts det_sin and det_cos are within 1e-14 of the platform's sin and cos at the points `synth` takes and that a cut series misses that bound (control), then prints `split xplat: det vs libm <e> (control <e>); inputs <hash>, split <checksum>, fast <checksum>` |
| command | from `hp/`: `cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1`, **RUSTFLAGS unset** (multidouble's portable backend on x86-64, as in the earlier runs), `CARGO_BUILD_JOBS=8`, BelowNormal. A new target directory, so a full compile (check (b): 31 min 56 s; the crates are new versions) |
| cap | 7200 s by the exact root pid of cargo (command line checked for `cargo`), nothing else killed; estimate about 40 min, times 3 |
| watches | alert-only copies of the #1034 watches (`mem_watch.ps1`, `commit_watch.ps1`, 30 s samples, kill nothing) into `mem.log`, `commit.log`, `alerts.log` here; the coordinator's triggers (commit over 99 GB, page file +2 GB, available under 1 GB for 5 min) are not expected to matter (check (b)'s compile peaked at 8.75 GB working set, commit at most 52.35 GB) |
| the Mac's values for the libm-free line (its multidouble 5.0.0 build, which #1056 found bit-identical to 5.1.0), from the coordinator's hc | inputs `5f95f417b17d3166`, split `a1ca213203d6e285`, fast `47fd7fabd2134782`, det vs libm `4.29e-16`, control `2.11e-5` |
| to report as before | the `split inputs` line (win2 at 1926c1c3: libm 55456d7ef2d3396a, state 52249698dc35cab9, planted 78f7357f4999efc3; the Mac's: 82c612f380d2fcfc, 7efba3560fe23d45, 78f7357f4999efc3) and the libm-path checksums (win2 at 9980cd93 and 1926c1c3: fast bfab7c94d50d60b9, split 19412eac043921aa; the Mac's: 30acdab9851616fb, a0aada9b8fe95419) |

## Readings, fixed before the run (the coordinator's, applied by `run_xplat.sh` in this order and written as `READING:` in `summary_xplat.txt`)

1. **inputs differ** from `5f95f417b17d3166`: the libm-free construction is not platform-independent, a fault in the coordinator's test; reported.
2. **inputs equal and split and fast equal** the Mac's: the series' arithmetic has the same bits on win2 and the Mac; #1034's checksum mismatch was the libm inputs alone.
3. **inputs equal but split or fast differs**: the arithmetic differs across platforms. A fault, reported at once; check (a), the `target-cpu=native` compile, then becomes useful.
The `det vs libm` and `control` figures are information (the first depends on this platform's libm, which differs from the Mac's); a run that does not print the `split xplat` line, a failed assertion of the test, or a cap that fires is a result and is reported as such. The log is parsed without an anchor at the line start (the previous run's anchored parse missed lines that cargo prints after the test name; the parse was tested on a synthetic log before this run). Nothing of the code is changed.

## Result (written 2026-11-20 18:25 UTC)

**Reading 2: the inputs hash, the split checksum and the fast checksum all equal the Mac's. The series' arithmetic has the same bits on win2 (x86-64, Windows) and the Mac (aarch64). #1034's checksum mismatch was the libm inputs alone.** `cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1` at main 7ca74dd5, RUSTFLAGS unset, BelowNormal, 8 jobs: exit 0 (cargo root pid 33252, 1895 s, 17:53:01 to 18:24:35 UTC, no cap); `Finished release-dev in 30m 04s` (multidouble v5.1.0, multishoot v4.1.0, multisolver v0.2.2 downloaded and compiled); **5 passed, 2 ignored (`bench_split`, `split_file`), 38 filtered out, tests 89.07 s** (`cargo_xplat.log`).

The `split xplat` line, win2 against the Mac (its multidouble 5.0.0 build, bit-identical to 5.1.0 per #1056):

| value | win2 | Mac | |
|---|---|---|---|
| inputs hash (det_sin, det_cos and \`synth_det\`'s z_0) | `5f95f417b17d3166` | `5f95f417b17d3166` | **equal** |
| split checksum | `a1ca213203d6e285` | `a1ca213203d6e285` | **equal** |
| fast checksum | `47fd7fabd2134782` | `47fd7fabd2134782` | **equal** |
| det vs libm (worst \|det_sin - sin\|, \|det_cos - cos\| at synth's points) | 4.29e-16 | 4.29e-16 | equal as printed (information) |
| control (the cut series' distance from libm) | 2.11e-5 | 2.11e-5 | equal as printed (information) |

The `split inputs` line and the libm-path checksums, as before (all unchanged from win2's runs at 9980cd93 and 1926c1c3, so the move to multidouble 5.1.0, multishoot 4.1.0, multisolver 0.2.2 changed no bit of them on win2):

| value | win2 at 7ca74dd5 | Mac | |
|---|---|---|---|
| libm hash | `55456d7ef2d3396a` | `82c612f380d2fcfc` | different |
| state hash | `52249698dc35cab9` | `7efba3560fe23d45` | different |
| planted hash | `78f7357f4999efc3` | `78f7357f4999efc3` | equal |
| libm-path fast checksum | `bfab7c94d50d60b9` | `30acdab9851616fb` | different |
| libm-path split checksum | `19412eac043921aa` | `a0aada9b8fe95419` | different |

What this shows and does not. On inputs built from only +, -, * and / (det_sin and det_cos), win2 and the Mac produce the same inputs hash and the same bits of the split series (the split-1 form) and of the fast series (series_split 2, fastmul) of the synthetic context: the series' octo-double arithmetic and the fast product give the same bits on x86-64 Windows (portable backend, no RUSTFLAGS) and aarch64, and the earlier mismatch came from the libm inputs. It is one synthetic context (qd_residual's \`synth_det\`, 12 orders), one build flag set (RUSTFLAGS unset, so not the AVX2 backend; check (a) was not run, and the reading does not call for it), and two machines. The first three readings of the coordinator's list: 1 (inputs differ) did not occur and 3 (inputs equal, checksums differ) did not occur.

Memory (alert-only watches, 30 s samples, 66 samples): the compile's rustc peaked at 8.68 GB working set, commit at most 51.99 GB (18:14:11 UTC), minimum available 46.46 GB, \`alerts.log\` never written, no trigger. Beside it: win2b's #1025 ell_refine solves.

The log was parsed without a line-start anchor this time and the parse was tested on a synthetic log first; all VALUE lines of \`summary_xplat.txt\` read correctly.

Files: \`cargo_xplat.log\`, \`summary_xplat.txt\`, \`exits_xplat.txt\`, \`mem.log\`, \`commit.log\`, \`run_xplat.sh\`, \`lib_xplat.sh\`, the two watch scripts.
