#!/bin/bash
# #657, the kf 33 half (the coordinator's message of 2026-11-13 13:52 UTC): #551's box at kf 33 on the exact determinant, M 48, --ball=320, as I551-win2/run_551.sh ran it at kf 29 and 31
# (same seed, layout and options; only the cut changed): the control circle (R 0.2 around lambda_phys 2.043532530673195) and the four R 0.36 circles at 2.85 +- 0.25i and 3.35 +- 0.25i.
# From hp/ of the worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2 (the build of #656). The five circles are independent, so each runs as its own process with its own cache,
# 1 thread each (5 threads; the control ends first), instead of one process on 6 threads: the first (the control) makes the kf 33 state with setup, the others start when it is saved.
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw-641/I657-macm3
cd /Users/nathan/Source/choptuik-large-d-b596/hp
go() {  # name circle
  mkdir -p $R/kf33/$1/data
  echo "657 kf33 $1 start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
  caffeinate -is nice -n 10 python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz $2 --M=48 --kf=33 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf33 --ball=320 --threads=1 --data=$R/kf33/$1/data > $R/kf33/$1/run.log 2>&1
  echo "657 kf33 $1 exit $? at $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_657.txt
}
go control 2.043532530673195,0,0.2 &
while ! grep -q "saved modecount_state_D61.0264_M48_kf33.npz" $R/kf33/control/run.log 2>/dev/null; do sleep 15; if ! pgrep -f "kf33/control/data" > /dev/null; then break; fi; done
go c_2.85_p0.25 2.85,0.25,0.36 &
go c_3.35_p0.25 3.35,0.25,0.36 &
go c_2.85_m0.25 2.85,-0.25,0.36 &
go c_3.35_m0.25 3.35,-0.25,0.36 &
wait
