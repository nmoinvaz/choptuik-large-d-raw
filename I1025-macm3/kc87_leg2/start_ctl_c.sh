#!/bin/bash
# #1025 macm3 kc87_leg2 (replaces start_c.sh, t5's insertion of 24 Nov: "when part b ends, run a control leap at h 0.03125 from dh370's k_c 87 states D 21.21875 and 21.25 (the seeds of part a) to D 21.375 (4 points), same guard and
# checks, as kc87_leg2/ctl/ ... and scan its D 21.375 state (same window as part a's) ... Then start part c as set."): when part b has ended, run the control leap (run_leg2ctl.sh run), queue the scan of its D 21.375 state,
# then start part c (run_leg2c.sh run) when part b ended cleanly at D 22.5 with lambda_1 still positive (t5's order, hc 24 Nov: "when part b reaches D 22.5 with lambda_1 still positive, start part c the same way from
# part b's last two states to D 24.0 (h 0.0625), and keep scanning every 0.125; stop part c early once two consecutive scanned roots are below 0 or on the guard's fold rule").
# Conditions: b/LEG_DONE.txt with exit 0, no b/leg_STOP.txt, the leap log ends "reached D 22.5", D 22.4375 and D 22.5 pushed. "Still positive": the latest scanned root (largest D) is above 0 and chain_next.py crossed says NO;
# if not, "part c not needed" (hc to t5, nothing started). Any other failure: "NOT started" (hc to t5). Log: start_c.log.
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc)
LOG=$L2/start_c.log      # the same log name as start_c.sh: the chain reads "NOT started" and "not needed" in it
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
say "waiting for part b (b/LEG_DONE.txt)"
while [ ! -e $L2/b/LEG_DONE.txt ]; do
  # part b refused: nothing to continue
  grep -q 'NOT started' $L2/start_b.log 2>/dev/null && { tell "macm3 #1025 kc87_leg2: part c NOT started: part b was not started"; exit 1; }
  sleep 30
done
sleep 5
# 1. the control leap, whatever the end of part b (a measurement of the h 0.0625 path's drift at k_c 87)
say "part b ended; starting the control leap (h 0.03125, D 21.21875 and D 21.25 to D 21.375)"
bash $L2/run_leg2ctl.sh run >> $L2/start_ctl.out 2>&1; rcc=$?
say "run_leg2ctl.sh run returned $rcc"
[ $rcc = 0 ] || tell "macm3 #1025 kc87_leg2: the control leap driver returned $rcc (see ctl/exits_leg2ctl.txt); part c goes on as set"
if grep -q 'LEG DONE exit 0' $L2/ctl/LEG_DONE.txt 2>/dev/null && grep -qx '21.375' $L2/ctl/pushed_points.txt 2>/dev/null; then
  say "control leap ended at D 21.375; queueing the scan of its D 21.375 state (window as part a's: prediction 0.791593 = part a's root, centre 0.790; the scan lock puts it behind the chain's running scan)"
  ( env SRC=I1025-macm3/kc87_leg2/ctl TAG=l1kc87Lmacm3ctl NP=4 NICE=15 DNSUFFIX=_ctl bash $L/pipeline87.sh 21.375 21.375 0.791593 0 > $L2/ctl/scan_launch.out 2>&1 ) &
  tell "macm3 #1025 kc87_leg2: control leap (h 0.03125) ended; its D 21.375 scan is queued (folder 21.375_ctl); ctl_compare.py compares the states; part c starts next"
else
  tell "macm3 #1025 kc87_leg2: the control leap did not end cleanly at D 21.375 (see ctl/); no control scan; part c goes on as set"
fi
# 2. part c as set
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
