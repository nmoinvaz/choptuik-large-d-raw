#!/bin/bash
# #1025 macm3 kc87_leg2: starts part c (run_leg2c2.sh run) when part b2 has ended cleanly at D 22.5 with lambda_1 still positive (t5's orders, hc 24 Nov: "restart part b as b2 ... part c after b2 as set"; part b stopped at D 21.96875,
# the SVD exception; the first start_c.sh / start_ctl_c.sh looked at part b and are not the starters for this).
# Conditions: b2/LEG_DONE.txt with exit 0, no b2/leg_STOP.txt, the b2 leap log ends "reached D 22.5", D 22.4375 and D 22.5 of b2 pushed. "Still positive": the latest scanned root (largest D) is above 0 and chain_next.py crossed says NO;
# if not, "part c not needed" (hc to t5, nothing started). Any other failure: "NOT started" (hc to t5). Log: start_c2.log (the chain reads "NOT started" and "not needed" in it).
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc)
LOG=$L2/start_c2.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
say "waiting for part b2 (b2/LEG_DONE.txt)"
while [ ! -e $L2/b2/LEG_DONE.txt ]; do
  grep -q 'NOT started' $L2/start_b2.log 2>/dev/null && { tell "macm3 #1025 kc87_leg2: part c NOT started: part b2 was not started"; exit 1; }
  sleep 30
done
sleep 5
why=""
grep -q 'LEG DONE exit 0' $L2/b2/LEG_DONE.txt || why="$why b2/LEG_DONE says: $(cat $L2/b2/LEG_DONE.txt);"
[ ! -e $L2/b2/leg_STOP.txt ] || why="$why a STOP file in b2: $(head -1 $L2/b2/leg_STOP.txt | cut -c1-200);"
tail -3 $L2/b2/leap.log | grep -q 'reached D 22.5' || why="$why the part b2 leap log does not end with 'reached D 22.5';"
grep -qx '22.4375' $L2/b2/pushed_points.txt && grep -qx '22.5' $L2/b2/pushed_points.txt || why="$why D 22.4375 and D 22.5 of part b2 are not both pushed;"
if [ -n "$why" ]; then tell "macm3 #1025 kc87_leg2: part c NOT started:$why"; exit 1; fi
last=$(grep -v '^#' $L/roots87.txt | sort -g | tail -1)
crossed=$(python3 $L/chain_next.py crossed)
if [ "$crossed" = YES ] || ! python3 -c "import sys; sys.exit(0 if float('$(echo $last | cut -d' ' -f2)') > 0 else 1)"; then
  tell "macm3 #1025 kc87_leg2: part c not needed: lambda_1 is not positive any more at the latest scanned root ($last; crossed: $crossed); part c is not started"; exit 0
fi
say "part b2 ended cleanly at D 22.5; the latest scanned root is $last (crossed: $crossed); starting part c"
bash $L2/run_leg2c2.sh run >> $L2/start_c2.out 2>&1; rc=$?
say "run_leg2c2.sh run returned $rc"
[ $rc = 0 ] || tell "macm3 #1025 kc87_leg2: part c driver returned $rc (see c/exits_leg2c.txt)"
