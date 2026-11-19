#!/usr/bin/env bash
# #966 tol_od 1.5e-35 test (coordinator's hc 2026-11-19): wakes on N more accepted step records, on a stalled or refused corrector of the attempts of legs from $3 on
# (a 'stopping (stalled)' line, 'no trial step accepted', 'octo-double Newton: ... not converged', or 4 or more iteration lines '  on K: |F| a -> b' in one attempt
# or in the base polish), on a non-routine alert or WALL, on the chain's exit line, or on a Traceback. usage: bash wait966b.sh SEEN N LEG0   (e.g. 16 1 leg05)
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
touch alerts966.txt; e0=$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt); seen=${1:-0}; a0=$(wc -l < alerts966.txt 2>/dev/null || echo 0); leg0=${3:-leg05}
while sleep 15; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -ge $((seen + ${2:-1})) ] && { echo "STEP records $n"; exit 0; }
  for lg in ks_chain3b/leg*/anm_run.log; do
    leg=$(basename $(dirname $lg)); [[ "$leg" < "$leg0" ]] && continue
    if grep -qE 'stopping \(stalled\)|no trial step accepted|octo-double Newton: [0-9]+ steps, max\|F\| [0-9.e+-]+, not converged' $lg; then echo "STALL or not converged in $lg"; grep -nE 'stopping \(stalled\)|no trial step accepted|not converged' $lg | tail -3 | cut -c1-200; exit 0; fi
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
