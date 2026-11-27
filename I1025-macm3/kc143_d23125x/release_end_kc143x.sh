#!/bin/bash
# t5's order (#1025 comment 7213649039): the k_c 87 chain holds until the cross-path check kc143_d23125x ends. At the lane's normal end (its hc line "kc143_d23125x done:", written by lane_d23125x.sh after a secant exit 0 or 4, or by
# ext_d23125x.sh after the extension scan's secant) this watcher renames every HOLD_kc143*.txt in the chain's folder to <name>.released.<epoch> (no deletion), STARTS THE CHAIN DRIVER AGAIN (scan_chain.sh was killed at 08:35:02 UTC
# with the D 22.3125 scan; chain_next.py then picks D 22.3125 again) and tells t5. If the lane (and the extension watcher) end without that line (a STOP, a result not accepted, a scan with several robust changes or a mixed reading,
# the lane gone) the hold stays, the driver stays dead, and t5 is told. Nothing else is touched. Test knobs (env): NAME LG HDIR LANEPAT HC POLL WAITH AFTER REPWAIT CHAINPAT DRIVER DRIVERPAT LAUNCH.
NAME=${NAME:-kc143_d23125x}
LG=${LG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/$NAME/exits_kc143.txt}
HDIR=${HDIR:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda}
LANEPAT=${LANEPAT:-$NAME/(lane_d23125x|ext_d23125x)[.]sh}; HC=${HC:-$(command -v hc)}; POLL=${POLL:-30}; WAITH=${WAITH:-14}; AFTER=${AFTER:-150}; REPWAIT=${REPWAIT:-1800}; CHAINPAT=${CHAINPAT:-d18_hybsign[.]py|d18_secant[.]py scan}
DRIVER=${DRIVER:-$HDIR/scan_chain.sh}; DRIVERPAT=${DRIVERPAT:-kc87_leg_lambda/scan_chain[.]sh}
LAUNCH=${LAUNCH:-python3 $HOME/Source/choptuik-large-d-raw-903/I1025-macm3/$NAME/in/launch_1070.py}
stamp() { date -u '+%F %T UTC'; }
tell() { echo "$(stamp) hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" 2>&1 | tail -1; }
procs() { ps -axo rss=,ni=,command= | awk -v pat="$1" '{r=$1; $1=""; $2=""; c=substr($0,3); if (c ~ /^[^ ]*[Pp]ython[^ ]* / && c ~ pat) print r}'; }
END=$(( $(date +%s) + WAITH * 3600 ))
while :; do
  grep -q "$NAME done:" "$LG" 2>/dev/null && break
  if ! pgrep -f "$LANEPAT" > /dev/null; then
    sleep 5; grep -q "$NAME done:" "$LG" 2>/dev/null && break
    echo "$(stamp) the $NAME lane is gone without its done line: the hold stays"
    tell "macm3 #1025 (release watcher, $(stamp)): the $NAME lane ended without its 'done' line (a stop, a result not accepted, or a scan that the extension watcher does not cover); the k_c 87 chain stays HELD (HOLD_kc143*.txt not touched) and its driver scan_chain.sh stays stopped. Your word."
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
if pgrep -f "$DRIVERPAT" > /dev/null; then dr="the chain driver was already running (pid $(pgrep -f "$DRIVERPAT" | head -1))"
else dp=$($LAUNCH $HDIR/chain.out -- caffeinate -is nice -n 15 bash $DRIVER 2>&1 | tail -1); sleep 3
  if pgrep -f "$DRIVERPAT" > /dev/null; then dr="the chain driver scan_chain.sh was started again (launch pid $dp, now pid $(pgrep -f "$DRIVERPAT" | head -1))"; else dr="THE CHAIN DRIVER DID NOT START (launch said '$dp')"; fi
fi
tell "macm3 #1025 (release watcher, $(stamp)): the $NAME lane has ended normally (its done line); the k_c 87 chain is RELEASED for good: $n hold file(s) renamed to .released.$T (${names# }); $dr. The chain's report follows when its scan has started."
t0=$(date +%s); while [ $(( $(date +%s) - t0 )) -lt $REPWAIT ]; do
  c=$(procs "$CHAINPAT" | wc -l | tr -d ' ')
  if [ "$c" -gt 0 ]; then sleep $AFTER; c=$(procs "$CHAINPAT" | wc -l | tr -d ' '); RS=$(procs "$CHAINPAT" | awk '{s += $1} END {printf "%.2f", s/1048576}')
    tell "macm3 #1025 (release watcher, $(stamp)): the chain's scan has started: $c scan processes, RSS sum $RS GiB; $(grep 'next:' "$HDIR/chain.log" 2>/dev/null | tail -1 | cut -c1-200)"; exit 0; fi
  sleep $POLL
done
tell "macm3 #1025 (release watcher, $(stamp)): HOLD_kc143x was released, but no chain scan process appeared within $((REPWAIT/60)) min; $(tail -n 2 "$HDIR/chain.log" 2>/dev/null | cut -c1-200 | tr '\n' ' ')"
exit 0
