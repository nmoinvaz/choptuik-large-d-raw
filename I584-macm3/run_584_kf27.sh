#!/bin/bash
# #584, the kf 27 half (win3's, taken over by macm3): hp/modecount_qdet.py at #579's q3 and q4 and #585's N1, N2, F1, F2, F3 on the kf 27 state,
# the coordinator's command (message of 2026-11-12 14:44 UTC), from the worktree's hp/ (main 4b33cc9d, the modecount_cx of 14db20a9), 3 threads.
cd ~/Source/choptuik-large-d-b584/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I584-macm3/started_kf27.txt
caffeinate -is nice -n 10 python3 -u modecount_qdet.py $raw/I280-macm3/hp_data_after/modecount_state_D61.0264_M48_kf27.npz 3.595442,0.504558 4.530000,-1.061769 1.923548,0.910715 2.396619,0.567672 2.7387538820250192,-0.9076196541337447 3.6,1.0 4.35,-1.75 --M=48 --kf=27 --fmax=1e-15 --threads=3 --ulp --draws=4 --json=$raw/I584-macm3/kf27_M48.json > $raw/I584-macm3/kf27_M48.log 2>&1
echo "kf27_M48 exit $? at $(date -u +%FT%TZ)" >> $raw/I584-macm3/exits.txt
