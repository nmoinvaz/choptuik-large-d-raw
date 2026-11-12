#!/bin/bash
# #552's kf 29 command again with modecount_pivots.py of main 80b5056 (it prints arg det's change), the coordinator's message of 2026-11-12 06:43 UTC.
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I552-macm3/started_arg.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py data/seeds/local/up23_D61.0264.npz 3.1023 -0.0068 --M=48 --kf=29 --fmax=1e-15 --json=$raw/I552-macm3/kf29_arg.json > $raw/I552-macm3/kf29_arg.log 2>&1
echo "kf29_arg exit $? at $(date -u +%FT%TZ)" >> $raw/I552-macm3/exits.txt
