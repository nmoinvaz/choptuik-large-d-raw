#!/bin/bash
# #1025 kc79_d195 (t5's hc 2026-11-22, received before 18:36 UTC): win2's k_c 71 D 19.5 state regridded to k_c 79 with ell_refine.py, accepted only by
# kc79_syscheck_1025.py and its two controls (winb's recipe of I1025-win/kc79_d19, f712f94c). 6 threads, nice 10, cap 21600 s, outside the terminal
# (unit i1025k79). Steps and verdicts go to steps.txt and VERDICT.txt; no hc from here (the session watches the files).
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc79_d195
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1025
WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
SRC=l1kc71Lw1025b; TAG=l1kc79dh370d195; D=19.5; LAM0=2.1132623525
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
step "start (load $(cut -d' ' -f1-3 /proc/loadavg))"
# pins
declare -A PIN=(
  [$RAWIN/I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.500000.npy]=6b65c531
  [$RAWIN/I1025-win2/kc71_leap/kc71_syscheck.py]=4cd86cd4
  [$RAWIN/I1025-win/kc79_d19/kc79_syscheck_1025.py]=29dce7ea
  [$RAWIN/I1025-mac/d18/d18_hybsign.py]=e089207a
  [$RAWIN/I1025-dh170/lower_root/read_lower.py]=89309d3c
  [$RAWIN/I1025-mac/d18/d185_scan_read.py]=7c9d400f )
for f in "${!PIN[@]}"; do
  [ "$(blob $f | cut -c1-8)" = "${PIN[$f]}" ] || stop "$f is not blob ${PIN[$f]}"
  cp $f $OUT/in/
done
# the record file: the blob of raw b343a4da (win2's leg 2 state D 19.5 commit, 3 lines to D 19.5); the current raw file (c6dc4397) appends D 19.5625, its D 19.5 line is identical (checked)
git -C $RAWIN show b343a4da:I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl > $OUT/in/l1kc71Lw1025b.jsonl || stop "cannot read the record at b343a4da"
[ "$(blob $OUT/in/l1kc71Lw1025b.jsonl | cut -c1-8)" = 464fe2f2 ] || stop "the record from b343a4da is not blob 464fe2f2"
step "inputs pinned and copied to in/ (state 6b65c531, record 464fe2f2 from raw b343a4da, kc71_syscheck 4cd86cd4, kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
# source state under the name ell_refine reads
cp $OUT/in/sol_l1kc71Lw1025b_D19.500000.npy $WTM/data/sol_${SRC}_D19.5000.npy
[ "$(blob $WTM/data/sol_${SRC}_D19.5000.npy | cut -c1-8)" = 6b65c531 ] || stop "copied source state blob differs"
# selftests
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py --selftest > $OUT/selftest_kc71_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc71_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# source check on this machine, with its controls
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025b.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
step "source check (win2's kc71_syscheck.py on the k_c 71 D 19.5 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
# the regrid
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 6 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
cp $WTM/data/$TAG.jsonl $OUT/ ; cp $WTM/data/sol_${TAG}_D19.5000.npy $OUT/
# the acceptance
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ]; then
  echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt
else
  echo "REFUSED: syscheck $a0, controls $a1 $a2" > $OUT/VERDICT.txt
fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
