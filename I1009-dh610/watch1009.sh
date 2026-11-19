#!/bin/bash
# watch1009.sh UNIT LOG [DT]: while the user unit UNIT is active, every DT s (30) one line to LOG: MemAvailable, the unit's memory.current, the K 49 unit's memory.current,
# and, when MemAvailable falls below 4 GB, a line "STOP" and `systemctl --user stop UNIT` (that unit only, never another process). Ends when UNIT is inactive.
UNIT=$1; LOG=$2; DT=${3:-30}
CG=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice
LOW_KB=$((4 * 1024 * 1024))
echo "# $(date -u '+%F %T') UTC watch start on $UNIT, stop below 4 GB MemAvailable" >> "$LOG"
while systemctl --user is-active --quiet "$UNIT"; do
  av=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
  uc=$(cat $CG/$UNIT.service/memory.current 2>/dev/null || echo 0)
  kc=$(cat $CG/i1003k49.service/memory.current 2>/dev/null || echo 0)
  echo "$(date -u '+%T') avail $((av / 1024)) MiB, $UNIT $((uc / 1048576)) MiB, K49 $((kc / 1048576)) MiB" >> "$LOG"
  if [ "$av" -lt "$LOW_KB" ]; then
    echo "# $(date -u '+%F %T') UTC STOP: MemAvailable $((av / 1024)) MiB below 4 GB, stopping $UNIT" >> "$LOG"
    systemctl --user stop "$UNIT"; break
  fi
  sleep "$DT"
done
echo "# $(date -u '+%F %T') UTC watch end" >> "$LOG"
