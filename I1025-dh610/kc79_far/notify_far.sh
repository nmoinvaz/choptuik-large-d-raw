#!/bin/bash
# notify_far.sh D: sends the coordinator an hc line at each event of the kc79_far lane of D (pins, source check, scan start, reading, widening, end, a stop); ends at the lane's end; runs from the runner session's shell, where hc works
D=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D$D; T5="nathans-macbook-air-m5-3/t5"; mkdir -p $F
timeout 86400 tail -n0 -F $F/exits_far.txt | while read -r line; do
  case "$line" in
    *"state and record pinned"*|*"both states pinned"*|*"source check, tag"*|*"compare_states.py exit"*|*"source check:"*|*"reading:"*|*"no robust change"*|*"reading of the widened"*|*"far point done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 kc79_far D $D (auto): ${line:0:1100}";;
  esac
  case "$line" in *"far point done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
