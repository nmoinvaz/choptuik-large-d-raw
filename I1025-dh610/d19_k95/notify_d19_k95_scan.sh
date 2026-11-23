#!/bin/bash
# sends the coordinator an hc line at each event of the d19_k95 scan lane (the source check, each process's end, the reading, a stop); ends at "scan done" or a stop; runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95; T5="nathans-macbook-air-m5-3/t5"
timeout 86400 tail -n0 -F $F/exits_d19k95_scan.txt | while read -r line; do
  case "$line" in
    *"source check on"*|*"scan: D 19.0"*|*"scan p"*" exit "*|*"reading:"*|*"scan done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 d19_k95 scan (auto): ${line:0:1100}";;
  esac
  case "$line" in *"scan done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
