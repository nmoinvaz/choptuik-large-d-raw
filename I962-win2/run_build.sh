#!/bin/bash
# I962 win2: build hp at main 40f4b4a5 into venv-i962 (worktree D:\choptuik-i962), the low-memory recipe.
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I962-win2
V=/c/Users/nathan/Source/venv-i962
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i962
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=4
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
cd /d/choptuik-i962
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
  echo "CARGO_BUILD_JOBS=$CARGO_BUILD_JOBS LTO=$CARGO_PROFILE_RELEASE_LTO CODEGEN_UNITS=$CARGO_PROFILE_RELEASE_CODEGEN_UNITS"
} > "$OUT/build.times"
bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$?
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc" >> "$OUT/build.times"
{
  echo "## hpkernel"
  "$V/Scripts/python.exe" -c "import hpkernel, multidouble, os; print(hpkernel.__file__); print('isa', hpkernel.isa(), multidouble.isa(), multidouble.__file__)"
  echo "## crates in hp/Cargo.lock"
  grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## crate strings in the .so"
  strings -n 8 "$V"/Lib/site-packages/hpkernel/*.pyd | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -12
  echo "## python multidouble (direct_url)"
  cat "$V"/Lib/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## pip list"
  "$V/Scripts/python.exe" -m pip list 2>/dev/null | grep -i -E 'numpy|scipy|mpmath|sympy|flint|maturin|hpkernel|multidouble'
} > "$OUT/versions.txt" 2>&1
touch "$OUT/build.done"
exit $rc
