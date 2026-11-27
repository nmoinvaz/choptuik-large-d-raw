#!/bin/bash
# #1098 on win2 (Git Bash): D 8000's M 32 stages by recipe v2's amendment 2 (ladder_new.sh): x_l 0.7062221 (its own
# L = 20 node), the guess from #1088's lastnode states at D 4000, 5657 and 8000 (blobs f06d04d5, 127bbb58, 511a1ff8),
# deg 2 in 1/n, so at D 8000 the lastnode state itself (dh610's ratio test read 1.1e-16), the jump from it, then
# ladder_point2.sh (blob e0cf5880) with the downward gate from ks0 9600, KSBAR 1e-64, kc 260, chord-free, THREADS threads
# (12 by default), through rls13 (STOP_AFTER=rls13). It waits (at most WAIT_H hours, 24 by default) for D 3214's
# job.done, writes the tools pinned at raw commit TC into I1098-win2/ladder/tools4 and the inputs from their blobs, and
# installs wip/large-d-form-s 3b3bfc60's ks_gate.py (blob a91c7363) as hp/ks_gate.py. Output into
# I1098-win2/ladder/D8000/ of the live worktree, no --allow_unraw; the last act writes "job rc N" to run.log and job.done.
#
#     TC=<raw commit> [THREADS=12] [WAIT_H=24] d8000_win2.sh
{
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
V=/c/Users/nathan/Source/venv-i1098
LV=/d/choptuik-i1098-raw-live
LW=D:/choptuik-i1098-raw-live
T=$LW/I1098-win2/ladder/tools4
I=$LW/I1098-win2/ladder/inputs
O=$LW/I1098-win2/ladder/D8000
TH=${THREADS:-12}
export HP=/d/choptuik-i1098/hp SITE=$V/Lib/site-packages PY=$V/Scripts/python.exe
[ -n "$TC" ] || { echo "TC (the raw commit of the tools) is not set"; exit 1; }
n=0
until [ -f $LW/I1098-win2/ladder/D3214/job.done ]; do
  n=$((n + 1)); [ $n -gt $(( ${WAIT_H:-24} * 6 )) ] && exit 2; sleep 600
done
mkdir -p $T $I $O
cd $LV || exit 1
git fetch -q origin || exit 3
for f in ladder_new.sh ladder_point2.sh variant_state.py resample_m.py kstar_stage.sh kstar_gain.py kstar_summary.py \
         kmax_rule.py; do
  git show $TC:I1098-mac-a/tools/$f > $T/$f || exit 3
done
[ "$(git hash-object --no-filters $T/ladder_point2.sh)" = "e0cf58809f062a6791e7d982369be5eaa57d97ad" ] || exit 3
for f in lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7 \
         lastnode_D5656.8542.npz:127bbb585763caf0029e903c455cb65dc1907319 \
         lastnode_D8000.0000.npz:511a1ff828a54aa235775c972082b4a5876274f2; do
  git cat-file blob ${f#*:} > $I/${f%%:*} || exit 4
  [ "$(git hash-object --no-filters $I/${f%%:*})" = "${f#*:}" ] || exit 4
done
git -C /d/choptuik-i1098 fetch -q origin wip/large-d-form-s || exit 5
git -C /d/choptuik-i1098 show 3b3bfc60:hp/ks_gate.py > $O/ks_gate_v2.py || exit 5
[ "$(git hash-object --no-filters $O/ks_gate_v2.py)" = "a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7" ] || exit 5
cp $O/ks_gate_v2.py $HP/ks_gate.py
echo "tools4 from raw $TC, inputs and ks_gate.py (3b3bfc60) checked by blob $(date -u +%H:%M:%S)" > $O/setup.log
PYTHONPATH=$SITE:$HP $PY -c "import form_s, form_s_lastnode, hpkernel; print('preflight', form_s.__file__, hpkernel.__file__)" \
  >> $O/setup.log 2>&1 || exit 6
export STOP_AFTER=rls13 KSBAR=1e-64 INNER_CHORD=0 EXTRA=
bash $T/ladder_new.sh 8000 260 $TH $O $I/lastnode_D4000.0000.npz,$I/lastnode_D5656.8542.npz,$I/lastnode_D8000.0000.npz \
  0.7062221251334241 48 23
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
touch $O/job.done
exit $rc
}
