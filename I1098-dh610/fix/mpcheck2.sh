#!/bin/bash
# #1098: horizon_mp_check.py again at D 300's base state: the u partial sums scanned in ks, and the Moebius values with
# the relaxed products on and off
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/mpcheck
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
S=$W/out/budget300_src/D300_full_base.npz
HP_HORIZON_RELAXED=1 timeout 3h $PY -u horizon_mp_check.py $S --ks_mob 600 --u_scan 20,50,100,140,160,200,306 > $O/horizon300_r1.log 2>&1 &
HP_HORIZON_RELAXED=0 timeout 3h $PY -u horizon_mp_check.py $S --ks_mob 600 > $O/horizon300_r0.log 2>&1 &
wait
exit
}
