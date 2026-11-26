#!/bin/bash
# #1098: horizon_mp_check.py with mpmath's u series given horizon_mob's split B_0 = 1 + X (--split 1): if Moebius's
# fixed 1e-40 offset is the double-double D_e's row sums, the kernel's Moebius values match this series far below 1e-40
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/mpcheck
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
S=$W/out/budget300_src/D300_full_base.npz
timeout 2h $PY -u horizon_mp_check.py $S --ks_mp 500 --ks_mob 600 --split 1 --mob_scan 4:600,8:800 > $O/horizon300_split.log 2>&1
echo "rc $?" >> $O/horizon300_split.log
exit
}
