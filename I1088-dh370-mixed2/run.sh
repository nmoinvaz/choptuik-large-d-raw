#!/bin/bash
# #1088: Newton with the double-double Jacobian refreshed per step and the octo-double residual, at D 300 from the guess
{
W=/home/nathan/Source/choptuik-large-d-1088a
T=/home/nathan/Source/t5-mixed2
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1
S=$W/out/j300_held/jump_s_D300.0000.npz
date -u "+start %Y-%m-%d %H:%M:%S UTC"
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 8 1e-40 > $T/dd.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.01 8 1e-40 > $T/dd_scale101.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 f64 1.0 8 1e-40 > $T/f64_fresh.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
