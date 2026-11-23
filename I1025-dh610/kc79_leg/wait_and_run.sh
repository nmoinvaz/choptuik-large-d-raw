#!/bin/bash
# wait_and_run.sh D CENTER PRED: waits (polling origin every 60 s, cap 10 h) for win2's k_c 79 leg state at D, pins state and record by blob (fetch_point.sh), pushes the pins, then runs lane_leg.sh for D under a lock
# shared by all points (one point at a time: 8 threads).
D=$1; C=$2; PRED=$3
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F/D$D
L=$F/D$D/exits_leg.txt
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_leg D $D: $*" | tee -a $L; }
t0=$(date +%s)
until bash $F/fetch_point.sh $D > $F/D$D/fetch.log 2>&1; do
  rc=$?
  [ $rc = 1 ] || { say "STOP: fetch_point.sh exit $rc: $(cat $F/D$D/fetch.log | tail -2)"; exit 1; }
  [ $(( $(date +%s) - t0 )) -lt 36000 ] || { say "STOP: the state of D $D is not on origin after 10 h"; exit 1; }
  sleep 60
done
say "state and record pinned: $(cat $F/D$D/fetch.log); $(cat $F/D$D/source_commit.txt | cut -c1-200)"
bash $PUSH I1025-dh610/kc79_leg/D$D "I1025-dh610/kc79_leg/D$D: pins, scan starts when the lock is free" > $F/D$D/push_pins.txt 2>&1
exec 8> /tmp/claude-1000/kc79_leg.lock
flock 8
say "lock taken, lane starts"
bash $F/lane_leg.sh $D $C $PRED
