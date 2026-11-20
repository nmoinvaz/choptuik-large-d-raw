#!/bin/bash
{
# #1025 P4 amendment 8: after lane B's D 16.75 k_c 63 python (pid 91081) exits, the D 16.5 k_c 63 row in slot B.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
cd /Users/nathan/Source/choptuik-1025/solver/matter
while kill -0 91081 2> /dev/null; do sleep 30; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane B's D 16.75 python (pid 91081) has exited; p4_list_b_mac2.txt"
bash $R/lane_p4.sh $R/p4_list_b_mac2.txt > $R/lane_p4b_mac2.log 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane slotB2 done"
exit
}
