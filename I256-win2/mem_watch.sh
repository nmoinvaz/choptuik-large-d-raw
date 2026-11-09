#!/usr/bin/env bash
# #256: alert-only memory watch. Every 60 s reads free physical memory; below 22 GB it writes MEM_ALERT with the time and the value
# and exits 20. Kills and pauses nothing. Stops by itself when the file STOP_MEM_WATCH appears.
R=/d/choptuik-large-d-raw/I256-win2
LIMIT=22
while [ ! -e $R/STOP_MEM_WATCH ]; do
  f=$(powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)" | tr -d '\r')
  echo "$(date -u '+%F %T') free $f" >> $R/mem_watch.log
  if awk "BEGIN{exit !($f < $LIMIT)}"; then
    echo "$(date -u '+%F %T UTC') free memory $f GB below $LIMIT GB" >> $R/MEM_ALERT
    exit 20
  fi
  sleep 60
done
