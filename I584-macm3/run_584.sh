#!/bin/bash
# #584, macm3's part: hp/modecount_qdet.py (main 14db20a9) at #579's stuck points s1 and s2 on the kf 29 state, the coordinator's command
# (message of 2026-11-12 11:26 UTC), from the worktree's hp/, 3 threads.
cd ~/Source/choptuik-large-d-b584/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I584-macm3/started.txt
caffeinate -is nice -n 10 python3 -u modecount_qdet.py data/seeds/local/up23_D61.0264.npz 3.100221,0.002981 3.100564,-0.016648 --M=48 --kf=29 --fmax=1e-15 --threads=3 --ulp --draws=4 --json=$raw/I584-macm3/kf29_s1s2.json > $raw/I584-macm3/kf29_s1s2.log 2>&1
echo "kf29_s1s2 exit $? at $(date -u +%FT%TZ)" >> $raw/I584-macm3/exits.txt
