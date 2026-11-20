# I1058-dh370: hp at main 7ca74dd5 (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0) in a new venv on dh370, the build log and the four stored-reference checks

Machine dh370 (Fedora 45, i7-8700, 31 GB plus 8 GB zram swap). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058

Worktree `~/Source/choptuik-large-d-1058` (detached 7ca74dd5), venv `~/Source/choptuik-large-d-1058/.venv` (Python 3.14.10, requirements.txt). The build runs beside ks_chain3b's leg 11 (#966) with the low-memory recipe
(`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`), `CARGO_BUILD_JOBS=2`, nice 19, as a user unit `i1058b` with OOMScoreAdjust 1000 (if the kernel has to kill something, it is the build, not the chain).
`mem1058.py` (unit `i1058w`) samples memory every 5 s into `mem1058.log` and raises an alert only (hc when MemAvailable is under 4096 MB); it never stops anything.
Files: `run1058.sh` (build, then the checks), `mem1058.py`, `build.log`, `build_time.txt` (`/usr/bin/time -v`), `direct_url.json`, `check_*.log`, `exits_1058.txt`, `mem1058.log`, `alerts1058.txt`.
