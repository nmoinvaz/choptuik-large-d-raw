#!/bin/bash
# #749 (the coordinator): kf 41's small circles on macm3, placed from win2's kf 41 circles (I749-win2/kf41/run.log).
# First kf 41's lambda_phys control (R 0.2, 6 threads), which makes the cut's state on this machine; win2's control read
# omega 3.476755, lam_g 0.8992305398, |F| 1.3e-19 and winding +1. Then, at 3 threads each, side by side:
#   pair  R 0.1 on the real axis at 2.8709: the two left circles read 2.870773 -+ 0.031054i (estimate 3.0e-2) and
#         2.871088 +- 0.030294i (4.1e-2); the nearest other zero (3.14861 + 0.19079i) is 0.32 away. Winding +2 expected.
#   lens  R 0.05 at 3.14861 + 0.19079i, the mean of the upper left (3.148461 + 0.190972i) and upper right
#         (3.148764 + 0.190610i) circles' reports. Winding +1 if they are one zero (the count at kf 41 is then 10).
# The same command and build as the kf 39 circles (choptuik-large-d-749 at bd7df22f), only the cut, centre and radius changed.
. /Users/nathan/Source/choptuik-large-d-raw-749/I749-macm3/common.sh
go 41 control 2.043532530673195,0,0.2 6
go 41 pair 2.8709,0,0.1 3 &
go 41 lens 3.14861,0.19079,0.05 3 &
wait
echo "749 run_749_kf41.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_749.txt
