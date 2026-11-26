#!/bin/bash
# win2: release build of hp from origin/wip/large-d-form-s (the head at build time) in the worktree D:\choptuik-formsq, venv C:\Users\nathan\Source\venv-formsq
# (the coordinator's order of 2026-11-26 ~00:59 UTC, item (1)): multidouble's Python package uninstalled first, then hp/build.sh (fat LTO, one codegen unit, target-cpu=native),
# BelowNormal (started through kc71_leap/cim_start.ps1). The build needs about 37 GB of commit headroom (#1078: 36.1 GB rustc peak): the driver waits until
# TotalVirtualMemorySize - FreeVirtualMemory leaves GATE_GB (38) free, checks every 60 s, and logs it. usage: run_formsq_build.sh   (NOGATE=1 skips the wait)
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/hp_form_s_build
WT=/d/choptuik-formsq
V=/c/Users/nathan/Source/venv-formsq
GATE_GB=${GATE_GB:-38}
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-formsq
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=${CARGO_BUILD_JOBS:-6}
say() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" >> "$OUT/build.times"; }
headroom() { powershell -NoProfile -Command '$o=Get-CimInstance Win32_OperatingSystem; [math]::Round(($o.FreeVirtualMemory)/1MB,1)' | tr -d '\r'; }
[ -e "$OUT/build.done" ] && { say "refuse: build.done exists"; exit 2; }
say "driver started: gate $GATE_GB GB of commit headroom, CARGO_BUILD_JOBS $CARGO_BUILD_JOBS"
if [ "${NOGATE:-0}" != 1 ]; then
  n=0
  while :; do
    h=$(headroom)
    ok=$(awk -v h="$h" -v g="$GATE_GB" 'BEGIN{print (h>=g)?1:0}')
    [ "$ok" = 1 ] && { say "gate open: commit headroom $h GB >= $GATE_GB GB"; break; }
    [ $((n % 10)) = 0 ] && say "gate closed: commit headroom $h GB < $GATE_GB GB (waiting)"
    [ -e "$OUT/build.cancel" ] && { say "build.cancel found: the driver stops without building"; touch "$OUT/build.done"; exit 3; }
    n=$((n + 1)); sleep 60
  done
fi
# the branch's head at build time
git -C /d/choptuik-large-d fetch origin > "$OUT/fetch.log" 2>&1
H=$(git -C /d/choptuik-large-d rev-parse origin/wip/large-d-form-s)
git -C "$WT" checkout --detach "$H" > "$OUT/checkout.log" 2>&1 || { say "refuse: checkout of $H failed"; touch "$OUT/build.done"; exit 4; }
cd "$WT" || exit 1
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD) (origin/wip/large-d-form-s)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  git status --short | head -5
} >> "$OUT/build.times"
"$V/Scripts/python.exe" -m pip uninstall -y multidouble hpkernel > "$OUT/pip_uninstall.log" 2>&1
say "multidouble's Python package uninstalled first (pip uninstall exit $?; see pip_uninstall.log)"
"$V/Scripts/python.exe" -m pip list 2>/dev/null | grep -iE 'multidouble|hpkernel' >> "$OUT/pip_uninstall.log" || echo "(neither multidouble nor hpkernel is installed now)" >> "$OUT/pip_uninstall.log"
bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$?
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc" >> "$OUT/build.times"
touch "$OUT/build.done"
exit $rc
