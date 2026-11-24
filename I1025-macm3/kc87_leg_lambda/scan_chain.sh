#!/bin/bash
# #1025 macm3: the scan chain of the k_c 87 leg2 (t5's orders of 24 Nov: every leg point is scanned with 4 processes at nice 15, the latest-local-slope rule, the -0.33 rule scored beside it; report each root).
# Loop: record the root of every finished scan (chain_next.py record: one robust change, all noise-robust, repeat PASS, else STOP) and hc it; wait while a scan runs; start the next pushed point (pipeline87.sh with the slope
# from my two latest roots); stop on any anomaly (hc to t5), finish when both parts of the leg are done and every point has a root. Log: chain.log. Started by launch_1070.py under caffeinate -is nice -n 15.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
HC=$(command -v hc)
LOG=$L/chain.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
cd $L || exit 9
say "chain starts; chain_next.py selftest: $(python3 chain_next.py selftest > /dev/null 2>&1; echo exit $?), mutations $(for m in slope changes repeat robust; do python3 chain_next.py selftest --mutate=$m > /dev/null 2>&1; echo -n "$? "; done)(1 wanted each)"
python3 chain_next.py selftest > /dev/null 2>&1 || { tell "macm3 #1025 chain STOP: chain_next.py selftest fails"; exit 1; }
for m in slope changes repeat robust; do python3 chain_next.py selftest --mutate=$m > /dev/null 2>&1 && { tell "macm3 #1025 chain STOP: chain_next.py selftest --mutate=$m passed (must fail)"; exit 1; }; done
while :; do
  for D in $(python3 chain_next.py pending); do
    out=$(python3 chain_next.py record $D)
    case "$out" in
      OK*) tell "$out";;
      *) tell "macm3 #1025 chain STOP (not scanning on): $out"; exit 1;;
    esac
  done
  if pgrep -f "pipeline87.sh|rescan87.sh" > /dev/null; then sleep 30; continue; fi
  nxt=$(python3 chain_next.py next)
  case "$nxt" in
    NEXT*)
      set -- $nxt; D=$2; PD=$3; PR=$4; SL=$5; SRC=$6; TAG=$7
      say "next: D $D (previous D $PD, root $PR, local slope $SL, source $SRC, tag $TAG)"
      env SRC=$SRC TAG=$TAG NP=4 NICE=15 SL2=-0.33 bash $L/pipeline87.sh $D $PD $PR $SL
      say "pipeline87.sh D $D returned $?"
      [ -e $L/$D/SCAN_DONE.txt ] || { tell "macm3 #1025 chain STOP: the scan of D $D did not finish (no SCAN_DONE.txt; see $D/pipeline.log, $D/steps.txt)"; exit 1; };;
    DONE*) say "done: both parts finished and every point has a root"; tell "macm3 #1025 chain: every leg2 point has a root (see roots87.txt); chain ends"; exit 0;;
    *) sleep 60;;
  esac
done
