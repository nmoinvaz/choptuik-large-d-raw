#!/usr/bin/env bash
# #966 floor-rule triggers (coordinator's hc 2026-11-19): wakes on a new accepted step (check its final |F| against 1e-34), on a stalled or not converged corrector, on a refused attempt
# ('re-seeded (FAILED' or 'attempt stopped' in a leg from $3 on), on 4 or more iteration lines in one attempt, a non-routine alert or WALL, a chain exit or a Traceback.
# usage: bash wait966c.sh SEEN N LEG0
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
touch alerts966.txt; e0=$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt); a0=$(wc -l < alerts966.txt 2>/dev/null || echo 0); seen=${1:-0}; leg0=${3:-leg06}
while sleep 15; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -ge $((seen + ${2:-1})) ] && { echo "STEP records $n"; exit 0; }
  for lg in ks_chain3b/leg*/anm_run.log; do
    leg=$(basename $(dirname $lg)); [[ "$leg" < "$leg0" ]] && continue
    if grep -qE 'stopping \(stalled\)|no trial step accepted|octo-double Newton: [0-9]+ steps, max\|F\| [0-9.e+-]+, not converged|re-seeded \(FAILED|attempt stopped' $lg; then echo "TRIGGER (stall or refusal) in $lg"; grep -nE 'stopping \(stalled\)|no trial step accepted|not converged|re-seeded \(FAILED|attempt stopped' $lg | tail -3 | cut -c1-200; exit 0; fi
    k=$(awk '/a_rule reseed:/{c=0} /^  on [0-9]+: \|F\| .* -> /{c++} END{print c+0}' $lg)
    [ -z "$NOCRAWL" ] && [ "$k" -ge 4 ] && { echo "CRAWL: $k iteration lines in the attempt of $lg"; grep -E '^  on [0-9]+: \|F\| ' $lg | tail -4 | cut -c1-200; exit 0; }
  done
  a=$(wc -l < alerts966.txt 2>/dev/null || echo 0)
  if [ "$a" -gt "$a0" ]; then
    new=$(tail -n $((a-a0)) alerts966.txt); a0=$a
    rest=$(echo "$new" | grep -v 'FAILED' | grep -vE 'refinement ended at rung max\|R\| [0-9.]+e-(19|[2-9][0-9]),')
    if [ -n "$rest" ] || echo "$new" | grep -q 'WALL'; then echo "ALERT"; echo "$new"; exit 0; fi
  fi
  [ "$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt)" -gt "$e0" ] && { echo "CHAIN EXIT"; grep '^966 ks_chain3' exits_966.txt | tail -2; exit 0; }
  grep -q '^Traceback' ks_chain3b/leg*/anm_run.log ks_chain3b.log 2>/dev/null && { echo TRACEBACK; exit 0; }
done
