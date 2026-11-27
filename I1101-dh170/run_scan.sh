#!/bin/bash
# #1101 dh170 steps 2 and 3 (t5's order, comment 7212323177): d18_secant.py scan --b12=rust --b12_threads=1, one process per lambda, 1 thread each, nice 10.
# usage: run_scan.sh TAG STATE_FILE RECORD_FILE STATE_BLOB RECORD_BLOB "LAMS" [pins only for TAG=ctl: results_1101.py control]
#   TAG ctl: R0's state (state B) at 0.045 and 0.050: control bars, results_1101.py control;  TAG r2: R2's state, results_1101.py r2.
# Stops at the first failure (STOP_<TAG>.txt). Needs GATES_DONE.txt. Output: scan_<TAG>/scan_D23.0_p<i>.jsonl, scan_<TAG>_p<i>.raw, results_<TAG>.md, read_lower_<TAG>.txt
{
TAG=${1:?tag}; SF=${2:?state}; RF=${3:?record}; SB=${4:?state blob}; RB=${5:?record blob}; LAMS=${6:?lambdas}
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170
WTM=/home/nathan/Source/choptuik-large-d-1102/solver/matter
SITE=/home/nathan/Source/ellrs-site-1102
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
D=23.0
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ -f GATES_DONE.txt ] || stop "GATES_DONE.txt is missing"
[ "$(git -C $WTM rev-parse --short=8 HEAD)" = d4b6b6ce ] && [ "$(blob $WTM/d18_secant.py)" = 9706e506 ] && [ "$(blob $WTM/ell_b12rs.py)" = a1fff74f ] || stop "the worktree is not d4b6b6ce or the scanner is not 9706e506"
[ "$(blob $SF)" = "$SB" ] && [ "$(blob $RF)" = "$RB" ] || stop "$SF or $RF is not the pinned blob ($SB, $RB)"
[ "$(blob in/read_lower.py)" = 89309d3c ] && [ "$(blob in/d185_scan_read.py)" = 7c9d400f ] || stop "the reader or its change finder is not the pinned blob"
step "pins ok: state $(blob $SF) record $(blob $RF); d18_secant.py 9706e506, ell_b12rs.py a1fff74f at d4b6b6ce; read_lower.py 89309d3c; lambdas $LAMS"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1
if [ "$TAG" = ctl ]; then
  ( cd $WTM
    nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftests/selftest_secant.txt 2>&1; echo $? > $OUT/.e0
    nice -n 10 $PY -I d18_secant.py selftest --mutate=half > $OUT/selftests/selftest_secant_half.txt 2>&1; echo $? > $OUT/.e1
    nice -n 10 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/selftests/selftest_secant_norobust.txt 2>&1; echo $? > $OUT/.e2
    nice -n 10 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/selftests/selftest_secant_nosigncheck.txt 2>&1; echo $? > $OUT/.e3 )
  e0=$(cat .e0); e1=$(cat .e1); e2=$(cat .e2); e3=$(cat .e3); rm -f .e0 .e1 .e2 .e3
  step "d18_secant.py selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
  [ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || stop "a d18_secant.py selftest or mutation did not read as written"
  ( cd in
    nice -n 10 $PY -I read_lower.py selftest > $OUT/selftests/selftest_read_lower.txt 2>&1; echo $? > $OUT/.r0
    nice -n 10 $PY -I read_lower.py selftest --mutate=shift > $OUT/selftests/selftest_read_lower_shift.txt 2>&1; echo $? > $OUT/.r1
    nice -n 10 $PY -I read_lower.py selftest --mutate=round2 > $OUT/selftests/selftest_read_lower_round2.txt 2>&1; echo $? > $OUT/.r2 )
  r0=$(cat .r0); r1=$(cat .r1); r2=$(cat .r2); rm -f .r0 .r1 .r2
  step "read_lower selftest exit $r0 (0 wanted); mutations shift exit $r1, round2 exit $r2 (1 wanted each)"
  [ $r0 = 0 ] && [ $r1 = 1 ] && [ $r2 = 1 ] || stop "a read_lower selftest or mutation did not read as written"
fi
$PY -I $OUT/results_1101.py selftest > $OUT/selftests/selftest_results_$TAG.txt 2>&1; [ $? = 0 ] || stop "results_1101.py selftest failed"
mkdir -p scan_$TAG
step "scan starts: D $D, lambda $LAMS, one process per lambda, 1 thread each, nice 10, --b12=rust --b12_threads=1"
t0=$(date +%s); pids=(); i=0
for L in ${LAMS//,/ }; do
  ( cd $WTM && PYTHONPATH=$SITE nice -n 10 /usr/bin/time -v $PY -u $WTM/d18_secant.py scan $OUT/$RF $OUT/$SF $D $L $OUT/scan_$TAG/scan_D23.0_p$i.jsonl --b12=rust --b12_threads=1 --pin=$SB,$RB > $OUT/scan_${TAG}_p$i.raw 2>&1
    rc=$?; echo "$(stamp) UTC [$TAG] lambda $L exit $rc" >> $OUT/steps.txt ) &
  pids+=($!); i=$((i+1))
done
wait "${pids[@]}"
step "scan done: $(( $(date +%s) - t0 )) s"
for f in scan_${TAG}_p*.raw; do grep -h 'the record system\|NOT the record system\|block 12 by ellrs' $f | head -3 >> steps.txt; grep -hE 'Elapsed|Maximum resident' $f >> steps.txt; done
grep -l 'NOT the record system' scan_${TAG}_p*.raw && stop "a scan did not reproduce the record system"
( cd in; lo=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | head -1); hi=$(echo ${LAMS//,/ } | tr ' ' '\n' | sort -g | tail -1)
  { echo "== $TAG: read_lower.py scan_$TAG $lo $hi"; $PY -I read_lower.py $OUT/scan_$TAG $lo $hi; echo "(exit $?)"; } > $OUT/read_lower_$TAG.txt 2>&1 )
if [ "$TAG" = ctl ]; then MODE=control; else MODE=r2; fi
$PY -I $OUT/results_1101.py $MODE $OUT/scan_$TAG > results_$TAG.md 2> results_$TAG.err; rc=$?
step "results_1101.py $MODE exit $rc (results_$TAG.md)"
echo "$TAG DONE $(stamp) UTC, results exit $rc" > $OUT/DONE_$TAG.txt
step "done"
exit 0
}
