#!/bin/bash
# I935 win2: build hp on multidouble 4.8.2 into venv-md482 (worktree D:\choptuik-i935).
set -u
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I935-win2
V=/c/Users/nathan/Source/venv-md482
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-md482
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
cd /d/choptuik-i935
{
  echo "start $(date -u '+%Y-%m-%d %H:%M:%S UTC') commit $(git rev-parse HEAD)"
  echo "rustc $(rustc --version) | cargo $(cargo --version) | maturin $(maturin --version) | python $("$V/Scripts/python.exe" --version)"
} > "$OUT/build.times"
bash hp/build.sh > "$OUT/build.log" 2>&1
rc=$?
echo "end $(date -u '+%Y-%m-%d %H:%M:%S UTC') exit $rc" >> "$OUT/build.times"
touch "$OUT/build.done"
exit $rc
