#!/bin/bash
# fastmul7's split check failed its bar: Moebius (a 8, ks 800) against mpmath's converged u sum 4.65e-70 at D 300's u
# h21 state, with the old split's control at 1.7e-60. Whether the 4.65e-70 is the Moebius series' truncation at ks 800
# (the bar 1e-100 set for rounding alone) or arithmetic: the same check with a ks scan (a 8 at ks 800..1600) and the
# main comparison at ks 1600, on site_z
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/fastmul7_build
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
nice -n 10 $PY -u horizon_mp_check.py $W/out/mpcheck/states/D300u_h21.npz --ks_mp 1100 --ks_mob 1600 --bar 1e-100 \
  --mob_scan 8:800,8:1000,8:1200,8:1400,8:1600,4:800,4:1200 --ctl_mutate 57 --ctl_bar 1e-80 > $O/split300_scan.log 2>&1
echo "split scan exit=$?" >> $O/exit_codes.txt
exit
}
