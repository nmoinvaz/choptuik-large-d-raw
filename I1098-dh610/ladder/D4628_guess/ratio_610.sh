#!/bin/bash
# #1098 D 4628 (Track A): the held guess's horizon block against the other blocks (form_s_lastnode.py ratio, the basin
# measure) at the inherited last node x_l 0.7035589 (D 2000's L = 20 node, L = 46 at D 4628) and at nodes outward,
# the sources carried there by Taylor steps (path_s): deg 1 from the jump's two inputs; deg 2 from #1088's lastnode
# states (L = 20 each) at D 2828, 4000, 5657 and 8000. Double-double residuals, a 11.565, ks 6959, kc 260, 4 threads
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
I=$LV/I1098-dh610/ladder/inputs
O=$LV/I1098-dh610/ladder/D4628_guess
G=$O/inputs
mkdir -p $G
git -C $LV fetch -q origin || exit 1
for f in I1088-dh370/L2828/lastnode_D2828.4271.npz I1088-mac-a/form_s/L4000q/lastnode_D4000.0000.npz \
         I1088-dh370/L5657c/lastnode_D5656.8542.npz I1088-mm5/L8000/lastnode_D8000.0000.npz; do
  git -C $LV show origin/main:$f > $G/$(basename $f) || exit 1
  echo "$f blob $(git -C $LV hash-object --no-filters $G/$(basename $f))" >> $O/ratio.log
done
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
C="--D 4628 --mob 11.565 --ks 6959 --kc 260 --parts 2 --threads 4"
date -u "+start %Y-%m-%d %H:%M:%S UTC" >> $O/ratio.log
echo "R1: deg 1, D2000_base6_h13 + D4000_jump_mm5" >> $O/ratio.log
nice -n 10 $PY -u form_s_lastnode.py ratio $O/r1 $C --deg 1 --states_s $I/D2000_base6_h13.npz,$I/D4000_jump_mm5.npz \
  --xl 0.7035589258590665,0.705576,0.705855 >> $O/ratio.log 2>&1
echo "R2: deg 2, #1088 lastnode D 4000, 5657, 8000 (interpolation)" >> $O/ratio.log
nice -n 10 $PY -u form_s_lastnode.py ratio $O/r2 $C --deg 2 \
  --states_s $G/lastnode_D4000.0000.npz,$G/lastnode_D5656.8542.npz,$G/lastnode_D8000.0000.npz \
  --xl 0.7062221251334241 >> $O/ratio.log 2>&1
echo "R3: deg 2, #1088 lastnode D 2828, 4000, 5657" >> $O/ratio.log
nice -n 10 $PY -u form_s_lastnode.py ratio $O/r3 $C --deg 2 \
  --states_s $G/lastnode_D2828.4271.npz,$G/lastnode_D4000.0000.npz,$G/lastnode_D5656.8542.npz \
  --xl 0.7058552367160431 >> $O/ratio.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> $O/ratio.log
exit
}
