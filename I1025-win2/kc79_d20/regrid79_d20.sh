#!/bin/bash
# #1025 kc79_d20 on win2 (t5's hc, ~22:55 UTC 22 Nov): when the leap's D 20 state lands and reproduces its record, regrid it to k_c 79 as winb did at D 19 (raw I1025-win/kc79_d19):
#   ell_refine.py SRC 71 l1kc79W20m1025 79 1 20 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (lambda_0(20) = ell_delta.lam0_at(20) = 2.1110019498, unused with --no-gamma)
# 8 threads, BelowNormal (the launcher), cap 21600 s by the exact pid. Accepted only by kc79_syscheck_1025.py (blob 29dce7ea) and its two controls (--mutate=F and --mutate=steps must exit 1). Any refusal, failed
# control or non-converging regrid stops with a report; no retry. usage: regrid79_d20.sh   (env STD=20 the D, DRY=1: every step but the regrid; STD=19.5 DRY=1 is the rehearsal on the D 19.5 state)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_d20
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_d20   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc79.txt; SUM=$OUT/summary_kc79.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc71Lw1025b
STD=${STD:-20}
TAG=l1kc79W20m1025; [ "$STD" != 20 ] && TAG=l1kc79Wrehearsal${STD}
LAM0=${LAM0:-2.1110019498}
F6=$(printf '%.6f' $STD); F4=$(printf '%.4f' $STD)
STS=$KC/states/sol_${SRC}_D${F6}.npy; ST4=$KC/states/sol_${SRC}_D${F4}.npy; RECS=$KC/states/${SRC}.jsonl
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
refuse() { log "kc79 regrid STOP: $*"; echo "kc79 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc79 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/inputs/kc71_syscheck.py 4cd86cd4 "kc71_syscheck.py"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc79 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc79 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $DATA/sol_${TAG}_D${F4}.npy $OUT/regrid_accepted.txt; do [ -e $f ] && { log "kc79 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc79 regrid pins checked (inputs 29dce7ea 4cd86cd4, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 with solver code = 505d8399), D $STD, tag $TAG"
log "kc79 regrid waits for $STS and its record line"
until [ -e $STS ] && [ -e $ST4 ] && [ $(( $(date +%s) - $(date -r $STS +%s) )) -ge 60 ] && [ $(( $(date +%s) - $(date -r $ST4 +%s) )) -ge 60 ] && grep -q "\"D\": $(python -I -c "print(repr(float('$STD')))")," $RECS 2>/dev/null; do
  [ -e $KC/leap2.finished ] && { [ ! -e $STS ] && refuse "the leap ended without the D $STD state" 3; }
  sleep 30
done
cmp -s $STS $ST4 || refuse "the .6f and .4f state files of D $STD differ"
grep "\"D\": $(python -I -c "print(repr(float('$STD')))")," $RECS | tail -n 1 > $OUT/rec_k71_D${F4}.jsonl
log "kc79 regrid source: state $(git hash-object --no-filters $STS | cut -c1-8), record $(git hash-object --no-filters $OUT/rec_k71_D${F4}.jsonl | cut -c1-8): $(cut -c1-170 $OUT/rec_k71_D${F4}.jsonl)"
cd $OUT
"$PY" -I inputs/kc71_syscheck.py $RECS $STS $STD $WTM > $OUT/source_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls)' $OUT/source_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "the k_c 71 source state is not accepted by kc71_syscheck.py (exit $s)"
for m in F steps; do "$PY" -I inputs/kc71_syscheck.py $RECS $STS $STD $WTM --mutate=$m > $OUT/source_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m did not exit 1"; done
log "kc79 regrid: the k_c 71 source of D $STD is accepted (record class |F|, steps come back, both controls refused)"
cp $STS $DATA/sol_${SRC}_D${F4}.npy
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy)" = "$(git hash-object --no-filters $STS)" ] || refuse "the copied source state differs from its blob"
CMD="$PY -u ell_refine.py $SRC 71 $TAG 79 1 $STD $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, cap 21600 s)"; log "kc79 regrid DRY run ended before the regrid"; exit 0; }
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid79 0 21600 ell_refine.py $CMD >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "kc79 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc79 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${TAG}_D${F4}.npy ] && [ -s $DATA/${TAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${TAG}_D${F4}.npy $DATA/${TAG}.jsonl $OUT/
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM > $OUT/syscheck.txt 2>&1; s=$?
cat $OUT/syscheck.txt | grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' >> $SUM
[ $s = 0 ] || refuse "kc79_syscheck_1025.py does not accept the k_c 79 state (exit $s)"
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM --mutate=$m > $OUT/syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
tail -n 1 $OUT/${TAG}.jsonl > $OUT/rec_k79_D${F4}.jsonl
python -I - $OUT/rec_k71_D${F4}.jsonl $OUT/rec_k79_D${F4}.jsonl > $OUT/regrid_accepted.txt <<'PYEOF'
import json, sys
a = json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); b = json.loads(open(sys.argv[2]).read().strip().splitlines()[-1])
print("ACCEPTED: k_c 71 source |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 79 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 79 minus k_c 71 %.4e), regrid %s s" % (a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
PYEOF
cat $OUT/regrid_accepted.txt >> $SUM; log "kc79 regrid ACCEPTED: $(cat $OUT/regrid_accepted.txt | cut -c1-200)"
touch $OUT/regrid.done
exit 0
