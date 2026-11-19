#!/bin/bash
# #1009 step 4, line 1 again with RUSTFLAGS="-C target-cpu=native": the issue's command (no RUSTFLAGS) ran the cols_ tests on multidouble's Sse2 backend (cols_test.log); the SIMD
# backend is chosen at compile time, so this run is the AVX2 one the hpkernel build and the x86 question are about.
. "$(dirname "$0")/common1009.sh"
export CARGO_BUILD_JOBS=6
. $VENV/bin/activate
cd "$WT/hp" || exit 1
SUM=$OUT/summary_checks.txt
s=$(date +%s)
RUSTFLAGS="-C target-cpu=native" nice -n 10 cargo test --profile release-dev --lib cols_ -- --nocapture > $OUT/cols_test_native.log 2>&1
rc=$?
echo "cols_test_native (RUSTFLAGS target-cpu=native): expected exit 0, got $rc, $(( $(date +%s) - s )) s $([ $rc = 0 ] && echo OK || echo MISMATCH); backends: $(grep -oE 'backend::[A-Za-z0-9]+' $OUT/cols_test_native.log | sort | uniq -c | tr '\n' ' ')" >> $SUM
