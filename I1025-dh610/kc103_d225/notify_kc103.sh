#!/bin/bash
# notify_kc103.sh: sends the coordinator an hc line at each event of the k_c 103 D 22.5 lane (exits_kc103.txt); ends at the lane's end or a stop
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc103_d225; T5="nathans-macbook-air-m5-3/t5"; touch $F/exits_kc103.txt
timeout 172800 tail -n0 -F $F/exits_kc103.txt | while read -r line; do
  case "$line" in
    *"source check"*|*"regrid starts"*|*"regrid exit"*|*"verdict:"*|*"scan memory gate"*|*"scan: lambda"*|*"reading:"*|*"no robust change"*|*"point done"*|*"STOP:"*|*"waiting for memory"*) hc send "$T5" "dh610 kc103_d225 (auto): ${line:0:700}" > /dev/null 2>&1;;
  esac
  case "$line" in *"point done"*|*"STOP:"*) break;; esac
done
