#!/bin/bash
# #1088: the Jacobian's precision (qd per step; od once, as a chord) with the octo-double residual, D 300 from the guess
{
W=/home/nathan/Source/choptuik-large-d-1088a
T=/home/nathan/Source/t5-mixed2
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1
S=$W/out/j300_held/jump_s_D300.0000.npz
date -u "+start %Y-%m-%d %H:%M:%S UTC"
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 6 1e-40 qd 0 > $T/qd_fresh.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 10 1e-40 od 1 > $T/od_chord.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.01 6 1e-40 qd 0 > $T/qd_scale101.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
