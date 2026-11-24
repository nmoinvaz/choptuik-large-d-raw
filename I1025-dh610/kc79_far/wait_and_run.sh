#!/bin/bash
# wait_and_run.sh D CENTER PRED: waits (polling origin every 60 s, cap 10 h) for win2's k_c 79 far scout state at D, pins state and record by blob (fetch_point.sh), pushes the pins, then runs lane_far.sh for D under a lock
# shared by all far points (one point at a time: 8 threads; own lock, so a tag g lane of ../kc79_leg runs beside it).
D=$1; C=$2; PRED=$3
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
mkdir -p $F/D$D
L=$F/D$D/exits_far.txt
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_far D $D: $*" | tee -a $L; }
t0=$(date +%s)
until bash $F/fetch_point.sh $D > $F/D$D/fetch.log 2>&1; do
  rc=$?
  [ $rc = 1 ] || { say "STOP: fetch_point.sh exit $rc: $(cat $F/D$D/fetch.log | tail -2)"; exit 1; }
  [ $(( $(date +%s) - t0 )) -lt 36000 ] || { say "STOP: the state of D $D is not on origin after 10 h"; exit 1; }
  sleep 60
done
say "state and record pinned: $(cat $F/D$D/fetch.log); $(cat $F/D$D/source_commit.txt | cut -c1-200)"
bash $PUSH I1025-dh610/kc79_far/D$D "I1025-dh610/kc79_far/D$D: pins, scan starts when the lock is free" > $F/D$D/push_pins.txt 2>&1
# thread budget (the cap of 20 threads of mine, counted by what is planned: the recount's 12 while unit i1076c is active, the tag g lane's 8 while its lock is held, this lane's 8);
# the scan starts only when they fit under LIM (budget.txt of this folder, default 20); the tag g lane never waits for this one
tw=$(date +%s)
while :; do
  LIM=$(cat $F/budget.txt 2>/dev/null || echo 20); used=0
  [ "$(systemctl --user is-active i1076c)" = active ] && used=$((used + 12))
  ( flock -n 7 ) 7> /tmp/claude-1000/kc79_leg.lock || used=$((used + 8))
  [ $((used + 8)) -le $LIM ] && break
  [ -e $F/D$D/budget_wait.txt ] || say "waiting for threads: $used planned in use (recount 12 if active, tag g lane 8 if running) + 8 > $LIM"
  echo "$(date -u '+%F %T') UTC $used in use, limit $LIM" > $F/D$D/budget_wait.txt
  sleep 60
done
[ $(( $(date +%s) - tw )) -lt 60 ] || say "threads free after $(( $(date +%s) - tw )) s: $used planned in use + 8 <= $LIM"
exec 8> /tmp/claude-1000/kc79_far.lock
flock 8
say "lock taken, lane starts"
bash $F/lane_far.sh $D $C $PRED
