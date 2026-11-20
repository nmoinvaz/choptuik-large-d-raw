#!/usr/bin/env bash
# fallback leg (ks 293, unit i966r): wakes on a new accepted step, a NEW 're-seeded (FAILED' line beyond the baseline count, a stalled or refused corrector, a new non-refinement alert, a chain exit or a Traceback.
# usage: bash wait966m.sh SEEN N LEGDIR FAILED_BASE STALL_BASE     e.g. bash wait966m.sh 46 1 leg12_D260.8483_ks293 1 1   (the known lines are the baselines)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
LG=ks_chain3b/$3/anm_run.log; fb=${4:-0}; sb=${5:-0}
touch alerts966.txt; e0=$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt); a0=$(wc -l < alerts966.txt)
while sleep 15; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -ge $(( $1 + ${2:-1} )) ] && { echo "STEP records $n"; exit 0; }
  f=$(grep -c 're-seeded (FAILED' $LG 2>/dev/null)
  [ "${f:-0}" -gt "$fb" ] && { echo "NEW FAILED re-seed ($f > $fb)"; grep 're-seeded (FAILED' $LG | tail -2 | cut -c1-220; exit 0; }
  sc=$(grep -cE 'stopping \(stalled\)|no trial step accepted|attempt stopped|octo-double Newton: [0-9]+ steps, max\|F\| [0-9.e+-]+, not converged' $LG 2>/dev/null)
  if [ "${sc:-0}" -gt "$sb" ]; then echo "TRIGGER (stall or refusal) $sc > $sb"; grep -nE 'stopping \(stalled\)|no trial step accepted|attempt stopped|not converged' $LG | tail -3 | cut -c1-200; exit 0; fi
  a=$(wc -l < alerts966.txt)
  if [ "$a" -gt "$a0" ]; then new=$(tail -n $((a-a0)) alerts966.txt); a0=$a; echo "ALERT"; echo "$new"; exit 0; fi
  [ "$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt)" -gt "$e0" ] && { echo "CHAIN EXIT"; grep '^966 ks_chain3' exits_966.txt | tail -2; exit 0; }
  grep -qs '^Traceback' $LG ks_chain3b.log && { echo TRACEBACK; exit 0; }
done
