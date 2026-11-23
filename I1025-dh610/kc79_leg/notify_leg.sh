#!/bin/bash
# notify_leg.sh D: sends the coordinator an hc line at each event of the kc79_leg lane of D (pins, source check, scan start, reading, widening, end, a stop); ends at the lane's end; runs from the runner session's shell, where hc works
D=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D$D; T5="nathans-macbook-air-m5-3/t5"; mkdir -p $F
timeout 86400 tail -n0 -F $F/exits_leg.txt | while read -r line; do
  case "$line" in
    *"state and record pinned"*|*"source check:"*|*"reading:"*|*"no robust change"*|*"reading of the widened"*|*"leg point done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 kc79_leg D $D (auto): ${line:0:1100}";;
  esac
  case "$line" in *"leg point done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
