#!/bin/bash
# #1025 kc95_d22 / kc95_d225 on win2 (the coordinator's hc of 2026-11-24 ~17:25 UTC): "k_c 95 REGRIDS at chosen D from macm3's k_c 87 leg states, which are at h 0.03125 from D 21.8125 on: first D 22.0, then D 22.5, each as soon as macm3
# pushes that state (raw I1025-macm3/kc87_leg2/b/, tag l1kc87Lmacm3b). Each: pin by blob, kc87_syscheck accepts it (controls 1 1); ell_refine.py <tag> 87 <new tag> 95 1 <D> <lambda_0 from its record> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12
# --wait 60 --no-gamma, 4 threads BelowNormal, 6 h cap; kc95_syscheck_1025.py accepts the result (controls 1 1, kc87 check refuses)".
# usage: kc95_regrid.sh D NEWTAG SUBFOLDER   (e.g. 22.0 l1kc95win2d22 kc95_d22; DRY=1: fetch, pins, source checks and the command, no regrid)
# Steps: pins and selftests; fetch_macm3.py waits (gh api, blob-verified) for the state of D and its record row; the k_c 87 check accepts the state (selftest 0; --mutate=F and --mutate=steps exit 1); the state is copied into the k_c 79 worktree's
# data/ under the name ell_refine reads (sol_l1kc87Lmacm3b_D{D:.4f}.npy); lambda_0 = ell_delta.lam0_at(D) (unused with --no-gamma); ell_refine in one process (crun, cap 21600 s by the exact root pid, no retry); the k_c 95 check accepts the result
# (selftest 0, --mutate=F and --mutate=steps exit 1) and the k_c 87 check refuses it.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
D=$1; NEWTAG=$2; SUB=$3
[ -n "$D" ] && [ -n "$NEWTAG" ] && [ -n "$SUB" ] || { echo "usage: kc95_regrid.sh D NEWTAG SUBFOLDER"; exit 2; }
OUT=$BASE/$SUB; WOUT=D:/choptuik-i935-raw/I1025-win2/$SUB
EX=$OUT/exits_regrid.txt; SUM=$OUT/summary_regrid.txt
INP=$BASE/kc95_leap/inputs
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc87Lmacm3b; F4=$(printf "%.4f" $D)
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
mkdir -p $OUT/in
refuse() { log "kc95 D $D regrid STOP: $*"; echo "kc95 D $D regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc95 D $D regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $INP/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $INP/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc95 D $D regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc95 D $D regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${NEWTAG}.jsonl $DATA/sol_${NEWTAG}_D${F4}.npy $OUT/regrid_accepted.txt $OUT/regrid_refused.txt; do [ -e $f ] && { log "kc95 D $D regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc95 D $D regrid pins checked (kc95 check d487e628, kc87 check 6df5d960, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399)"
cd $OUT
"$PY" -I $INP/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1 || refuse "kc87_syscheck_1025.py --selftest did not exit 0"
"$PY" -I $INP/kc95_syscheck_1025.py --selftest > selftest_kc95_syscheck.txt 2>&1 || refuse "kc95_syscheck_1025.py --selftest did not exit 0"
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest > selftest_fetch.txt 2>&1 || refuse "fetch_macm3.py --selftest did not exit 0"
"$PY" -I $BASE/kc95_d22/fetch_macm3.py --selftest --mutate > /dev/null 2>&1; [ $? = 1 ] || refuse "fetch_macm3.py --selftest --mutate did not exit 1"
log "kc95 D $D regrid: waits for macm3's state of D $D (raw I1025-macm3/kc87_leg2/b/)"
"$PY" -I $BASE/kc95_d22/fetch_macm3.py $D $WOUT/in > fetch.log 2>&1; fr=$?
[ $fr = 0 ] || refuse "fetch_macm3.py exit $fr (see fetch.log)"
log "kc95 D $D regrid: fetched $(grep -E '^(state|record)' $OUT/in/fetched.txt | tr '\n' ' ' | cut -c1-260)"
STS=$OUT/in/sol_${SRC}_D${F4}.npy; RECS=$OUT/in/${SRC}.jsonl
"$PY" -I $INP/kc87_syscheck_1025.py $RECS $STS $D $WTM > source_kc87_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc87_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc87_syscheck_1025.py does not accept the k_c 87 source (exit $s)"
for m in F steps; do "$PY" -I $INP/kc87_syscheck_1025.py $RECS $STS $D $WTM --mutate=$m > source_kc87_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m did not exit 1"; done
log "kc95 D $D regrid: the k_c 87 source is accepted (selftest 0; --mutate=F and --mutate=steps exit 1); state blob $(git hash-object --no-filters $STS | cut -c1-8)"
cp $STS $DATA/sol_${SRC}_D${F4}.npy
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy)" = "$(git hash-object --no-filters $STS)" ] || refuse "the copied source state differs from its blob"
LAM0=$("$PY" -I -c "
import sys
sys.path.insert(0, '$WTM')
import ell_delta
Ds, L = ell_delta.lam0_table()
print('%.10f' % ell_delta.lam0_at($D, Ds, L)[0])" | tr -d '\r')
[ -n "$LAM0" ] || refuse "lambda_0 could not be computed"
CMD="$PY -u ell_refine.py $SRC 87 $NEWTAG 95 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (4 threads, cap 21600 s)"; log "kc95 D $D regrid DRY run ended before the regrid"; exit 0; }
# threads: the order starts the regrids at tag g's end (all8.done, 19:19:49 UTC at its cap); one regrid of mine at a time (4 threads each)
log "kc95 D $D regrid waits for the tag g leap's end (all8.done) and for any other regrid of mine to end"
until [ -e /d/choptuik-i935-raw/I1025-win2/kc79_leap/all8.done ]; do sleep 30; done
while [ "$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.Name -match '^python' -and \$_.CommandLine -match 'ell_refine.py l1kc87Lmacm3b' }).Count" | tr -d '\r')" != 0 ]; do sleep 30; done
# the coordinator's hc of 24 Nov ~17:55 UTC: "hold the k_c 95 regrids until the #1078 build on t25 ends ...; start them when committed memory is back below ~80 GB" (a wait, nothing is stopped)
commit_gb() { powershell -NoProfile -Command "[math]::Round((Get-Counter '\\Memory\\Committed Bytes').CounterSamples[0].CookedValue/1GB,1)" | tr -d '\r'; }
# 24 Nov ~19:30 UTC: "start the D 21.875 regrid now; drop the 80 GB gate" (win2's pagefile is system-managed, 197 GB free on C:, so the commit limit grows): COMMIT_GATE_GB=off skips the wait, a number replaces the 80
cg=$(commit_gb); held=0; GATE=${COMMIT_GATE_GB:-80}
while [ "$GATE" != off ] && awk -v c="$cg" -v g="$GATE" 'BEGIN { exit !(c >= g) }'; do
  [ $held = 0 ] && { log "kc95 D $D regrid held: committed memory $cg GB is not below $GATE GB (the order's gate); waits"; held=1; }
  sleep 60; cg=$(commit_gb)
