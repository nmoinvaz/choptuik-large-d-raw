#!/bin/bash
# #1048 section 1: noise1048.py run at nice 10 (its solves call nice -n 10), 6 h cap; selftests first. Writes noise/.
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
. "$(cd "$(dirname "$0")" && pwd)/../z7_m7/common_z7.sh"
C=$(cd "$(dirname "$0")" && pwd)
EX=$C/exits_ctrl.txt
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = fc7dee4d ] || { echo "$WT is not at fc7dee4d"; exit 1; }
[ -z "$(git -C $WT status --short)" ] || { echo "$WT not clean"; exit 1; }
mkdir -p $C/noise/logs
$PY $C/noise1048.py selftest > $C/noise/selftest.log 2>&1; echo "noise selftest exit $? (0) $(stamp)" >> $EX
$PY $C/noise1048.py selftest --mutate=sigma > $C/noise/selftest_mutate.log 2>&1; echo "noise selftest --mutate=sigma exit $? (1) $(stamp)" >> $EX
echo "noise run start $(stamp)" >> $EX
timeout -s TERM 6h $PY -u $C/noise1048.py run > $C/noise/run.log 2>&1; echo "noise run exit $? $(stamp)" >> $EX
$PY $C/noise1048.py table > $C/noise/table.jsonl 2> $C/noise/table.err; echo "noise table exit $? $(stamp)" >> $EX
exit
}
