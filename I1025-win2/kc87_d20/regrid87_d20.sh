#!/bin/bash
# #1025 kc87_d20 on win2 (the coordinator's task, comment 7090320838, hc ~03:10 UTC 23 Nov): k_c 87 at D 20 from win2's OWN accepted k_c 79 D 20 state (raw c9d6762c, ../kc79_d20/). Step 1:
#   ell_refine.py l1kc79W20m1025 79 l1kc87win2d20 87 1 20.0 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (lambda_0 = the k_c 79 D 20 regrid's 2.1110019498, unused with --no-gamma)
# Source: kc79_syscheck_1025.py (29dce7ea) must ACCEPT it (its --mutate=F and --mutate=steps exit 1) and kc87_syscheck_1025.py (6df5d960, dh610's, raw ec9fb489) must REFUSE it. Result: accepted only by kc87_syscheck_1025.py
# (selftest 0, --mutate=F and --mutate=steps exit 1) with kc79_syscheck_1025.py REFUSING it. 8 threads, BelowNormal (the launcher), cap 21600 s by the exact pid. A refusal, a failed control or a regrid that does not converge
# stops with a report; no retry. usage: regrid87_d20.sh   (env DRY=1: the source checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc87_d20   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc87.txt; SUM=$OUT/summary_kc87.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc79W20m1025; TAG=l1kc87win2d20; LAM0=2.1110019498
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
refuse() { log "kc87 regrid STOP: $*"; echo "kc87 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc87 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/inputs/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $OUT/inputs/sol_${SRC}_D20.0000.npy 7e288cc8 "the pinned k_c 79 D 20 state"
chk $OUT/inputs/${SRC}.jsonl d659667f "the pinned k_c 79 D 20 record"
chk $DATA/sol_${SRC}_D20.0000.npy 7e288cc8 "the worktree's copy of the k_c 79 D 20 state"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc87 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc87 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $DATA/sol_${TAG}_D20.0000.npy $OUT/regrid_accepted.txt $OUT/regrid_refused.txt; do [ -e $f ] && { log "kc87 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc87 regrid pins checked (kc79 check 29dce7ea, kc87 check 6df5d960, source state 7e288cc8, record d659667f, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399)"
cd $OUT
RECS=$OUT/inputs/${SRC}.jsonl; STS=$OUT/inputs/sol_${SRC}_D20.0000.npy
# the checks' own selftests, then the source: the k_c 79 check accepts it (both mutations exit 1), the k_c 87 check refuses it
"$PY" -I inputs/kc87_syscheck_1025.py --selftest > selftest_kc87_syscheck.txt 2>&1; [ $? = 0 ] || refuse "kc87_syscheck_1025.py --selftest did not exit 0"
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > selftest_kc79_syscheck.txt 2>&1; [ $? = 0 ] || refuse "kc79_syscheck_1025.py --selftest did not exit 0"
"$PY" -I inputs/kc79_syscheck_1025.py $RECS $STS 20 $WTM > source_kc79_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc79_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc79_syscheck_1025.py does not accept the k_c 79 source (exit $s)"
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $RECS $STS 20 $WTM --mutate=$m > source_kc79_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m (k_c 79 check) did not exit 1"; done
"$PY" -I inputs/kc87_syscheck_1025.py $RECS $STS 20 $WTM > source_kc87_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED)' source_kc87_syscheck.txt >> $SUM
[ $s = 1 ] || refuse "kc87_syscheck_1025.py did not refuse the k_c 79 source (exit $s)"
log "kc87 regrid: the k_c 79 D 20 source is accepted by the k_c 79 check (controls exit 1) and refused by the k_c 87 check"
CMD="$PY -u ell_refine.py $SRC 79 $TAG 87 1 20.0 $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, cap 21600 s)"; log "kc87 regrid DRY run ended before the regrid"; exit 0; }
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid87 0 21600 ell_refine.py $CMD >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "kc87 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc87 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${TAG}_D20.0000.npy ] && [ -s $DATA/${TAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${TAG}_D20.0000.npy $DATA/${TAG}.jsonl $OUT/
cd $OUT
"$PY" -I inputs/kc87_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D20.0000.npy 20 $WTM > syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc87_syscheck_1025.py does not accept the k_c 87 state (exit $s)"
for m in F steps; do "$PY" -I inputs/kc87_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D20.0000.npy 20 $WTM --mutate=$m > syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D20.0000.npy 20 $WTM > syscheck_kc79_on_result.txt 2>&1; [ $? = 1 ] || refuse "kc79_syscheck_1025.py did not refuse the k_c 87 result"
tail -n 1 $OUT/${TAG}.jsonl > $OUT/rec_k87_D20.0000.jsonl
python -I -c "
import json, sys
a = json.loads(open('$RECS').read().strip().splitlines()[-1]); b = json.loads(open('$OUT/rec_k87_D20.0000.jsonl').read().strip().splitlines()[-1])
print('ACCEPTED: k_c 79 source |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 87 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 87 minus k_c 79 %.4e), regrid %s s' % (a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
" > $OUT/regrid_accepted.txt
cat $OUT/regrid_accepted.txt >> $SUM; log "kc87 regrid ACCEPTED: $(cut -c1-220 $OUT/regrid_accepted.txt)"
touch $OUT/regrid.done
exit 0
