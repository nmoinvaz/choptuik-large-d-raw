#!/bin/bash
# #1109 stage 1b: the 18 states of list_1b.tsv in its order, one at a time (run_state_b.sh each); paused between states while the
# 1-minute load average is above 16
{
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
while IFS=$'\t' read -r TAG D KC RECP STP SB RB; do
  while [ "$(sysctl -n vm.loadavg | awk '{printf "%d", $2}')" -gt 16 ]; do echo "$(date -u +%H:%M:%S) load above 16: waiting before $TAG" >> $H/run_1b.log; sleep 60; done
  bash $H/run_state_b.sh $TAG $D $(basename $RECP) $(basename $STP)
  echo "$(date -u +%H:%M:%S) $TAG done" >> $H/run_1b.log
done < $H/list_1b.tsv
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $H/run_1b.log
exit
}
