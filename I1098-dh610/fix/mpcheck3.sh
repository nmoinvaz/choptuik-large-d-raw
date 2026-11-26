#!/bin/bash
# #1098: horizon_mp_check.py at D 300's base state with every sum exact: the u values against mpmath's converged u series
# (to order 900) at ks 306-706, and the Moebius values at a 4-16 and ks 600-1200 (fastmul5, site_x)
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/mpcheck
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
S=$W/out/budget300_src/D300_full_base.npz
timeout 3h $PY -u horizon_mp_check.py $S --ks_mp 900 --ks_mob 600 --u_scan 306,406,506,706 \
  --mob_scan 8:600,8:800,8:1000,6:600,6:800,4:600,4:800,16:1200 > $O/horizon300_v3.log 2>&1
echo "rc $?" >> $O/horizon300_v3.log
exit
}
