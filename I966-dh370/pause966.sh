#!/usr/bin/env bash
# #966 PAUSE (coordinator's hc 2026-11-22 ~02:50 UTC): on xfchecks' DECIDING verdict stop at once by exact pids (driver first), even mid-step; the pause base is the last saved base, the partial step is discarded.
# usage: bash pause966.sh "reason"   (unit i966y). Stops the unit, keeps the logs, prints the last saved base, runs the restart script's --dry (NOSTOP NOSTART) to print the restart command, pushes the raw folder.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I966-dh370
cd $OUT || exit 9
LEG=$(ls -d $OUT/ks_chain3b/leg*/ | sort | tail -1)
cp ${LEG}anm_run.log $OUT/leg_at_pause_$(basename $LEG)_anm_run.log
{ echo "# the running leg's command line at the pause, $(date -u '+%F %T') UTC, from /proc"; for p in $(systemctl --user show i966y -p MainPID --value) ; do :; done; pgrep -af 'anm_run.py' | grep -v bash | cut -c1-3000; } > $OUT/leg_args_at_pause966.txt
bash $OUT/stop966.sh i966y "${1:-pause on the deciding verdict of xfchecks}" ; echo "stop exit $?"
tail -4 $OUT/exits_966.txt | cut -c1-230
echo "running chain processes after the stop: $(pgrep -af 'ks_chain.py|anm_run.py' | grep -v bash | wc -l)"
B=$(ls $LEG/anm_pin3_D*.npz | sort -t_ -k3 -V | tail -1); echo "last saved base: $B"
ls -la --time-style=+%F\ %T $LEG | tail -6 | cut -c20-120
NOSTOP=1 NOSTART=1 timeout 250 bash $OUT/restart966v.sh; echo "dry exit $?"
tail -3 $OUT/exits_966.txt | cut -c1-260
grep -m1 'anm_run.py' $OUT/ks_chain3b_v_dry.log | cut -c1-3000
