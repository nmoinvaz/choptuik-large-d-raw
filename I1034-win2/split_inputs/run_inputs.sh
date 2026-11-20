#!/bin/bash
# #1034 check (b), the coordinator's hc of 2026-11-20 (about 16:30 UTC): hp at main 1926c1c3 (worktree D:\choptuik-i1034b, new), from hp/:
#   cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1      (RUSTFLAGS unset, BelowNormal)
# It prints the "split inputs" line (libm, state, planted hashes) and the fast and split series' checksums. 8 jobs as in the first run. Cap 7200 s by the exact root pid of cargo (the first run's compile took 36 min 47 s,
# its tests 44 s in parallel, so about 40 min is the estimate, times 3 = 120 min). The values are compared with the Mac's below and the readings of the README applied; nothing is changed.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1034-win2/split_inputs
. $OUT/lib_inputs.sh
V=/c/Users/nathan/Source/venv-i1034
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i1034
export PATH="$V/Scripts:$PATH"
export CARGO_BUILD_JOBS=8
unset RUSTFLAGS CARGO_PROFILE_RELEASE_LTO CARGO_PROFILE_RELEASE_CODEGEN_UNITS HP_PROFILE
cd /d/choptuik-i1034b/hp || exit 1
echo "# split_inputs start $(date -u '+%F %T') UTC, hp $(git rev-parse HEAD), $(rustc --version), RUSTFLAGS='${RUSTFLAGS:-}'" >> $SUM
crun cargo_inputs 0 7200 cargo cargo test --profile release-dev --lib split_ -- --nocapture --test-threads 1 > $OUT/cargo_inputs.log 2>&1
echo "cargo_inputs: expected exit 0, got $RC capped $CAPPED $([ $RC = 0 ] && echo OK || echo MISMATCH)" >> $SUM
tr -d '\r' < $OUT/cargo_inputs.log | grep -E "^split inputs:|^fast series' checksum|^split series' checksum|^test |^test result" | cut -c1-220 >> $SUM
declare -A mac=( [libm]=82c612f380d2fcfc [state]=7efba3560fe23d45 [planted]=78f7357f4999efc3 [fast]=30acdab9851616fb [split]=a0aada9b8fe95419 )
line=$(tr -d '\r' < $OUT/cargo_inputs.log | grep -a "^split inputs:" | head -1)
g_libm=$(echo "$line" | sed -n 's/.*libm \([0-9a-f]*\),.*/\1/p'); g_state=$(echo "$line" | sed -n 's/.*state \([0-9a-f]*\),.*/\1/p'); g_planted=$(echo "$line" | sed -n 's/.*planted \([0-9a-f]*\).*/\1/p')
g_fast=$(tr -d '\r' < $OUT/cargo_inputs.log | sed -n "s/^fast series' checksum \([0-9a-f]*\).*/\1/p" | head -1)
g_split=$(tr -d '\r' < $OUT/cargo_inputs.log | sed -n "s/^split series' checksum \([0-9a-f]*\).*/\1/p" | head -1)
for k in libm state planted fast split; do v=g_$k; echo "VALUE $k: win2 ${!v:-MISSING} Mac ${mac[$k]} $([ "${!v}" = "${mac[$k]}" ] && echo EQUAL || echo DIFFERENT)" >> $SUM; done
# the readings fixed in the README, in the coordinator's order
if [ -z "$g_libm" ] || [ -z "$g_fast" ] || [ -z "$g_split" ]; then r="NO READING: a value is missing"
elif [ "$g_libm" != "${mac[libm]}" ]; then r="libm differs: expected, not a fault (the platforms' libm sin/cos/tan differ; the checksums part at the inputs)"
elif [ "$g_state" != "${mac[state]}" ]; then r="FAULT: libm equal but state differs (the double-double integration differs across platforms): report at once"
elif [ "$g_planted" = "${mac[planted]}" ] && { [ "$g_fast" != "${mac[fast]}" ] || [ "$g_split" != "${mac[split]}" ]; }; then r="FAULT: libm, state and planted equal but fast or split differs (the kernel's series arithmetic differs): report at once"
elif [ "$g_planted" != "${mac[planted]}" ]; then r="UNLISTED: libm and state equal, planted differs (not one of the three readings): report"
else r="all five equal to the Mac's"; fi
echo "READING: $r" >> $SUM
echo "# split_inputs done $(date -u '+%F %T') UTC" >> $SUM
touch $OUT/all.done
