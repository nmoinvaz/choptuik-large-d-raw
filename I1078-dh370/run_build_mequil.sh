#!/bin/bash
# #1078, build of feat/mode-equil a2607acb (unit i1078m) in its own venv beside #1078's: hp/build.sh after uninstalling multidouble and hpkernel,
# the low-memory recipe (same bits as fat LTO: AGENTS.md, #600, #604). A sampler logs the largest process's RSS and MemAvailable every 15 s
# (a log; nothing is stopped or killed). Writes build_mequil.log, build_mequil_samples.csv, build_mequil_result.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
WT=/home/nathan/Source/choptuik-large-d-1078m
stamp() { date -u '+%F %T'; }
cd $WT || exit 9
[ "$(git rev-parse --short=8 HEAD)" = a2607acb ] || { echo "REFUSED: worktree not at a2607acb" > $OUT/build_mequil_result.txt; echo "BUILD DONE exit 1 $(stamp) UTC" > $OUT/BUILD_MEQUIL_DONE.txt; exit 1; }
export VIRTUAL_ENV=$WT/.venv PATH=$WT/.venv/bin:$PATH
echo "$(stamp) UTC build starts; python $(python -V 2>&1); MemAvailable $(awk '/MemAvailable/ {printf "%.1f GB", $2/1048576}' /proc/meminfo); load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/build_mequil_result.txt
python -m pip uninstall -y multidouble hpkernel >> $OUT/build_mequil.log 2>&1
( echo "time,max_rss_kb,proc,mem_available_kb" > $OUT/build_mequil_samples.csv
  while sleep 15; do
    echo "$(date -u +%T),$(ps -eo rss=,comm= --sort=-rss | head -1 | awk '{print $1","$2}'),$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" >> $OUT/build_mequil_samples.csv
  done ) &
SAMP=$!
t0=$(date +%s)
CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 nice -n 8 bash hp/build.sh >> $OUT/build_mequil.log 2>&1; rc=$?
kill $SAMP 2>/dev/null
echo "$(stamp) UTC build exit $rc, wall $(( $(date +%s) - t0 )) s; peak largest-process RSS $(sort -t, -k2 -n $OUT/build_mequil_samples.csv | tail -1 | cut -d, -f2) kB; lowest MemAvailable $(sort -t, -k4 -n $OUT/build_mequil_samples.csv | sed -n 2p | cut -d, -f4) kB" >> $OUT/build_mequil_result.txt
tail -1 $OUT/build_mequil.log >> $OUT/build_mequil_result.txt
python -m pip list 2>/dev/null | grep -iE 'hpkernel|multidouble' >> $OUT/build_mequil_result.txt
sha256sum $WT/.venv/lib/python3.14/site-packages/hpkernel/_hpkernel*.so >> $OUT/build_mequil_result.txt
echo "BUILD DONE exit $rc $(stamp) UTC" > $OUT/BUILD_MEQUIL_DONE.txt
exit 0
}
