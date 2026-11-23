#!/bin/bash
# #1025 macm3b kc79_d2075: the source check (run_source.sh), then, only if it ended ACCEPTED, the scan and its reading (run_scan.sh). Own session under caffeinate -is.
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d2075
bash $OUT/run_source.sh && bash $OUT/run_scan.sh
exit $?
