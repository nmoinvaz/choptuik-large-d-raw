#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~12:10 UTC): after part c2's guard stop at D 23.0, scan in this order: D 23.0 and D 22.9375 (lambda -0.10 to 0.30 by 0.02 plus a repeat of 0.10), then part c's points from D 22.875 down
# (22.875, 22.8125, 22.75, 22.6875, 22.625, 22.5625), then D 22.5 and D 22.375 (my grids: +-0.03 by 0.01 around the primary prediction, a repeat of its centre); then the chain's hold is released (HOLD*.txt moved aside).
# Each scan is pipeline87_post23.sh; the chain's record loop (scan_chain.sh, still running, held) writes each root to roots87.txt and reports it to t5 by hc, and the next point's prediction needs it, so this waits for it.
# Log: post23_scans.log. A point whose SCAN_DONE.txt exists is skipped (restart). Stops (hc to t5): a scan without SCAN_DONE.txt, a root that does not appear within 20 min.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
cd $L || exit 9
have_root() { grep -q "^$1 " $L/roots87.txt; }
for D in 23.0 22.9375 22.875 22.8125 22.75 22.6875 22.625 22.5625 22.5 22.375; do
  if [ -e $L/$D/SCAN_DONE.txt ]; then say "D $D already scanned: skipped"
  else
    case $D in 23.0|22.9375) OPT="--window=-0.10:0.30:0.02 --rep=0.10";; *) OPT="--auto";; esac
    say "starting D $D ($OPT)"
    env NP=4 NICE=15 bash $L/pipeline87_post23.sh $D $OPT; say "pipeline87_post23.sh D $D returned $?"
    [ -e $L/$D/SCAN_DONE.txt ] || { tell "macm3 #1025 post23_scans STOP: the scan of D $D did not finish (no SCAN_DONE.txt; see $D/pipeline.log, $D/steps.txt); the hold stays"; exit 1; }
  fi
  n=0; until have_root $D; do n=$((n+1)); [ $n -gt 40 ] && { tell "macm3 #1025 post23_scans STOP: no root of D $D in roots87.txt 20 min after the scan (the chain's record may have stopped: see chain.log); the hold stays"; exit 1; }; sleep 30; done
  say "D $D: root recorded: $(grep "^$D " $L/roots87.txt | tail -1)"
done
for f in $L/HOLD*.txt; do [ -e "$f" ] && mv "$f" "$f.released.$(date +%s)"; done
echo "$(date -u '+%F %T') UTC HOLD released after the ordered scans of D 23.0 to D 22.375 (t5's order, 25 Nov)" >> $L/chain.log
tell "macm3 #1025 post23_scans: all ten points (D 23.0, 22.9375, 22.875, 22.8125, 22.75, 22.6875, 22.625, 22.5625, 22.5, 22.375) have a root (roots87.txt); the chain's hold (HOLD_low2.txt, HOLD_refine.txt) is released: the chain continues with the points between (phase 2)."
