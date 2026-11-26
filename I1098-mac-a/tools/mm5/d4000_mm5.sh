#!/bin/bash
# #1098 on mm5: D 4000's M 32 stages on fastmul7 (~/Source/choptuik-fastmul7 at d40a9c62, ~/Source/fastmul7-site),
# chord-free, 6 threads: <ladder>/tools3/ladder_point2.sh (blob 8802fb26; tools3_check.sh first) through rls13 only
# (STOP_AFTER=rls13), kc 260, KSBAR 1e-70, the M 48 tail to kmax 31 a later job. The jump fits in 1/n to S1000 (D 1000's
# fastmul6 base h13) and D 2000's fastmul6 base h13, both in <ladder>/inputs, checked by blob. Output in <ladder>/D4000;
# the last act writes "job rc N" to its run.log
{
L=$HOME/Source/choptuik-large-d-raw/I1098-mm5/ladder
I=$L/inputs
bash $L/tools3/tools3_check.sh > $L/tools3/check.log 2>&1 || exit 1
[ "$(git hash-object --no-filters $I/S1000_D1000_base6_h13.npz)" = "48db1b6cf09ca4feebd9ca5a0976ec8154711635" ] || exit 2
[ "$(git hash-object --no-filters $I/D2000_base6_h13.npz)" = "b897ba43adb46653785b362d2ae6a2f712fdd8db" ] || exit 2
mkdir -p $L/D4000
export HP=$HOME/Source/choptuik-fastmul7/hp SITE=$HOME/Source/fastmul7-site PY=$HOME/venv-314/bin/python
export KSBAR=1e-70 STOP_AFTER=rls13 INNER_CHORD=0 EXTRA=
bash $L/tools3/ladder_point2.sh 4000 260 6 $L/D4000 $I/S1000_D1000_base6_h13.npz $I/D2000_base6_h13.npz 48 31
rc=$?
echo "job rc $rc $(date -u +%H:%M:%S)" >> $L/D4000/run.log
exit $rc
}
