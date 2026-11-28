#!/bin/bash
# #1109 stage 1: the four remaining k_c 55 states, one at a time (run_state.sh each); paused between states while the 1-minute load average is above 16
{
H=$HOME/Source/choptuik-large-d-raw/I1109-mm5
for D in 14.5 15.0 15.5 16.5; do
  while [ "$(sysctl -n vm.loadavg | awk '{printf "%d", $2}')" -gt 16 ]; do echo "$(date -u +%H:%M:%S) load above 16: waiting before D $D" >> $H/run_rest.log; sleep 60; done
  bash $H/run_state.sh D$D $D l1kc55Fb1025.jsonl sol_l1kc55Fb1025_D${D}000.npy
  echo "$(date -u +%H:%M:%S) D $D done" >> $H/run_rest.log
done
echo "all done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $H/run_rest.log
exit
}
