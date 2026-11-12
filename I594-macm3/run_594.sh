#!/bin/bash
# #594 (a) then the control, macm3's part: modecount_circle.py --ball=320 (main f338b9ef) from the worktree ~/Source/choptuik-large-d-b584, 3 threads each.
# Waits for #590 (7 exits) first, as the coordinator said "after #590".
raw=/Users/nathan/Source/choptuik-large-d-raw
while [ "$(wc -l < $raw/I590-macm3/exits.txt 2>/dev/null || echo 0)" -lt 7 ]; do sleep 20; done
cd ~/Source/choptuik-large-d-b584
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=../choptuik-large-d-raw/I594-macm3
date -u +%FT%TZ > $raw/I594-macm3/kf29/started.txt
caffeinate -is nice -n 10 python3 -u hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 3.1023,-0.0068,0.01 --M=48 --kf=29 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf29 --ball=320 --threads=3 --data=$R/kf29 > $R/kf29/circle.log 2>&1
echo "kf29_R0.01 exit $? at $(date -u +%FT%TZ)" >> $raw/I594-macm3/exits.txt
date -u +%FT%TZ > $raw/I594-macm3/ctl_kf27/started.txt
caffeinate -is nice -n 10 python3 -u hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 1.902797,0.916032,0.06 --M=48 --kf=27 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf27 --ball=320 --threads=3 --data=$R/ctl_kf27 > $R/ctl_kf27/circle.log 2>&1
echo "ctl_kf27_R0.06 exit $? at $(date -u +%FT%TZ)" >> $raw/I594-macm3/exits.txt
