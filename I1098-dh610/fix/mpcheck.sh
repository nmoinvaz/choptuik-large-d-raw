#!/bin/bash
# #1098: the independent mpmath checks on fastmul5 (site_x): the Taylor step (taylor_mp_check.py) and the horizon values
# (horizon_mp_check.py: u and Moebius against mpmath's u series) at D 300's base state
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/mpcheck
mkdir -p $O
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
S=$W/out/budget300_src/D300_full_base.npz
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/run.log
$PY -u taylor_mp_check.py $S > $O/taylor300.log 2>&1
echo "taylor rc $?" >> $O/run.log
timeout 3h $PY -u horizon_mp_check.py $S --ks_mob 600 > $O/horizon300.log 2>&1
echo "horizon rc $?" >> $O/run.log
date -u "+end %Y-%m-%d %H:%M:%S UTC" >> $O/run.log
exit
}
