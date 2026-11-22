#!/bin/bash
# #1075 step 2 (t5's order, 2026-11-22): win2's k_c 71 D 20 state: win2's kc71_syscheck.py on it (and its two controls), then the regrid to k_c 79 with
# ell_refine.py as dh370's D 19.5 regrid, accepted only by kc79_syscheck_1025.py and its two controls. 3 threads, nice 10, cap 43200 s, a systemd user unit.
# Steps and verdicts go to steps.txt and VERDICT.txt. usage: run_regrid.sh   (pins.txt: "blob8 path-in-raw" per line, written at launch)
{
OUT=/home/nathan/Source/choptuik-large-d-raw/I1075-rpi5/kc79_d20
RAWIN=/home/nathan/Source/choptuik-large-d-raw-964
WT=/home/nathan/Source/choptuik-large-d-1075; WTM=$WT/solver/matter
PY=/home/nathan/Source/venv-1025/bin/python
SRC=l1kc71Lw1025b; TAG=l1kc79rpi5d20; D=20.0; LAM0=2.1110019498
export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
step "start (load $(cut -d' ' -f1-3 /proc/loadavg))"
while read -r b p; do
  [ "$(blob $RAWIN/$p | cut -c1-8)" = "$b" ] || stop "$p is not blob $b"
  cp $RAWIN/$p $OUT/in/
done < $OUT/pins.txt
step "inputs pinned and copied to in/: $(tr '\n' ';' < $OUT/pins.txt)"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 505d8399 ] || stop "worktree not at 505d8399"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(git -C $WT hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
step "worktree 505d8399, ell_refine.py 631e5801; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
cp $OUT/in/sol_${SRC}_D20.000000.npy $WTM/data/sol_${SRC}_D20.0000.npy
[ "$(blob $WTM/data/sol_${SRC}_D20.0000.npy | cut -c1-8)" = "$(grep 'sol_l1kc71Lw1025b_D20.000000.npy' $OUT/pins.txt | cut -d' ' -f1)" ] || stop "copied source state blob differs"
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py --selftest > $OUT/selftest_kc71_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc71_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
REC71=$OUT/in/l1kc71Lw1025b.jsonl
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $REC71 $WTM/data/sol_${SRC}_D20.0000.npy $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $REC71 $WTM/data/sol_${SRC}_D20.0000.npy $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $REC71 $WTM/data/sol_${SRC}_D20.0000.npy $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
step "source check (win2's kc71_syscheck.py on the k_c 71 D 20 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
CMD="nice -n 10 timeout 43200 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 3 threads, nice 10, cap 43200 s): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python3.14 -o rss=,pcpu=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-3)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
cp $WTM/data/$TAG.jsonl $OUT/ ; cp $WTM/data/sol_${TAG}_D20.0000.npy $OUT/
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.0000.npy $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.0000.npy $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D20.0000.npy $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: syscheck $a0, controls $a1 $a2" > $OUT/VERDICT.txt; fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}
