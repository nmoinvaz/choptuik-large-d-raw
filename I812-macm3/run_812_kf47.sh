#!/bin/bash
# #812 step 2 (the coordinator): kf 47, the control and the four R 0.36 circles, five single-thread processes; the
# circles wait for the cut's state, which the control's setup saves. Stop and report if the control's log header does
# not show kfreeze 47, or the control does not wind +1.
R=/Users/nathan/Source/choptuik-large-d-raw-749/I812-macm3
printf '%s\n' "47 control" "47 c_2.85_p0.25" "47 c_2.85_m0.25" "47 c_3.35_p0.25" "47 c_3.35_m0.25" | xargs -P 5 -L 1 $R/job.sh
echo "812 run_812_kf47.sh done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_812.txt
