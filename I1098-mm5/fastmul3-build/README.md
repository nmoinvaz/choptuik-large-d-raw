# I1098-mm5/fastmul3-build: relaxed-horizon hp kernel build and its check on the Mac mini M5 Pro (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098 (the #1096 agent's recipe, comment 7188677368)

A release build of branch `wip/large-d-fastmul3` at 34ca174541cdbd0241c8c76226d073f81baa9bcd (worktree
`~/Source/choptuik-fastmul3`) into its own site folder `~/Source/fastmul3-site`, beside the L50000 solve and the kfree1000qd
release. The installed hpkernel and `~/venv-314` stay as they are. Runs on this kernel later need
`PYTHONPATH=~/Source/fastmul3-site` and `HP_HORIZON_RELAXED=1`; nothing runs on it yet.

## Expected results (written 2026-11-26 09:57 UTC, before the build)

| item | expectation |
|---|---|
| build | `maturin build --profile release` exit 0, at nice 10 with `RUSTFLAGS="-C target-cpu=native"`, `CARGO_PROFILE_RELEASE_STRIP=false`, `CARGO_TARGET_DIR=$W/target`; about 21 min and 24.8 GB (this machine's earlier release build of 1ccd32ab: 20.7 min, 24.81 GB) |
| site | the wheel extracted into `~/Source/fastmul3-site/` and `python/hpkernel/__init__.py`, `driver.py` copied over |
| input | `D2000_step.npz` from origin/main `I1088-dh610/L2000/`, git blob 392276089bb4a24974e8359adad661a2a0bb72ba (`git hash-object --no-filters`) |
| check | `PYTHONPATH=$SITE python relaxed_build_check.py D2000_step.npz`: an hpkernel path under `~/Source/fastmul3-site/`, then `D 2000 ks 2618: ... \|F_relaxed - F_naive\| 3.62e-57 (<= 1e-50), control ... 3.69e-05 (> 1e-40) ... PASS`, exit 0 (the #1096 agent's numbers from a dev-o1 build; the lanes' bits do not depend on the profile) |
| stop and report | a build error, a failed check, or swap use past a few GB (swap is 0 now) |
| the two running jobs | step times against their predictions: kfree1000qd's outer steps took 909, 897 and 915 s against a prediction of 915 s; L50000's dd step 1 is predicted to end at 10:20 UTC (6422 s from 08:33:16) |

Files: `build.log` (the build's last lines and `/usr/bin/time -l`), `mem_samples.log` (the build's resident memory and swap use, every
20 s), `check.log`, `exit_codes.txt`, `times.txt`.
