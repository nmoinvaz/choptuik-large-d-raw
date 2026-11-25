#!/bin/bash
# the check of the Moebius series' z recurrence (ae0b5453) against the full Cauchy sums and its control, at the D 1000
# held state and the D 2000 guess, on this machine's release build, 1 thread
{
W=/home/nathan/Source/choptuik-large-d-1088a
cd $W/hp || exit 1
mkdir -p $W/out/zcheck
for st in $W/out/j1000_held_mob/jump_s_D1000.0000.npz $W/out/g2000_B/jump_s_D2000.0000.npz; do
  HP_DIR=$W/hp PYTHONPATH=$W/site OPENBLAS_NUM_THREADS=1 $(cat $W/python_path) -u $W/zcheck.py $st 1
done > $W/out/zcheck/zcheck.log 2>&1
exit
}
