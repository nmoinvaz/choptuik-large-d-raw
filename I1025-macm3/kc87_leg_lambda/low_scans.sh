#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov): the low-lambda scans, lambda 0.02 to 0.18 by 0.02 + a repeat of 0.10, at D 22.25 and then at D 22.125, after the D 22.125 wide scan (wide_scans.log says HOLD released); then HOLD_low.txt is moved aside
# (the chain starts nothing while any HOLD*.txt exists). If the wide scans stopped on an error nothing is started and both holds stay. Log: low_scans.log.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
say() { echo "$(date -u '+%F %T') UTC low_scans: $*" >> $L/low_scans.log; }
say "waiting for the wide scans (wide_scans.log)"
while ! grep -qE "HOLD released|STOP" $L/wide_scans.log 2>/dev/null; do sleep 30; done
grep -q "STOP" $L/wide_scans.log && { say "the wide scans stopped on an error: nothing started, the holds stay"; exit 1; }
for DN in 22.25_low 22.125_low; do
  say "starting $DN"
  bash $L/pipeline87_rescan.sh $DN; say "pipeline87_rescan.sh $DN returned $?"
  [ -e $L/$DN/SCAN_DONE.txt ] || { say "STOP: $DN has no SCAN_DONE.txt; HOLD_low.txt stays"; exit 1; }
done
if [ -e $L/HOLD_low.txt ]; then mv $L/HOLD_low.txt $L/HOLD_low.txt.released.$(date +%s); echo "$(date -u '+%F %T') UTC HOLD_low released after the low-lambda scans of D 22.25 and D 22.125 (t5's orders, 25 Nov)" >> $L/chain.log; say "HOLD_low released"; fi
