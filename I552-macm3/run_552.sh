#!/bin/bash
# #552: the coordinator's two commands (message of 2026-11-12 05:30 UTC), one after the other, from the worktree's hp/.
cd ~/Source/choptuik-large-d-b80/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
date -u +%FT%TZ > $raw/I552-macm3/started.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py data/seeds/local/up23_D61.0264.npz 3.1023 -0.0068 --M=48 --kf=29 --fmax=1e-15 --json=$raw/I552-macm3/kf29.json > $raw/I552-macm3/kf29.log 2>&1
echo "kf29 exit $? at $(date -u +%FT%TZ)" >> $raw/I552-macm3/exits.txt
caffeinate -is nice -n 10 python3 modecount_pivots.py data/seeds/local/up23_D61.0264.npz 2.0510 0 --M=48 --kf=22 --fmax=1e-15 --json=$raw/I552-macm3/kf22.json > $raw/I552-macm3/kf22.log 2>&1
echo "kf22 exit $? at $(date -u +%FT%TZ)" >> $raw/I552-macm3/exits.txt
