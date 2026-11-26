#!/bin/bash
# horizon_mp_check.py with --mp_mob 1 (mpmath's Moebius series), a short test on fastmul7 (site_z) at D 300's u h21
# state: ks_mob TEST (100 by default), the u reference to ks_mp 300; then, when TEST is "full", the standing check at
# a 8, ks 800 against the u reference to 1100
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/fastmul7_build
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
T=${1:-100}
if [ "$T" = "full" ]; then
  nice -n 10 $PY -u horizon_mp_check_v2.py $W/out/mpcheck/states/D300u_h21.npz --ks_mp 1100 --ks_mob 800 --mp_mob 1 \
    --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80 > $O/split300_mpmob.log 2>&1
  echo "split mpmob exit=$?" >> $O/exit_codes.txt
else
  nice -n 10 $PY -u horizon_mp_check_v2.py $W/out/mpcheck/states/D300u_h21.npz --ks_mp 300 --ks_mob $T --mp_mob 1 \
    --bar 1e-100 --ctl_mutate 57 --ctl_bar 1e-80 > $O/mpmob_test_$T.log 2>&1
  echo "rc $?" >> $O/mpmob_test_$T.log
fi
exit
}
