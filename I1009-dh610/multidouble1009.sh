#!/bin/bash
# #1009 step 6 on dh610: multidouble at perf/dmat-apply-chunks (6dfd5b0, clone ~/Source/multidouble-dmat) on x86.
# 1. cargo test --release --features mutate --test field f64_matrix, with RUSTFLAGS="-C target-cpu=native" (the AVX2 path; the SIMD level is chosen at compile time) and without (the portable path);
#    the control f64_matrix_products_control_one_ulp (mutate::DMAT_CHUNK) is in the same filter and must pass (it asserts the differences are seen).
# 2. cargo bench --bench field -- dmat_f64 with target-cpu=native (criterion; the two forms in one binary, so the ratio is the result: K 49 shares the machine).
. "$(dirname "$0")/common1009.sh"
export CARGO_BUILD_JOBS=6
SUM=$OUT/summary_multidouble.txt
cd /home/nathan/Source/multidouble-dmat || exit 1
echo "# $(stamp) UTC multidouble $(git rev-parse --short=7 HEAD) start, load $(cut -d' ' -f1-3 /proc/loadavg), $(rustc --version)" > $SUM
for mode in native portable; do
  if [ $mode = native ]; then RF="-C target-cpu=native"; else RF=""; fi
  s=$(date +%s)
  RUSTFLAGS="$RF" nice -n 10 cargo test --release --features mutate --test field f64_matrix -- --nocapture --test-threads=1 > $OUT/md_f64_matrix_$mode.log 2>&1
  echo "f64_matrix $mode: exit $?, $(( $(date +%s) - s )) s; $(grep -E 'test result|entries differ' $OUT/md_f64_matrix_$mode.log | tr '\n' ';' | cut -c1-300)" >> $SUM
done
s=$(date +%s)
RUSTFLAGS="-C target-cpu=native" nice -n 10 cargo bench --bench field -- dmat_f64 > $OUT/md_bench_dmat_f64.log 2>&1
echo "bench dmat_f64 native: exit $?, $(( $(date +%s) - s )) s, load at end $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
echo "# $(stamp) UTC multidouble done" >> $SUM
