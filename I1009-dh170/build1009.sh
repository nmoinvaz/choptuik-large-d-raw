#!/bin/bash
# #1009 on dh170: hp perf/cauchy-cache-chunks 76fdcbc9 (worktree ~/Source/choptuik-large-d-ccc) built into the new venv ~/Source/venv-ccc, low-memory recipe, 6 jobs, nice 15, /usr/bin/time -v.
# A watchdog kills the build's process group when MemAvailable falls under 2 GiB (the issue's rule) and logs the largest processes. usage: bash build1009.sh
WT=/home/nathan/Source/choptuik-large-d-ccc
V=/home/nathan/Source/venv-ccc
OUT=/home/nathan/Source/choptuik-large-d-raw/I1009-dh170
LIMIT_KB=2097152
cd "$WT" || exit 9
{ echo "# $(date -u '+%F %T') UTC build, worktree $WT at $(git rev-parse HEAD), $(rustc --version), $(cargo --version), maturin $($V/bin/maturin --version), python $($V/bin/python --version 2>&1)"
  echo "# env: CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6, nice 15, MemAvailable at start $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MB"; } > $OUT/build.log
setsid bash -c "export VIRTUAL_ENV=$V PATH=$V/bin:\$PATH CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6; cd $WT; nice -n 15 /usr/bin/time -v bash hp/build.sh" >> $OUT/build.log 2>&1 &
BP=$!
min=999999999; n=0; tripped=0
while kill -0 $BP 2>/dev/null; do
  a=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  [ "$a" -lt "$min" ] && min=$a
  n=$((n+1)); [ $((n % 15)) -eq 1 ] && echo "$(date -u '+%T') MemAvailable $((a/1024)) MB, min so far $((min/1024)) MB" >> $OUT/mem1009.log
  if [ "$a" -lt "$LIMIT_KB" ]; then
    tripped=1
    { echo "# $(date -u '+%F %T') UTC WATCHDOG: MemAvailable $((a/1024)) MB under 2048 MB, killing the build's process group $BP"; ps -eo pid,rss,args --sort=-rss | head -8 | cut -c1-150; } >> $OUT/build.log
    kill -TERM -- -$BP; sleep 3; kill -KILL -- -$BP 2>/dev/null
    break
  fi
  sleep 2
done
wait $BP 2>/dev/null; rc=$?
echo "# $(date -u '+%F %T') UTC build exit $rc, watchdog tripped $tripped, minimum MemAvailable $((min/1024)) MB" >> $OUT/build.log
{ echo "## hp/Cargo.lock"; grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## hpkernel"; $V/bin/python -c 'import hpkernel,multidouble; print(hpkernel.__file__); print("isa", hpkernel.isa(), multidouble.isa())'
  so=$($V/bin/python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
  echo "## crate strings in the .so"; strings -n 8 $so 2>/dev/null | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -20
  echo "## python multidouble"; cat $V/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo; } > $OUT/versions.txt 2>&1
exit $rc
