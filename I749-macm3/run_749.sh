#!/bin/bash
# #749: the ten circles (control and four R 0.36 circles at kf 39 and at kf 41), at most P single-thread processes at a
# time (default 4, since #722 holds macm3's other threads), in this order: kf 39's five and kf 41's control first (the
# control makes the cut's state), kf 41's circles as slots free up. The small circles (the pair, and a zero shared by a
# left and a right circle) are placed by the coordinator from these circles' positions and started by hand.
P=${1:-4}
R=/Users/nathan/Source/choptuik-large-d-raw-749/I749-macm3
printf '%s\n' "39 control" "39 c_2.85_p0.25" "39 c_2.85_m0.25" "39 c_3.35_p0.25" "39 c_3.35_m0.25" "41 control" "41 c_2.85_p0.25" "41 c_2.85_m0.25" "41 c_3.35_p0.25" "41 c_3.35_m0.25" |
  xargs -P $P -L 1 $R/job.sh
echo "749 run_749.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_749.txt
