#!/usr/bin/env bash
# leg 14 pause watch (coordinator 2026-11-21 18:18 UTC, #903 comment 7067155180): wakes on a new accepted state (STEP), on a comment since $SINCE that names xfchecks' reading
# ("reading_real" or "path reading", not my own posts and not the coordinator's order 7067155180), on the cap time $CAP (UTC), and on the usual triggers (bar skip, FAILED re-seed, stalled
# or refused corrector, a non-refinement alert, a chain exit, a Traceback). usage: bash wait966z.sh SEEN N LEGDIR BAR_BASE FAILED_BASE STALL_BASE [CAP='2026-11-22 04:18:00'] [SINCE=2026-11-21T18:19:00Z]
cd /home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370 || exit 9
LG=ks_chain3b/$3/anm_run.log; bb=${4:-0}; fb=${5:-0}; sb=${6:-0}
CAPTS=$(date -u -d "${7:-2026-11-22 04:18:00}" +%s); SINCE=${8:-2026-11-21T18:19:00Z}
touch alerts966.txt; e0=$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt); a0=$(wc -l < alerts966.txt); lastgh=0
Q='[.[]|select((.body|test("reading_real|path reading";"i")) and (.id!=7067155180) and (.id!=7060114909) and (.id!=7067019274) and (.id!=7066990195) and ((.body|startswith("ks_chain3b (dh370"))|not) and ((.body|startswith("dh370"))|not))]'
while sleep 15; do
  n=$(cat ks_chain3b/leg*/anm_run.jsonl 2>/dev/null | grep -c '"converged": true')
  [ "$n" -ge $(( $1 + ${2:-1} )) ] && { echo "STEP records $n"; exit 0; }
  [ "$(date -u +%s)" -ge "$CAPTS" ] && { echo "CAP TIME $(date -u '+%F %T') >= ${7:-2026-11-22 04:18:00}"; exit 0; }
  now=$(date +%s)
  if [ $((now - lastgh)) -ge 150 ]; then lastgh=$now
    hits=$(gh api "repos/nmoinvaz/choptuik-large-d/issues/comments?since=$SINCE&per_page=100" --jq "$Q|length" 2>/dev/null)
    if [ "${hits:-0}" -gt 0 ]; then echo "READING candidates ($hits)"; gh api "repos/nmoinvaz/choptuik-large-d/issues/comments?since=$SINCE&per_page=100" --jq "$Q|.[]|{id,created_at,url:.html_url,head:(.body[:300])}" 2>/dev/null; exit 0; fi
    # xfchecks' running per-base table (#966 comment 7060114909, edited as bases land): wake when it lists two bases at D 263.5 or more
    rows=$(gh api repos/nmoinvaz/choptuik-large-d/issues/comments/7060114909 --jq .body 2>/dev/null | grep -cE '^\| (263\.[5-9]|26[4-9]\.)')
    [ "${rows:-0}" -ge 2 ] && [ "${rows:-0}" -gt "${TROWS:-1}" ] && { echo "xfchecks TABLE lists $rows bases at D >= 263.5 (comment 7060114909): look for its reading"; exit 0; }
  fi
  b=$(grep -c 'above --reseed_o_bar' $LG 2>/dev/null)
  [ "${b:-0}" -gt "$bb" ] && { echo "reseed_o_bar SKIP ($b > $bb)"; grep -n 'above --reseed_o_bar' $LG | tail -2 | cut -c1-240; exit 0; }
  f=$(grep -c 're-seeded (FAILED' $LG 2>/dev/null)
  [ "${f:-0}" -gt "$fb" ] && { echo "NEW FAILED re-seed ($f > $fb)"; grep 're-seeded (FAILED' $LG | tail -2 | cut -c1-220; exit 0; }
  sc=$(grep -cE 'stopping \(stalled\)|no trial step accepted|attempt stopped|octo-double Newton: [0-9]+ steps, max\|F\| [0-9.e+-]+, not converged' $LG 2>/dev/null)
  if [ "${sc:-0}" -gt "$sb" ]; then echo "TRIGGER (stall or refusal) $sc > $sb"; grep -nE 'stopping \(stalled\)|no trial step accepted|attempt stopped|not converged' $LG | tail -3 | cut -c1-200; exit 0; fi
  a=$(wc -l < alerts966.txt)
  if [ "$a" -gt "$a0" ]; then new=$(tail -n $((a-a0)) alerts966.txt); a0=$a; rest=$(echo "$new" | grep -v 'refinement ended at rung'); [ -n "$rest" ] && { echo "ALERT"; echo "$rest"; exit 0; }; fi
  [ "$(grep -c '^966 ks_chain3[a-z0-9]* exit' exits_966.txt)" -gt "$e0" ] && { echo "CHAIN EXIT"; grep '^966 ks_chain3' exits_966.txt | tail -2; exit 0; }
  grep -qs '^Traceback' $LG ks_chain3b.log ks_chain3b_s.log && { echo TRACEBACK; exit 0; }
done
