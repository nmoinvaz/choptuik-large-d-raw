#!/bin/bash
# #1025 kc79_d20375 (t5's order, 23 Nov, hc after #1025 comment 7102960982): leg 3's k_c 71 D 20.375 state (tag l1kc71Lw1025c, raw I1025-win2/kc71_leap/states/, state blob 90817a16, record file at commit c4c93318) regridded to
# k_c 79 on Linux with ell_refine.py (the D 20.5 command, D and lambda_0 changed), accepted only by kc79_syscheck_1025.py (29dce7ea) with its two controls. Source accepted first by kc71_syscheck.py (4cd86cd4) with its two controls
# (and refused by the k_c 79 check). 8 threads, nice 10, cap 21600 s, a systemd user unit (i1025-k79d20375r). Memory: alert only (alert.log), nothing is stopped for memory. Writes steps.txt and VERDICT.txt;
# writes nothing outside this folder and the worktree's solver/matter/data/. usage: run_regrid.sh [dry]
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc79_d20375
WT=/home/nathan/Source/choptuik-large-d-1025k79
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
SRC=l1kc71Lw1025c; TAG=l1kc79dh170d20375; D=20.375; LAM0=2.1093568559
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
cd $OUT || exit 9
MODE=${1:-}
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
[ -e $OUT/VERDICT.txt ] && [ "$MODE" != dry ] && { echo "VERDICT.txt exists"; exit 2; }
step "start${MODE:+ ($MODE)} (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB)"
while read -r h f; do [ -f $OUT/in/$f ] && [ "$(blob $OUT/in/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
SS=$OUT/in/sol_l1kc71Lw1025c_D20.375000.npy; SR=$OUT/in/l1kc71Lw1025c.jsonl
[ "$(blob $SS | cut -c1-8)" = 90817a16 ] && [ "$(blob $SR | cut -c1-8)" = 123253fc ] || stop "the source state or record is not 90817a16 and 123253fc"
[ "$(blob $OUT/in/kc71_syscheck.py | cut -c1-8)" = 4cd86cd4 ] && [ "$(blob $OUT/in/kc79_syscheck_1025.py | cut -c1-8)" = 29dce7ea ] || stop "a check is not 4cd86cd4 / 29dce7ea"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; source state 90817a16, record 123253fc, kc71_syscheck 4cd86cd4, kc79_syscheck 29dce7ea)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] && [ "$(git -C $WT hash-object $WTM/ell_delta.py | cut -c1-8)" = fde699f5 ] || stop "ell_refine.py or ell_delta.py is not 631e5801 / fde699f5"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
for f in $WTM/data/sol_${SRC}_D20.3750.npy $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.3750.npy; do [ -e $f ] && [ "$MODE" != dry ] && stop "$f exists"; done
L0=$(cd $WTM && $PY -c "import ell_delta; print('%.10f' % ell_delta.lam0_at(20.375, *ell_delta.lam0_table())[0])" 2>/dev/null)
[ "$L0" = "$LAM0" ] || stop "lam0_at(20.375) is $L0, not $LAM0"
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801, ell_delta.py fde699f5; ell_delta.lam0_at(20.375) = $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py --selftest > $OUT/selftest_kc71_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc71_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# STEP 1: kc71_syscheck accepts the k_c 71 source (both controls exit 1); the k_c 79 check refuses it (as in kc79_d20 and kc79_d205)
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $SR $SS $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $SR $SS $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $SR $SS $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM > $OUT/source_kc79check_refuses.txt 2>&1; s3=$?
step "STEP 1 source check (kc71_syscheck.py on leg 3's k_c 71 D 20.375 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc79_syscheck_1025.py on the k_c 71 source exit $s3 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
cp $SS $WTM/data/sol_${SRC}_D20.3750.npy
[ "$(blob $WTM/data/sol_${SRC}_D20.3750.npy | cut -c1-8)" = 90817a16 ] || stop "copied source state blob differs"
# STEP 2: the regrid (the D 20.5 command, D and lambda_0 changed)
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "STEP 2 regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
RR=$WTM/data/$TAG.jsonl; RS=$WTM/data/sol_${TAG}_D20.3750.npy
[ -s $RR ] && [ -s $RS ] || stop "the regrid wrote no state or record"
cp $RR $OUT/ ; cp $RS $OUT/
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $RR $RS $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $RR $RS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $RR $RS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "kc79 syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
kill $MEM 2>/dev/null
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ]; then
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: kc79 syscheck $a0, controls $a1 $a2" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
