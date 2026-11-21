#!/bin/bash
# #1025 P4 on dh170: memory sampler, alert-only (logs, stops nothing). One line per 60 s into p4_mem.log until p4_driver_rows.sh is gone.
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/p4
min=999999
while :; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); sw=$(awk '/SwapTotal/ {t=$2} /SwapFree/ {f=$2} END {print int((t-f)/1024)}' /proc/meminfo)
  [ "$av" -lt "$min" ] && min=$av
  top=$(ps -eo rss=,comm= --sort=-rss | head -n 2 | awk '{printf "%d MiB %s; ", $1/1024, $2}')
  echo "$(date -u '+%T') MemAvailable $av MiB, min so far $min MiB, swap used $sw MiB, top: $top" >> $OUT/p4_mem.log
  ps -eo args= | grep -q '[p]4_driver_rows.sh' || { echo "$(date -u '+%T') p4_driver_rows.sh gone, sampler ends" >> $OUT/p4_mem.log; exit 0; }
  sleep 60
done
