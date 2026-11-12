#!/usr/bin/env bash
# lane B: #543 last node 0.74 (with the renode control), 0.76, 0.80, then #544 nodes 0.3,0.4,0.5,0.62,0.7 and 0.25,... (with the controls)
. /d/choptuik-large-d-raw/I543-win2/layout_lib.sh
layout I543-win2 B last074 0.3,0.4,0.5,0.6,0.74
ctl_renode I543-win2 B last074 0.3,0.4,0.5,0.6,0.74
layout I543-win2 B last076 0.3,0.4,0.5,0.6,0.76
layout I543-win2 B last080 0.3,0.4,0.5,0.6,0.80
echo "lane B #543 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I543-win2/exits.txt
layout I544-win2 B node4_062 0.3,0.4,0.5,0.62,0.7
layout I544-win2 B first025 0.25,0.4,0.5,0.6,0.7
ctl_renode I544-win2 B first025 0.25,0.4,0.5,0.6,0.7
ctl_nn I544-win2 B first025
echo "lane B #544 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I544-win2/exits.txt
