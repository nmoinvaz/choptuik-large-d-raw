# I1098-mm5/fastmul4-build: relaxed-horizon hp kernel with form S at M 64, build and its check on the Mac mini M5 Pro (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098 (the subagent's recipe, comment 7190243331)

A release build of branch `wip/large-d-fastmul4` at a3888ffe1ac95c6589f25156926c59f555f223b3 (worktree `~/Source/choptuik-fastmul4`) into its own site
folder `~/Source/fastmul4-site`, beside the L50000 solve and the m48_1000 test. The installed hpkernel, `~/venv-314` and
`~/Source/fastmul3-site` stay as they are. Runs on this kernel later need `PYTHONPATH=~/Source/fastmul4-site` and `HP_HORIZON_RELAXED=1`.
The branch is wip/large-d-form-s at f50707a8 (form S at M 64, the slaving refinement counts from the environment, the qq acceptance
fixes) plus six commits (the relaxed horizon, its hook, multidouble by `[patch]`, `relaxed_build_check.py` with an M 64 Solver).

## Expected results (written 2026-11-26 11:06 UTC, before the build)

| item | expectation |
|---|---|
| build | `maturin build --profile release` exit 0, nice 10, `RUSTFLAGS="-C target-cpu=native"`, `CARGO_PROFILE_RELEASE_STRIP=false`, `CARGO_TARGET_DIR=$W/target`. fastmul3 took 34.3 min and 23.05 GB on this machine with two other jobs running; the tip adds an M 64 instantiation, so a bit more |
| input | `D2000_step.npz`: the file of the fastmul3 worktree, git blob 392276089bb4a24974e8359adad661a2a0bb72ba (`git hash-object --no-filters`) |
| check | `PYTHONPATH=$SITE python relaxed_build_check.py D2000_step.npz`, exit 0: an hpkernel path under `~/Source/fastmul4-site/`; `D 2000 ks 2618: ... \|F_relaxed - F_naive\| 3.62e-57 (<= 1e-50), control ... 3.69e-05 (> 1e-40) ... PASS`; and `M 64: size_s 1153, horizon block 192 values, finite True: PASS` |
| the M 64 line | has never run anywhere; reported exactly as printed |
| stop and report | a build error, a failed line, or swap use past a few GB (swap is 0.00M now) |
| the two running jobs | step times against their predictions: m48_1000's outer steps took 347 s and 452 s (h17, the second predicted from the first); L50000's qd start residual (serial, started about 10:19, predicted about 45 min) |

Files: `build.log`, `mem_samples.log` (build memory and swap every 20 s), `check.log`, `exit_codes.txt`, `times.txt`.
