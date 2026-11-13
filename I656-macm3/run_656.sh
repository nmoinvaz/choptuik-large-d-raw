#!/bin/bash
# #656: one exact-determinant circle (--ball=320) of radius 0.05 around 3.10 at kf 29 and around 3.027 at kf 31, M 48, with modecount_circle.py exactly as #551 ran it
# (I551-win2/run_551.sh: same seed, layout and options; only the centre and radius changed). From hp/ of the worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2
# (hp/modecount_circle.py, modecount_common.py, modecount_cx and modecount_qdet.py are identical to 98ee71bd, #551's commit: git diff empty). The kf K state is made by setup
# from data/seeds/local/up23_D61.0264.npz. The two cuts run at once, 3 threads each, nice 10, caffeinate.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I656-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
go() {  # K centre
  mkdir -p $R/kf$1/data
  echo "656 kf$1 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_656.txt
  caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $2,0,0.05 --M=48 --kf=$1 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$1 --ball=320 --threads=3 --data=$R/kf$1/data > $R/kf$1/run.log 2>&1
  echo "656 kf$1 exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_656.txt
}
go 29 3.10 &
go 31 3.027 &
wait
