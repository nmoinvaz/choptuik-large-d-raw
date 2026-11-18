#!/bin/bash
# #949: when every queued backfill read has exited (23 exit lines, all but ctl_planted_mut with rc 0), freeze the baseline
# (track949.py --freeze refuses if a state of ks > 240 has been read) and only then release leg 8's held queue lines.
HERE=/home/nathan/Source/choptuik-large-d-raw/I949-dh170
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
cd $HERE || exit 9
until [ "$(grep -c ' exit ' exits_949.txt)" -ge "$(wc -l < queue949.txt)" ]; do sleep 20; done
bad=$(grep ' exit ' exits_949.txt | grep -v ' exit 0 ' | grep -v ctl_planted_mut)
[ -n "$bad" ] && { echo "a read exited non-zero, not freezing: $bad"; exit 3; }
$PY track949.py --freeze . || { echo "freeze refused"; exit 4; }
cat queue949_leg08_hold.txt >> queue949.txt && echo "released $(wc -l < queue949_leg08_hold.txt) leg 8 lines at $(date -u '+%F %T')"
