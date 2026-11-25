#!/bin/bash
# #1088: D 300 with the Moebius horizon (a = 8): double-double Jacobian with octo-double or double-double residuals
{
W=/home/nathan/Source/choptuik-large-d-1088a
T=/home/nathan/Source/t5-mixed2
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1
S=$W/out/j300_held/jump_s_D300.0000.npz
until PYTHONPATH=$W/site $PY -c "import sys; from hpkernel import Solver; sys.exit(0 if hasattr(Solver, 'set_horizon_mobius') else 1)" 2>/dev/null && ! systemctl --user is-active -q i1088a-buildmob; do sleep 60; done
date -u "+start %Y-%m-%d %H:%M:%S UTC"
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 8 1e-40 dd 0 8 od > $T/mob_ddJ_odR.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 8 1e-28 dd 0 8 dd > $T/mob_ddJ_ddR.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.01 8 1e-40 dd 0 8 od > $T/mob_ddJ_scale101.log 2>&1
nice -n 10 $PY -u $T/mixed2.py $S 4 $W/raw 252.5 3 dd 1.0 6 1e-40 qd 0 8 od > $T/mob_qdJ_odR.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
