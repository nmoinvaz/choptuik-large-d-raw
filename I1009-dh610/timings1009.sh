#!/bin/bash
# #1009 step 5 on dh610: dump_ctx.py of T100-win2's D 3.0444 M 320 state to I1009-dh610/ctx320.bin (input, not committed), then bench_fill at THREADS=1 and THREADS=4, ROUNDS default 6,
# the two forms timed alternately inside one binary (cargo test --release --lib bench_fill -- --ignored --nocapture, low-memory profile). K 49 shares the machine, so the ratio is the result.
. "$(dirname "$0")/common1009.sh"
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6 RUSTFLAGS="-C target-cpu=native"
SUM=$OUT/summary_timings.txt
. $VENV/bin/activate
cd "$WT/hp" || exit 1
echo "# $(stamp) UTC timings start, hp $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > $SUM
python3 dump_ctx.py $R/T100-win2/states/lowDhm_x0.000157-0.975_D3.0444_M320.npz $OUT/ctx320.bin > $OUT/dump_ctx.log 2>&1; echo "dump_ctx: exit $? $(stat -c %s $OUT/ctx320.bin) bytes" >> $SUM
# compile once (no run), so that the compile's load is not inside the timed runs
nice -n 10 cargo test --release --lib bench_fill --no-run > $OUT/bench_compile.log 2>&1; echo "bench compile: exit $?" >> $SUM
for T in 1 4; do
  s=$(date +%s)
  FILE=$OUT/ctx320.bin THREADS=$T nice -n 10 cargo test --release --lib bench_fill -- --ignored --nocapture > $OUT/bench_fill_T$T.log 2>&1
  echo "bench_fill THREADS=$T: exit $?, $(( $(date +%s) - s )) s, load at end $(cut -d' ' -f1-3 /proc/loadavg), K49 load beside it" >> $SUM
done
echo "# $(stamp) UTC timings done" >> $SUM
