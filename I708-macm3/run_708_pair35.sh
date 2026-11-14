#!/bin/bash
# #708, the coordinator's message 1794619159598-0: centre the R 0.05 pair circle at kf 35 from the left R 0.36 circles' positions (rerun/, main 989e103c), not from an extrapolation.
# The four pair values in rerun/c_2.85_*/data/modecount_circles.jsonl (|Im| < 0.05) have mean Re 2.909365 and mean |Im| 0.029654 (estimates 2.3e-2 and 2.6e-2): an R 0.05 circle at 2.9094,
# 2 threads (four kf 37 processes run), the same command and builds as the other kf 35 circles (b596, main b5d69cc2), only the centre and radius changed.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf35/pair/data
echo "708 kf35 pair start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.9094,0,0.05 --M=48 --kf=35 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf35 --ball=320 --threads=2 --data=$R/kf35/pair/data > $R/kf35/pair/run.log 2>&1
echo "708 kf35 pair exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
