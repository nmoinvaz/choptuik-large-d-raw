#!/bin/bash
# #1034's cross-platform test on libm-free inputs, the coordinator's hc of 2026-11-20 (read 17:51 UTC): hp at main 7ca74dd5 (worktree D:\choptuik-i1034c, new; main now pins multidouble 5.1.0), from hp/:
#   cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1      (RUSTFLAGS unset, BelowNormal)
# 8 jobs as in the two earlier runs. Cap 7200 s by the exact root pid of cargo (the check (b) compile took 31 min 56 s, so the estimate is about 40 min with the new crate versions to fetch, times 3 = 120 min).
# It prints "split xplat: det vs libm .. (control ..); inputs .., split .., fast .." and, as before, "split inputs: libm .., state .., planted .." and the two libm-path checksums. Lines are read from the log WITHOUT an
# anchor at the line start (cargo prints a test's output after "test <name> ... " on the same line, which broke the anchored parse of the previous run). The readings of the README are applied below; nothing is changed.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1034-win2/split_xplat
. $OUT/lib_xplat.sh
V=/c/Users/nathan/Source/venv-i1034
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1034
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
unset RUSTFLAGS CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE
cd /d/choptuik-i1034c/hp || exit 1
echo "# split_xplat start $(date -u '+%F %T') UTC, hp $(git rev-parse HEAD), $(rustc --version), RUSTFLAGS='${RUSTFLAGS:-}'" >> $SUM
crun cargo_xplat 0 7200 cargo cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1 > $OUT/cargo_xplat.log 2>&1
echo "cargo_xplat: expected exit 0, got $RC capped $CAPPED $([ $RC = 0 ] && echo OK || echo MISMATCH)" >> $SUM
tr -d '\r' < $OUT/cargo_xplat.log | grep -aE "split xplat:|split inputs:|fast series' checksum|split series' checksum|^test |test result|panicked|FAILED" | cut -c1-240 >> $SUM
L=$(tr -d '\r' < $OUT/cargo_xplat.log)
xl=$(echo "$L" | grep -a "split xplat:" | head -1)
x_det=$(echo "$xl" | sed -n 's/.*det vs libm \([^ ]*\) (control.*/\1/p'); x_ctrl=$(echo "$xl" | sed -n 's/.*(control \([^)]*\)).*/\1/p')
x_inputs=$(echo "$xl" | sed -n 's/.*; inputs \([0-9a-f]*\), split.*/\1/p'); x_split=$(echo "$xl" | sed -n 's/.*, split \([0-9a-f]*\), fast.*/\1/p'); x_fast=$(echo "$xl" | sed -n 's/.*, fast \([0-9a-f]*\).*/\1/p')
il=$(echo "$L" | grep -a "split inputs:" | head -1)
i_libm=$(echo "$il" | sed -n 's/.*libm \([0-9a-f]*\),.*/\1/p'); i_state=$(echo "$il" | sed -n 's/.*state \([0-9a-f]*\),.*/\1/p'); i_planted=$(echo "$il" | sed -n 's/.*planted \([0-9a-f]*\).*/\1/p')
c_fast=$(echo "$L" | sed -n "s/.*fast series' checksum \([0-9a-f]*\).*/\1/p" | head -1); c_split=$(echo "$L" | sed -n "s/.*split series' checksum \([0-9a-f]*\).*/\1/p" | head -1)
v() { echo "VALUE $1: win2 ${2:-MISSING} | Mac ${3:-(none stated)} | $4" >> $SUM; }
eq() { [ -n "$1" ] && [ "$1" = "$2" ] && echo EQUAL || echo DIFFERENT; }
v "xplat inputs" "$x_inputs" 5f95f417b17d3166 "$(eq "$x_inputs" 5f95f417b17d3166)"
v "xplat split" "$x_split" a1ca213203d6e285 "$(eq "$x_split" a1ca213203d6e285)"
v "xplat fast" "$x_fast" 47fd7fabd2134782 "$(eq "$x_fast" 47fd7fabd2134782)"
v "xplat det vs libm" "$x_det" 4.29e-16 "information (depends on the platform's libm)"
v "xplat control" "$x_ctrl" 2.11e-5 "information"
v "inputs libm" "$i_libm" 82c612f380d2fcfc "$(eq "$i_libm" 82c612f380d2fcfc) (win2 at 1926c1c3: 55456d7ef2d3396a)"
v "inputs state" "$i_state" 7efba3560fe23d45 "$(eq "$i_state" 7efba3560fe23d45) (win2 at 1926c1c3: 52249698dc35cab9)"
v "inputs planted" "$i_planted" 78f7357f4999efc3 "$(eq "$i_planted" 78f7357f4999efc3) (win2 at 1926c1c3: 78f7357f4999efc3)"
v "libm-path fast checksum" "$c_fast" 30acdab9851616fb "$(eq "$c_fast" 30acdab9851616fb) (win2 at 9980cd93 and 1926c1c3: bfab7c94d50d60b9)"
v "libm-path split checksum" "$c_split" a0aada9b8fe95419 "$(eq "$c_split" a0aada9b8fe95419) (win2 at 9980cd93 and 1926c1c3: 19412eac043921aa)"
if [ -z "$x_inputs" ] || [ -z "$x_split" ] || [ -z "$x_fast" ]; then r="NO READING: a split xplat value is missing"
elif [ "$x_inputs" != 5f95f417b17d3166 ]; then r="READING 1: inputs differ: the libm-free construction is not platform-independent, a fault in the test: report it"
elif [ "$x_split" = a1ca213203d6e285 ] && [ "$x_fast" = 47fd7fabd2134782 ]; then r="READING 2: inputs, split and fast all equal the Mac's: the series' arithmetic has the same bits on win2 and the Mac; the checksum mismatch was the libm inputs alone"
else r="READING 3: inputs equal but split or fast differs: the arithmetic differs across platforms. A FAULT: report at once; check (a), target-cpu=native, becomes useful"; fi
echo "READING: $r" >> $SUM
echo "# split_xplat done $(date -u '+%F %T') UTC" >> $SUM
touch $OUT/all.done
