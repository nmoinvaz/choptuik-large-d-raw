#!/usr/bin/env bash
# exits when ks_chain3 has a new converged step record, an alert line, or the chain's exit line (arg 1: step records already seen)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
touch alerts966.txt; e0=$(grep -c '^966 ks_chain3[bc0]* exit' exits_966.txt); seen=${1:-0}; a0=$(wc -l < alerts966.txt 2>/dev/null || echo 0)
while sleep 20; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -ge $((seen + ${2:-1})) ] && { echo "STEP records $n"; exit 0; }
  a=$(wc -l < alerts966.txt 2>/dev/null || echo 0)
  [ "$a" -gt "$a0" ] && { echo "ALERT"; tail -n $((a-a0)) alerts966.txt; exit 0; }
  [ "$(grep -c '^966 ks_chain3[bc0]* exit' exits_966.txt)" -gt "$e0" ] && { echo "CHAIN EXIT"; grep '^966 ks_chain3' exits_966.txt | tail -2; exit 0; }
  grep -q '^Traceback' ks_chain3b/leg*/anm_run.log ks_chain3b.log 2>/dev/null && { echo TRACEBACK; exit 0; }
done
