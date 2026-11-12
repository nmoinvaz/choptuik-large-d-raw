#!/usr/bin/env bash
# lane A: #543 last node 0.66, 0.68, 0.69, 0.71, then #544 nodes 0.3,0.42,... and 0.3,0.4,0.52,...
. /d/choptuik-large-d-raw/I543-win2/layout_lib.sh
for x in 066 068 069 071; do layout I543-win2 A last$x 0.3,0.4,0.5,0.6,0.${x:1}; done
echo "lane A #543 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I543-win2/exits.txt
layout I544-win2 A node2_042 0.3,0.42,0.5,0.6,0.7
layout I544-win2 A node3_052 0.3,0.4,0.52,0.6,0.7
echo "lane A #544 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I544-win2/exits.txt
