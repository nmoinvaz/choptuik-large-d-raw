#!/bin/bash
# watch1031.sh PID LOG [DT]: while PID lives, every DT s (30) one line to LOG: MemAvailable and the sum of the RSS of PID's process tree (cargo, rustc); alert-only (kills nothing)
P=$1; LOG=$2; DT=${3:-30}
echo "# $(date -u '+%F %T') UTC watch start on pid $P, alert-only" >> "$LOG"
peak=0
while kill -0 "$P" 2>/dev/null; do
  av=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
  ids=$P; for _ in 1 2 3 4 5 6; do ids="$ids $(pgrep -P ${ids// /,} 2>/dev/null | tr '\n' ' ')"; done
  rss=$(ps -o rss= -p ${ids// /,} 2>/dev/null | awk '{s+=$1} END{print s+0}')
  [ "$rss" -gt "$peak" ] && peak=$rss
  echo "$(date -u '+%T') avail $((av / 1024)) MiB, tree rss $((rss / 1024)) MiB, peak $((peak / 1024)) MiB" >> "$LOG"
  [ "$av" -lt $((6 * 1048576)) ] && echo "# $(date -u '+%F %T') UTC ALERT: MemAvailable $((av / 1024)) MiB below 6 GB (nothing stopped)" >> "$LOG"
  sleep "$DT"
done
echo "# $(date -u '+%F %T') UTC watch end, peak tree rss $((peak / 1024)) MiB" >> "$LOG"
