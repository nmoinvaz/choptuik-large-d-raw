#!/bin/bash
# #848 (the coordinator): #812's kf 47 count on a second radial layout, in three stages.
#   1. the control (R 0.2 at lambda_phys) at 6 threads, whose setup re-converges and saves the layout's state.
#      Stop if the log still shows #812's centre tail 7.1e-26 (the layout did not change).
#   2. the noise test on the saved state: modecount_qdet --draws=5 at lambda 2.00 and 2.05, 320 bits. The verdict is
#      read by the runner against the issue's line (b); the circles start only if it passes.
#   3. the seven circles of #812 (four R 0.36, the triple, the lens and its conjugate), one thread each, 6 at a time.
#   bash run_848.sh 1|2|3
. /Users/nathan/Source/choptuik-large-d-raw-749/I848-macm3/common.sh
case $1 in
  1) go control 2.043532530673195,0,0.2 6
     grep -q "centre 7.1e-26" $R/kf47_ct$CT/control/run.log && log "STOP: the layout did not change (centre 7.1e-26)"
     grep -m1 "series truncation (solution)" $R/kf47_ct$CT/control/run.log >> $R/exits_848.txt ;;
  2) cd $WT/hp || exit 9
     [ -f data/$ST ] || { log "STOP: data/$ST is missing"; exit 9; }
     mkdir -p $R/qdet_draws; log "qdet_draws start"
     caffeinate -is nice -n 10 python3 -u modecount_qdet.py data/$ST 2.0,0 2.05,0 --kf=47 --fmax=1e-15 --prec=320 \
       --draws=5 --threads=6 --json=$R/qdet_draws/qdet.json > $R/qdet_draws/run.log 2>&1
     log "qdet_draws exit $?" ;;
  3) printf '%s\n' c_2.85_p0.25 c_2.85_m0.25 c_3.35_p0.25 c_3.35_m0.25 triple lens lensc | xargs -P 6 -L 1 $R/job.sh
     log "run_848.sh 3 done" ;;
  *) echo "usage: run_848.sh 1|2|3"; exit 2 ;;
esac
