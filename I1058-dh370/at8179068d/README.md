# I1058-dh370/at8179068d: hp at main 8179068d in a second new venv on dh370 (the #1058 target moved from 7ca74dd5), build log and the four stored-reference checks

Machine dh370. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058 (comment 7049678470). Worktree `~/Source/choptuik-large-d-1058b` (detached 8179068d), venv `.venv` at its root.
Same recipe as the 7ca74dd5 build one folder up (`I1058-dh370/`): low-memory (`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`), `CARGO_BUILD_JOBS=2`, nice 19, user unit `i1058c` with OOMScoreAdjust 1000, beside ks_chain3b's leg 11 (#966); `mem1058b.py` (unit `i1058d`) is the alert-only sampler.
Files: `run1058b.sh` and `mem1058b.py` are one folder up, `build.log`, `build_time.txt`, `direct_url.json`, `check_*.log`, `exits_1058.txt`, `mem1058.log`.
