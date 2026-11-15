#!/bin/bash
# #838 (the coordinator): the four R 0.36 circles at M 64 kf 47, single-thread each, on the state the pilot saved.
R=/Users/nathan/Source/choptuik-large-d-raw-749/I838-macm3
printf '%s\n' "47 c_2.85_p0.25" "47 c_2.85_m0.25" "47 c_3.35_p0.25" "47 c_3.35_m0.25" | xargs -P 4 -L 1 $R/job.sh
echo "838 run_838_kf47.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_838.txt
