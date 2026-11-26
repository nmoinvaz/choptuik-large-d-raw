#!/bin/bash
# #1025 kc135_d23 on win2 (the coordinator's hc of 2026-11-26 14:14 UTC), steps 1 to 3: k_c 135 at D 23.0, regridded from winb's accepted k_c 127 state (raw I1025-win/kc127_d23).
# Step 1: pins; selftests of the three checks; kc127_syscheck_1025.py exits 0 on the source, --mutate=F and --mutate=steps exit 1, the kc119 and kc135 checks refuse it.
# Step 2: ell_refine.py l1kc127wind23 127 l1kc135win2d23 135 1 23.0 2.0992182200 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, one process, 8 threads, Normal priority
# (started through cim_start.ps1 -Normal), cap 43200 s by the exact root pid (crun), no retry.
# Step 3: kc135_syscheck_1025.py exits 0 on the result (selftest 0, --mutate=F and --mutate=steps exit 1), the kc127 check refuses it; the table beside the source's.
# usage: kc135_regrid.sh   (DRY=1: pins, selftests, the source checks and the command; no regrid)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
BASE=/d/choptuik-i935-raw/I1025-win2
OUT=$BASE/kc135_d23; WOUT=D:/choptuik-i935-raw/I1025-win2/kc135_d23
IN=$OUT/inputs; WIN=$WOUT/inputs
SUM=$OUT/summary_regrid.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data
SRC=l1kc127wind23; NEW=l1kc135win2d23; D=23.0; F4=23.0000; CAP=43200
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
mkdir -p $OUT
refuse() { log "kc135 regrid STOP: $*"; echo "kc135 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc135 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $IN/src/sol_l1kc127wind23_D23.0000.npy 7a1b150c "the k_c 127 state"
chk $IN/src/l1kc127wind23.jsonl eea03461 "the k_c 127 record"
chk $IN/checks/kc127_syscheck_1025.py 898ebefa "kc127_syscheck_1025.py"
chk $IN/checks/kc135_syscheck_1025.py b353d466 "kc135_syscheck_1025.py"
chk $IN/checks/kc119_syscheck_1025.py fc6e0dd6 "kc119_syscheck_1025.py"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc135 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc135 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${NEW}.jsonl $DATA/sol_${NEW}_D${F4}.npy $OUT/regrid_accepted.txt $OUT/regrid_refused.txt; do [ -e $f ] && { log "kc135 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc135 regrid pins checked (state 7a1b150c, record eea03461, checks 898ebefa b353d466 fc6e0dd6, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399)"
cd $OUT
for k in 127 135 119; do "$PY" -I $IN/checks/kc${k}_syscheck_1025.py --selftest > selftest_kc${k}_syscheck.txt 2>&1 || refuse "kc${k}_syscheck_1025.py --selftest did not exit 0"; done
REC=$WIN/src/l1kc127wind23.jsonl; STS=$WIN/src/sol_l1kc127wind23_D23.0000.npy
"$PY" -I $WIN/checks/kc127_syscheck_1025.py $REC $STS $D $WTM > source_kc127_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc127_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc127_syscheck_1025.py does not accept the k_c 127 source (exit $s)"
for m in F steps; do "$PY" -I $WIN/checks/kc127_syscheck_1025.py $REC $STS $D $WTM --mutate=$m > source_kc127_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m did not exit 1"; done
for k in 119 135; do "$PY" -I $WIN/checks/kc${k}_syscheck_1025.py $REC $STS $D $WTM > source_kc${k}_syscheck_refuses.txt 2>&1; [ $? = 1 ] || refuse "kc${k}_syscheck_1025.py did not refuse the k_c 127 source"; done
log "kc135 regrid: the k_c 127 source is accepted (selftests 0; --mutate=F and --mutate=steps exit 1; the kc119 and kc135 checks refuse it)"
cp $IN/src/sol_l1kc127wind23_D23.0000.npy $DATA/sol_${SRC}_D${F4}.npy
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy | cut -c1-8)" = 7a1b150c ] || refuse "the copied source state differs from its blob"
LAM0=$("$PY" -I -c "
import sys
sys.path.insert(0, '$WTM')
import ell_delta
Ds, L = ell_delta.lam0_table()
print('%.10f' % ell_delta.lam0_at($D, Ds, L)[0])" | tr -d '\r')
[ "$LAM0" = 2.0992182200 ] || refuse "lambda_0 prints $LAM0, not the order's 2.0992182200"
CMD="$PY -u ell_refine.py $SRC 127 $NEW 135 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, Normal, cap $CAP s)"; log "kc135 regrid DRY run ended before the regrid"; exit 0; }
log "kc135 regrid starting: free RAM $(powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)" | tr -d '\r') GB"
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads, Normal priority)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid135 0 $CAP ell_refine.py $CMD >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "kc135 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at $CAP s")" >> $SUM; log "kc135 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${NEW}_D${F4}.npy ] && [ -s $DATA/${NEW}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${NEW}_D${F4}.npy $DATA/${NEW}.jsonl $OUT/
cd $OUT
RESREC=$WOUT/${NEW}.jsonl; RESST=$WOUT/sol_${NEW}_D${F4}.npy
"$PY" -I $WIN/checks/kc135_syscheck_1025.py $RESREC $RESST $D $WTM > syscheck135.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck135.txt >> $SUM
[ $s = 0 ] || refuse "kc135_syscheck_1025.py does not accept the k_c 135 state (exit $s)"
for m in F steps; do "$PY" -I $WIN/checks/kc135_syscheck_1025.py $RESREC $RESST $D $WTM --mutate=$m > syscheck135_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I $WIN/checks/kc127_syscheck_1025.py $RESREC $RESST $D $WTM > syscheck_kc127_on_k135_result.txt 2>&1; [ $? = 1 ] || refuse "kc127_syscheck_1025.py did not refuse the k_c 135 result"
echo "accepted $(date -u '+%F %T') UTC: state blob $(git hash-object --no-filters $OUT/sol_${NEW}_D${F4}.npy | cut -c1-8) record blob $(git hash-object --no-filters $OUT/${NEW}.jsonl | cut -c1-8)" > $OUT/regrid_accepted.txt
"$PY" -I -c "
import json
a = json.loads(open('$OUT/inputs/src/l1kc127wind23.jsonl').readline()); b = json.loads(open('$OUT/${NEW}.jsonl').readlines()[-1])
print('%-12s %-26s %-26s' % ('', 'k_c 127 (source)', 'k_c 135 (result)'))
for k in ('steps', 'F', 'F_start', 'constraint', 'Delta', 'seconds', 'dDelta_dF'):
    print('%-12s %-26s %-26s' % (k, a.get(k), b.get(k)))
print('steps ratio %.4f; Delta difference %.3e' % (b['steps'] / a['steps'], b['Delta'] - a['Delta']))" | tee -a $SUM
log "kc135 regrid accepted: $(tail -n 1 $SUM | cut -c1-200)"
touch $OUT/regrid.done
exit 0
