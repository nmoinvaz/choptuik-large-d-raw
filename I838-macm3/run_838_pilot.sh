#!/bin/bash
# #838 pilot (the coordinator): the M 64 kf 47 control alone at 6 threads, which also makes and saves the cut's state.
# Bar: winds +1, 0 mismatches, setup |F| <= 1e-15. Then run_838_kf47.sh.
. /Users/nathan/Source/choptuik-large-d-raw-749/I838-macm3/common.sh
go 47 control 2.043532530673195,0,0.2 6
echo "838 run_838_pilot.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_838.txt
