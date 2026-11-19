#!/bin/bash
# I1031 win2: hp at origin/chore/multidouble-4.9.1 (6266a213) into venv-md491 (worktree D:\choptuik-i1031): hp/build.sh, fat LTO (the default profile), 8 jobs.
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1031-win2
V=/c/Users/nathan/Source/venv-md491
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md491
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
unset CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE       # the fat recipe: nothing overrides Cargo.toml's release profile
cd /d/choptuik-i1031
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  echo "CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS LTO=fat (default) HP_PROFILE=${HP_PROFILE:-release}"
} > "$OUT/build.times"
bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$?
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc" >> "$OUT/build.times"
{
  echo "## hpkernel"
  "$V/Scripts/python.exe" -c "import hpkernel, multidouble, os; print(hpkernel.__file__); print('isa', hpkernel.isa(), multidouble.isa(), multidouble.__file__)"
  echo "## crates in hp/Cargo.lock"
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## crate path strings in the .pyd (Git Bash has no strings)"
  "$V/Scripts/python.exe" -c "
import re, glob
for f in glob.glob(r'C:/Users/nathan/Source/venv-md491/Lib/site-packages/hpkernel/*.pyd'):
    b = open(f, 'rb').read()
    print(f, sorted({m.decode() for m in re.findall(rb'(?:multidouble|multishoot|multisolver)[-/][0-9][0-9A-Za-z.\-]*', b)})[:12])
"
  echo "## python multidouble (direct_url)"
  cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## pip list"
  "$V/Scripts/python.exe" -m pip list 2>/dev/null | grep -i -E 'numpy|scipy|mpmath|sympy|flint|maturin|hpkernel|multidouble'
} > "$OUT/versions.txt" 2>&1
exit $rc
