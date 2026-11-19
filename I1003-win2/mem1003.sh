#!/usr/bin/env bash
# #1003 memory log, alert only (coordinator's hc of 2026-11-19 ~07:30 UTC: "an alert-only memory log, no kills on memory; if free memory falls below 8 GB, tell me"). Every 120 s it appends
# "UTC label free_GiB tree_working_set_GiB processes" to mem_1003.log for the process tree under the root pid in WINPIDFILE, until that tree is gone. If the free physical memory is below 8 GiB it sends
# the coordinator an hc, at most once an hour (the hour is counted only after a delivered message). It never kills anything. usage: bash mem1003.sh WINPIDFILE LABEL
X=/d/choptuik-large-d-raw-743/I1003-win2
root=$(cat "$1"); label=$2; last=0
while true; do
  r=$(powershell -NoProfile -File "D:/choptuik-large-d-raw-743/I1003-win2/mem1003.ps1" -Root $root | tr -d '\r')
  set -- $r
  free=$1; ws=$2; n=$3
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') $label free $free GiB tree $ws GiB procs $n" >> $X/mem_1003.log
  [ "${n:-0}" -eq 0 ] && break
  if [ "$(awk "BEGIN{print ($free<8)}")" = "1" ] && [ $(( $(date +%s) - last )) -ge 3600 ]; then
    if hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1003 memory alert: free physical memory on win2 is $free GiB (below 8), the $label tree holds $ws GiB over $n processes. Nothing is killed, the run goes on." 2>&1 | grep -q '"started":true'; then last=$(date +%s); fi
  fi
  sleep 120
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S') $label tree gone" >> $X/mem_1003.log
