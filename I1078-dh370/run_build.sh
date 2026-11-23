#!/bin/bash
# #1078 step 1, build (unit i1078a): hp/build.sh in the new venv at main c016b932, after uninstalling multidouble's Python package (and the old hpkernel),
# the low-memory recipe of dh370's #1058 build (same bits as fat LTO: AGENTS.md, #600, #604). A sampler logs the largest process's RSS and MemAvailable every 15 s
# (a log; nothing is stopped or killed). Writes build.log, build_samples.csv, build_result.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
WT=/home/nathan/Source/choptuik-large-d-1078
stamp() { date -u '+%F %T'; }
cd $WT || exit 9
[ "$(git rev-parse --short=8 HEAD)" = c016b932 ] || { echo "REFUSED: worktree not at c016b932" > $OUT/build_result.txt; exit 1; }
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$PATH
echo "$(stamp) UTC build starts; python $(python -V 2>&1); MemAvailable $(awk '/MemAvailable/ {printf "%.1f GB", $2/1048576}' /proc/meminfo); load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/build_result.txt
python -m pip uninstall -y multidouble hpkernel >> $OUT/build.log 2>&1
( echo "time,max_rss_kb,proc,mem_available_kb" > $OUT/build_samples.csv
  while sleep 15; do
    echo "$(date -u +%T),$(ps -eo rss=,comm= --sort=-rss | head -1 | awk '{print $1","$2}'),$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" >> $OUT/build_samples.csv
  done ) &
SAMP=$!
t0=$(date +%s)
CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 nice -n 8 bash hp/build.sh >> $OUT/build.log 2>&1; rc=$?
kill $SAMP 2>/dev/null
echo "$(stamp) UTC build exit $rc, wall $(( $(date +%s) - t0 )) s; peak largest-process RSS $(sort -t, -k2 -n $OUT/build_samples.csv | tail -1 | cut -d, -f2) kB; lowest MemAvailable $(sort -t, -k4 -n $OUT/build_samples.csv | sed -n 2p | cut -d, -f4) kB" >> $OUT/build_result.txt
tail -1 $OUT/build.log >> $OUT/build_result.txt
python -m pip list 2>/dev/null | grep -iE 'hpkernel|multidouble' >> $OUT/build_result.txt
sha256sum $WT/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so >> $OUT/build_result.txt
echo "BUILD DONE exit $rc $(stamp) UTC" > $OUT/BUILD_DONE.txt
exit 0
}
