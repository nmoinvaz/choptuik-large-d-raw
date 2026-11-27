#!/bin/bash
# #1098 D 5555, 6666, 8000 (Track A): the held guess's blocks (form_s_lastnode.py ratio, double-double) at the last
# node 0.7062221 (D 8000's L = 20 node), deg 2 in 1/n from #1088's lastnode states at D 4000, 5657 and 8000, with
# a = (D - 2)/400, ks = ceil(1.5 (D - 2)) + 20, kc 260; and, as the contrast, D 5555 at the inherited 0.7035589
# (L 55) from the same states (deg 1, D 2000 base h13 and D 4000's jump). 2 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh610/ladder/inputs
O=$LV/I1098-dh610/ladder/D4628_guess
G=$O/inputs
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
S3=$G/lastnode_D4000.0000.npz,$G/lastnode_D5656.8542.npz,$G/lastnode_D8000.0000.npz
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $O/ratio_hi.log
for c in 5555:13.8825:8350 6666:16.66:10016 8000:19.995:12017; do
  IFS=: read D A K <<< "$c"
  echo "D $D: deg 2, #1088 lastnode D 4000, 5657, 8000, a $A, ks $K" >> $O/ratio_hi.log
  nice -n 10 $PY -u form_s_lastnode.py ratio $O/rhi_$D --D $D --mob $A --ks $K --kc 260 --parts 2 --threads 2 --deg 2 \
    --states_s $S3 --xl 0.7062221251334241 >> $O/ratio_hi.log 2>&1
done
echo "D 5555: deg 1, D2000_base6_h13 + D4000_jump_mm5 (the inherited node)" >> $O/ratio_hi.log
nice -n 10 $PY -u form_s_lastnode.py ratio $O/rhi_5555b --D 5555 --mob 13.8825 --ks 8350 --kc 260 --parts 2 --threads 2 \
  --deg 1 --states_s $I/D2000_base6_h13.npz,$I/D4000_jump_mm5.npz --xl 0.7035589258590665,0.7062221251334241 \
  >> $O/ratio_hi.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/ratio_hi.log
exit
}
