#!/bin/bash
# t5's ruling (hc 27 Nov 01:51 UTC, kept 04:21 UTC): the k_c 87 chain stays held through both k_c 143 lanes and is released for good once the D 23.125 lane ends.
# Waits for the lane's normal end (its hc line "kc143_d23125 done:", written only after a secant exit 0 or 4), then renames every HOLD_kc143*.txt in the chain's folder to <name>.released.<epoch> (no deletion) and tells t5.
# If the lane ends without that line (a STOP, a scan with no or several robust changes, the lane gone), the hold stays and t5 is told. Nothing else is touched.
NAME=${NAME:-kc143_d23125}
LG=${LG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/$NAME/exits_kc143.txt}
HDIR=${HDIR:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda}
LANEPAT=${LANEPAT:-$NAME/lane_d23125.sh}; HC=${HC:-$(command -v hc)}; POLL=${POLL:-30}; WAITH=${WAITH:-14}; AFTER=${AFTER:-150}; REPWAIT=${REPWAIT:-1800}; CHAINPAT=${CHAINPAT:-d18_hybsign[.]py|d18_secant[.]py scan}
stamp() { date -u '+%F %T UTC'; }
tell() { echo "$(stamp) hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" 2>&1 | tail -1; }
procs() { ps -axo rss=,ni=,command= | awk -v pat="$1" '{r=$1; $1=""; $2=""; c=substr($0,3); if (c ~ /^[^ ]*[Pp]ython[^ ]* / && c ~ pat) print r}'; }
END=$(( $(date +%s) + WAITH * 3600 ))
while :; do
  grep -q "$NAME done:" "$LG" 2>/dev/null && break
  if ! pgrep -f "$LANEPAT" > /dev/null; then
    sleep 5; grep -q "$NAME done:" "$LG" 2>/dev/null && break
    echo "$(stamp) the $NAME lane is gone without its done line: the hold stays"
    tell "macm3 #1025 (release watcher, $(stamp)): the $NAME lane ended without its 'done' line (a stop, or a scan with no or several robust changes); the k_c 87 chain stays HELD (HOLD_kc143*.txt not touched). Your word."
    exit 0
  fi
  [ $(date +%s) -gt $END ] && { echo "$(stamp) gave up waiting"; exit 0; }
  sleep $POLL
done
T=$(date +%s); n=0; names=""
for h in "$HDIR"/HOLD_kc143*.txt; do
  [ -e "$h" ] || continue
  case "$h" in *.released.*) continue;; esac
  mv "$h" "$h.released.$T" && { n=$((n+1)); names="$names $(basename "$h")"; }
done
ls "$HDIR"/HOLD* 2>/dev/null
tell "macm3 #1025 (release watcher, $(stamp)): the $NAME lane has ended normally (its done line); the k_c 87 chain is RELEASED for good: $n hold file(s) renamed to .released.$T (${names# }). The chain's report follows when its scan has started."
t0=$(date +%s); while [ $(( $(date +%s) - t0 )) -lt $REPWAIT ]; do
  c=$(procs "$CHAINPAT" | wc -l | tr -d ' ')
  if [ "$c" -gt 0 ]; then sleep $AFTER; c=$(procs "$CHAINPAT" | wc -l | tr -d ' '); RS=$(procs "$CHAINPAT" | awk '{s += $1} END {printf "%.2f", s/1048576}')
    tell "macm3 #1025 (release watcher, $(stamp)): the chain's scan has started: $c scan processes, RSS sum $RS GiB; $(grep 'next:' "$HDIR/chain.log" 2>/dev/null | tail -1 | cut -c1-200)"; exit 0; fi
  sleep $POLL
done
tell "macm3 #1025 (release watcher, $(stamp)): HOLD_kc143 was released, but no chain scan process appeared within $((REPWAIT/60)) min; $(tail -n 2 "$HDIR/chain.log" 2>/dev/null | cut -c1-200 | tr '\n' ' ')"
exit 0
