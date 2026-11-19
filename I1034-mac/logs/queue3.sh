#!/bin/bash
# after queue2: fastmul on the dumped chain factors, the planted timings, then the D 253 context at ks 240 (6 orders,
# one run per form, fast then split 1)
set -u
B=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/hptest_v2
F=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/bench_target/release/fastmul_bench
cd /Users/nathan/Source/choptuik-large-d-1034/hp
run() { local log=$1; shift; { date -u '+start %H:%M'; uptime; time "$@"; date -u '+end %H:%M'; } > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/$log 2>&1; echo "$log exit $?"; }
( cd /Users/nathan/Source/choptuik-large-d-1034/hp/fastmul_bench && nice -n 10 lockf -k /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/cargo_a.lock env CARGO_BUILD_JOBS=3 CARGO_TARGET_DIR=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/bench_target cargo build --release ) > /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/bench_build.log 2>&1 || { echo bench build failed; exit 1; }
run v2_dump130_bench.log nice -n 10 $F --dump /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/i1034/dump130 --reps 3
run v2_planted_bench.log nice -n 10 $F --no-check --reps 5
echo QUEUE3-DONE
