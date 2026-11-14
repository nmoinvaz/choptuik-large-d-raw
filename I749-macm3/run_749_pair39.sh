#!/bin/bash
# #749 (the coordinator): an R 0.1 circle for the pair near the real axis at kf 39, centred on the real axis at 2.8623, as
# #708's at kf 37. The kf 39 left circles read the pair at 2.860537 + 0.067449i and 2.864028 - 0.069163i (estimates 3.8e-2,
# 2.1e-2), about 2.8623 +- 0.0683i, inside R 0.1; the nearest other zero (3.1333 + 0.1147i) is 0.30 away. The winding
# should be +2. 3 threads; the command and build of the other kf 39 circles (choptuik-large-d-749 at bd7df22f), only the
# centre and radius changed.
. /Users/nathan/Source/choptuik-large-d-raw-749/I749-macm3/common.sh
go 39 pair 2.8623,0,0.1 3
