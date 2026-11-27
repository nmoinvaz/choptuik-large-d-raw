#!/bin/bash
# #1098 on dh610: D 5555's M 32 stages by recipe v2's amendment 2 (ladder_new.sh): x_l 0.7062221 (D 8000's L = 20 node,
# L 13.9 here), the guess deg 2 in 1/n from #1088's lastnode states at D 4000, 5657 and 8000 (in
# ladder/D4628_guess/inputs; dh610's ratio test read 7.5e-13), the jump from it, then ladder_point2.sh (blob e0cf5880)
# with the downward gate from ks0 6660, KSBAR 1e-64, kc 260, chord-free, fastmul7 (hp_z, site_z at c21ba40d), THREADS
# threads (8 by default), through rls13 (STOP_AFTER=rls13). Tools pinned at raw commit TC into ladder/tools4;
# hp_z/ks_gate.py must be 3b3bfc60's (hp_z/ks_gate_v2.py, blob a91c7363, put in place here). Output into the live raw
# worktree's I1098-dh610/ladder/D5555 (no --allow_unraw); the last act writes "job rc N" to its run.log. For another
# Linux machine set W, LV, HP, SITE, PY and the inputs' folder G.
#
#     TC=<raw commit> [THREADS=8] d5555_610.sh
{
W=${W:-/home/nathan/Source/choptuik-large-d-1088a}
LV=${LV:-/home/nathan/Source/choptuik-large-d-raw-1088a-live}
G=${G:-$LV/I1098-dh610/ladder/D4628_guess/inputs}
T=$LV/I1098-dh610/ladder/tools4
O=$LV/I1098-dh610/ladder/D5555
export HP=${HP:-$W/hp_z} SITE=${SITE:-$W/site_z} PY=${PY:-$(cat $W/python_path)} COMMIT=${COMMIT:-c21ba40d}
[ -n "$TC" ] || { echo "TC (the raw commit of the tools) is not set"; exit 1; }
mkdir -p $T $O
git -C $LV fetch -q origin || exit 3
for f in ladder_new.sh ladder_point2.sh variant_state.py resample_m.py kstar_stage.sh kstar_gain.py kstar_summary.py \
         kmax_rule.py; do
  git -C $LV show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
[ "$(git -C $LV hash-object --no-filters $T/ladder_point2.sh)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 3
for f in lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319 \
         lastnode_D8000.0000.npz:511a1ff828a54aa235775c972082b4a5876274f2; do
  [ "$(git -C $LV hash-object --no-filters $G/${f%%:*})" = "${f#*:}" ] || exit 4
done
[ "$(git -C $LV hash-object --no-filters $HP/ks_gate_v2.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
cp $HP/ks_gate_v2.py $HP/ks_gate.py
echo "tools4 from raw $TC, inputs and ks_gate.py (3b3bfc60) checked by blob $(date -u +%H:%M:%S)" > $O/setup.log
export STOP_AFTER=rls13 KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $T/ladder_new.sh 5555 260 ${THREADS:-8} $O $G/lastnode_D4000.0000.npz,$G/lastnode_D5656.8542.npz,$G/lastnode_D8000.0000.npz \
  0.7062221251334241 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
