#!/bin/bash
# #708, the coordinator's message 1794626380955-0: an R 0.05 circle around the zero at 3.191 + 0.164i at kf 37, as at kf 35, started when the kf 35 pair circle ends (its threads). The circle winds +1 if the left and the
# right R 0.36 circles report one zero there (the box's count at kf 37 is then 10) and otherwise the count changes. Centre: the mean of the left circle's report (3.192676 + 0.168031i) and the right circle's
# (3.189818 + 0.159717i), 3.1912 + 0.1639i; the lower circle is its conjugate. 2 threads (the kf 37 pair circle runs 4), the same command and builds as the other kf 37 circles (b596, main b5d69cc2), only the centre and radius changed.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf37/lens/data
echo "708 kf37 lens start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 3.1912,0.1639,0.05 --M=48 --kf=37 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf37 --ball=320 --threads=2 --data=$R/kf37/lens/data > $R/kf37/lens/run.log 2>&1
echo "708 kf37 lens exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
