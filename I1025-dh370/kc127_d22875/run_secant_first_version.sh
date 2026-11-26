#!/bin/bash
# #1025 kc127_d22875 step 4b (t5's order): with exactly one robust change in the scan, d18_secant.py (eb1396ad, worktree ~/Source/choptuik-large-d-1025v at 92b9bf53, the scan's) on its bracket, as macm3's
# kc111_d230625 secant: --tol=1e-5 --maxev=10 --pin=<state blob>,<record blob>, ONE process of 1 thread, nice 10, cap 28800 s. Refuses unless read_lower.txt says "robust changes: 1" and the
# bracket given equals that change's bracket. First d18_secant.py selftest (exit 0) and its three mutations (exit 1 each). A systemd user unit (i1025k127s). usage: run_secant.sh LO HI
{
LO=$1; HI=$2
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc127_d22875
WT=/home/nathan/Source/choptuik-large-d-1025v; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
. $OUT/stage.conf
STATE=$OUT/sol_${TAG}_${DT}.npy; STUB=$OUT/$TAG.jsonl
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
mkdir -p $OUT/secant; cd $OUT || exit 9
grep -q '^ACCEPTED' VERDICT.txt || { step "SECANT STOP: no ACCEPTED verdict"; exit 1; }
grep -q '^robust changes: 1;' read_lower.txt && grep -qE "robust change \($LO, $HI\)" read_lower.txt || { step "SECANT STOP: read_lower.txt does not show exactly one robust change with the bracket ($LO, $HI)"; exit 1; }
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 92b9bf53 ] && [ "$(blob $WTM/d18_secant.py)" = eb1396ad ] || { step "SECANT STOP: the worktree is not 92b9bf53 or d18_secant.py is not eb1396ad"; exit 1; }
SB=$(blob $STATE); RB=$(blob $STUB)
step "secant: selftest, then bracket ($LO, $HI), --tol=1e-5 --maxev=10 --pin=$SB,$RB, 1 process x 1 thread, nice 10, cap 28800 s"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM
cd $WTM
nice -n 10 $PY -I d18_secant.py selftest > $OUT/secant/selftest.txt 2>&1; e0=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=half > $OUT/secant/selftest_half.txt 2>&1; e1=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=norobust > $OUT/secant/selftest_norobust.txt 2>&1; e2=$?
nice -n 10 $PY -I d18_secant.py selftest --mutate=nosigncheck > $OUT/secant/selftest_nosigncheck.txt 2>&1; e3=$?
step "d18_secant selftest exit $e0 (0 wanted); mutations half exit $e1, norobust exit $e2, nosigncheck exit $e3 (1 wanted each)"
[ $e0 = 0 ] && [ $e1 = 1 ] && [ $e2 = 1 ] && [ $e3 = 1 ] || { step "SECANT STOP: a selftest or a mutation did not read as written"; exit 1; }
t0=$(date +%s)
nice -n 10 timeout 28800 /usr/bin/time -v $PY -u d18_secant.py run $STUB $STATE $D $LO $HI $OUT/secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=$SB,$RB > $OUT/secant/secant.log 2>&1; rc=$?
echo $rc > $OUT/secant/exit.txt
step "secant exit $rc, $(( $(date +%s) - t0 )) s; $(grep '^root:' $OUT/secant/secant.log | cut -c1-300)"
grep -hE 'Elapsed|Maximum resident' $OUT/secant/secant.log >> $OUT/steps.txt
echo "SECANT DONE exit $rc $(stamp) UTC" > $OUT/SECANT_DONE.txt
exit 0
}
