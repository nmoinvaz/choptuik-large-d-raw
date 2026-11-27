#!/bin/bash
# #1098 on mm5 (coordinator, 2026-11-27 06:30 UTC): D 8000's M 32 stages by recipe v2's amendment 2 (ladder_new.sh), moved
# here from win2's queue: x_l 0.7062221 (D 8000's own L = 20 node), the guess deg 2 in 1/n from #1088's lastnode states at
# D 4000, 5657 and 8000 (blobs f06d04d5, 127bbb58, 511a1ff8), which at D 8000 is the lastnode state itself (dh610's ratio
# test read 1.1e-16, I1098-dh610/ladder/D4628_guess/ratio_hi.log), the jump from it (a 19.995, ks 12017), then
# ladder_point2.sh (blob e0cf5880) with the downward gate from ks0 9600, KSBAR 1e-64, kc 260, chord-free, 6 threads,
# through rls13 (STOP_AFTER=rls13; the M 48 tail is a later job). No wait: it starts at once. It writes the tools pinned
# at raw commit TC into <ladder>/tools4 and the inputs from their blobs, and installs wip/large-d-form-s 3b3bfc60's
# ks_gate.py (--down, --ks0; blob a91c7363) as the fastmul7 worktree's hp/ks_gate.py. Output into <ladder>/D8000; the
# last act writes "job rc N" to its run.log.
#
#     TC=<raw commit> d8000_mm5.sh     (detached, from the ladder folder)
{
R=$HOME/Source/choptuik-large-d-raw
L=$R/I1098-mm5/ladder
I=$L/inputs
T=$L/tools4
O=$L/D8000
F7=$HOME/Source/choptuik-fastmul7
HP=$F7/hp
[ -n "$TC" ] || { echo "TC (the raw commit of the tools) is not set"; exit 1; }
mkdir -p $T $O
git -C $R fetch -q origin || exit 3
for f in ladder_new.sh ladder_point2.sh variant_state.py resample_m.py kstar_stage.sh kstar_gain.py kstar_summary.py \
         kmax_rule.py; do
  git -C $R show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
[ "$(git -C $R hash-object --no-filters $T/ladder_point2.sh)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 3
for f in lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319 \
         lastnode_D8000.0000.npz:511a1ff828a54aa235775c972082b4a5876274f2; do
  git -C $R cat-file blob ${f#*:} > $I/${f%%:*} || exit 4
  [ "$(git -C $R hash-object --no-filters $I/${f%%:*})" = "${f#*:}" ] || exit 4
done
git -C $F7 fetch -q origin wip/large-d-form-s || exit 5
git -C $F7 show 3b3bfc60:hp/ks_gate.py > $O/ks_gate_v2.py || exit 5
[ "$(git -C $F7 hash-object --no-filters $O/ks_gate_v2.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
cp $O/ks_gate_v2.py $HP/ks_gate.py
echo "tools4 from raw $TC, inputs and ks_gate.py (3b3bfc60) checked by blob $(date -u +%H:%M:%S)" > $O/setup.log
export HP SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python STOP_AFTER=rls13 KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $T/ladder_new.sh 8000 260 6 $O $I/lastnode_D4000.0000.npz,$I/lastnode_D5656.8542.npz,$I/lastnode_D8000.0000.npz \
  0.7062221251334241 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
exit $rc
}
