#!/bin/bash
# #1021: the recount of record of #1013's 32 unresolved M = 3 cells at xi1 0.17 (m3/leaves_M3_cand_r0.25.jsonl), from
# the merged cache of all parts, at argcount 6da7da7b with the default starts (0.25, 0.2), --retry, cap 1e7; then the
# plant (+1 at A 3.53, w/w_inf 0.555, box 17) on a copy of the record's cache, and the checks.
#   run_record.sh MERGED PROCS     MERGED: a merged.jsonl that passed merge_check and the sheet check
# From I1021-mac/final. Writes record/ and plant/; record/exits.txt gets one line per step.
set -u
{ # read whole before it runs: an edit of this file cannot reach a running job
MERGED=$1; PROCS=$2
cd "$(dirname "$0")" || exit 1
R=$(cd .. && pwd)
CODE=/Users/nathan/Source/choptuik-large-d-1021b; PY=/Users/nathan/venv-314/bin/python; IS=$CODE/solver/inner_stokes
[ "$(git -C $CODE rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "CODE has local changes"; exit 1; }
[ -e record ] || [ -e plant ] && { echo "record/ or plant/ exists"; exit 1; }
mkdir -p record plant
X=record/exits.txt
echo "start $(date -u '+%F %T') merged $(shasum -a 256 "$MERGED" | cut -c1-16) procs $PROCS" >> $X
(cd $IS && { nice -n 10 $PY -u argcount.py --selftest; s=$?
  for m in seedfix nocap lowcap; do nice -n 10 $PY -u argcount.py --selftest --mutate=$m; s="$s $?"; done
  echo "selftest plain seedfix nocap lowcap exits: $s"; }) > record/selftest.log 2>&1
tail -1 record/selftest.log >> $X
[ "$(tail -1 record/selftest.log)" = "selftest plain seedfix nocap lowcap exits: 0 1 1 1" ] || { echo "selftests not 0 1 1 1" >> $X; exit 1; }
cp -p "$MERGED" record/points_M3_r0.17.jsonl
cp -p ../m3/points_M3_r0.2.jsonl record/points_M3_r0.2.jsonl
ARGS="--M=3 --recount=$R/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --m3fix --retry --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=$PROCS"
(cd $IS && nice -n 10 timeout 24h $PY -u argcount.py $ARGS --seed=$R/final/record/points_M3_r0.2.jsonl \
   --out=$R/final/record --tag=M3_record_r0.17 > $R/final/record/recount.log 2>&1); s=$?
echo "record exit $s $(date -u '+%F %T')" >> $X
[ $s -eq 0 ] || exit 1
cp -p record/points_M3_r0.17.jsonl plant/points_M3_r0.17.jsonl
cp -p record/points_M3_r0.2.jsonl plant/points_M3_r0.2.jsonl
(cd $IS && nice -n 10 timeout 24h $PY -u argcount.py $ARGS --plant=3.53,0.555 --seed=$R/final/plant/points_M3_r0.2.jsonl \
   --out=$R/final/plant --tag=M3_record_r0.17_plant > $R/final/plant/recount.log 2>&1); s=$?
echo "plant exit $s $(date -u '+%F %T')" >> $X
$PY $IS/argcount_samebits.py "$MERGED" record/points_M3_r0.17.jsonl > record/samebits.log 2>&1; echo "samebits merged -> record exit $?" >> $X
$PY $IS/argcount_samebits.py record/points_M3_r0.17.jsonl plant/points_M3_r0.17.jsonl > plant/samebits.log 2>&1; echo "samebits record -> plant exit $?" >> $X
for L in record/leaves_M3_record_r0.17.jsonl lines; do
  nice -n 19 $PY $R/diag/sheet_check.py record/points_M3_r0.17.jsonl $L --count record/count_M3_record_r0.17.json
  echo "exit $?"
done > record/sheet_check.log 2>&1
grep -c 'sheet check: PASS' record/sheet_check.log | sed 's/^/sheet checks passed (of 2): /' >> $X
echo "end $(date -u '+%F %T')" >> $X
exit
}