done
log "kc95 D $D regrid: the threads are free, committed memory is $cg GB (gate: $GATE GB), starting"
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid95_$F4 0 21600 ell_refine.py $CMD >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "kc95 D $D regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc95 D $D regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${NEWTAG}_D${F4}.npy ] && [ -s $DATA/${NEWTAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${NEWTAG}_D${F4}.npy $DATA/${NEWTAG}.jsonl $OUT/
cd $OUT
"$PY" -I $INP/kc95_syscheck_1025.py $OUT/${NEWTAG}.jsonl $OUT/sol_${NEWTAG}_D${F4}.npy $D $WTM > syscheck95.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck95.txt >> $SUM
[ $s = 0 ] || refuse "kc95_syscheck_1025.py does not accept the k_c 95 state (exit $s)"
for m in F steps; do "$PY" -I $INP/kc95_syscheck_1025.py $OUT/${NEWTAG}.jsonl $OUT/sol_${NEWTAG}_D${F4}.npy $D $WTM --mutate=$m > syscheck95_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I $INP/kc87_syscheck_1025.py $OUT/${NEWTAG}.jsonl $OUT/sol_${NEWTAG}_D${F4}.npy $D $WTM > syscheck_kc87_on_k95_result.txt 2>&1; [ $? = 1 ] || refuse "kc87_syscheck_1025.py did not refuse the k_c 95 result"
tail -n 1 $OUT/${NEWTAG}.jsonl > $OUT/rec_k95_D${F4}.jsonl
# the summary line: python gets Windows paths (an MSYS path wrote an empty file once)
"$PY" -I -c "
import json
rows = [json.loads(l) for l in open('$WOUT/in/${SRC}.jsonl') if l.strip()]
a = [r for r in rows if abs(r['D'] - $D) < 1e-9][-1]
b = json.loads(open('$WOUT/rec_k95_D${F4}.jsonl').read().strip().splitlines()[-1])
print('ACCEPTED: k_c 87 source D %s |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 95 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 95 minus k_c 87 %.4e), regrid %s s' % (a['D'], a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
" > $OUT/regrid_accepted.txt
[ -s $OUT/regrid_accepted.txt ] || refuse "regrid_accepted.txt is empty (the summary step failed)"
cat $OUT/regrid_accepted.txt >> $SUM; log "kc95 D $D regrid ACCEPTED: $(cut -c1-220 $OUT/regrid_accepted.txt)"
touch $OUT/regrid.done
exit 0
