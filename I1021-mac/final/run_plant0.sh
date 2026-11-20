#!/bin/bash
# #1021: the record's planted check, run beside the recount of record so that it is done when the record ends: the
# plant (+1 at A 3.53, w/w_inf 0.555) on a copy of the record's input (MERGED), with run_record.sh's argcount arguments,
# then samebits MERGED -> plant0 and plant_check.py (criteria in its docstring). run_record.sh's own plant, on the
# record's cache, still runs after the record.
#   run_plant0.sh MERGED PROCS      From I1021-mac/final; writes plant0/, plant0/exits.txt gets one line per step.
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
MERGED=$1; PROCS=$2
cd "$(dirname "$0")" || exit 1
R=$(cd .. && pwd)
CODE=/Users/nathan/Source/choptuik-large-d-1021b; PY=/Users/nathan/venv-314/bin/python; IS=$CODE/solver/inner_stokes
[ "$(git -C $CODE rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e plant0 ] && { echo "plant0/ exists"; exit 1; }
mkdir -p plant0
X=plant0/exits.txt
echo "start $(date -u '+%F %T') merged $(shasum -a 256 "$MERGED" | cut -c1-16) procs $PROCS" >> $X
$PY plant_check.py --selftest > plant0/plant_check_selftest.log 2>&1; echo "plant_check selftest exit $? (0)" >> $X
cp -p "$MERGED" plant0/points_M3_r0.17.jsonl
cp -p ../m3/points_M3_r0.2.jsonl plant0/points_M3_r0.2.jsonl
ARGS="--M=3 --recount=$R/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --m3fix --retry --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=$PROCS"
(cd $IS && nice -n 10 timeout 24h $PY -u argcount.py $ARGS --plant=3.53,0.555 --seed=$R/final/plant0/points_M3_r0.2.jsonl \
   --out=$R/final/plant0 --tag=M3_record_r0.17_plant0 > $R/final/plant0/recount.log 2>&1); s=$?
echo "plant exit $s $(date -u '+%F %T')" >> $X
$PY $IS/argcount_samebits.py "$MERGED" plant0/points_M3_r0.17.jsonl > plant0/samebits.log 2>&1; echo "samebits merged -> plant0 exit $? (0)" >> $X
C=plant0/count_M3_record_r0.17_plant0.json
$PY plant_check.py $C > plant0/plant_check.log 2>&1; echo "plant_check exit $? (0)" >> $X
$PY plant_check.py $C --mutate=shift > plant0/plant_check_shift.log 2>&1; echo "plant_check --mutate=shift exit $? (1)" >> $X
echo "end $(date -u '+%F %T')" >> $X
exit
}
