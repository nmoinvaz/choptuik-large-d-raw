#!/bin/bash
# #1013 step 4 on rpi5: the upper box, then its two recount rungs. Stops at the first step that exits non-zero or leaves no leaves file.
# Run from anywhere:  setsid nohup bash run1013.sh > logs/driver.log 2>&1 &
set -u
RAW=$(cd "$(dirname "$0")" && pwd); PY=$HOME/Source/venv-choptuik/bin/python; N=4
cd $HOME/Source/cl-995/solver/inner_stokes || exit 9
stamp() { echo "$(date -u '+%F %H:%M:%S UTC') $*"; }
stamp "driver start, code $(git -C . rev-parse --short HEAD), N=$N"
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=3.6,5.1 --wf=0.5,1.3 --nA=6 --nwf=8 --procs=$N --out=$RAW/m3 --tag=M3_upper > $RAW/logs/m3_upper.log 2>&1
rc=$?; stamp "step 1 (box) exit $rc"; [ $rc -eq 0 ] && [ -s $RAW/m3/leaves_M3_upper.jsonl ] || { stamp "stop: step 1 did not finish cleanly"; exit 1; }
nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper.jsonl --r1=0.25 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.25 > $RAW/logs/m3_upper_r0.25.log 2>&1
rc=$?; stamp "step 2 (recount r 0.25) exit $rc"; [ $rc -eq 0 ] && [ -s $RAW/m3/leaves_M3_upper_r0.25.jsonl ] || { stamp "stop: step 2 did not finish cleanly"; exit 2; }
nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.17 > $RAW/logs/m3_upper_r0.17.log 2>&1
rc=$?; stamp "step 3 (recount r 0.17) exit $rc"; [ $rc -eq 0 ] || { stamp "stop: step 3 did not finish cleanly"; exit 3; }
stamp "driver done"
