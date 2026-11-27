#!/bin/bash
# #1098 D 4628 (Track A): the dd residual of form_s.py jump's guess (no Newton), per block, at a 9.995 and 11.565,
# degree 0 from D 4000's jump state and degree 1 from D 2000 base h13 + D 4000's jump; D 4000's state at its own D as
# the baseline. fastmul7 hp_z/site_z, 4 threads, into I1098-dh610/ladder/D4628_guess/
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh610/ladder/inputs
O=$LV/I1098-dh610/ladder/D4628_guess
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
A=$I/D4000_jump_mm5.npz; B=$I/D2000_base6_h13.npz
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/gtest.log
nice -n 10 $PY -u $O/jump_guess_resid.py $W/hp_z 4 own:0:9.995:own:$A own:0:11.565:6959:$A \
  4628:0:9.995:6959:$A 4628:0:11.565:6959:$A 4628:1:9.995:6959:$B+$A 4628:1:11.565:6959:$B+$A >> $O/gtest.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/gtest.log
exit
}
