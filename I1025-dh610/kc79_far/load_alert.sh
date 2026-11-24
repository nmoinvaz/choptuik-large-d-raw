#!/bin/bash
# load_alert.sh: alert-only (stops and kills nothing). Samples the 5-minute load average every minute; when every one of the last 60 samples is above 22 (the coordinator's word, hc 24 Nov: "if the actual load stays above 22
# for an hour, tell me") sends the coordinator one hc line, then waits until a sample is at or below 22 before it can fire again. Runs from the runner session's shell, where hc works. Ends after 72 h.
T5="nathans-macbook-air-m5-3/t5"; LIM=22; n=0; end=$(( $(date +%s) + 259200 )); fired=0
while [ $(date +%s) -lt $end ]; do
  l5=$(cut -d' ' -f2 /proc/loadavg)
  if awk -v l=$l5 -v m=$LIM 'BEGIN {exit !(l > m)}'; then n=$((n + 1)); else n=0; fired=0; fi
  if [ $n -ge 60 ] && [ $fired = 0 ]; then
    fired=1
    hc send "$T5" "dh610 (t1m, auto): the 5-minute load average has been above $LIM for 60 samples (an hour), now $l5 (1-min $(cut -d' ' -f1 /proc/loadavg)); units active: $(systemctl --user list-units --state=active --no-legend 'i1025-*' 'i1076*' | awk '{print $1}' | tr '\n' ' '); alert only, nothing stopped."
  fi
  sleep 60
done
