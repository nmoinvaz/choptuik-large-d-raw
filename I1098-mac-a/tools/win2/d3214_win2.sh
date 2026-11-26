#!/bin/bash
# #1098 on win2 (Git Bash): D 3214's M 32 stages on fastmul7 (worktree /d/choptuik-i1098 at d40a9c62, venv V), chord-free,
# THREADS threads (12 by default): ladder_point2.sh from the live raw worktree's I1098-mac-a/tools (blob 8802fb26 or
# later) through rls13 only (STOP_AFTER=rls13), kc 250, KSBAR 1e-70; the M 48 tail to kmax 31 is a later job.
# The jump fits in 1/n to D 1549's h13 (I1098-dh170/ladder/D1549/rls13/release_ls_h13_D1549.0000.npz, made chord-free on
# dh170) and D 2000's fastmul6 base h13 (I1098-dh610/fix6/D2000_base6/release_ls_h13_D2000.0000.npz, blob b897ba43).
# It waits (a fetch every 10 min, at most WAIT_H hours, 8 by default) until D 1549's run.log in origin/main reads
# "rls h13 rc 0", writes both states from their blobs into I1098-win2/ladder/inputs/, checks that form_s and hpkernel
# import through the PYTHONPATH the ladder scripts build, then runs. Output into I1098-win2/ladder/D3214/ of the live
# worktree, no --allow_unraw; the last act writes "job rc N" to run.log and the file job.done.
#
#     [THREADS=12] [WAIT_H=8] d3214_win2.sh
{
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
V=/c/Users/nathan/Source/venv-i1098
LV=/d/choptuik-i1098-raw-live
LW=D:/choptuik-i1098-raw-live
T=$LV/I1098-mac-a/tools
I=$LW/I1098-win2/ladder/inputs
O=$LW/I1098-win2/ladder/D3214
mkdir -p $I $O
cd $LV || exit 1
P1549=I1098-dh170/ladder/D1549
n=0
until git fetch -q origin && git show origin/main:$P1549/run.log 2>/dev/null | grep -q "^rls h13 rc 0"; do
  n=$((n + 1))
  [ $n -gt $(( ${WAIT_H:-8} * 6 )) ] && { echo "D 1549's h13 not in raw after ${WAIT_H:-8} h" >> $O/run.log; exit 2; }
  sleep 600
done
B1549=$(git rev-parse origin/main:$P1549/rls13/release_ls_h13_D1549.0000.npz) || exit 3
git cat-file blob $B1549 > $I/D1549_rls13_h13.npz || exit 3
git cat-file blob b897ba43adb46653785b362d2ae6a2f712fdd8db > $I/D2000_base6_h13.npz || exit 3
[ "$(git hash-object --no-filters $I/D1549_rls13_h13.npz)" = "$B1549" ] || exit 3
[ "$(git hash-object --no-filters $I/D2000_base6_h13.npz)" = "b897ba43adb46653785b362d2ae6a2f712fdd8db" ] || exit 3
echo "inputs: D1549_rls13_h13.npz blob $B1549, D2000_base6_h13.npz blob b897ba43 ($(date -u +%H:%M:%S))" > $I/README_inputs.txt
export HP=/d/choptuik-i1098/hp SITE=$V/Lib/site-packages PY=$V/Scripts/python.exe
# the ladder scripts hand Python PYTHONPATH=$SITE:$HP in Git Bash's form, which Git Bash converts for a Windows program
PYTHONPATH=$SITE:$HP $PY -c "import form_s, hpkernel; print('preflight', form_s.__file__, hpkernel.__file__)" \
  >> $I/README_inputs.txt 2>&1 || exit 4
export KSBAR=1e-70 STOP_AFTER=rls13 INNER_CHORD=0 EXTRA=
bash $T/ladder_point2.sh 3214 250 ${THREADS:-12} $O $I/D1549_rls13_h13.npz $I/D2000_base6_h13.npz 48 31
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $O/run.log
touch $O/job.done
exit $rc
}
