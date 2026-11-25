#!/bin/bash
# #1087 stopped by order (t5's hc, 2026-11-25 00:06 UTC): no new rung. The chain's later calls end here. The real script is run_rung_used.sh.
K=$1; TAG=$2
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1087-dh370/ks${K}_$TAG
mkdir -p $OUT
echo "$(date -u '+%F %T') UTC K $K tag $TAG: ended by: not run, stopped by order; seconds to that point 0; exit 0" > $OUT/rung.txt
exit 0
