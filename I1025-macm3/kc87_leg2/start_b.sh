#!/bin/bash
# #1025 macm3 kc87_leg2: starts part b (run_leg2b.sh run) when part a has ended cleanly at D 21.5 (t5's order, hc 24 Nov: "when the leap reaches D 21.5 start a second leap from its D 21.4375 and 21.5 states to D 22.5").
# Conditions: LEG_DONE.txt with exit 0, no leg_STOP.txt, the leap log ends "reached D 21.5", D 21.4375 and D 21.5 pushed. Otherwise: hc to t5 and nothing started. Log: start_b.log.
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
HC=$(command -v hc)
LOG=$L2/start_b.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
say "waiting for part a (LEG_DONE.txt)"
while [ ! -e $L2/LEG_DONE.txt ]; do sleep 30; done
sleep 5
why=""
grep -q 'LEG DONE exit 0' $L2/LEG_DONE.txt || why="$why LEG_DONE says: $(cat $L2/LEG_DONE.txt);"
[ ! -e $L2/leg_STOP.txt ] || why="$why a STOP file: $(head -1 $L2/leg_STOP.txt | cut -c1-200);"
tail -3 $L2/leap.log | grep -q 'reached D 21.5' || why="$why the leap log does not end with 'reached D 21.5';"
grep -qx '21.4375' $L2/pushed_points.txt && grep -qx '21.5' $L2/pushed_points.txt || why="$why D 21.4375 and D 21.5 are not both pushed;"
if [ -n "$why" ]; then tell "macm3 #1025 kc87_leg2: part b NOT started:$why"; exit 1; fi
say "part a ended cleanly at D 21.5; starting part b"
bash $L2/run_leg2b.sh run >> $L2/start_b.out 2>&1; rc=$?
say "run_leg2b.sh run returned $rc"
[ $rc = 0 ] || tell "macm3 #1025 kc87_leg2: part b driver returned $rc (see b/exits_leg2b.txt)"
