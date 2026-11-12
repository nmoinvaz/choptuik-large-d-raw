#!/bin/bash
# #568's command again with modecount_pivots.py of main 80b5056 (it prints arg det's change), the coordinator's message of 2026-11-12 06:43 UTC.
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I568-macm3/started_arg.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py $raw/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz 0.032 3.286 --M=64 --kf=23 --fmax=1e-15 --json=$raw/I568-macm3/top_arg.json > $raw/I568-macm3/top_arg.log 2>&1
echo "top_arg exit $? at $(date -u +%FT%TZ)" >> $raw/I568-macm3/exits.txt
