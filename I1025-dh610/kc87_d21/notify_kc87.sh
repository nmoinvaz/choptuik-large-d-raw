#!/bin/bash
# sends the coordinator an hc line at each event of the kc87_d21 lane (the source check, the regrid's end, its acceptance, the scan's end, a stop); ends at the lane's end; runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_d21; T5="nathans-macbook-air-m5-3/t5"
timeout 43200 tail -n0 -F $F/exits_kc87_d21.txt | while read -r line; do
  case "$line" in
    *"source check:"*|*"ell_refine exit"*|*"regrid ACCEPTED"*|*"acceptance:"*|*"pair check"*|*"kc87 done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 kc87_d21 (auto): ${line:0:1100}";;
  esac
  case "$line" in *"kc87 done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
