#!/bin/bash
# hp's d/dtheta operator against the 120-digit one in one D 300 residual (dmat_ms_check.py), fastmul6 site_y, 4 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
mkdir -p $W/out/dmat_ms
cd $W/hp_y || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_y
nice -n 10 $(cat $W/python_path) -u dmat_ms_check.py $W/out/budget300_src/D300_full_base.npz --kfreeze 13 --threads 4 \
  > $W/out/dmat_ms/D300.log 2>&1
echo "rc $?" >> $W/out/dmat_ms/D300.log
exit
}
