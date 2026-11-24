#!/bin/bash
# chain_m3.sh: the four points of the coordinator's order of 24 Nov (hc, read at 19:43 UTC), one at a time: for each D the wait_m3.sh (state already on origin: pins, push, lock, memory wait, lane_m3.sh).
# The chain stops at the first point whose lane does not exit 0 (a failed check or control stops the work and is reported; nothing is loosened). D CENTER PRED: the coordinator's predictions rounded to 0.005.
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_m3pts
for pt in "21.5625 0.720 0.7203" "21.6875 0.670 0.6715" "21.8125 0.620 0.6217" "21.9375 0.570 0.5713"; do
  set -- $pt
  mkdir -p $F/$1
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: D $1 starts (centre $2, prediction $3)" >> $F/exits_chain.txt
  bash $F/wait_m3.sh $1 $2 $3; rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: D $1 ended with exit $rc" >> $F/exits_chain.txt
  [ $rc = 0 ] || { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: STOP at D $1 (exit $rc); the later points do not start" >> $F/exits_chain.txt; exit $rc; }
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc87_m3pts chain: all four points done" >> $F/exits_chain.txt
