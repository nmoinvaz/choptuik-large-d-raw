#!/bin/bash
# wait_k87.sh D CENTER PRED: waits (polling origin every 60 s, cap 10 h) for macm3's k_c 87 leg state (tag l1kc87Lmacm3b) at D, pins state and record by blob (fetch_m3.sh), pushes the pins, then runs lane_m3.sh for D under a lock shared by
# the rotation points (one point at a time: 8 threads).
D=$1; C=$2; PRED=$3
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_m3pts; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F/$D
# inserted by the coordinator's word (hc, 24 Nov, about 22:40 UTC): the k_c 87 scan of macm3's D 21.75 state on Linux (window 0.640 to 0.660 by 0.005 and a repeat of 0.650) runs first after D 21.6875 and before D 21.8125
if [ "$D" = 21.8125 ] && [ ! -e $F/21.75/INSERTED_DONE ]; then
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: inserted point D 21.75 (k_c 87 of macm3's state, on Linux, HALF 2) runs before D 21.8125" >> $F/exits_chain.txt
  mkdir -p $F/21.75; HALF=2 bash $F/wait_m3.sh 21.75 0.650 0.646846; rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: inserted point D 21.75 ended with exit $rc" >> $F/exits_chain.txt
  [ $rc = 0 ] || exit $rc
  touch $F/21.75/INSERTED_DONE
fi
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
# the coordinator's word (hc, 24 Nov, about 21:50 UTC): priority to the k_c 95 scan of ../kc95_d2175; hold this lane until that scan has read (its "point done" line) or has stopped (a STOP line)
K95=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc95_d2175/exits_kc95.txt; th=$(date +%s)
until grep -q -E "kc95_d2175: (.*kc95 D 21.75 point done|STOP: )" $K95 2>/dev/null; do
  [ -e $F/$D/hold.txt ] || say "holding: the k_c 95 scan of D 21.75 has not read yet (the coordinator's priority order); nothing of this point starts"
  echo "$(date -u '+%F %T') UTC holding" > $F/$D/hold.txt
  [ $(( $(date +%s) - th )) -lt 43200 ] || { say "STOP: the hold for the k_c 95 scan ended after 12 h"; exit 1; }
  sleep 60
done
[ ! -e $F/$D/hold.txt ] || say "hold ended: $(grep -E "kc95_d2175: (.*kc95 D 21.75 point done|STOP: )" $K95 | tail -n 1 | cut -c1-120)"
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
