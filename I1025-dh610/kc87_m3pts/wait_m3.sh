#!/bin/bash
# wait_k87.sh D CENTER PRED: waits (polling origin every 60 s, cap 10 h) for macm3's k_c 87 leg state (tag l1kc87Lmacm3b) at D, pins state and record by blob (fetch_m3.sh), pushes the pins, then runs lane_m3.sh for D under a lock shared by
# the rotation points (one point at a time: 8 threads).
D=$1; C=$2; PRED=$3
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_m3pts; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F/$D
L=$F/$D/exits_k87l.txt
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts D $D: $*" | tee -a $L; }
t0=$(date +%s)
until bash $F/fetch_m3.sh $D > $F/$D/fetch.log 2>&1; do
  rc=$?
  [ $rc = 1 ] || { say "STOP: fetch_m3.sh exit $rc: $(cat $F/$D/fetch.log | tail -2)"; exit 1; }
  [ $(( $(date +%s) - t0 )) -lt 36000 ] || { say "STOP: the state of D $D is not on origin after 10 h"; exit 1; }
  sleep 60
done
say "state and record pinned: $(cat $F/$D/fetch.log); $(cat $F/$D/source_commit.txt | cut -c1-200)"
bash $PUSH I1025-dh610/kc87_m3pts/$D "I1025-dh610/kc87_m3pts/$D: pins, scan starts when the lock is free" > $F/$D/push_pins.txt 2>&1
exec 8> /tmp/claude-1000/kc87_m3pts.lock
flock 8
tm=$(date +%s)
while :; do  # a wait, not a stop: the lane needs 8 x 2.5 GB + 4 GB; nothing is stopped for memory
  av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo); [ "$av" -ge $(( 8 * 2500000 + 4000000 )) ] && break
  [ -e $F/$D/mem_wait.txt ] || say "waiting for memory: MemAvailable $av kB is below 8 x 2.5 GB + 4 GB (nothing is stopped)"
  echo "$(date -u '+%F %T') UTC MemAvailable $av kB" > $F/$D/mem_wait.txt
  [ $(( $(date +%s) - tm )) -lt 21600 ] || { say "STOP: the memory wait ended after 6 h"; exit 1; }
  sleep 60
done
say "lock taken, lane starts"
bash $F/lane_m3.sh $D $C $PRED
