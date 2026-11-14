#!/bin/bash
# #708, the coordinator's message 1794621728516-0: an R 0.1 circle for the pair near the real axis at kf 37, centred on the real axis at 2.903, started when the kf 37 right circles free threads.
# The kf 37 left circles' pair (rerun37/, main 989e103c) is at 2.903 +- 0.057i (estimates 2.0e-2 and 1.9e-2), inside R 0.1; the nearest other zero (3.193 + 0.168i) is 0.33 away. The winding should be +2.
# 2 threads, the same command and builds as the other kf 37 circles (b596, main b5d69cc2), only the centre and radius changed.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf37/pair/data
echo "708 kf37 pair start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.903,0,0.1 --M=48 --kf=37 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf37 --ball=320 --threads=2 --data=$R/kf37/pair/data > $R/kf37/pair/run.log 2>&1
echo "708 kf37 pair exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
