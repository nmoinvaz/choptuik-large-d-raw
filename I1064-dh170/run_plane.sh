#!/bin/bash
# #1064 part 2 (scalar equation): usage run_plane.sh KS KEEP_PLAN TAG   (the control: 293 1 ks293; the raise: 315 0 ks315). 4 threads, nice 10, a 4 h cap by exact pid.
KS=$1; KP=$2; TAG=$3; EXTRA=${4:-}
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1064-dh170; HP=/home/nathan/Source/choptuik-large-d-1058b/hp
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; RAW=/home/nathan/scratch949
ST=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 HP_DIR=$HP
say() { echo "== $(date -u '+%F %T') UTC $*" >> $D/exits_1064dh170.txt; }
[ "$(git hash-object --no-filters $RAW/$ST | cut -c1-12)" = eb34f3c845a4 ] || { say "refuse: state blob is not eb34f3c8"; exit 2; }
cd $HP || exit 9
[ -e $D/plane_$TAG.log ] && { say "refuse: plane_$TAG.log exists (no overwrite)"; exit 3; }
say "start $TAG: ks $KS keep_plan $KP"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $D/scalar_plane1064.py $RAW $ST --ks=$KS --keep_plan=$KP --its=32 --threads=4 --json=$D/plane_$TAG.json $EXTRA > $D/plane_$TAG.log 2>&1 &
tp=$!; echo $tp > $D/time_pid_plane_$TAG.txt
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 14400 ]; then py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "4 h cap: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break; fi
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' ')
  rss=$([ -n "$py" ] && awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status 2>/dev/null || echo 0)
  echo "$(date -u '+%T') MemAvailable $av MiB, python pid ${py:-none} RSS ${rss:-0} MiB" >> $D/memlog_plane_$TAG.log
  [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%T') MemAvailable $av MiB (alert only)" >> $D/alert_plane_$TAG.log
  sleep 30
done
wait $tp; r=$?
say "exit $r, $(( $(date +%s) - s0 )) s wall ($TAG)"
