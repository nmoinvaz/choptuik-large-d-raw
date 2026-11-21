#!/bin/bash
# #1058 on win2 (the coordinator's hc of 2026-11-20 18:04 UTC, Nathan: "update all machines to latest multi libs"): hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0; Python package 8c4360ac) in a NEW worktree D:\choptuik-i1058b
# and a NEW venv venv-i1058b. Step 1 of the issue: PIP_NO_CACHE_DIR=1 pip uninstall -y multidouble (a no-op in a new venv, logged), then hp/build.sh: fat LTO (the default profile), CARGO_BUILD_JOBS=8, BelowNormal. Log the time, the peak memory
# (the alert-only watches' mem.log and commit.log) and pip's direct_url, which must name 8c4360ac. Cap: three times this machine's own fat build of 18327 s (5 h 5 min at 9980cd93, beside other jobs): 54981 s.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1058-win2
. $OUT/lib1058.sh
export PIP_NO_CACHE_DIR=1
V=/c/Users/nathan/Source/venv-i1058b
[ -e $V ] && { log "not started: $V exists"; exit 9; }
BASE="/c/Users/nathan/AppData/Local/Programs/Python/Python314/python.exe"
"$BASE" -m venv $V > $OUT/venv.log 2>&1 || { log "venv failed"; exit 1; }
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1058b
export PATH="$V/Scripts:$PATH"
"$V/Scripts/python.exe" -m pip install -r $OUT/requirements.txt > $OUT/pip_requirements.log 2>&1; rc=$?
log "venv made, pip install -r requirements.txt exit $rc"
[ $rc = 0 ] || exit $rc
"$V/Scripts/python.exe" -m pip uninstall -y multidouble > $OUT/pip_uninstall.log 2>&1; log "pip uninstall -y multidouble exit $? ($(tail -n 1 $OUT/pip_uninstall.log | cut -c1-80))"
export CARGO_BUILD_JOBS=8
unset CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE RUSTFLAGS
cd /d/choptuik-i1058b
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  echo "CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS LTO=fat (default) HP_PROFILE=${HP_PROFILE:-release} PIP_NO_CACHE_DIR=$PIP_NO_CACHE_DIR"
} > "$OUT/build.times"
crun build 0 54981 build.sh bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$RC
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc capped $CAPPED (the exit is from crun's wait on the build's bash; the build is complete only if hpkernel imports below)" >> "$OUT/build.times"
{
  echo "## hpkernel"
  "$V/Scripts/python.exe" -c "import hpkernel, multidouble, os; print(hpkernel.__file__); print('isa', hpkernel.isa(), multidouble.isa(), multidouble.__file__)"
  echo "## crates in hp/Cargo.lock"
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## crate path strings in the .pyd"
  "$V/Scripts/python.exe" -c "
import re, glob, hashlib
for f in glob.glob(r'C:/Users/nathan/Source/venv-i1058b/Lib/site-packages/hpkernel/*.pyd'):
    b = open(f, 'rb').read()
    print(f, hashlib.sha256(b).hexdigest(), sorted({m.decode() for m in re.findall(rb'(?:multidouble|multishoot|multisolver)[-/][0-9][0-9A-Za-z.\-]*', b)})[:12])
"
  echo "## python multidouble (direct_url)"
  cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## pip list"
  "$V/Scripts/python.exe" -m pip list 2>/dev/null | grep -i -E 'numpy|scipy|mpmath|sympy|flint|maturin|hpkernel|multidouble'
} > "$OUT/versions.txt" 2>&1
exit $rc
