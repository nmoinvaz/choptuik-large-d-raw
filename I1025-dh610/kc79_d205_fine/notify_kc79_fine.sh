#!/bin/bash
# sends the coordinator an hc line at each event of the kc79_d205_fine lane (the source check, the regrid's end, its acceptance, the scan's end, a stop); ends at the lane's end; runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_d205_fine; T5="nathans-macbook-air-m5-3/t5"
timeout 43200 tail -n0 -F $F/exits_kc79_d205_fine.txt | while read -r line; do
  case "$line" in
    *"source check:"*|*"ell_refine exit"*|*"regrid ACCEPTED"*|*"acceptance:"*|*"pair check"*|*"kc79_fine done"*|*"STOP:"*|*"refuse:"*) hc send "$T5" "dh610 kc79_d205_fine (auto): ${line:0:1100}";;
  esac
  case "$line" in *"kc79_fine done"*|*"STOP:"*|*"refuse:"*) break;; esac
done
