#!/bin/bash
# v3: build, the tests, then the D 253 context at ks 130 (stats) and at ks 240 by both forms (6 orders, one run each)
set -u
cd /Users/nathan/Source/choptuik-large-d-1034/hp
( time nice -n 10 lockf -k /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/cargo_a.lock env CARGO_BUILD_JOBS=3 CARGO_TARGET_DIR=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/target cargo test --profile release-dev --lib --no-run ) > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/build3.log 2>&1 || { echo build3 failed; exit 1; }
exe=$(grep -o "/private[^)]*_hpkernel-[0-9a-f]*" /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/build3.log | head -1); cp "$exe" /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/hptest_v3 || exit 1
echo built
B=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/hptest_v3
run() { local log=$1; shift; { date -u '+start %H:%M'; uptime; time "$@"; date -u '+end %H:%M'; } > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/$log 2>&1; echo "$log exit $?"; }
run v3_split_fast_accuracy.log nice -n 10 $B split_fast_accuracy --nocapture
run v3_split_series_accuracy.log nice -n 10 $B split_series_accuracy --nocapture
run v3_fastmul_planted.log nice -n 10 $B fastmul_planted --nocapture
CF="FILE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/ctx_D253.3382.bin JET=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/jet_D253.3382.bin NORD=6 REPS=1"
run v3_D253_ks130_N6_s2.log env $CF SPLIT=2 nice -n 10 $B split_file --ignored --nocapture
run v3_D253_ks240_N6_s2.log env $CF SPLIT=2 KS=240 nice -n 10 $B split_file --ignored --nocapture
run v3_D253_ks240_N6_s1.log env $CF SPLIT=1 KS=240 nice -n 10 $B split_file --ignored --nocapture
echo QUEUE4-DONE
