#!/bin/bash
# sends the coordinator an hc line at each event of the #1081 lane (pins, pool start, each config's last job, the Krawczyk stage, the end, a stop); ends at the lane's end or a stop; runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1081-dh610; T5="nathans-macbook-air-m5-3/t5"
timeout 86400 tail -n0 -F $F/exits_1081.txt | while read -r line; do
  case "$line" in
    *"pins checked"*|*"pool starts"*|*"pool ended"*|*"krawczyk stage"*|*"lane done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 #1081 (auto): ${line:0:1100}";;
  esac
  case "$line" in *"lane done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
