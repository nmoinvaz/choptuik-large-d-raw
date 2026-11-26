#!/bin/bash
# #1098 on mm5, the 6 threads of D 1291's point once its tail ends, on fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62,
# ~/Source/fastmul7-site), chord-free, each step after the one before:
#   0. waits for D 1291's run.log to read "end " (its fastmul6 M 48 tail to kmax 31), at most 8 h;
#   1. D 1291's k* stage (tools3/kstar_stage.sh at kfree 15) on its tail, into <ladder>/D1291/kstar;
#   2. the fastmul7 cross-check of D 1291's tail: h23..h31 released again from the fastmul6 h21 state, at its own ks
#      (2354, from the state) and options, so that only the kernel differs (fastmul6's 1.7e-60 Moebius split offset),
#      into <ladder>/D1291/tail_fm7;
#   3. D 1549's M 48 tail to kmax 31 (tools3/ladder_tail.sh mob, ks 2941 by dh170's octo-double gate, the k* stage last)
#      from dh170's chord-free h13 (I1098-dh170/ladder/D1549/rls13/release_ls_h13_D1549.0000.npz), once dh170's
#      run.log in origin/main reads "rls h13 rc 0" (a fetch every 10 min, at most 12 h), into <ladder>/D1549/tail
{
R=$HOME/Source/choptuik-large-d-raw
L=$R/I1098-mm5/ladder
bash $L/tools3/tools3_check.sh > $L/tools3/check2.log 2>&1 || exit 1
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python INNER_CHORD=0 EXTRA=
n=0
until grep -q "^end " $L/D1291/run.log; do n=$((n + 1)); [ $n -gt 1440 ] && exit 3; sleep 20; done
echo "D 1291's tail ended; its k* stage starts $(date -u +%H:%M:%S)"
bash $L/tools3/kstar_stage.sh $L/D1291/tail $L/D1291/kstar 6
echo "kstar rc $? $(date -u +%H:%M:%S)" >> $L/D1291/kstar/run.log
O=$L/D1291/tail_fm7
mkdir -p $O
(
  cd $HP || exit 1
  export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE
  date -u "+start %Y-%m-%d %H:%M:%S UTC, fastmul7 $(git -C $HP rev-parse --short=8 HEAD), from the fastmul6 h21 state" > $O/run.log
  nice -n 10 timeout 10h $PY -u form_s.py release_ls $L/D1291/tail/release_ls_h21_D1291.0000.npz $O --harm 23,25,27,29,31 \
    --kmax 31 --jac_by 23:qq,25:qq,27:qq,29:qq,31:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 6 \
    --outer 8 --inner_chord 0 --commit $(git -C $HP rev-parse --short=8 HEAD) > $O/rls.log 2>&1
  echo "rc $? $(date -u +%H:%M:%S)" >> $O/run.log
)
P=I1098-dh170/ladder/D1549
n=0
until git -C $R fetch -q origin && git -C $R show origin/main:$P/run.log 2>/dev/null | grep -q "^rls h13 rc 0"; do
  n=$((n + 1)); [ $n -gt 72 ] && exit 4; sleep 600
done
B=$(git -C $R rev-parse origin/main:$P/rls13/release_ls_h13_D1549.0000.npz) || exit 5
git -C $R cat-file blob $B > $L/inputs/D1549_rls13_h13.npz || exit 5
[ "$(git hash-object --no-filters $L/inputs/D1549_rls13_h13.npz)" = "$B" ] || exit 5
echo "D 1549's h13: blob $B ($(date -u +%H:%M:%S))"
mkdir -p $L/D1549
KS=2941 MT=48 KMAX=31 bash $L/tools3/ladder_tail.sh mob 1549 $L/inputs/D1549_rls13_h13.npz $L/D1549/tail 6
echo "D 1549 tail rc $? $(date -u +%H:%M:%S)"
exit
}
