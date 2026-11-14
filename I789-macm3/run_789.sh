#!/bin/bash
# #789: the ten circles (control and four R 0.36 circles at kf 43 and at kf 45), at most P single-thread processes at a
# time (default 6, macm3's budget), in this order: kf 43's five and kf 45's control first (the control makes the cut's
# state), kf 45's circles as slots free up. The small circles are placed by the coordinator from these circles' positions.
P=${1:-6}
R=/Users/nathan/Source/choptuik-large-d-raw-749/I789-macm3
printf '%s\n' "43 control" "43 c_2.85_p0.25" "43 c_2.85_m0.25" "43 c_3.35_p0.25" "43 c_3.35_m0.25" "45 control" "45 c_2.85_p0.25" "45 c_2.85_m0.25" "45 c_3.35_p0.25" "45 c_3.35_m0.25" |
  xargs -P $P -L 1 $R/job.sh
echo "789 run_789.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_789.txt
