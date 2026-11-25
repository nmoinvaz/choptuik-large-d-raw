#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov): the wide scans lambda 0.20 to 0.50 by 0.02 + a repeat of 0.44 at D 22.25 and then at D 22.125, after D 22.1875's scan (between_22.log has both pipelines returned); then the chain's HOLD is released
# (t5 had ordered it after the two in-between points; the wide scans go first so that D 22.375 does not take the scan lock before them). Log: wide_scans.log.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
say() { echo "$(date -u '+%F %T') UTC wide_scans: $*" >> $L/wide_scans.log; }
say "waiting for D 22.15625 and D 22.1875 (between_22.log)"
while [ "$(grep -c returned $L/between_22.log 2>/dev/null)" != 2 ]; do sleep 30; done
for DN in 22.25_wide 22.125_wide; do
  say "starting $DN"
  bash $L/pipeline87_rescan.sh $DN; say "pipeline87_rescan.sh $DN returned $?"
  [ -e $L/$DN/SCAN_DONE.txt ] || { say "STOP: $DN has no SCAN_DONE.txt; HOLD stays"; exit 1; }
done
if [ -e $L/HOLD.txt ]; then mv $L/HOLD.txt $L/HOLD.txt.released.$(date +%s); echo "$(date -u '+%F %T') UTC HOLD released after the in-between roots and the two wide scans (t5's orders, 25 Nov)" >> $L/chain.log; say "HOLD released"; fi
