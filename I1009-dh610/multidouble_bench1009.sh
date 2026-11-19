#!/bin/bash
# #1009 step 6, the dmat_f64 bench again (criterion filters on benchmark ids, which are "f64 matrix product, Fun<4>, M = 80" and "M = 320", not on the function name dmat_f64: the filter dmat_f64 matched nothing, md_bench_dmat_f64_filter_matched_nothing.log). Its first runs failed to link here (md_bench_dmat_f64_fatlto_link_failure.log, and again with the profile's LTO off,
# md_bench_dmat_f64_lto_off_link_failure.log): clang (CC=clang) compiles criterion's dependency `alloca`'s C stub as LLVM bitcode, which ld.bfd cannot read ("liballoca-*.rlib:
# error adding symbols: file format not recognized"). CFLAGS=-fno-lto makes that object ELF; everything else is the crate's own bench profile (lto = "fat", one codegen unit)
# and RUSTFLAGS="-C target-cpu=native".
. "$(dirname "$0")/common1009.sh"
export CARGO_BUILD_JOBS=6 CFLAGS="-fno-lto"
SUM=$OUT/summary_multidouble.txt
cd /home/nathan/Source/multidouble-dmat || exit 1
s=$(date +%s)
RUSTFLAGS="-C target-cpu=native" nice -n 10 cargo bench --bench field -- "f64 matrix product" > $OUT/md_bench_dmat_f64.log 2>&1
echo "bench dmat_f64 native, crate's bench profile, CFLAGS=-fno-lto: exit $?, $(( $(date +%s) - s )) s, load at end $(cut -d' ' -f1-3 /proc/loadavg)" >> $SUM
