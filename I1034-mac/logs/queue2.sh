#!/bin/bash
# v2 runs, one at a time: the synthetic tests, then the D 253 context at ks 240 (8 orders, one run per form) with the
# fast form's factors dumped at ks 130 first
set -u
B=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/hptest_v2
cd /Users/nathan/Source/choptuik-large-d-1034/hp
run() { local log=$1; shift; { date -u '+start %H:%M'; time "$@"; date -u '+end %H:%M'; } > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/$log 2>&1; echo "$log exit $?"; }
run v2_split_fast_accuracy.log nice -n 10 $B split_fast_accuracy --nocapture
run v2_split_series_accuracy.log nice -n 10 $B split_series_accuracy --nocapture
run v2_fastmul_planted.log nice -n 10 $B fastmul_planted --nocapture
mkdir -p /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/dump130
run v2_D253_ks130_N6_s2_dump.log env FASTMUL_DUMP=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/dump130 FILE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/ctx_D253.3382.bin JET=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i6data/jet_D253.3382.bin NORD=6 SPLIT=2 REPS=1 nice -n 10 $B split_file --ignored --nocapture
echo QUEUE2-DONE
