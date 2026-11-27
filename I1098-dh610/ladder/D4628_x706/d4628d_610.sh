#!/bin/bash
# #1098 D 4628 with the last node moved (Track A, 2026-11-27). The jumps of D 4000 and 4628 kept D 2000's last node
# x_l 0.7035589 (its L = (n/2) ln(1/x_l^2 - 1) = 20 node), L 40 at D 4000 and 46 at D 4628, where the fast mode makes
# the horizon map about e^L nonlinear (#1088, form_s_lastnode.py): d4628b's guess read a horizon block 1.8e9 times the
# other blocks, and 2.7 times them at L 20 (D4628_guess/ratio.log). Here x_l is D 8000's L = 20 node 0.7062221 (L 11.6
# at D 4628), so #1088's lastnode states at D 4000, 5657 and 8000 interpolate the guess (deg 2 in 1/n, carried to x_l
# by Taylor steps; ratio.log R2: 8.0e-12, 3.9 times the others). Steps: (1) that guess (form_s_lastnode.py guess);
# (2) form_s.py jump from it, ladder_point2.sh's jump with --deg 0 (held, a 11.565, ks 6959, kc 260, dd then qd,
# it_max 12, 8 threads); (3) when it converges: stop i1088a-d4628b, i1088a-d4628c and i1088a-ksdown3 (the L 46 jump
# and the two units waiting on it), install the downward gate (hp_z/ks_gate_v2.py, wip/large-d-form-s 3b3bfc60) as
# hp_z/ks_gate.py and ladder_point2.sh blob e0cf5880 in tools3, as d4628c would, and run the point from the kept jump:
# KSGATE_EXTRA="--down 1 --step 100", KSBAR 1e-64, STOP_AFTER=rls13, chord-free, fastmul7, into ladder/D4628_x706
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
T=$LV/I1098-dh610/ladder/tools3
G=$LV/I1098-dh610/ladder/D4628_guess/inputs
O=$LV/I1098-dh610/ladder/D4628_x706
mkdir -p $O/jump $O/guess
P=$O/pre.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $P
for f in lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319 \
         lastnode_D8000.0000.npz:511a1ff828a54aa235775c972082b4a5876274f2; do
  [ "$(git -C $LV hash-object --no-filters $G/${f%%:*})" = "${f#*:}" ] || { echo "input ${f%%:*}: blob differs" >> $P; exit 2; }
done
cd $W/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_z
PY=$(cat $W/python_path)
nice -n 10 $PY -u form_s_lastnode.py guess $O/guess --D 4628 --mob 11.565 --ks 6959 --kc 260 --deg 2 --threads 8 \
  --states_s $G/lastnode_D4000.0000.npz,$G/lastnode_D5656.8542.npz,$G/lastnode_D8000.0000.npz \
  --xl 0.7062221251334241 >> $P 2>&1
GS=$O/guess/guess_D4628.0000.npz
[ -s $GS ] || { echo "no guess" >> $P; exit 3; }
nice -n 10 timeout 3h $PY -u form_s.py jump $O/jump --D 4628 --states_s $GS --deg 0 --held 1 --mob 11.565 --ks 6959 \
  --kc 260 --delta fit --tol 1e-300 --it_max 12 --threads 8 --commit c21ba40d > $O/jump/jump.log 2>&1
echo "jump rc $? $(date -u +%H:%M:%S)" >> $P
grep -q "^  converged" $O/jump/jump.log && [ -s $O/jump/jump_s_D4628.0000.npz ] || exit 4
for u in i1088a-d4628b i1088a-d4628c i1088a-ksdown3; do
  systemctl --user is-active --quiet $u && systemctl --user stop $u && echo "stopped $u $(date -u +%H:%M:%S)" >> $P
done
[ "$(git -C $LV hash-object --no-filters $W/hp_z/ks_gate_v2.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
cp $W/hp_z/ks_gate_v2.py $W/hp_z/ks_gate.py
git -C $LV fetch -q origin
git -C $LV show e0cf58809f062a6791e7d982369be5eaa57d97ad > $O/ladder_point2.sh.new || exit 5
[ "$(git -C $LV hash-object --no-filters $O/ladder_point2.sh.new)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 5
mv $O/ladder_point2.sh.new $T/ladder_point2.sh
echo "ks_gate.py = 3b3bfc60's, tools3/ladder_point2.sh = e0cf5880 $(date -u +%H:%M:%S)" >> $P
export HP=$W/hp_z SITE=$W/site_z PY COMMIT=c21ba40d
export KSBAR=1e-64 STOP_AFTER=rls13 INNER_CHORD=0 EXTRA= KSGATE_EXTRA="--down 1 --step 100"
bash $T/ladder_point2.sh 4628 260 8 $O $GS $GS 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
