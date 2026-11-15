#!/bin/bash
# #789 (the coordinator): kf 43's small circles, placed from its R 0.36 circles (macm3's report, #789). The cut's state
# exists from kf 43's control. At 3 threads each, side by side:
#   pair  R 0.15 on the real axis at 2.9069: the upper left circle reads 2.853586 + 0.060683i (estimate 1.2e-1) and
#         2.960173 - 0.067355i (7.9e-2), the lower left their conjugates; one pair near 2.9069 +- 0.064i winds +2 (the
#         count at kf 43 is then 12 - 2 = 10), two pairs +4 (8). The nearest other zeros are 0.30 away (2.5636 + 0.3196i)
#         and 0.32 (3.2059 + 0.1741i).
#   lens  R 0.05 at 3.205855 + 0.174080i, the upper right circle's zero 0.0039 outside the upper left circle's edge
#         (estimate 3.2e-2): +1 places it.
# The same command and build as the other circles (choptuik-large-d-749 at bd7df22f); only the centre and radius change.
. /Users/nathan/Source/choptuik-large-d-raw-749/I789-macm3/common.sh
go 43 pair 2.9069,0,0.15 3 &
go 43 lens 3.205855,0.174080,0.05 3 &
wait
echo "789 run_789_kf43s.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_789.txt
