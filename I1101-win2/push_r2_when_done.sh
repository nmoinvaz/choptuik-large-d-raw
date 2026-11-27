#!/bin/bash
# #1101: pushes R2's record and state AS SOON AS R2 ends (the coordinator's hc of 06:58 UTC 27 Nov): waits for r2.done, then runs push_rel.sh on I1101-win2.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
O=/d/choptuik-i935-raw/I1101-win2
until [ -e $O/r2.done ]; do sleep 60; done
sleep 20
cd /d/choptuik-i935-raw/I1025-win2/kc71_leap && bash push_rel.sh I1101-win2 "I1101-win2: R2 (kappa 0.35) ended: record, state, log and the amended reading" > $O/push_r2.out 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') R2 pushed: $(tail -n 2 $O/push_r2.out | tr '\n' ' ')" >> $O/events_i1101.txt
