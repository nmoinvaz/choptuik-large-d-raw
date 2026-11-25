#!/bin/bash
# speed probes at D 300 (#1088): octo-double Jacobian with 1 and 2 tangents, then the f64-Jacobian iteration from the
# guess and its control (J times 1.01)
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1
S=$W/out/j300_held/jump_s_D300.0000.npz
O=$W/out/mixed
mkdir -p $O
date -u "+start %Y-%m-%d %H:%M:%S UTC"
$PY -u $W/mixed.py tangents $S 6 > $O/tangents.log 2>&1
$PY -u $W/mixed.py mixed $S 6 $W/raw 252.5 3 1.0 8 > $O/mixed.log 2>&1
$PY -u $W/mixed.py mixed $S 6 $W/raw 252.5 3 1.01 8 > $O/mixed_scale101.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
