#!/bin/bash
# #1098 on mm5 (coordinator, 2026-11-27): D 3214's full point by recipe v2's amendment 2 (ladder_new.sh), moved here from
# win2's queue (win2 is unreachable since its 10:25 UTC reboot and needs its fastmul7 build first) into the 6 threads
# D 2828 freed. x_l 0.7058552367160431, the largest source's own fifth node (the L = 20 node of D 4000 sqrt 2; from
# D rounded to 5656.8542 it would be 1.1e-11 inside that node, which form_s_lastnode.py refuses; L 11.4 here),
# the guess deg 2 in 1/n from
# #1088's lastnode states at D 2828.4271, 4000 and 5656.8542 (blobs 52f878b7, f06d04d5, 127bbb58), which bracket
# D 3214, the jump from it (a 8.03, kc 250), then ladder_point2.sh (blob e0cf5880) with the downward gate from 1.2 n,
# KSBAR 1e-64, chord-free, 6 threads, through the M 48 tail to kmax 23 and the k* stage, as D 2828 ran (no
# STOP_AFTER). The tools pinned at raw commit TC go into <ladder>/tools5, not tools4, whose ladder_point2.sh D 8000's
# running bash is reading. hold_timeouts.sh (raw 6267c60b4, blob b9a711ca) runs beside it on <ladder>/D3214 with a cap
# of 16 h per stage. fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62, ~/Source/fastmul7-site; its hp/ks_gate.py is
# already 3b3bfc60's, blob a91c7363, checked here). Output into <ladder>/D3214; the last act writes "job rc N" to
# its run.log.
#
#     TC=<raw commit> d3214_mm5.sh     (detached, from the ladder folder)
{
R=$HOME/Source/choptuik-large-d-raw
L=$R/I1098-mm5/ladder
I=$L/inputs
T=$L/tools5
O=$L/D3214
F7=$HOME/Source/choptuik-fastmul7
HP=$F7/hp
[ -n "$TC" ] || { echo "TC (the raw commit of the tools) is not set"; exit 1; }
mkdir -p $T $O
git -C $R fetch -q origin || exit 3
for f in ladder_new.sh ladder_point2.sh variant_state.py resample_m.py kstar_stage.sh kstar_gain.py kstar_summary.py \
         kmax_rule.py hold_timeouts.sh; do
  git -C $R show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
[ "$(git -C $R hash-object --no-filters $T/ladder_point2.sh)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 3
[ "$(git -C $R hash-object --no-filters $T/ladder_new.sh)" = "3039e5b9b92dc98280a0e9e52b55f71a00b6165d" ] || exit 3
[ "$(git -C $R hash-object --no-filters $T/hold_timeouts.sh)" = "b9a711cad555836b1887162281073b955c42ce21" ] || exit 3
[ "$(git -C $F7 hash-object --no-filters $HP/ks_gate.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
for f in lastnode_D2828.4271.npz:52f878b72194d15bee4c1bef348fd9ff65275a5e \
         lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319; do
  git -C $R cat-file blob ${f#*:} > $I/${f%%:*} || exit 4
  [ "$(git -C $R hash-object --no-filters $I/${f%%:*})" = "${f#*:}" ] || exit 4
done
echo "tools5 from raw $TC, inputs and ks_gate.py (3b3bfc60) checked by blob $(date -u +%H:%M:%S)" > $O/setup.log
bash $T/hold_timeouts.sh $O 57600 $O/hold_timeouts.log &
export HP SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $T/ladder_new.sh 3214 250 6 $O $I/lastnode_D2828.4271.npz,$I/lastnode_D4000.0000.npz,$I/lastnode_D5656.8542.npz \
  0.7058552367160431 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
