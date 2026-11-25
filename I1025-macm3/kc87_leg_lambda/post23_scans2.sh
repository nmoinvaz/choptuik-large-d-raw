#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~12:10 UTC, then ~14:07 UTC): the ordered scans of the late leg points from D 22.875 down, with t5's extension rule added to post23_scans.sh:
# "if D 22.875 shows no change in 0.100-0.160, extend it at once to 0.060-0.100 by 0.01 (plus a repeat), no need to ask; the same rule for the later points (extend by the window's width on the side the end signs point to)".
# Per point: pipeline87_post23.sh (a scan already running for it is waited for), then ext23.py need: a robust change in the window -> EXT_CLEARED.txt (the chain's record loop reads the root as before);
# none -> ext23.py setup (grid and README section first), pipeline87_rescan.sh on D_ext, ext23.py merge (the merged reading replaces D/read_lower.txt, the first one stays as read_lower_first.txt), push, EXT_CLEARED.txt.
# chain_next.py pending skips a point listed in EXT_ORDER.txt until its EXT_CLEARED.txt exists, so the chain's record does not stop on a window without a change. After the last point the hold is released as before.
# Stops (hc to t5): a scan without SCAN_DONE.txt, an ext23 answer that is not NO/EXT, a failed extension step, a root that does not appear within 20 min.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans2: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
cd $L || exit 9
have_root() { grep -q "^$1 " $L/roots87.txt; }
stopp() { tell "macm3 #1025 post23_scans2 STOP: $*; the hold stays"; exit 1; }
python3 ext23.py selftest > $L/selftest_ext23.txt 2>&1 || stopp "ext23.py selftest fails"
for m in side width merge; do python3 ext23.py selftest --mutate=$m > /dev/null 2>&1 && stopp "ext23.py selftest --mutate=$m passed (it must fail)"; done
python3 chain_next.py selftest > /dev/null 2>&1 || stopp "chain_next.py selftest fails"
python3 chain_next.py selftest --mutate=ext > /dev/null 2>&1 && stopp "chain_next.py selftest --mutate=ext passed (it must fail)"
say "started: ext23 selftest exit 0, mutations side, width, merge exit 1; chain_next selftest exit 0, mutation ext exit 1"
for D in 22.875 22.8125 22.75 22.6875 22.625 22.5625 22.5 22.375; do
  if [ -e $L/$D/SCAN_DONE.txt ]; then say "D $D already scanned: skipped"
  elif pgrep -f "pipeline87_post23.sh $D " > /dev/null; then
    say "D $D: its scan is running (pipeline87_post23.sh): waiting for it"
    while pgrep -f "pipeline87_post23.sh $D " > /dev/null; do sleep 20; done
    [ -e $L/$D/SCAN_DONE.txt ] || stopp "the scan of D $D did not finish (no SCAN_DONE.txt; see $D/pipeline.log, $D/steps.txt)"
  else
    say "starting D $D (--auto)"
    env NP=4 NICE=15 bash $L/pipeline87_post23.sh $D --auto; say "pipeline87_post23.sh D $D returned $?"
    [ -e $L/$D/SCAN_DONE.txt ] || stopp "the scan of D $D did not finish (no SCAN_DONE.txt; see $D/pipeline.log, $D/steps.txt)"
  fi
  if [ ! -e $L/$D/EXT_CLEARED.txt ]; then
    r=$(python3 ext23.py need $D)
    case "$r" in
      NO*) say "D $D: the window has a robust change (or more): no extension"; echo "no extension: $(date -u '+%F %T') UTC" > $L/$D/EXT_CLEARED.txt;;
      EXT*)
        set -- $r; LO=$2; HI=$3; SIDE=$4
        tell "macm3 #1025 kc87 leg2 D $D: no robust change in its window ($(grep -h 'endpoint signs' $L/$D/read_lower.txt)); extension to $LO-$HI ($SIDE) by 0.01 plus a repeat started at once (t5's order), folder ${D}_ext"
        fe=$(python3 ext23.py setup $D $LO $HI) || stopp "ext23.py setup D $D failed"
        env NP=4 NICE=15 bash $L/pipeline87_rescan.sh $fe; say "pipeline87_rescan.sh $fe returned $?"
        [ -e $L/$fe/SCAN_DONE.txt ] || stopp "the extension scan $fe did not finish (see $fe/pipeline.log, $fe/steps.txt)"
        python3 ext23.py merge $D >> $LOG 2>&1 || stopp "ext23.py merge D $D failed"
        bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $D extension scanned and merged" >> $LOG 2>&1; say "extension pushed ($?)"
        echo "extended to $LO-$HI: $(date -u '+%F %T') UTC" > $L/$D/EXT_CLEARED.txt;;
      *) stopp "ext23.py need D $D answered: $r";;
    esac
  fi
  n=0; until have_root $D; do n=$((n+1)); [ $n -gt 40 ] && stopp "no root of D $D in roots87.txt 20 min after the scan (the chain's record may have stopped: see chain.log)"; sleep 30; done
  say "D $D: root recorded: $(grep "^$D " $L/roots87.txt | tail -1)"
done
for f in $L/HOLD*.txt; do [ -e "$f" ] && mv "$f" "$f.released.$(date +%s)"; done
echo "$(date -u '+%F %T') UTC HOLD released after the ordered scans of D 23.0 to D 22.375 (t5's order, 25 Nov)" >> $L/chain.log
tell "macm3 #1025 post23_scans2: all ten points (D 23.0, 22.9375, 22.875, 22.8125, 22.75, 22.6875, 22.625, 22.5625, 22.5, 22.375) have a root (roots87.txt); the chain's hold (HOLD_low2.txt, HOLD_refine.txt) is released: the chain continues with the points between (phase 2)."
