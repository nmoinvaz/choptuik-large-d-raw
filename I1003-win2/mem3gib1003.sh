#!/usr/bin/env bash
# #1003: second memory watch (coordinator's hc of 2026-11-19 ~17:55 UTC: keep the 8 GiB alert as it is, and tell him if free memory falls under 3 GiB). Read only: every 30 s it reads the last line of mem_1003.log
# (written by mem1003.sh every 120 s), and when free physical memory is under 3 GiB it sends the coordinator one hc and exits (so I see it and re-arm). It ends without a message when the log says "tree gone". It kills nothing.
# usage: bash mem3gib1003.sh
X=/d/choptuik-large-d-raw-743/I1003-win2
while true; do
  l=$(tail -n 1 $X/mem_1003.log)
  case "$l" in *"tree gone"*) echo "$(date -u '+%H:%M:%S') tree gone, watch ends"; exit 0;; esac
  free=$(echo "$l" | awk '{print $5}')
  if [ -n "$free" ] && [ "$(awk "BEGIN{print ($free<3)}")" = "1" ]; then
    hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1003 memory: free physical memory on win2 fell to $free GiB (under 3, as you asked to be told), at $(date -u '+%H:%M') UTC. Nothing is killed, the K 49 run goes on. Log line: $l"
    echo "$(date -u '+%H:%M:%S') SENT under-3-GiB hc: $l"
    exit 0
  fi
  sleep 30
done
