#!/bin/bash
# #1025 macm3 kc87_leg2: starts part c (run_leg2c.sh run) when part b has ended cleanly at D 22.5 with lambda_1 still positive (t5's order, hc 24 Nov: "when part b reaches D 22.5 with lambda_1 still positive, start part c the same way from
# part b's last two states to D 24.0 (h 0.0625), and keep scanning every 0.125; stop part c early once two consecutive scanned roots are below 0 or on the guard's fold rule").
# Conditions: b/LEG_DONE.txt with exit 0, no b/leg_STOP.txt, the leap log ends "reached D 22.5", D 22.4375 and D 22.5 pushed. "Still positive": the latest scanned root (largest D) is above 0 and chain_next.py crossed says NO;
# if not, "part c not needed" (hc to t5, nothing started). Any other failure: "NOT started" (hc to t5). Log: start_c.log.
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc)
LOG=$L2/start_c.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
say "waiting for part b (b/LEG_DONE.txt)"
while [ ! -e $L2/b/LEG_DONE.txt ]; do
  # part b refused: nothing to continue
  grep -q 'NOT started' $L2/start_b.log 2>/dev/null && { tell "macm3 #1025 kc87_leg2: part c NOT started: part b was not started"; exit 1; }
  sleep 30
done
sleep 5
why=""
grep -q 'LEG DONE exit 0' $L2/b/LEG_DONE.txt || why="$why b/LEG_DONE says: $(cat $L2/b/LEG_DONE.txt);"
[ ! -e $L2/b/leg_STOP.txt ] || why="$why a STOP file in b: $(head -1 $L2/b/leg_STOP.txt | cut -c1-200);"
tail -3 $L2/b/leap.log | grep -q 'reached D 22.5' || why="$why the part b leap log does not end with 'reached D 22.5';"
grep -qx '22.4375' $L2/b/pushed_points.txt && grep -qx '22.5' $L2/b/pushed_points.txt || why="$why D 22.4375 and D 22.5 of part b are not both pushed;"
if [ -n "$why" ]; then tell "macm3 #1025 kc87_leg2: part c NOT started:$why"; exit 1; fi
last=$(grep -v '^#' $L/roots87.txt | sort -g | tail -1)
crossed=$(python3 $L/chain_next.py crossed)
if [ "$crossed" = YES ] || ! python3 -c "import sys; sys.exit(0 if float('$(echo $last | cut -d' ' -f2)') > 0 else 1)"; then
  tell "macm3 #1025 kc87_leg2: part c not needed: lambda_1 is not positive any more at the latest scanned root ($last; crossed: $crossed); part c is not started"; exit 0
fi
say "part b ended cleanly at D 22.5; the latest scanned root is $last (crossed: $crossed); starting part c"
bash $L2/run_leg2c.sh run >> $L2/start_c.out 2>&1; rc=$?
say "run_leg2c.sh run returned $rc"
[ $rc = 0 ] || tell "macm3 #1025 kc87_leg2: part c driver returned $rc (see c/exits_leg2c.txt)"
