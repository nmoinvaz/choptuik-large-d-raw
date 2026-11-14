#!/bin/bash
# #749 (the coordinator): an R 0.05 circle around the zero both the left and the right kf 39 circles report, as #708's lens
# at kf 37. Centre: the mean of the left circle's report (3.133852 + 0.114724i) and the right circle's (3.132808 +
# 0.114687i), 3.1333 + 0.1147i; the lower one is its conjugate. It winds +1 if the two circles report one zero there (the
# box's count at kf 39 is then 10), and anything else changes the count. 3 threads, the same command and build.
. /Users/nathan/Source/choptuik-large-d-raw-749/I749-macm3/common.sh
go 39 lens 3.1333,0.1147,0.05 3
