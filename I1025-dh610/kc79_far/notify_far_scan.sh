#!/bin/bash
# notify_far_scan.sh D: sends the coordinator an hc line at each event of the tag i scan of the shared D (scan_after_compare.sh: D<D>/i/exits_far.txt); ends at the lane's end or a stop
D=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D$D/i; T5="nathans-macbook-air-m5-3/t5"; mkdir -p $F; touch $F/exits_far.txt
timeout 86400 tail -n0 -F $F/exits_far.txt | while read -r line; do
  case "$line" in
    *"lane starts"*|*"source check:"*|*"reading:"*|*"no robust change"*|*"reading of the widened"*|*"far point done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 kc79_far D $D tag i scan (auto): ${line:0:1100}";;
  esac
  case "$line" in *"far point done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
