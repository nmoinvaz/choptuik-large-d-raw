#!/bin/bash
# #789 (the coordinator): kf 45's small circles, placed from its R 0.36 circles (macm3's report, #789, 01:17 UTC). The
# cut's state exists from kf 45's control. At 3 threads each, side by side:
#   pair  R 0.15 on the real axis at 2.8662: the upper left circle reads 2.866067 - 0.039286i (estimate 3.6e-2) and
#         2.866424 + 0.038910i (5.3e-2), the lower left their conjugates; one pair near 2.8662 +- 0.039i winds +2 (the
#         count at kf 45 is then 14 - 2 - 2 = 10 with the lens), two pairs +4. The nearest other zeros are 0.31 away
#         (3.1318 + 0.1627i) and 0.48 (2.5246 + 0.3354i).
#   lens  R 0.05 at 3.131427 + 0.163000i, the mean of the shared zero's two readings (3.131788 + 0.162692i on the left,
#         estimate 1.6e-2, and 3.131066 + 0.163309i on the right, 5.2e-3, 9.5e-4 apart), inside the upper left circle by
#         +0.065 and the upper right by +0.125: +1 places one zero there, counted in both. The nearest other zero is 0.25
#         away (3.3357 + 0.3074i).
# The same command and build as the other circles (choptuik-large-d-749 at bd7df22f); only the centre and radius change.
. /Users/nathan/Source/choptuik-large-d-raw-749/I789-macm3/common.sh
go 45 pair 2.8662,0,0.15 3 &
go 45 lens 3.131427,0.163000,0.05 3 &
wait
echo "789 run_789_kf45s.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_789.txt
