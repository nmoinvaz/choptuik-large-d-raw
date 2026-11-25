#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~05:4x UTC; replaces low2_scans.sh and refine_scans.sh, stopped by their exact pids): the scans in t5's order: (1) D 22.21875 lambda 0.02 to 0.50 by 0.02 + a repeat of 0.10, (2) D 22.1875 lambda 0.20 to 0.44 by 0.02
# + a repeat of 0.32, (3) D 22.15625 lambda 0.50 to 0.70 by 0.02 (+ a repeat of 0.60), then the queued D 22.25 refinement (0.100 to 0.120 by 0.0025 + a repeat of 0.110); then HOLD_low2.txt and HOLD_refine.txt are moved aside
# (the chain starts nothing while any HOLD*.txt exists). A scan that fails stops the queue and the holds stay. Log: queue3_scans.log.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
say() { echo "$(date -u '+%F %T') UTC queue3_scans: $*" >> $L/queue3_scans.log; }
for DN in 22.21875_full 22.1875_mid 22.15625_high 22.25_refine; do
  say "starting $DN"
  bash $L/pipeline87_rescan.sh $DN; say "pipeline87_rescan.sh $DN returned $?"
  [ -e $L/$DN/SCAN_DONE.txt ] || { say "STOP: $DN has no SCAN_DONE.txt; the holds stay"; exit 1; }
done
for H in HOLD_low2 HOLD_refine; do
  [ -e $L/$H.txt ] && mv $L/$H.txt $L/$H.txt.released.$(date +%s) && echo "$(date -u '+%F %T') UTC $H released after the queue of scans of D 22.21875, 22.1875, 22.15625 and 22.25 (t5's orders, 25 Nov)" >> $L/chain.log
done
say "holds released"
