#!/bin/bash
# #605, a third root run (the control between run 1 and run 2 failed at 1e-10 in ln|det|; run 1 made the state, run 2 loaded the saved one): same command as run_605.sh's root.
cd ~/Source/choptuik-large-d-b596/hp
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
raw=/Users/nathan/Source/choptuik-large-d-raw
caffeinate -is nice -n 10 python3 -u modecount_qdet.py data/states/up10_D55.0351.npz 2.0476841270,0 --M=64 --kf=33 --fmax=1e-15 --threads=4 --ulps=1,2,4,8 --json=$raw/I605-macm3/root_repeat2.json > $raw/I605-macm3/root_repeat2.log 2>&1
echo "root_repeat2 exit $? at $(date -u +%FT%TZ)" >> $raw/I605-macm3/exits.txt
