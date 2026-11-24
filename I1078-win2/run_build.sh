#!/bin/bash
# #1078 on win2: hp at wip/i1078-dm (7c6177e1; kernel = main 68b563f9) in worktree D:\choptuik-i1078dm, NEW venv venv-i1078.
# pip uninstall -y multidouble (a no-op in a new venv, logged), then hp/build.sh: fat LTO (default), CARGO_BUILD_JOBS=6,
# BelowNormal (set by the launcher). Cap 57000 s (about 3x #1058's 5 h 16 min build on this machine).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-raw-i1078/I1078-win2
. $OUT/lib.sh
export PIP_NO_CACHE_DIR=1
V=/c/Users/nathan/Source/venv-i1078
[ -e $V ] && { log "not started: $V exists"; exit 9; }
BASE="/c/Users/nathan/AppData/Local/Programs/Python/Python314/python.exe"
"$BASE" -m venv $V > $OUT/venv.log 2>&1 || { log "venv failed"; exit 1; }
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1078
export PATH="$V/Scripts:$PATH"
"$V/Scripts/python.exe" -m pip install -r $OUT/requirements.txt > $OUT/pip_requirements.log 2>&1; rc=$?
log "venv made, pip install -r requirements.txt exit $rc"
[ $rc = 0 ] || exit $rc
"$V/Scripts/python.exe" -m pip uninstall -y multidouble > $OUT/pip_uninstall.log 2>&1; log "pip uninstall -y multidouble exit $?"
export CARGO_BUILD_JOBS=6
unset CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE RUSTFLAGS
cd /d/choptuik-i1078dm
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  echo "CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS LTO=fat (default) HP_PROFILE=${HP_PROFILE:-release}"
} > "$OUT/build.times"
( while [ ! -e $OUT/build.end ]; do
    echo "$(date -u '+%H:%M:%S') $(powershell -NoProfile -Command "\$o=Get-CimInstance Win32_OperatingSystem; \$r=(Get-Process rustc -ErrorAction SilentlyContinue | Measure-Object WorkingSet64 -Sum).Sum; '{0:N2} GB free, rustc {1:N2} GB' -f (\$o.FreePhysicalMemory/1MB), (\$r/1GB)" | tr -d '\r')" >> $OUT/mem.log
    sleep 120
  done ) &
crun build 0 57000 build.sh bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$RC
touch $OUT/build.end
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc capped $CAPPED" >> "$OUT/build.times"
{
  echo "## hpkernel"
  "$V/Scripts/python.exe" -c "import hpkernel, multidouble; print(hpkernel.__file__); print('isa', hpkernel.isa(), multidouble.isa(), multidouble.__file__)"
  echo "## crates in hp/Cargo.lock"
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## .pyd sha256"
  "$V/Scripts/python.exe" -c "
import glob, hashlib
for f in glob.glob(r'C:/Users/nathan/Source/venv-i1078/Lib/site-packages/hpkernel/*.pyd'):
    print(f, hashlib.sha256(open(f, 'rb').read()).hexdigest())
"
  echo "## python multidouble (direct_url)"
  cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## pip list"
  "$V/Scripts/python.exe" -m pip list 2>/dev/null
} > "$OUT/versions.txt" 2>&1
touch $OUT/build.done
exit $rc
