#!/bin/bash
# #949 on dh170: near_null.py --k=6 --its=16 --threads=4 on the order-tied chain's stored states, two lanes (4 threads each, 8 in all),
# nice 10, worktree ~/Source/choptuik-large-d-935 (its 4.8.2 .venv), raw root ~/scratch949 (copies of the committed states, sync949.sh).
#   run949.sh lane N    a worker: takes the next unclaimed line of queue949.txt, runs it, and when the queue is empty waits and
#                       looks again until the file STOP949 exists. Start two (lane 1, lane 2).
# queue949.txt lines:   NAME STATE [extra near_null.py flags]   (STATE relative to the scratch root). Lines are claimed in order
# with flock, so lines can be appended while the lanes run. Each run writes NAME.json and NAME.log here and a line
# "949 NAME exit RC wall S s" to exits_949.txt (exit 1 is the planted control's required result, or a failed check).
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/scratch949
PY=$WT/.venv/bin/python
Q=$HERE/queue949.txt
CL=$HERE/claimed949.txt
L=$HERE/exits_949.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
[ "$1" = lane ] || { echo "usage: run949.sh lane N"; exit 2; }
lane=$2
touch $CL
while :; do
  line=$( flock $CL.lock bash -c '
    while read -r name rest; do
      [ -z "$name" ] && continue
      grep -qx "$name" '"$CL"' && continue
      echo "$name" >> '"$CL"'; echo "$name $rest"; exit 0
    done < '"$Q"'' )
  if [ -z "$line" ]; then
    [ -f $HERE/STOP949 ] && exit 0
    sleep 60; continue
  fi
  name=${line%% *}; rest=${line#* }; state=${rest%% *}; extra=""
  [ "$rest" != "$state" ] && extra=${rest#* }
  t=$(date +%s)
  echo "949 $name start $(date -u '+%F %T') lane $lane hp $(git -C "$WT" rev-parse --short HEAD) $state $extra, load $(cut -d' ' -f1-3 /proc/loadavg)" >> $L
  ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u near_null.py "$R" "$state" --k=6 --its=16 --threads=4 \
      --json="$HERE/$name.json" $extra ) > "$HERE/$name.log" 2>&1
  rc=$?
  echo "949 $name exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> $L
done
