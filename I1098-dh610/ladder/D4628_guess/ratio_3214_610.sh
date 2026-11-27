#!/bin/bash
# #1098 D 3214 (Track A): the held guess's blocks (form_s_lastnode.py ratio, double-double, a 8.03, ks 4838, kc 250) at
# x_l 0.7053359 (D 4000's L = 20 node, L 16.1 at D 3214), deg 2 in 1/n from D 2000's base h13 and #1088's lastnode
# states at D 2828 and 4000. 2 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh610/ladder/inputs
O=$LV/I1098-dh610/ladder/D4628_guess
G=$O/inputs
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/ratio_3214.log
nice -n 10 $PY -u form_s_lastnode.py ratio $O/r3214 --D 3214 --mob 8.03 --ks 4838 --kc 250 --parts 2 --threads 2 --deg 2 \
  --states_s $I/D2000_base6_h13.npz,$G/lastnode_D2828.4271.npz,$G/lastnode_D4000.0000.npz \
  --xl 0.705335927228362 >> $O/ratio_3214.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/ratio_3214.log
exit
}
