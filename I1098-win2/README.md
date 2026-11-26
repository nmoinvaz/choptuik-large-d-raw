# I1098-win2: fastmul7 on win2 and its ladder jobs (#1098)

Machine win2 (Windows 11, Core Ultra 7 265K, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098 (the record: Delta_inf to 20 digits from a ladder of full direct solves, D 250 to 4000). Written 2026-11-26 21:26 UTC, **before step 1 (the build) starts**. This is a third job beside #1025's k_c 135 scan (`I1025-win2/kc135_d23/`) and #1101's kappa runs (`I1101-win2/`), which keep priority.

## Order (coordinator t5, hc 2026-11-26 21:24 UTC), verbatim
"a third job on win2, #1098, for the spare threads (you use about 6 of 20). #1025's k_c 135 scan and #1101 keep priority. Raw folder I1098-win2/, README first line "# I1098-win2: fastmul7 on win2 and its ladder jobs (#1098)". Scripts: raw 04f8e8066, I1098-mac-a/tools/win2/: setup_wt.sh 419ed9e6, checks_fastmul7.sh 2b09481a, push_ladder_win.sh 7a48197b, d3214_win2.sh 57368ca6. Verify each blob first.

1. BUILD fastmul7 into a new venv; leave the installed hpkernel and other venvs alone. Git Bash:
git -C /d/choptuik-large-d fetch origin wip/large-d-fastmul7
git -C /d/choptuik-large-d worktree add --detach /d/choptuik-i1098 d40a9c62
/c/Users/nathan/AppData/Local/Programs/Python/Python314/python.exe -m venv /c/Users/nathan/Source/venv-i1098
/c/Users/nathan/Source/venv-i1098/Scripts/python.exe -m pip install -r /d/choptuik-i1098/requirements.txt
PIP_NO_CACHE_DIR=1 /c/Users/nathan/Source/venv-i1098/Scripts/python.exe -m pip uninstall -y multidouble
cd /d/choptuik-i1098 && VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1098 PATH=/c/Users/nathan/Source/venv-i1098/Scripts:$PATH CARGO_BUILD_JOBS=8 PIP_NO_CACHE_DIR=1 bash hp/build.sh
Run it BelowNormal under your crun, cap 57000 s, with the alert-only memory and commit watches. Use fat LTO (the default) if commit is at or below 45 GB at the start. Otherwise add CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16, which gives the same bits. Report: hpkernel imports from venv-i1098 with isa avx2; Cargo.lock has multidouble 5.1.0 from git 09f1118b, multishoot 4.1.0 and multisolver 0.2.2.

2. RAW WORKTREES: fetch the raw clone, then bash D:/choptuik-large-d-raw/I1098-mac-a/tools/win2/setup_wt.sh (it makes /d/choptuik-i1098-raw-live for runs and /d/choptuik-i1098-raw-push for pushes; nothing pulls the live one while a run writes there).

3. CHECKS (about 1 h), the two commands side by side:
V=/c/Users/nathan/Source/venv-i1098 RAW=D:/choptuik-large-d-raw bash /d/choptuik-i1098-raw-live/I1098-mac-a/tools/win2/checks_fastmul7.sh
PY=/c/Users/nathan/Source/venv-i1098/Scripts/python.exe bash /d/choptuik-i1098-raw-live/I1098-mac-a/tools/win2/push_ladder_win.sh 6 D:/choptuik-i1098-raw-live/I1098-win2/fastmul7_build/checks.done /d/choptuik-i1098-raw-live/I1098-win2/fastmul7_build:I1098-win2/fastmul7_build
Expected (exit 0 each unless noted): relaxed_build_check passes its own bar (fastmul6 read 4.53e-57, control 3.69e-05); recip_check D 300 and D 1000 step-plan change 0, controls 5.06e-37 and 1.72e-36; dmat_check 5.21e-6 and 2.72e-6, controls 1.0; taylor_mp_check 1.1e-124, control 2.36e-31; horizon_mp_check at a 8 ks 1600 9.74e-129, controls 4.62e-28 and 1.7e-60; highm_check ref against T81 72 of 72; scaled 22 of 22 with its control firing; jets 28 of 28 (only M 32's input differs, by numpy resampling); jets --mutate=kappa exit 1. ref against T45-win is information only. Report any difference with its size and place, and loosen no bar. Any failed check is a stop.

4. FIRST LADDER JOB, after every check passes: D 3214's M 32 stages, about 12-14 h at 12 threads.
THREADS=12 bash /d/choptuik-i1098-raw-live/I1098-mac-a/tools/win2/d3214_win2.sh
PY=/c/Users/nathan/Source/venv-i1098/Scripts/python.exe bash /d/choptuik-i1098-raw-live/I1098-mac-a/tools/win2/push_ladder_win.sh 30 D:/choptuik-i1098-raw-live/I1098-win2/ladder/D3214/job.done /d/choptuik-i1098-raw-live/I1098-win2/ladder/D3214:I1098-win2/ladder/D3214
The job is chord-free, kc 250, KSBAR 1e-70, a 8.03, start ks 4838, STOP_AFTER=rls13. It waits (a fetch every 10 min, at most 8 h) for D 1549's h13 to appear in raw (dh170, expected about 03:00-04:30 UTC), then writes and blob-checks its two fit states. It exits 4 before any stage if form_s or hpkernel fails to import. The pilot is the jump plus the ks gate. Report the jump's time, the gated ks and h5 outer 0's time, then leave it running.
Stop rules: a qq inner solve that does not converge (a floor at the first outer step right after an M resample is only logged), a line search that fails at every trial, an outer step 3x its harmonic's first, or any exit code other than 0. Push the README before step 1. Report at each step's end."

## Registered before the run: what I read, and where I deviate (each stated here, none changes a bar)
- **Script blobs** (raw 04f8e8066, `git rev-parse` of the committed blobs): setup_wt.sh 419ed9e6, checks_fastmul7.sh 2b09481a, push_ladder_win.sh 7a48197b, d3214_win2.sh 57368ca6: all four as the order names them. I read all four before running any.
- **`D:/choptuik-large-d-raw` is stale:** it is the old clone (HEAD b2f965f83 of 10 Nov, 148 modified files, no `I1098-mac-a`, no `I1088-dh610`). The scripts read their inputs from RAW at origin/main. `setup_wt.sh` only fetches that repository and adds worktrees (all my raw worktrees share its .git), so I run it as given (script file from my current worktree, blob-checked). **For `checks_fastmul7.sh` I give `RAW=D:/choptuik-large-d-raw-743p`**, my push worktree, a full checkout at origin/main which holds every input (`I1088-dh610/L2000/lastnode_D2000.0000_step.npz` 39227608, `I1098-dh610/budget300_src/D300_full_base.npz` 569779b2, `I1098-dh610/fix/D1000_base/release_ls_h13_D1000.0000.npz` 57af5b81, `I1098-mm5/ladder/D300u/tail/release_ls_h21_D300.0000.npz` 3f609c95, `T81/ref_main.json`, `T81/scaled_main.json`, `T45-win/.../ref_new.json`, `anm-mac/jets_inputs/jets_inputs.json`); the script blob-checks the four states itself. If I pull that worktree while the checks run, only added or updated files change.
- **Build recipe:** commit is 92.6 of 103.0 GB at 21:26 UTC (the scan, R0 and the kernel pools), above the order's 45 GB: so **`CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16`** is added (same bits, the order says; on win2 a thin build still held up to 32 GB working set in #962). The driver logs the commit at its start and applies the rule by the number. BelowNormal, `crun` cap 57,000 s, `CARGO_BUILD_JOBS=8`. The alert-only sampler `commit_watch.ps1` (nothing is killed) logs commit and the build's memory every 30 s.
- **Disk:** D: has 18 GB free (92% used); the build writes its target under `D:\choptuik-i1098\hp\target`; C: has 188 GB. The stale `D:\choptuik-formsq\hp\target` holds 0.17 GB.
- **Load:** the scan uses 4 threads (Normal), R0 6 (then R1 and R2 12), the build 8 (BelowNormal), the ladder job 12 later: above 20 at times. The build and the ladder run BelowNormal so the Normal jobs keep priority; I tell the coordinator if the scan's evaluations slow by more than 1.5x.

## Files (this folder)
`README.md`; `fastmul7_build/` (build log, times, sampler log, driver; later the checks' logs and `exit_codes.txt`); `ladder/` (later: D 3214's inputs and outputs). Raw output goes only into the live worktree's copy of this folder and is pushed from the push worktree by `push_ladder_win.sh`.

## Status
- 2026-11-26 21:26 UTC: README written; step 1 starts after this README is pushed, then step 2 (`setup_wt.sh`) makes the worktrees from origin/main (which then holds this README).
