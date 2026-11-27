#!/bin/bash
# #1098: the downward gate's control again at D 4000's jump state, ks 4717 (ks_gate.py of wip/large-d-form-s 3b3bfc60 as
# hp_z/ks_gate_v2.py: Delta's 1e-40 in the third part; in the second part it was lost to rounding and read 0.0),
# fastmul7 site_z, 4 threads; log into I1098-dh610/ksdown/D4000_d.log
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=/home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ksdown
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
nice -n 10 $(cat $W/python_path) -u ks_gate_v2.py $O/jump_s_D4000.0000.npz --bar 1e-64 --down 1 --ks0 4717 --step 100 \
  --ks_min 4717 --threads 4 > $O/D4000_d.log 2>&1
echo "rc $?" >> $O/D4000_d.log
exit
}
