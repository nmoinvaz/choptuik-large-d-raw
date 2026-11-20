#!/bin/bash
# prints the sheetfix run's state and exits when: the driver exited, the time cap passed (arg, seconds), or any argcount process passes 3 GB RSS (checked every 60 s)
OUT=$(cd "$(dirname "$0")/.." && pwd); T0=$(date +%s); LIM=${1:-3600}
while true; do
  sleep 60
  if grep -q "^driver exit" $OUT/logs/driver.start; then echo "driver done"; break; fi
  big=$(ps -eo rss,args | grep "argcount\|multiprocessing" | grep -v grep | awk '$1 > 3000000 {print $1}' | head -1)
  [ -n "$big" ] && { echo "RSS over 3 GB: $big kB"; break; }
  [ $(( $(date +%s) - T0 )) -ge $LIM ] && { echo "time cap"; break; }
done
date -u '+%F %T UTC'; cat $OUT/logs/exits.txt; echo "--- log"; grep -v "Warning\|return self\|sc = \|z = q\|err[35] =" $OUT/logs/m3_sheetfix_r0.17.log | tail -30 | cut -c1-260
echo "--- records"; wc -l $OUT/m3/*.jsonl
echo "--- processes"; ps -eo pid,etimes,ni,pcpu,rss,args | grep -E "argcount|multiprocessing" | grep -v "grep\|timeout" | cut -c1-120
free -m | head -2
