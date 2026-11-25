#!/bin/bash
# the condition table at one horizon order for every D (#1088): forms A and S at D 100, 200 and 245.56, ks 293
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=2
date -u "+start %Y-%m-%d %H:%M:%S UTC"
$PY -u form_s.py cond $W/states/anm_pin3_D100.0000.npz $W/states/anm_pin3_D200.0000.npz --threads 8 --kfreeze 13 --ks 293 --segs plan > $W/out/cond_ks293.log 2>&1
date -u "+end %Y-%m-%d %H:%M:%S UTC"
exit
}
