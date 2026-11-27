#!/bin/bash
# t5's standing order of 26 Nov 20:35 UTC for the k_c 135 D 23.125 lane, carried to the k_c 143 lanes as "hold it as before" (hc 27 Nov 01:38 UTC): the k_c 87 chain is held through the regrid and the scan; when the scan has
# ended and only the 1-process secant runs, release it and report. Derived from kc135_d23125/release_hold_low2.sh (sandbox-tested there), with the names of this lane and one more step: when the secant ends, the hold is placed
# again (HOLD_kc143b.txt) so that the next k_c 143 lane (D 23.125) starts without waiting for another chain scan; the next lane's launch (or t5's word) renames it.
# Waits for the line "<NAME>: secant starts:" in the lane's exits file, checks that no scan process runs and that at least MINAVAIL GiB are available, then renames HOLD_kc143.txt to HOLD_kc143.txt.released.<epoch>
# (no deletion), tells t5, reports the chain's process count and memory when its scan has started, then waits for "<NAME>: secant exit" and re-places the hold. Nothing else is touched.
NAME=${NAME:-kc143_d230625}
LG=${LG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/$NAME/exits_kc143.txt}
HOLD=${HOLD:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/HOLD_kc143.txt}
REHOLD=${REHOLD:-$(dirname "$HOLD")/HOLD_kc143b.txt}
CLOG=${CLOG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/chain.log}
SCANPAT=${SCANPAT:-d18_hybsign[.]py|d18_secant[.]py scan}; CHAINPAT=${CHAINPAT:-d18_hybsign[.]py}
HC=${HC:-$(command -v hc)}; POLL=${POLL:-30}; MINAVAIL=${MINAVAIL:-8}; LANEPAT=${LANEPAT:-$NAME/lane_d230625.sh}; WAITH=${WAITH:-30}; AFTER=${AFTER:-120}; REPWAIT=${REPWAIT:-1800}; SETTLE=${SETTLE:-20}
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
# python processes only (a shell command that merely contains the name is not a scan process): prints "rss ni" per match of the pattern, capped_run's wrapper excluded
procs() { ps -axo rss=,ni=,command= | awk -v pat="$1" '{r=$1; n=$2; $1=""; $2=""; c=substr($0,3); if (c ~ /^[^ ]*[Pp]ython[^ ]* / && c ~ pat && c !~ /capped_run/) print r, n}'; }
stamp() { date -u '+%F %T UTC'; }
tell() { echo "$(stamp) hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" 2>&1 | tail -1; }
END=$(( $(date +%s) + WAITH * 3600 ))
while :; do
  grep -q "$NAME: secant starts:" "$LG" 2>/dev/null && break
  pgrep -f "$LANEPAT" > /dev/null || { echo "$(stamp) the $NAME lane is gone and no secant started: HOLD_kc143 NOT released"; tell "macm3 #1025 (release watcher, $(stamp)): the $NAME lane ended without starting its secant; HOLD_kc143 NOT released (see $NAME/exits_kc143.txt)"; exit 0; }
  [ $(date +%s) -gt $END ] && { echo "$(stamp) gave up waiting"; exit 0; }
  sleep $POLL
done
sleep $SETTLE      # let the scan's processes finish
SCANP=$(procs "$SCANPAT" | wc -l | tr -d ' ')
AV=$(availgib)
if [ "$SCANP" != 0 ] || ! python3 -c "import sys; sys.exit(0 if $AV >= $MINAVAIL else 1)"; then
  tell "macm3 #1025 (release watcher, $(stamp)): the $NAME secant started, but HOLD_kc143 NOT released: $SCANP scan processes still run, $AV GiB available (wanted 0 and at least $MINAVAIL). Held; your word."
  exit 0
fi
T=$(date +%s); mv "$HOLD" "$HOLD.released.$T" && REL="$(stamp)" || { tell "macm3 #1025 (release watcher, $(stamp)): the rename of HOLD_kc143.txt failed; held"; exit 1; }
ls "$(dirname "$HOLD")"/HOLD* 2>/dev/null
tell "macm3 #1025 (release watcher, $REL by date -u): HOLD_kc143 RELEASED (renamed to HOLD_kc143.txt.released.$T) as before: the $NAME scan has ended and only its 1-process secant runs; $AV GiB available at the release. The chain's report follows when its scan starts; the hold is placed again when the secant ends."
t0=$(date +%s); REPORTED=0
while [ $(( $(date +%s) - t0 )) -lt $REPWAIT ]; do
  n=$(procs "$CHAINPAT" | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ]; then
    sleep $AFTER
    n=$(procs "$CHAINPAT" | wc -l | tr -d ' ')
    RS=$(procs "$CHAINPAT" | awk '{s += $1} END {printf "%.2f", s/1048576}')
    NI=$(procs "$CHAINPAT" | awk '{print $2}' | sort -u | tr '\n' ' ')
    SEC=$(procs 'd18_secant[.]py run' | awk '{s += $1} END {printf "%.2f", s/1048576}')
    tell "macm3 #1025 (release watcher, $(stamp)): the chain's scan has started: $n scan processes (d18_hybsign), RSS sum $RS GiB, nice $NI; my secant RSS $SEC GiB; $(availgib) GiB available; $(grep 'next:' "$CLOG" | tail -1 | cut -c1-200)"
    REPORTED=1; break
  fi
  sleep $POLL
done
[ "$REPORTED" = 1 ] || tell "macm3 #1025 (release watcher, $(stamp)): HOLD_kc143 was released at $REL, but no chain scan process appeared within $((REPWAIT/60)) min; $(availgib) GiB available; $(tail -n 2 "$CLOG" | cut -c1-200 | tr '\n' ' ')"
# the secant ends: place the hold again for the next lane
END=$(( $(date +%s) + WAITH * 3600 ))
while :; do
  grep -q "$NAME: secant exit" "$LG" 2>/dev/null && break
  pgrep -f "$LANEPAT" > /dev/null || break
  [ $(date +%s) -gt $END ] && { echo "$(stamp) gave up waiting for the secant end"; exit 0; }
  sleep $POLL
done
echo "the k_c 143 lane kc143_d23125 follows (t5, hc 27 Nov 01:38 UTC): the chain starts no scan until its secant starts; placed $(stamp) by the release watcher of $NAME (the scan of the chain that runs now finishes first)" > "$REHOLD"
tell "macm3 #1025 (release watcher, $(stamp)): the $NAME secant has ended; the chain is held again ($(basename "$REHOLD")) for the D 23.125 lane; $(procs "$CHAINPAT" | wc -l | tr -d ' ') chain scan processes run now and finish their point."
exit 0
