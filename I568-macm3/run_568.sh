#!/bin/bash
# #568: the pivots at the top point of #445's unfinished circle (D 61, M 64, kf 23), the coordinator's command (message of 2026-11-12 06:03 UTC), from the worktree's hp/.
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I568-macm3/started.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py $raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz 0.032 3.286 --M=64 --kf=23 --fmax=1e-15 --json=$raw/I568-macm3/top.json > $raw/I568-macm3/top.log 2>&1
echo "top exit $? at $(date -u +%FT%TZ)" >> $raw/I568-macm3/exits.txt
