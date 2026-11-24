#!/bin/bash
# alert only: hc to t5 when available memory < 2 GiB, free memory < 8% or free disk < 3 GiB (at most one alert per 10 minutes); ends with the leap; stops and kills nothing
OUT=$1; HC=$2; last=0
while :; do
  alive=$(pgrep -f "ell_leap.py" | wc -l | tr -d ' ')
  [ "$alive" = 0 ] && exit 0
  av=$(vm_stat | awk -v ps=$(sysctl -n hw.pagesize) '/Pages free/ {f=$3} /Pages inactive/ {i=$3} /Pages speculative/ {s=$3} /Pages purgeable/ {p=$3} END {printf "%.1f", (f+i+s+p)*ps/2^30}')
  fr=$(memory_pressure | tail -1 | sed 's/.*: //;s/%//'); dk=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}')
  now=$(date +%s)
  if python3 -c "import sys; sys.exit(0 if ($av < 2 or $fr < 8 or $dk < 3) else 1)" && [ $((now - last)) -gt 600 ]; then
    msg="macm3 #1025 kc87_leg2 ALERT $(date -u '+%F %T') UTC: available memory $av GiB, free memory $fr%, free disk $dk GiB (alert only, nothing stopped)"
    echo "$msg" >> $OUT/alert.log; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$msg" >> $OUT/alert.log 2>&1; last=$now
  fi
  sleep 60
done
