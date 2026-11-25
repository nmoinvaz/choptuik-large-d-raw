#!/bin/bash
# #1025 macm3 (t5, hc 25 Nov after 15:53 UTC, quoted): "keep D 22.75 at 0.02 as queued. For the rest use 0.04 (-0.10 to 0.50, 16 points + a repeat) and only D 22.5 and D 22.625; skip 22.6875, 22.5625 and 22.375 for now.
# Refine F locally (0.01 around its bracket) only where its 0.04 bracket is ambiguous."
# Runs after post23_scans3.sh has ended (its (a), (b) and D 22.75 on 0.02): D 22.5 (part b2) and D 22.625 (part c) on -0.10 to 0.50 by 0.04 with a repeat of 0.30 (17 evaluations, 5 rounds). Same steps as post23_scans3.sh.
# A reading without exactly two changes ('- to +' then '+ to -') is not guessed: hc to t5 (the 0.01 refinement is decided by hand), roots87.txt unchanged for that D, and the next D is scanned.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc); LOG=$L/post23_scans.log
say() { echo "$(date -u '+%F %T') UTC post23_scans4: $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
stopp() { tell "macm3 #1025 post23_scans4 STOP: $*; the hold stays, nothing further is scanned"; exit 1; }
cd $L || exit 9
python3 label_roots.py selftest > /dev/null 2>&1 || stopp "label_roots.py selftest fails"
python3 mkF.py selftest > /dev/null 2>&1 || stopp "mkF.py selftest fails"
python3 mkF.py selftest --mutate=grid > /dev/null 2>&1 && stopp "mkF.py selftest --mutate=grid passed (it must fail)"
say "started: waiting for post23_scans3.sh to end"
while pgrep -f "kc87_leg_lambda/post23_scans3.sh" > /dev/null; do sleep 20; done
[ -e $L/22.75_both/SCAN_DONE.txt ] && grep -q '^22.75 .* F$' $L/roots87.txt || stopp "post23_scans3.sh ended without the D 22.75 both-roots scan labeled (see post23_scans.log)"
run_scan() {   # KIND (D@step)
  kind=$1; D=${kind%@*}
  fe=$(python3 mkF.py setup $kind) || stopp "mkF.py setup $kind failed"
  say "starting $fe"
  env NP=4 NICE=15 bash $L/pipeline87_rescan.sh $fe; say "pipeline87_rescan.sh $fe returned $?"
  [ -e $L/$fe/SCAN_DONE.txt ] || stopp "the scan $fe did not finish (see $fe/pipeline.log, $fe/steps.txt)"
  rd=$(python3 mkF.py read $kind) || stopp "mkF.py read $kind failed"
  out=$(python3 label_roots.py $D $rd); rc=$?
  say "label_roots $D: $out"
  bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: $fe scanned, read merged, roots labeled" >> $LOG 2>&1; say "pushed ($?)"
  if [ $rc = 0 ]; then tell "macm3 #1025 kc87 leg2 $fe read: $out"
  else tell "macm3 #1025 kc87 leg2 $fe read, NOT labeled (no guess; the 0.01 refinement is for you or me to order): $out (reading $rd)"; fi
}
run_scan 22.5@0.04; run_scan 22.625@0.04
tell "macm3 #1025 post23_scans4: D 22.5 and D 22.625 on 0.04 are done (22.6875, 22.5625 and 22.375 skipped as ordered); the chain hold stays"
