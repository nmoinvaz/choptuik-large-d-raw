#!/bin/bash
# #1098 on win2 (Git Bash): D 3214's M 32 stages on fastmul7 with the last node at x_l 0.7053359 (D 4000's L = 20 node,
# L = (n/2) ln(1/x_l^2 - 1) = 16.1 at D 3214), replacing d3214_win2.sh, whose fit to D 1549 (x_l 0.7) and D 2000
# (0.7035589) mixed two last nodes and put D 3214's at L 32 (I1098-dh610/ladder/D4628_guess). The guess:
# form_s_lastnode.py guess, deg 2 in 1/n from D 2000's fastmul6 base h13 (blob b897ba43) and #1088's lastnode states at
# D 2828 and 4000 (L 20 each; blobs 52f878b7, f06d04d5), carried outward to x_l by Taylor steps (dh610's ratio test:
# 1.9e-09 in every block, ratio_3214.log). Then form_s.py jump from it (ladder_point2.sh's jump with --deg 0: held,
# a 8.03, ks 4838, kc 250, dd then qd, it_max 12) into D3214/jump, and ladder_point2.sh, which keeps that converged jump,
# through rls13 (STOP_AFTER=rls13), KSBAR 1e-70, chord-free. No wait for D 1549. Output into I1098-win2/ladder/D3214/
# of the live worktree, no --allow_unraw; the last act writes "job rc N" to run.log and the file job.done.
#
#     [THREADS=12] d3214b_win2.sh
{
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
V=/c/Users/nathan/Source/venv-i1098
LV=/d/choptuik-i1098-raw-live
LW=D:/choptuik-i1098-raw-live
T=$LV/I1098-mac-a/tools
I=$LW/I1098-win2/ladder/inputs
O=$LW/I1098-win2/ladder/D3214
TH=${THREADS:-12}
mkdir -p $I $O/jump $O/guess
cd $LV || exit 1
git fetch -q origin
for f in D2000_base6_h13.npz:b897ba43adb46653785b362d2ae6a2f712fdd8db lastnode_D2828.4271.npz:52f878b72194d15bee4c1bef348fd9ff65275a5e \
         lastnode_D4000.0000.npz:f06d04d5b98e1df5b8040c263ea50d5e882f60f7; do
  git cat-file blob ${f#*:} > $I/${f%%:*} || exit 3
  [ "$(git hash-object --no-filters $I/${f%%:*})" = "${f#*:}" ] || exit 3
done
echo "inputs: D2000_base6_h13.npz b897ba43, lastnode_D2828.4271.npz 52f878b7, lastnode_D4000.0000.npz f06d04d5 ($(date -u +%H:%M:%S))" \
  > $I/README_inputs_b.txt
export HP=/d/choptuik-i1098/hp SITE=$V/Lib/site-packages PY=$V/Scripts/python.exe
export COMMIT=$(git -C $HP rev-parse --short=8 HEAD)
PYTHONPATH=$SITE:$HP $PY -c "import form_s, form_s_lastnode, hpkernel; print('preflight', form_s.__file__, hpkernel.__file__)" \
  >> $I/README_inputs_b.txt 2>&1 || exit 4
P=$O/pre.log
date -u "+start %Y-%m-%d %H:%M:%S UTC" > $P
(
  cd $HP || exit 1
  export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
  $PY -u form_s_lastnode.py guess $O/guess --D 3214 --mob 8.03 --ks 4838 --kc 250 --deg 2 --threads $TH \
    --states_s $I/D2000_base6_h13.npz,$I/lastnode_D2828.4271.npz,$I/lastnode_D4000.0000.npz --xl 0.705335927228362 >> $P 2>&1
  [ -s $O/guess/guess_D3214.0000.npz ] || exit 5
  nice -n 10 timeout 3h $PY -u form_s.py jump $O/jump --D 3214 --states_s $O/guess/guess_D3214.0000.npz --deg 0 --held 1 \
    --mob 8.03 --ks 4838 --kc 250 --delta fit --tol 1e-300 --it_max 12 --threads $TH --commit $COMMIT > $O/jump/jump.log 2>&1
  echo "jump rc $? $(date -u +%H:%M:%S)" >> $P
)
grep -q "^  converged" $O/jump/jump.log && [ -s $O/jump/jump_s_D3214.0000.npz ] || { touch $O/job.done; exit 6; }
export KSBAR=1e-70 STOP_AFTER=rls13 INNER_CHORD=0 EXTRA=
bash $T/ladder_point2.sh 3214 250 $TH $O $O/guess/guess_D3214.0000.npz $O/guess/guess_D3214.0000.npz 48 31
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
touch $O/job.done
exit $rc
}
