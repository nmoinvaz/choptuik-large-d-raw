#!/bin/bash
# after the first z-recurrence check (unit i1088a-zcheck, build ae0b5453): keep its log, rebuild with the constants in
# the lane's precision (815287c6 or later; rebuild_mob.sh), and check again at the D 1000 held state and the D 2000 guess
# (zcheck.py, bars 1e-100 and 1e-30), 6 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
while systemctl --user is-active --quiet i1088a-zcheck; do sleep 30; done
cp $W/out/zcheck/zcheck.log $W/out/zcheck/zcheck_ae0b5453.log
bash $W/rebuild_mob.sh > $W/out/zcheck/rebuild.log 2>&1 || exit 1
cd $W/hp || exit 1
for st in $W/out/j1000_held_mob/jump_s_D1000.0000.npz $W/out/g2000_B/jump_s_D2000.0000.npz; do
  HP_DIR=$W/hp PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1 $(cat $W/python_path) -u $W/zcheck.py $st 6
done > $W/out/zcheck/zcheck_815287c6.log 2>&1
exit
}
