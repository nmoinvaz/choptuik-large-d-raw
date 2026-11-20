#!/bin/bash
# I1034 step 1: hp at main 9980cd93 (PR #1041, #1045, #1046 and #1047 merged; worktree D:\choptuik-i1034) into venv-i1034: hp/build.sh, fat LTO (the default profile), 8 jobs, as #1031's build.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1034-win2
. $OUT/lib1034.sh
V=/c/Users/nathan/Source/venv-i1034
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1034
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
unset CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE
cd /d/choptuik-i1034
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  echo "CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS LTO=fat (default) HP_PROFILE=${HP_PROFILE:-release}"
} > "$OUT/build.times"
# cap: three times #1031's 4 h 21 min (261 min) = 783 min = 46980 s, by the exact pid of this bash, after checking its command line
crun build 0 46980 build.sh bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$RC
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc capped $CAPPED" >> "$OUT/build.times"
{
  echo "## hpkernel"
  "$V/Scripts/python.exe" -c "import hpkernel, multidouble, os; print(hpkernel.__file__); print('isa', hpkernel.isa(), multidouble.isa(), multidouble.__file__)"
  echo "## crates in hp/Cargo.lock"
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## crate path strings in the .pyd"
  "$V/Scripts/python.exe" -c "
import re, glob, hashlib
for f in glob.glob(r'C:/Users/nathan/Source/venv-i1034/Lib/site-packages/hpkernel/*.pyd'):
    b = open(f, 'rb').read()
    print(f, hashlib.sha256(b).hexdigest(), sorted({m.decode() for m in re.findall(rb'(?:multidouble|multishoot|multisolver)[-/][0-9][0-9A-Za-z.\-]*', b)})[:12])
"
  echo "## python multidouble (direct_url)"
  cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## pip list"
  "$V/Scripts/python.exe" -m pip list 2>/dev/null | grep -i -E 'numpy|scipy|mpmath|sympy|flint|maturin|hpkernel|multidouble'
} > "$OUT/versions.txt" 2>&1
exit $rc
