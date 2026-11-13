#!/bin/bash
# #657, the coordinator's instruction (message of 2026-11-13 13:52 UTC): "if the pair near the real axis appears again, add an R 0.05 circle around it as in #656". At kf 33 the R 0.36 circles at
# 2.85 +- 0.25i hold the pair 2.9593 +0.0272i and 2.9643 -0.0262i (estimates 6e-2): an R 0.05 circle at 2.962, 6 threads, same command and builds as #656 (only the centre and radius changed).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I657-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf33/pair/data
echo "657 kf33 pair start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.962,0,0.05 --M=48 --kf=33 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf33 --ball=320 --threads=6 --data=$R/kf33/pair/data > $R/kf33/pair/run.log 2>&1
echo "657 kf33 pair exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
