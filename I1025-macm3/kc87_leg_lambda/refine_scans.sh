#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~05:1x UTC): the refinement of D 22.25's second root, lambda 0.100 to 0.120 by 0.0025 + a repeat of 0.110, after low2_scans.sh has ended (the three low scans); then HOLD_refine.txt is moved aside. Log: refine_scans.log.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
say() { echo "$(date -u '+%F %T') UTC refine_scans: $*" >> $L/refine_scans.log; }
say "waiting for low2_scans.sh (low2_scans.log)"
while ! grep -qE "HOLD_low2 released|STOP" $L/low2_scans.log 2>/dev/null; do sleep 30; done
grep -q "STOP" $L/low2_scans.log && { say "low2_scans.sh stopped on an error: nothing started, the holds stay"; exit 1; }
DN=22.25_refine
say "starting $DN"
bash $L/pipeline87_rescan.sh $DN; say "pipeline87_rescan.sh $DN returned $?"
[ -e $L/$DN/SCAN_DONE.txt ] || { say "STOP: $DN has no SCAN_DONE.txt; HOLD_refine.txt stays"; exit 1; }
if [ -e $L/HOLD_refine.txt ]; then mv $L/HOLD_refine.txt $L/HOLD_refine.txt.released.$(date +%s); echo "$(date -u '+%F %T') UTC HOLD_refine released after the refinement scan of D 22.25 (t5's order, 25 Nov)" >> $L/chain.log; say "HOLD_refine released"; fi
