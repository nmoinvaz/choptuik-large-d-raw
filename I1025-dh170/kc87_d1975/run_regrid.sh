#!/bin/bash
# #1025 kc87_d1975 (t5's order, 23 Nov, comment 7090311364): dh170's accepted k_c 79 D 19.75 state regridded to k_c 87 with ell_refine.py (macm3's command, the tag changed), accepted only by dh610's kc87_syscheck_1025.py
# (6df5d960) with its two controls, and refused by kc79_syscheck_1025.py. 8 threads, nice 10, cap 21600 s, a systemd user unit (i1025-k87r). Memory: alert only (alert.log), nothing is stopped for memory.
# Steps and verdicts go to steps.txt and VERDICT.txt. Writes nothing outside this folder and the worktree's solver/matter/data/. usage: run_regrid.sh [dry]
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc87_d1975
WT=/home/nathan/Source/choptuik-large-d-1025k79
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
SRC=l1kc79dh170d1975; TAG=l1kc87dh170d1975; D=19.75; LAM0=2.1120935738
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
SS=$OUT/in/sol_l1kc79dh170d1975_D19.7500.npy; SR=$OUT/in/l1kc79dh170d1975.jsonl
[ "$(blob $SS | cut -c1-8)" = f2ad34b5 ] && [ "$(blob $SR | cut -c1-8)" = 0508163e ] || stop "the source state or record is not f2ad34b5 and 0508163e"
[ "$(blob $OUT/in/kc87_syscheck_1025.py | cut -c1-8)" = 6df5d960 ] || stop "kc87_syscheck_1025.py is not 6df5d960"
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; source state f2ad34b5, record 0508163e, kc87_syscheck 6df5d960, kc79_syscheck $(blob $OUT/in/kc79_syscheck_1025.py | cut -c1-8))"
# the k_c 87 check is the k_c 79 check with three lines changed, and its diff is dh610's
diff -u $OUT/in/kc79_syscheck_1025.py $OUT/in/kc87_syscheck_1025.py > $OUT/kc87_diff_rebuilt.txt
nl=$(diff $OUT/in/kc79_syscheck_1025.py $OUT/in/kc87_syscheck_1025.py | grep -c '^<'); nr=$(diff $OUT/in/kc79_syscheck_1025.py $OUT/in/kc87_syscheck_1025.py | grep -c '^>')
[ "$nl" = 3 ] && [ "$nr" = 3 ] || stop "kc87_syscheck differs from kc79_syscheck in $nl and $nr lines (3 and 3 wanted)"
diff <(tail -n +3 $OUT/kc87_diff_rebuilt.txt) <(tail -n +3 $OUT/in/kc87_syscheck_1025.diff.dh610) > /dev/null || stop "the rebuilt diff differs from dh610's"
step "kc87_syscheck_1025.py = kc79_syscheck_1025.py with 3 lines changed; the rebuilt diff's hunks equal dh610's (kc87_diff_rebuilt.txt)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
# the source under the names ell_refine reads: the worktree's data already holds the accepted k_c 79 regrid output (checked by blob)
[ "$(blob $WTM/data/sol_${SRC}_D19.7500.npy | cut -c1-8)" = f2ad34b5 ] && [ "$(blob $WTM/data/$SRC.jsonl | cut -c1-8)" = 0508163e ] || stop "the worktree's source state or record differs from the pins"
for f in $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy; do [ -e $f ] && [ "$MODE" != dry ] && stop "$f exists"; done
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801; the worktree's source state and record equal the pins; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
# memory: alert only
( while sleep 30; do av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo); [ "$av" -lt 2048 ] && echo "ALERT $(stamp) UTC MemAvailable $av MiB (alert only, nothing stopped)" >> $OUT/alert.log; done ) &
MEM=$!
# selftests
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc87_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# STEP 1: kc79 check accepts the source (both controls exit 1); the k_c 87 check refuses it
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $SR $SS $D $WTM > $OUT/source_kc87check_refuses.txt 2>&1; s3=$?
step "STEP 1 source check (kc79_syscheck_1025.py on dh170's k_c 79 D 19.75 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc87_syscheck_1025.py on the k_c 79 source exit $s3 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
# STEP 2: the regrid (macm3's command, the tag changed)
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 79 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "STEP 2 regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3),MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
RR=$WTM/data/$TAG.jsonl; RS=$WTM/data/sol_${TAG}_D19.7500.npy
cp $RR $OUT/ ; cp $RS $OUT/
# the acceptance: dh610's kc87 check and its controls; the k_c 79 check must refuse the result
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $RR $RS $D $WTM > $OUT/syscheck_kc79check_refuses.txt 2>&1; a3=$?
step "kc87 syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc79_syscheck_1025.py on the k_c 87 result exit $a3 (1 wanted)"
kill $MEM 2>/dev/null
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: kc87 syscheck $a0, controls $a1 $a2, kc79 check refuses $a3" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
