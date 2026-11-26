#!/bin/bash
# t5's order (hc 26 Nov 20:35 UTC): "Release HOLD_low2 yourself when the D 23.125 scan ends and only its 1-process secant runs (about 8 GB free then). Leave the lane and the chain as they are, and report at the release."
# Waits for the line "kc135_d23125: secant starts:" in the lane's exits file (the scan has ended), checks that no scan process runs and that at least MINAVAIL GiB are available,
# then renames HOLD_low2.txt to HOLD_low2.txt.released.<epoch> (no deletion), tells t5, and reports the chain's process count and memory when its scan has started. Nothing else is touched.
LG=${LG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc135_d23125/exits_kc135.txt}
HOLD=${HOLD:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/HOLD_low2.txt}
CLOG=${CLOG:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/chain.log}
HC=${HC:-$(command -v hc)}; POLL=${POLL:-30}; MINAVAIL=${MINAVAIL:-8}; LANEPAT=${LANEPAT:-kc135_d23125/lane_d23125.sh}; WAITH=${WAITH:-30}; AFTER=${AFTER:-120}; REPWAIT=${REPWAIT:-1800}
availgib() { vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}'; }
# python processes only (a shell command that merely contains the name is not a scan process): prints "rss ni" per match of the pattern, capped_run's wrapper excluded
procs() { ps -axo rss=,ni=,command= | awk -v pat="$1" '{r=$1; n=$2; $1=""; $2=""; c=substr($0,3); if (c ~ /^[^ ]*[Pp]ython[^ ]* / && c ~ pat && c !~ /capped_run/) print r, n}'; }
stamp() { date -u '+%F %T UTC'; }
tell() { echo "$(stamp) hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" 2>&1 | tail -1; }
END=$(( $(date +%s) + WAITH * 3600 ))
while :; do
  grep -q 'kc135_d23125: secant starts:' "$LG" 2>/dev/null && break
  pgrep -f "$LANEPAT" > /dev/null || { echo "$(stamp) the D 23.125 lane is gone and no secant started: HOLD_low2 NOT released"; tell "macm3 #1025 (release watcher, $(stamp)): the k_c 135 D 23.125 lane ended without starting its secant; HOLD_low2 NOT released (see kc135_d23125/exits_kc135.txt)"; exit 0; }
  [ $(date +%s) -gt $END ] && { echo "$(stamp) gave up waiting"; exit 0; }
  sleep $POLL
done
sleep 20      # let the scan's processes finish
SCANP=$(procs 'd18_hybsign[.]py|d18_secant[.]py scan' | wc -l | tr -d ' ')
AV=$(availgib)
if [ "$SCANP" != 0 ] || ! python3 -c "import sys; sys.exit(0 if $AV >= $MINAVAIL else 1)"; then
  tell "macm3 #1025 (release watcher, $(stamp)): the D 23.125 secant started, but HOLD_low2 NOT released: $SCANP scan processes still run, $AV GiB available (wanted 0 and at least $MINAVAIL). Held; your word."
  exit 0
fi
T=$(date +%s); mv "$HOLD" "$HOLD.released.$T" && REL="$(stamp)" || { tell "macm3 #1025 (release watcher, $(stamp)): the rename of HOLD_low2.txt failed; held"; exit 1; }
ls "$(dirname "$HOLD")"/HOLD* 2>/dev/null
tell "macm3 #1025 (release watcher, $REL by date -u): HOLD_low2 RELEASED (renamed to HOLD_low2.txt.released.$T) as ordered: the D 23.125 k_c 135 scan has ended and only its 1-process secant runs; $AV GiB available at the release. The chain's report follows when its scan starts."
t0=$(date +%s)
while [ $(( $(date +%s) - t0 )) -lt $REPWAIT ]; do
  n=$(procs 'd18_hybsign[.]py' | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ]; then
    sleep $AFTER
    n=$(procs 'd18_hybsign[.]py' | wc -l | tr -d ' ')
    RS=$(procs 'd18_hybsign[.]py' | awk '{s += $1} END {printf "%.2f", s/1048576}')
    NI=$(procs 'd18_hybsign[.]py' | awk '{print $2}' | sort -u | tr '\n' ' ')
    SEC=$(procs 'd18_secant[.]py run' | awk '{s += $1} END {printf "%.2f", s/1048576}')
    tell "macm3 #1025 (release watcher, $(stamp)): the chain's scan has started: $n scan processes (d18_hybsign), RSS sum $RS GiB, nice $NI; my secant RSS $SEC GiB; $(availgib) GiB available; $(grep 'next:' "$CLOG" | tail -1 | cut -c1-200)"
    exit 0
  fi
  sleep 30
done
tell "macm3 #1025 (release watcher, $(stamp)): HOLD_low2 was released at $REL, but no chain scan process appeared within $((REPWAIT/60)) min; $(availgib) GiB available; $(tail -n 2 "$CLOG" | cut -c1-200 | tr '\n' ' ')"
exit 0
