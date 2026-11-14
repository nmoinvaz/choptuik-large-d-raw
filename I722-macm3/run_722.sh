#!/bin/bash
# #722 (the coordinator's message 1794629933410-0): an R 0.05 circle around the pair near the real axis at kf 27, centre 3.159, on 6 threads, with the command macm3 ran at kf 33 (#657) and at kf 29 and 31 (#656):
# modecount_circle.py --ball=320, M 48, seed up23_D61.0264.npz, only the cut and the centre changed. The kf 27 state is made by setup from the seed (about 5 min, |F| 1.3e-19 as at the other cuts).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I722-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf27/pair/data
echo "722 kf27 pair start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_722.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 3.159,0,0.05 --M=48 --kf=27 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf27 --ball=320 --threads=6 --data=$R/kf27/pair/data > $R/kf27/pair/run.log 2>&1
echo "722 kf27 pair exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_722.txt
