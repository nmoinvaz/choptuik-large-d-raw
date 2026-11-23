#!/bin/bash
# sends the coordinator an hc line at each event of the d19_k95 lane (the source check, the regrid's end, the acceptance, a stop); ends at the verdict or a stop; runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95; T5="nathans-macbook-air-m5-3/t5"
timeout 43200 tail -n0 -F $F/regrid/steps.txt | while read -r line; do
  case "$line" in
    *"regrid exit"*|*"kc95 syscheck exit"*|*"verdict:"*|*"STOP:"*) hc send "$T5" "dh610 d19_k95 (auto): ${line:0:1100}";;
  esac
  case "$line" in *"verdict:"*|*"STOP:"*) break;; esac
done
