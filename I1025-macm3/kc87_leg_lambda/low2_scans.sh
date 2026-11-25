#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov ~04:4x UTC): the low-lambda scans (0.02 to 0.18 by 0.02 + a repeat of 0.10) of D 22.1875, then D 22.15625, then D 22.21875, after low_scans.sh has ended (D 22.25 and D 22.125); then HOLD_low2.txt is moved aside.
# If an earlier driver stopped on an error nothing is started and the holds stay. Log: low2_scans.log.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
say() { echo "$(date -u '+%F %T') UTC low2_scans: $*" >> $L/low2_scans.log; }
say "waiting for low_scans.sh (low_scans.log)"
while ! grep -qE "HOLD_low released|STOP" $L/low_scans.log 2>/dev/null; do sleep 30; done
grep -q "STOP" $L/low_scans.log && { say "low_scans.sh stopped on an error: nothing started, the holds stay"; exit 1; }
for DN in 22.1875_low 22.15625_low 22.21875_low; do
  say "starting $DN"
  bash $L/pipeline87_rescan.sh $DN; say "pipeline87_rescan.sh $DN returned $?"
  [ -e $L/$DN/SCAN_DONE.txt ] || { say "STOP: $DN has no SCAN_DONE.txt; HOLD_low2.txt stays"; exit 1; }
done
if [ -e $L/HOLD_low2.txt ]; then mv $L/HOLD_low2.txt $L/HOLD_low2.txt.released.$(date +%s); echo "$(date -u '+%F %T') UTC HOLD_low2 released after the low-lambda scans of D 22.1875, 22.15625 and 22.21875 (t5's orders, 25 Nov)" >> $L/chain.log; say "HOLD_low2 released"; fi
