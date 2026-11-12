#!/bin/bash
# #584, the M 64 points (win3's, taken over by macm3): hp/modecount_qdet.py at #579's q1, q2, s3 and s4 on #445's D 61 M 64 kf 23 state, the
# coordinator's command (message of 2026-11-12 16:22 UTC), from the worktree's hp/ (main 4b33cc9d, the modecount_cx of 14db20a9), 2 threads.
cd ~/Source/choptuik-large-d-b584/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I584-macm3/started_kf23.txt
caffeinate -is nice -n 10 python3 -u modecount_qdet.py $raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz 1.980000,0.749808 1.698092,1.097394 0.132000,2.912795 -0.141205,3.186000 --M=64 --kf=23 --fmax=1e-15 --threads=2 --ulp --draws=4 --json=$raw/I584-macm3/kf23_M64.json > $raw/I584-macm3/kf23_M64.log 2>&1
echo "kf23_M64 exit $? at $(date -u +%FT%TZ)" >> $raw/I584-macm3/exits.txt
