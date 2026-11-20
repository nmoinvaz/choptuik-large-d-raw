#!/bin/bash
# #1058 on dh170, second build: hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0, Python package 8c4360ac; plan_auto and set_exact_recip added since 7ca74dd5) in the new worktree
# and venv -1058b, the low-memory recipe (coordinator's order), 6 cargo jobs, nice 15, /usr/bin/time -v. No gate: started at once, alone.
# The memory watchdog is ALERT-ONLY (Nathan's standing rule): it logs and sends an hc line and stops nothing. usage: bash build1058.sh   (about 1 to 2.5 h, peak unknown, 26 to 35 GB)
WT=/home/nathan/Source/choptuik-large-d-1058b
V=$WT/.venv
OUT=${T1058_TEST:-/home/nathan/Source/choptuik-large-d-raw/I1058-dh170}      # T1058_TEST=<dir>: the watchdog's own test (selftest_build1058.sh), nothing is built
HC=nathans-macbook-air-m5-3/t5
HCSEND=${T1058_HCSEND:-hc send}
L1=${T_L1:-2097152}; L2=${T_L2:-1048576}; L3=${T_L3:-524288}      # KB of MemAvailable: 2 GiB, 1 GiB, 0.5 GiB
cd "$WT" || exit 9
# the second build starts at once (coordinator's order, 20:30 UTC); the box was checked idle by hand
{ echo "# $(date -u '+%F %T') UTC build, worktree $WT at $(git rev-parse HEAD), $(rustc --version), $(cargo --version), maturin $($V/bin/maturin --version), python $($V/bin/python --version 2>&1)"
  echo "# env: the low-memory recipe CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 (same bits as fat LTO, #600 and #604), CARGO_BUILD_JOBS=6, nice 15, PIP_NO_CACHE_DIR=1, oom_score_adj 1000 for the build; MemAvailable at start $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MB, swap used $(free -m | awk '/Swap/ {print $3}') MB"
  echo "# other jobs at start: $(ps -eo args | grep -E 'anm_lowd|near_null|run1057|anm_run|ks_chain' | grep -v grep | wc -l) (must be 0)"; } > $OUT/build.log
BUILD_CMD=${T1058_BUILD_CMD:-"pip uninstall -y multidouble; nice -n 15 /usr/bin/time -v bash hp/build.sh"}
setsid bash -c "export VIRTUAL_ENV=$V PATH=$V/bin:\$PATH CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=6 PIP_NO_CACHE_DIR=1; echo 1000 > /proc/self/oom_score_adj; cd $WT; $BUILD_CMD" >> $OUT/build.log 2>&1 &
BP=$!
min=999999999; n=0; lvl=0
while kill -0 $BP 2>/dev/null; do
  a=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  [ "$a" -lt "$min" ] && min=$a
  n=$((n+1)); [ $((n % 15)) -eq 1 ] && echo "$(date -u '+%T') MemAvailable $((a/1024)) MB, min so far $((min/1024)) MB, swap used $(free -m | awk '/Swap/ {print $3}') MB, top: $(ps -eo rss,comm --sort=-rss | sed -n 2p | awk '{printf "%d MB %s", $1/1024, $2}')" >> $OUT/mem1058.log
  new=$lvl
  [ "$a" -lt "$L1" ] && new=1
  [ "$a" -lt "$L2" ] && new=2
  [ "$a" -lt "$L3" ] && new=3
  if [ "$new" -gt "$lvl" ]; then            # alert only, once per new level: log and hc, nothing is stopped
    lvl=$new
    msg="ALERT $(date -u '+%F %T') UTC #1058 build: MemAvailable $((a/1024)) MB (level $lvl of 3: under 2 GiB, 1 GiB, 0.5 GiB), swap used $(free -m | awk '/Swap/ {print $3}') MB; nothing stopped"
    { echo "$msg"; ps -eo pid,rss,args --sort=-rss | head -5 | cut -c1-150; } >> $OUT/alert1058.log
    echo "# $msg" >> $OUT/build.log
    timeout 60 $HCSEND $HC "dh170 $msg" >> $OUT/hc_sent.log 2>&1 &
  fi
  sleep 2
done
wait $BP 2>/dev/null; rc=$?
echo "# $(date -u '+%F %T') UTC build exit $rc, minimum MemAvailable $((min/1024)) MB, alert level reached $lvl" >> $OUT/build.log
[ -n "$T1058_TEST" ] && exit $rc
{ echo "## hp/Cargo.lock"; grep -A1 -E '^name = "(multidouble|multishoot|multisolver)"' hp/Cargo.lock
  echo "## hpkernel"; $V/bin/python -c 'import hpkernel,multidouble; print(hpkernel.__file__); print("isa", hpkernel.isa(), multidouble.isa())'
  so=$($V/bin/python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
  echo "## crate strings in the .so"; strings -n 8 $so 2>/dev/null | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -20
  echo "## python multidouble direct_url"; cat $V/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null; echo
  echo "## direct_url names 8c4360ac: $(grep -c 8c4360ac0be804d081faeea524e5c1c6e2fffaaa $V/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null)"; } > $OUT/versions.txt 2>&1
exit $rc
