#!/bin/bash
# #1025 kc79_d2025 on win2 (the coordinator's task, comment 7093559078, hc ~07:50 UTC 23 Nov): lambda_1 past D 20 on win2's build. Step 1: leg 3's accepted k_c 71 D 20.25 state and record (raw 589d5f2a, kc71_leap/states/:
# sol_l1kc71Lw1025c_D20.250000.npy blob 8e137d6b, l1kc71Lw1025c.jsonl blob cc1e872c) regridded to k_c 79 as at D 20:
#   ell_refine.py l1kc71Lw1025c 71 l1kc79win2d2025 79 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (lambda_0 = ell_delta.lam0_at(20.25) = 2.1099063840, error 3.9e-6, unused with --no-gamma)
# Source first: kc71_syscheck.py (4cd86cd4) accepts it (its --mutate=F and --mutate=steps exit 1). Result accepted only by kc79_syscheck_1025.py (29dce7ea; selftest 0, controls refused, --mutate=F and --mutate=steps exit 1).
# 8 threads, the launcher's priority (Normal), cap 21600 s by the exact pid. A refusal, a failed control or a regrid that does not converge stops with a report; no retry. usage: regrid79_d2025.sh   (DRY=1: the source checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_d2025   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_kc79.txt; SUM=$OUT/summary_kc79.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data; WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_d2025
SRC=l1kc71Lw1025c; TAG=l1kc79win2d2025; STD=20.25; F4=20.2500; LAM0=2.1099063840
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
refuse() { log "kc79 d2025 regrid STOP: $*"; echo "kc79 d2025 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc79 d2025 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/kc71_syscheck.py 4cd86cd4 "kc71_syscheck.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/inputs/sol_${SRC}_D20.250000.npy 8e137d6b "the pinned k_c 71 D 20.25 state"
chk $OUT/inputs/${SRC}.jsonl cc1e872c "the pinned k_c 71 record file"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc79 d2025 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc79 d2025 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $DATA/sol_${TAG}_D${F4}.npy $OUT/regrid_accepted.txt $OUT/regrid_refused.txt; do [ -e $f ] && { log "kc79 d2025 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc79 d2025 regrid pins checked (kc71 check 4cd86cd4, kc79 check 29dce7ea, source state 8e137d6b, record file cc1e872c, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399)"
cd $OUT
RECS=$OUT/inputs/${SRC}.jsonl; STS=$OUT/inputs/sol_${SRC}_D20.250000.npy
# ell_refine reads data/sol_SRC_D{D:.4f}.npy: the pinned state is copied there under that name (blob checked)
cp $STS $DATA/sol_${SRC}_D${F4}.npy
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy)" = "$(git hash-object --no-filters $STS)" ] || refuse "the copied source state differs from its blob"
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > selftest_kc79_syscheck.txt 2>&1; [ $? = 0 ] || refuse "kc79_syscheck_1025.py --selftest did not exit 0"
"$PY" -I inputs/kc71_syscheck.py $RECS $STS $STD $WTM > source_kc71_syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc71_syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc71_syscheck.py does not accept the k_c 71 D 20.25 source (exit $s)"
for m in F steps; do "$PY" -I inputs/kc71_syscheck.py $RECS $STS $STD $WTM --mutate=$m > source_kc71_syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m did not exit 1"; done
grep -F "\"D\": $STD," $RECS | tail -n 1 > $OUT/rec_k71_D${F4}.jsonl
log "kc79 d2025 regrid: the k_c 71 D 20.25 source is accepted (record |F| and steps come back, both controls refused); record $(git hash-object --no-filters $OUT/rec_k71_D${F4}.jsonl | cut -c1-8)"
CMD="$PY -u ell_refine.py $SRC 71 $TAG 79 1 $STD $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, cap 21600 s)"; log "kc79 d2025 regrid DRY run ended before the regrid"; exit 0; }
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/regrid.log
s0=$(date +%s)
crun regrid79b 0 21600 ell_refine.py $CMD >> $OUT/regrid.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid.log
echo "kc79 d2025 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc79 d2025 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${TAG}_D${F4}.npy ] && [ -s $DATA/${TAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${TAG}_D${F4}.npy $DATA/${TAG}.jsonl $OUT/
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM > syscheck.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck.txt >> $SUM
[ $s = 0 ] || refuse "kc79_syscheck_1025.py does not accept the k_c 79 state (exit $s)"
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $STD $WTM --mutate=$m > syscheck_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
tail -n 1 $OUT/${TAG}.jsonl > $OUT/rec_k79_D${F4}.jsonl
# the summary line: python gets Windows paths (an MSYS path wrote an empty file at the k_c 87 D 20 regrid)
"$PY" -I -c "
import json
a = json.loads(open('$WOUT/rec_k71_D${F4}.jsonl').read().strip().splitlines()[-1]); b = json.loads(open('$WOUT/rec_k79_D${F4}.jsonl').read().strip().splitlines()[-1])
print('ACCEPTED: k_c 71 source |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 79 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 79 minus k_c 71 %.4e), regrid %s s' % (a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
" > $OUT/regrid_accepted.txt
[ -s $OUT/regrid_accepted.txt ] || refuse "regrid_accepted.txt is empty (the summary step failed)"
cat $OUT/regrid_accepted.txt >> $SUM; log "kc79 d2025 regrid ACCEPTED: $(cut -c1-220 $OUT/regrid_accepted.txt)"
touch $OUT/regrid.done
exit 0
