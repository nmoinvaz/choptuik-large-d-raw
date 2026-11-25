#!/bin/bash
# chain_kc95_22.sh: the coordinator's order of 25 Nov (hc, read at about 03:00 UTC): k_c 95 at D 22.125, then at D 22.1875, one lane at a time (8 threads); stops at the first lane that does not exit 0.
RAW=/home/nathan/Source/choptuik-large-d-raw/I1025-dh610
for f in kc95_d22125 kc95_d221875; do
  bash $RAW/$f/lane_kc95.sh; rc=$?
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc95 chain 22: lane $f exit $rc" >> $RAW/kc95_d22125/exits_kc95_chain22.txt
  [ $rc = 0 ] || exit $rc
done
