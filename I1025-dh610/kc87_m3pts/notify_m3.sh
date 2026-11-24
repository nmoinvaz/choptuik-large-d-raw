#!/bin/bash
# notify_k87.sh D: sends the coordinator an hc line at each event of the kc87_m3pts lane of D (pins, source check, scan start, reading, end, a stop); ends at the lane's end; runs from the runner's terminal.
D=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_m3pts/$D; T5="nathans-macbook-air-m5-3/t5"; mkdir -p $F
timeout 86400 tail -n0 -F $F/exits_k87l.txt | while read -r line; do
  case "$line" in
    *"state and record pinned"*|*"source check:"*|*"scan: lambda"*|*"reading:"*|*"no robust change"*|*"k87l point done"*|*"STOP: "*|*"refuse: "*) hc send "$T5" "dh610 kc87_m3pts D $D (auto): ${line:0:420}";;
  esac
  case "$line" in *"k87l point done"*|*"STOP: "*|*"refuse: "*) break;; esac
done
