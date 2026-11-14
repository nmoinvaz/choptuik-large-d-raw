#!/bin/bash
# #708, the coordinator's message 1794620581975-0: an R 0.05 circle around the zero at 3.198 + 0.190i at kf 35, started when the pair circle ends (its threads). The circle winds +1 if the left and the right R 0.36 circles
# report one zero there (the box's count is then 10) and otherwise the count is 12. Centre: the mean of the left circle's report (3.192775 + 0.192166i) and the right circle's (3.202642 + 0.188633i),
# 3.1977 + 0.1904i; the lower circle is its conjugate. 2 threads, the same command and builds as the other kf 35 circles (b596, main b5d69cc2), only the centre and radius changed.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
mkdir -p $R/kf35/lens/data
echo "708 kf35 lens start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 3.1977,0.1904,0.05 --M=48 --kf=35 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf35 --ball=320 --threads=2 --data=$R/kf35/lens/data > $R/kf35/lens/run.log 2>&1
echo "708 kf35 lens exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_708.txt
