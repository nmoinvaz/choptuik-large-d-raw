#!/bin/bash
# #1025 kc119_d2225 (t5's order, 26 Nov): dh370's accepted k_c 111 state at D 22.25 (tag l1kc111dh370d2225, raw I1025-dh370/kc111_d2225: state blob 7fc75ef8, record blob 06dc9d92) regridded to k_c 119 with ell_refine.py
# (dh170's recipe of I1025-dh170/kc111_d21125; this file is I1025-dh370/kc111_d2225/run_regrid.sh with the paths, the k_c and the checks changed: diff in run_regrid_vs_dh370.diff). 6 threads, nice 10, timeout 12 h = 43200 s.
# Accepted only by kc119_syscheck_1025.py (fc6e0dd6: the k_c 111 check with k_c 111 -> 119 in 3 lines and one header comment line) with its two controls and refused by the k_c 111 check; the source is first accepted by kc111_syscheck_1025.py
# with its two controls and refused by the k_c 103 and k_c 119 checks. Memory: alert only. Steps and verdicts go to steps.txt and VERDICT.txt. Writes nothing outside this folder and the worktree's solver/matter/data/. usage: run_regrid.sh [dry]
{
ROOT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc119_d2225
MODE=${1:-}
OUT=$ROOT; IN=$OUT/in
WT=/home/nathan/Source/choptuik-large-d-1025k79
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
[ -f $OUT/stage.conf ] || { echo "no $OUT/stage.conf"; exit 9; }
. $OUT/stage.conf
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
[ -e $OUT/VERDICT.txt ] && [ "$MODE" != dry ] && { echo "VERDICT.txt exists"; exit 2; }
step "start${MODE:+ ($MODE)}: k_c $SKC -> $TKC at D $D (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB)"
while read -r h f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
SS=$IN/sol_${SRC}_${DT}.npy; SR=$IN/${SRC}.jsonl
[ "$(blob $SS | cut -c1-8)" = $SRC_STATE_BLOB ] && [ "$(blob $SR | cut -c1-8)" = $SRC_REC_BLOB ] || stop "the source state or record is not $SRC_STATE_BLOB and $SRC_REC_BLOB"
[ "$(blob $IN/$SRC_CHK | cut -c1-8)" = $SRC_CHK_BLOB ] && [ "$(blob $IN/$ACC_CHK | cut -c1-8)" = $ACC_CHK_BLOB ] && [ "$(blob $IN/$XREF_CHK | cut -c1-8)" = $XREF_CHK_BLOB ] || stop "a check is not $SRC_CHK_BLOB / $ACC_CHK_BLOB / $XREF_CHK_BLOB"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; source state $SRC_STATE_BLOB, record $SRC_REC_BLOB, $SRC_CHK $SRC_CHK_BLOB, $ACC_CHK $ACC_CHK_BLOB)"
# the k_c 119 check is the k_c 111 check with k_c 111 -> 119 in three lines and one header comment line (3 removed, 4 added: macm3's reading, kc119_check_vs_kc111.diff)
diff -u $IN/$SRC_CHK $IN/$ACC_CHK > $OUT/check_diff_rebuilt.txt
nl=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^<'); nr=$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep -c '^>')
[ "$nl" = 3 ] && [ "$nr" = 4 ] || stop "$ACC_CHK differs from $SRC_CHK in $nl removed and $nr added lines (3 and 4 wanted)"
[ "$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep '^<' | grep -c 111)" = 3 ] && [ "$(diff $IN/$SRC_CHK $IN/$ACC_CHK | grep '^>' | grep -c 119)" = 4 ] || stop "the changed lines are not the k_c constants 111 -> 119 (and the header)"
step "$ACC_CHK = $SRC_CHK with k_c 111 -> 119 in 3 lines and one header comment line (check_diff_rebuilt.txt)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] && [ "$(git -C $WT hash-object $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "ell_refine.py or ell_delta.py is not 631e5801 / fde699f5"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
for f in $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_${DT}.npy; do [ -e $f ] && [ "$MODE" != dry ] && stop "$f exists"; done
L0=$(cd $WTM && $PY -c "import ell_delta; print('%.10f' % ell_delta.lam0_at($D, *ell_delta.lam0_table())[0])" 2>/dev/null)
[ "$L0" = "$LAM0" ] || stop "lam0_at($D) is $L0, not $LAM0"
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801, ell_delta.py fde699f5; ell_delta.lam0_at($D) = $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
# memory: alert only
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 1024 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
# selftests
nice -n 10 $PY -I $IN/$SRC_CHK --selftest > $OUT/selftest_src_check.txt 2>&1; r1=$?
nice -n 10 $PY -I $IN/$ACC_CHK --selftest > $OUT/selftest_acc_check.txt 2>&1; r2=$?
nice -n 10 $PY -I $IN/$XREF_CHK --selftest > $OUT/selftest_xref_check.txt 2>&1; r3=$?
step "selftests: $SRC_CHK exit $r1, $ACC_CHK exit $r2, $XREF_CHK exit $r3 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] && [ $r3 = 0 ] || stop "a selftest failed"
# STEP 1: the source k_c's check accepts the source (both controls exit 1); the next k_c's check refuses it
nice -n 10 $PY -I $IN/$SRC_CHK $SR $SS $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $IN/$SRC_CHK $SR $SS $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $IN/$SRC_CHK $SR $SS $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/$ACC_CHK $SR $SS $D $WTM > $OUT/source_acccheck_refuses.txt 2>&1; s3=$?
nice -n 10 $PY -I $IN/$XREF_CHK $SR $SS $D $WTM > $OUT/source_xrefcheck_refuses.txt 2>&1; s4=$?
step "STEP 1 source check ($SRC_CHK on the k_c $SKC D $D source): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); $ACC_CHK on the source exit $s3 (1 wanted); $XREF_CHK on the source exit $s4 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] && [ $s4 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
# the source under the names ell_refine reads (the state only, as in the earlier D 20.x regrids)
if [ -e $WTM/data/sol_${SRC}_${DT}.npy ]; then
  [ "$(blob $WTM/data/sol_${SRC}_${DT}.npy | cut -c1-8)" = $SRC_STATE_BLOB ] || stop "the worktree's source state differs from the pin"
else
  cp $SS $WTM/data/sol_${SRC}_${DT}.npy
  [ "$(blob $WTM/data/sol_${SRC}_${DT}.npy | cut -c1-8)" = $SRC_STATE_BLOB ] || stop "copied source state blob differs"
fi
# STEP 2: the regrid
CMD="nice -n 10 timeout 43200 $PY -u ell_refine.py $SRC $SKC $TAG $TKC 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 6 threads, nice 10, cap 43200 s): $CMD" > $OUT/regrid.log
step "STEP 2 regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
RR=$WTM/data/$TAG.jsonl; RS=$WTM/data/sol_${TAG}_${DT}.npy
[ -s $RR ] && [ -s $RS ] || stop "the regrid wrote no state or record"
cp $RR $OUT/ ; cp $RS $OUT/
# the acceptance: the next k_c's check and its controls; the source k_c's check must refuse the result
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $IN/$ACC_CHK $RR $RS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $IN/$SRC_CHK $RR $RS $D $WTM > $OUT/syscheck_srccheck_refuses.txt 2>&1; a3=$?
step "$ACC_CHK exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); $SRC_CHK on the k_c $TKC result exit $a3 (1 wanted)"
kill $MEM 2>/dev/null
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: $ACC_CHK $a0, controls $a1 $a2, $SRC_CHK refuses $a3" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
