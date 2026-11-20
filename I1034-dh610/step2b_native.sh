#!/bin/bash
# #1034 step 2, added: the split_ tests again with RUSTFLAGS='-C target-cpu=native' (multidouble's Avx2 backend), because step 2 as ordered (no RUSTFLAGS) ran on the portable Sse2 backend
# and its two checksums differ from the Mac's. Same commit (9980cd93), same worktree; est. 30 min (build 25 + tests 3), cap 1.5 h by timeout on the exact pid; nice 10, 4 jobs.
. "$(dirname "$0")/common1034.sh"
S=$OUT/summary_1034.txt
cd $WT/hp || exit 1
[ "$(git rev-parse HEAD | cut -c1-8)" = 9980cd93 ] || { echo "WT is not at 9980cd93"; exit 1; }
. $VENV/bin/activate
export CARGO_BUILD_JOBS=4 OMP_NUM_THREADS=1
{ echo "# $(stamp) UTC cmd: RUSTFLAGS='-C target-cpu=native' cargo test --profile release-dev --lib split_ -- --nocapture"; } > $OUT/step2b_split_native.log
s=$(date +%s)
RUSTFLAGS='-C target-cpu=native' nice -n 10 timeout -s TERM 5400 cargo test --profile release-dev --lib split_ -- --nocapture >> $OUT/step2b_split_native.log 2>&1
rc=$?; echo "exit $rc" >> $OUT/step2b_split_native.log
echo "step2b_split_native (RUSTFLAGS target-cpu=native): expected exit 0, got $rc, $(( $(date +%s) - s )) s; backends: $(grep -oE 'backend::[A-Za-z0-9]+' $OUT/step2b_split_native.log | sort | uniq -c | tr -s ' ' | tr '\n' ';'); checksums: $(grep -oE "(split|fast) series' checksum [0-9a-f]{16}" $OUT/step2b_split_native.log | tr '\n' ';')" >> $S
