#!/bin/bash
# #1098 on win2 (the coordinator's hc of 2026-11-26 21:24 UTC), steps 1 and 3: the fastmul7 build (wip/large-d-fastmul7 at d40a9c62) in the new worktree /d/choptuik-i1098 and venv venv-i1098, BelowNormal (started through
# cim_start.ps1), cap 57000 s on the exact root pid (crun), CARGO_BUILD_JOBS=8; fat LTO if the commit charge is at or below 45 GB at the start, otherwise CARGO_PROFILE_RELEASE_LTO=false
# CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 (the order: same bits). Then the import and Cargo.lock report. If the build ends 0 and hpkernel imports with isa avx2, step 3 starts by itself (the order's two commands side by side):
# checks_fastmul7.sh (RAW = D:/choptuik-large-d-raw-743p, a full checkout at origin/main: the stale D:/choptuik-large-d-raw has none of the inputs) and push_ladder_win.sh (cap 6 h, DONE = checks.done).
# usage: run_i1098_build.sh   (DRY=1: the pins and the plan only)
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i1098-raw-live/I1098-win2/fastmul7_build; WOUT=D:/choptuik-i1098-raw-live/I1098-win2/fastmul7_build
T=/d/choptuik-i1098-raw-live/I1098-mac-a/tools/win2
V=/c/Users/nathan/Source/venv-i1098; PY=$V/Scripts/python.exe
WT=/d/choptuik-i1098; COMMIT=d40a9c62; CAP=57000
mkdir -p $OUT
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a $OUT/build.times; log "i1098 build $*"; }
refuse() { say "STOP: $*"; echo "$*" > $OUT/build_refused.txt; touch $OUT/build.done; exit ${2:-1}; }
bad=0
for p in "setup_wt.sh 419ed9e6" "checks_fastmul7.sh 2b09481a" "push_ladder_win.sh 7a48197b" "d3214_win2.sh 57368ca6"; do set -- $p; h=$(git hash-object --no-filters $T/$1); case "$h" in $2*) ;; *) say "refuse: $1 is blob $h, not $2"; bad=1;; esac; done
[ -e $OUT/build.done ] && { echo "refuse: build.done exists"; bad=1; }
[ $bad = 0 ] || exit 2
cg=$(powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem | ForEach-Object { (\$_.TotalVirtualMemorySize - \$_.FreeVirtualMemory) / 1MB }), 1)" | tr -d '\r')
if awk -v c="$cg" 'BEGIN { exit !(c <= 45) }'; then RECIPE="fat LTO (the default): commit $cg GB is at or below 45 GB"; else export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16; RECIPE="CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16: commit $cg GB is above 45 GB"; fi
say "start: $RECIPE; CARGO_BUILD_JOBS 8, BelowNormal, cap $CAP s"
[ "${DRY:-0}" = 1 ] && { say "DRY: stops here"; exit 0; }
git -C /d/choptuik-large-d fetch origin wip/large-d-fastmul7 > $OUT/fetch.log 2>&1 || refuse "the fetch of wip/large-d-fastmul7 failed (fetch.log)"
[ -d $WT ] || git -C /d/choptuik-large-d worktree add --detach $WT $COMMIT >> $OUT/fetch.log 2>&1 || refuse "worktree add of $COMMIT failed (fetch.log)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = $COMMIT ] || refuse "the worktree $WT is not at $COMMIT"
git -C $WT status --short | head -3 >> $OUT/fetch.log
say "worktree $WT at $(git -C $WT rev-parse HEAD)"
if [ ! -e $V/Scripts/python.exe ]; then /c/Users/nathan/AppData/Local/Programs/Python/Python314/python.exe -m venv $V > $OUT/venv.log 2>&1 || refuse "the venv could not be made (venv.log)"; fi
$PY -m pip install -r $WT/requirements.txt >> $OUT/venv.log 2>&1 || refuse "pip install -r requirements.txt failed (venv.log)"
PIP_NO_CACHE_DIR=1 $PY -m pip uninstall -y multidouble > $OUT/pip_uninstall.log 2>&1
say "venv-i1098 ready (python $($PY --version 2>&1)); multidouble uninstalled first (pip uninstall exit $?; see pip_uninstall.log)"
{ echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $($V/Scripts/maturin.exe --version)"; } >> $OUT/build.times
cd $WT || exit 1
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1098 PATH=$V/Scripts:$PATH CARGO_BUILD_JOBS=8 PIP_NO_CACHE_DIR=1
s0=$(date +%s)
crun i1098_build 0 $CAP build.sh bash hp/build.sh > $OUT/build.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
say "hp/build.sh exit $rc after $w s$([ "$CAPPED" = 1 ] && echo ' (CAPPED, stopped by the exact pid)')"
touch $OUT/build.done
[ $rc = 0 ] || refuse "the build did not exit 0 (exit $rc)" 3
IM=$($PY -c "import hpkernel, multidouble; print('hpkernel', hpkernel.__file__, hpkernel.isa(), '| multidouble', multidouble.isa())" 2>&1 | tail -1)
say "import: $IM"
{ for c in multidouble multishoot multisolver; do grep -A2 "name = \"$c\"" $WT/hp/Cargo.lock | tr '\n' ' '; echo; done; } > $OUT/cargo_lock_report.txt
say "Cargo.lock: $(cat $OUT/cargo_lock_report.txt | tr '\n' '|' | cut -c1-400)"
case "$IM" in *"hpkernel "*avx2*) ;; *) refuse "hpkernel does not import with isa avx2 ($IM)" 4;; esac
say "step 3 starts: checks_fastmul7.sh (RAW D:/choptuik-large-d-raw-743p) and push_ladder_win.sh side by side"
( V=$V RAW=D:/choptuik-large-d-raw-743p bash $T/checks_fastmul7.sh > $OUT/checks_driver.out 2>&1 ) &
cq=$!
( PY=$PY bash $T/push_ladder_win.sh 6 $WOUT/checks.done /d/choptuik-i1098-raw-live/I1098-win2/fastmul7_build:I1098-win2/fastmul7_build > $OUT/push_driver.out 2>&1 ) &
wait $cq
say "checks_fastmul7.sh ended (exit_codes.txt): $(tail -n 16 $OUT/exit_codes.txt | tr '\n' ';' | cut -c1-700)"
exit 0
