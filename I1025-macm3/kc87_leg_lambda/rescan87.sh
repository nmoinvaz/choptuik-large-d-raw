#!/bin/bash
# #1025 macm3: the end of pipeline87.sh for a point whose scan was restarted (t5's change to 4 processes): the scan, then the push. usage: bash rescan87.sh D  (D as the folder name; point.env already has NP=4)
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
DN=$1; LOG=$L/$DN/pipeline.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
say "rescan: the scan restarts with $(grep -o '^NP=[0-9]*' $L/$DN/point.env) processes"
bash $L/point87.sh $DN scan >> $LOG 2>&1; say "scan exit $?"
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN scan done (rescan)" >> $LOG 2>&1; say "results pushed ($?)"
