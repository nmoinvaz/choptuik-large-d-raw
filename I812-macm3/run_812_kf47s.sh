#!/bin/bash
# #812 (the coordinator): kf 47's small circles, placed from its R 0.36 circles (macm3's report, 09:51 UTC), on the cut's
# saved state, side by side at 2 threads each:
#   triple  R 0.24 on the real axis at 2.905: the three near-axis zeros 2.753182, 2.867976 and 3.057052 (each read once in
#           the upper left circle, so real by conjugate symmetry), margins 0.088, 0.20, 0.088 against estimates 0.012,
#           0.044, 0.073; the shared zero lies 0.053 outside. +3 confirms three zeros there, inside both left circles.
#   lens    R 0.05 at 3.16186 + 0.14008i, the mean of the shared zero's readings (3.166384 + 0.132944i left, 3.157336 +
#           0.147225i right, 0.0169 apart), inside the upper left circle by 0.023-0.036. +1 places it.
#   lensc   R 0.05 at its conjugate, 3.16186 - 0.14008i: +1.
# Tally then: 5 + 5 + 3 + 3 = 16, minus 3 (the axis zeros in both left circles) minus 2 (the shared zero and its
# conjugate, each in two circles) = 11, against 10 at kf 39-45.
. /Users/nathan/Source/choptuik-large-d-raw-749/I812-macm3/common.sh
go 47 triple 2.905,0,0.24 2 &
go 47 lens 3.16186,0.14008,0.05 2 &
go 47 lensc 3.16186,-0.14008,0.05 2 &
wait
echo "812 run_812_kf47s.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_812.txt
