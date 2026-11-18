#!/bin/bash
# Alert-only memory log. Usage: memlog967.sh LOG PID [SECONDS]. Samples every SECONDS (30) while PID lives and writes a
# line only when MemAvailable falls below 12 GB or swap use passes 1 GB (and when it recovers), plus a header and one
# summary line at the end. It never signals anything.
LOG=$1; PID=$2; DT=${3:-30}
LOW_KB=$((12 * 1024 * 1024)); SWAP_KB=$((1024 * 1024))
stamp() { date -u '+%F %T'; }
echo "# $(stamp) UTC memlog start, watching pid $PID every $DT s, alert below $((LOW_KB / 1048576)) GB available or above $((SWAP_KB / 1048576)) GB swap" >> "$LOG"
min=999999999; maxswap=0; alert=0; n=0
while kill -0 "$PID" 2>/dev/null; do
  avail=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
  swap=$(awk '/^SwapTotal:/ {t=$2} /^SwapFree:/ {f=$2} END {print t-f}' /proc/meminfo)
  n=$((n + 1)); [ "$avail" -lt "$min" ] && min=$avail
  [ "$swap" -gt "$maxswap" ] && maxswap=$swap
  if [ "$avail" -lt "$LOW_KB" ] || [ "$swap" -gt "$SWAP_KB" ]; then
    echo "# $(stamp) UTC ALERT available $((avail / 1024)) MiB, swap used $((swap / 1024)) MiB" >> "$LOG"; alert=1
  elif [ "$alert" = 1 ]; then
    echo "# $(stamp) UTC recovered, available $((avail / 1024)) MiB" >> "$LOG"; alert=0
  fi
  sleep "$DT"
done
[ "$n" -gt 0 ] && echo "# $(stamp) UTC memlog end, $n samples, lowest MemAvailable $((min / 1024)) MiB, highest swap used $((maxswap / 1024)) MiB" >> "$LOG" \
  || echo "# $(stamp) UTC memlog end, no samples (pid $PID not alive)" >> "$LOG"
