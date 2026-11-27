#!/bin/bash
# #1098 on dh370 (coordinator, 2026-11-27 01:36 UTC): D 5555's M 32 stages by recipe v2's amendment 2 (ladder_new.sh,
# raw c281b00d3), moved here from dh610's chain. Kernel: fastmul6's Skylake wheel (site_sky, d368a0c0), not fastmul7,
# accepted for this point because D 1291's kernel cross-check (fastmul7 against fastmul6 from the same h21 state) moved
# Delta by 0.0 to 60 digits; the Moebius values carry fastmul6's 1.7e-60 split offset. Python: a copy of hp_y (f398e829)
# as hp_y5555, with wip/large-d-form-s 3b3bfc60's ks_gate.py (--down, --ks0; blob a91c7363) installed in the copy only.
# x_l 0.7062221 (D 8000's L = 20 node, L 13.9 here), the guess deg 2 in 1/n from #1088's lastnode states at D 4000, 5657
# and 8000 (blobs f06d04d5, 127bbb58, 511a1ff8; 7.5e-13 in dh610's ratio test), the jump from it, then ladder_point2.sh
# (e0cf5880) with the downward gate from ks0 6660, KSBAR 1e-64, kc 260, chord-free, 6 threads, through rls13
# (STOP_AFTER=rls13). Output into the live raw worktree's I1098-dh370/ladder/D5555; the last act writes "job rc N" to
# its run.log
{
W=/home/nathan/Source/choptuik-large-d-1088a
LV=/home/nathan/Source/choptuik-large-d-raw-1088a-live
MAINC=/home/nathan/Source/choptuik-large-d
TC=c281b00d3dd00ab1a9f9880cb332bf1b14325433
T=$LV/I1098-dh370/ladder/tools4
I=$LV/I1098-dh370/ladder/inputs
O=$LV/I1098-dh370/ladder/D5555
mkdir -p $T $I $O
S=$O/setup.log
date -u "+setup %Y-%m-%d %H:%M:%S UTC" > $S
git -C $LV fetch -q origin || exit 3
for f in ladder_new.sh ladder_point2.sh variant_state.py resample_m.py kstar_stage.sh kstar_gain.py kstar_summary.py \
         kmax_rule.py; do
  git -C $LV show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
[ "$(git -C $LV hash-object --no-filters $T/ladder_point2.sh)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 3
[ "$(git -C $LV hash-object --no-filters $T/ladder_new.sh)" = "3039e5b9b92dc98280a0e9e52b55f71a00b6165d" ] || exit 3
for f in lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319 \
         lastnode_D8000.0000.npz:511a1ff828a54aa235775c972082b4a5876274f2; do
  git -C $LV cat-file blob ${f#*:} > $I/${f%%:*} || exit 4
  [ "$(git -C $LV hash-object --no-filters $I/${f%%:*})" = "${f#*:}" ] || exit 4
done
[ -d $W/hp_y5555 ] || cp -a $W/hp_y $W/hp_y5555 || exit 5
git -C $MAINC fetch -q origin wip/large-d-form-s || exit 5
git -C $MAINC show 3b3bfc60:hp/ks_gate.py > $O/ks_gate_v2.py || exit 5
[ "$(git -C $LV hash-object --no-filters $O/ks_gate_v2.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
cp $O/ks_gate_v2.py $W/hp_y5555/ks_gate.py
echo "tools4 from raw $TC, inputs and ks_gate.py (3b3bfc60, in hp_y5555 only) checked by blob $(date -u +%H:%M:%S)" >> $S
export HP=$W/hp_y5555 SITE=$W/site_sky PY=/home/nathan/Source/choptuik-large-d-1082/.venv/bin/python COMMIT=f398e829
export STOP_AFTER=rls13 KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $T/ladder_new.sh 5555 260 6 $O $I/lastnode_D4000.0000.npz,$I/lastnode_D5656.8542.npz,$I/lastnode_D8000.0000.npz \
  0.7062221251334241 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
