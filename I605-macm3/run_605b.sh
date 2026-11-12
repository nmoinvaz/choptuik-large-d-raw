#!/bin/bash
# #605, the intermediate ulps (the coordinator's message of 2026-11-12 18:27 UTC): --ulps=3,5,6,7 at s3, after the root and its repeat, so the phase
# can be unwrapped along k = 1 to 8. Same tree, state and options as run_605.sh.
raw=/Users/nathan/Source/choptuik-large-d-raw
while ! grep -q '^root_repeat exit' $raw/I605-macm3/exits.txt 2>/dev/null; do sleep 20; done
cd ~/Source/choptuik-large-d-b596/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
caffeinate -is nice -n 10 python3 -u modecount_qdet.py $raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz 0.132000,2.912795 --M=64 --kf=23 --fmax=1e-15 --threads=4 --ulps=3,5,6,7 --json=$raw/I605-macm3/s3_ulps3567.json > $raw/I605-macm3/s3_ulps3567.log 2>&1
echo "s3_extra exit $? at $(date -u +%FT%TZ)" >> $raw/I605-macm3/exits.txt
