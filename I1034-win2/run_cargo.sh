#!/bin/bash
# I1034 step 2: the Rust tests on win2 (worktree D:\choptuik-i1034), the commands of #1034 comment 7019891857 as written (no RUSTFLAGS, so multidouble's portable backend on x86-64):
#   cargo test --profile release-dev --lib split_ -- --nocapture
#   cargo test --profile release-dev --lib fastmul_planted -- --nocapture
# 8 jobs, BelowNormal. The first compiles the test binary (peak memory unknown on win2); caps by exact pid: 12 h for the first (compile + run; a guess of 4 h for the estimate, times 3), 1 h for the second (same binary).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1034-win2
. $OUT/lib1034.sh
V=/c/Users/nathan/Source/venv-i1034
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1034
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
unset RUSTFLAGS CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE
cd /d/choptuik-i1034/hp || exit 1
echo "# cargo tests (step 2) start $(date -u '+%F %T') UTC, hp $(git rev-parse HEAD), $(rustc --version), RUSTFLAGS='${RUSTFLAGS:-}'" >> $SUM
crun cargo_split 0 43200 cargo cargo test --profile release-dev --lib split_ -- --nocapture > $OUT/cargo_split.log 2>&1
r1=$RC
echo "cargo_split: expected exit 0, got $r1 capped $CAPPED $([ $r1 = 0 ] && echo OK || echo MISMATCH)" >> $SUM
crun cargo_fastmul 0 3600 cargo cargo test --profile release-dev --lib fastmul_planted -- --nocapture > $OUT/cargo_fastmul.log 2>&1
r2=$RC
echo "cargo_fastmul: expected exit 0, got $r2 capped $CAPPED $([ $r2 = 0 ] && echo OK || echo MISMATCH)" >> $SUM
for want in "fast series' checksum 30acdab9851616fb" "split series' checksum a0aada9b8fe95419"; do
  got=$(grep -h "${want%% [0-9a-f]*}" $OUT/cargo_split.log | tr -d '\r' | head -2 | tr '\n' ';')
  if grep -q "$want" $OUT/cargo_split.log; then echo "checksum: '$want' FOUND" >> $SUM; else echo "checksum: '$want' NOT FOUND; log lines: $got" >> $SUM; fi
done
grep -h 'test result\|^test ' $OUT/cargo_split.log $OUT/cargo_fastmul.log | tr -d '\r' | cut -c1-200 >> $SUM
echo "# cargo tests done $(date -u '+%F %T') UTC" >> $SUM
touch $OUT/cargo.done
