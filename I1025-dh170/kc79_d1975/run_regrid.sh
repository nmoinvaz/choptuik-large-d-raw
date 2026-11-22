#!/bin/bash
# #1025 kc79_d1975 (t5's order, 22 Nov): win2's k_c 71 D 19.75 state regridded to k_c 79 with ell_refine.py, accepted only by kc79_syscheck_1025.py and its two controls (winb's recipe of I1025-win/kc79_d19, dh370's of
# I1025-dh370/kc79_d195). 8 threads, nice 10, cap 21600 s, a systemd user unit (i1025-k79r). Steps and verdicts go to steps.txt and VERDICT.txt. Writes nothing outside this folder and the worktree's solver/matter/data/.
# usage: run_regrid.sh [dry]   (dry: pins and worktree checks only)
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc79_d1975
WT=/home/nathan/Source/choptuik-large-d-1025k79
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
SRC=l1kc71Lw1025b; TAG=l1kc79dh170d1975; D=19.75; LAM0=2.1120935738
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
cd $OUT || exit 9
MODE=${1:-}
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
[ "$MODE" = dry ] && OUT_STEPS=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/5e14df5b-8f5b-49f8-ab79-88a302ef8042/scratchpad/dry_steps_k79d1975.txt
[ -e $OUT/VERDICT.txt ] && [ "$MODE" != dry ] && { echo "VERDICT.txt exists"; exit 2; }
step "start${MODE:+ ($MODE)} (load $(cut -d' ' -f1-3 /proc/loadavg))"
# pins: every file of in/ against in_blobs.txt
while read -r h f; do [ -f $OUT/in/$f ] && [ "$(blob $OUT/in/$f)" = "$h" ] || stop "in/$f is missing or not blob $h"; done < $OUT/in_blobs.txt
step "inputs pinned (in_blobs.txt: $(wc -l < $OUT/in_blobs.txt) files; state $(blob $OUT/in/sol_l1kc71Lw1025b_D19.750000.npy | cut -c1-8), record $(blob $OUT/in/l1kc71Lw1025b.jsonl | cut -c1-8), kc71_syscheck $(blob $OUT/in/kc71_syscheck.py | cut -c1-8), kc79_syscheck $(blob $OUT/in/kc79_syscheck_1025.py | cut -c1-8))"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
for f in $WTM/data/sol_${SRC}_D19.7500.npy $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy; do [ -e $f ] && [ "$MODE" != dry ] && stop "$f exists"; done
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
[ "$MODE" = dry ] && { step "dry run: pins and worktree ok, nothing started"; exit 0; }
# the source state under the name ell_refine reads
cp $OUT/in/sol_l1kc71Lw1025b_D19.750000.npy $WTM/data/sol_${SRC}_D19.7500.npy
[ "$(blob $WTM/data/sol_${SRC}_D19.7500.npy | cut -c1-8)" = ab514df3 ] || stop "copied source state blob differs"
# selftests
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py --selftest > $OUT/selftest_kc71_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc71_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# step 1: the source check on this machine, with its controls
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.7500.npy $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.7500.npy $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.7500.npy $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
step "STEP 1 source check (win2's kc71_syscheck.py on the k_c 71 D 19.75 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
# step 2: the regrid
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "STEP 2 regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
cp $WTM/data/$TAG.jsonl $OUT/ ; cp $WTM/data/sol_${TAG}_D19.7500.npy $OUT/
# the acceptance
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.7500.npy $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ]; then
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: syscheck $a0, controls $a1 $a2" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
