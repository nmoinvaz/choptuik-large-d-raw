#!/bin/bash
# #1025 kc79_leap on win2 (the coordinator's hc of 2026-11-23 ~12:20 UTC), step (1): leg 3's accepted k_c 71 state at D (20.5: blob 63399965, 20.75: blob fe8503cc) regridded to k_c 79 as at D 20.25 (../kc79_d2025/):
#   ell_refine.py l1kc71Lw1025c 71 TAG 79 1 D LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (LAM0 = ell_delta.lam0_at(D, *lam0_table()), unused with --no-gamma)
# Source first: kc71_syscheck.py (4cd86cd4) accepts it against leg 3's record file (blob b4f4bba7, 12 records; --mutate=F and --mutate=steps exit 1). Result accepted only by kc79_syscheck_1025.py (29dce7ea; selftest 0, controls
# refused, --mutate=F and --mutate=steps exit 1) with kc71_syscheck.py refusing it. 8 threads, Normal priority (the launcher), cap 21600 s by the exact pid; no retry. Two instances run at once (D 20.5 and D 20.75).
# usage: regrid79x.sh D TAG SRCSTATE_BLOB LAM0   (DRY=1: the pins, the source checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
D=$1; TAG=$2; SB=$3; LAM0=$4
[ -n "$D" ] && [ -n "$TAG" ] && [ -n "$SB" ] && [ -n "$LAM0" ] || { echo "usage: regrid79x.sh D TAG SRCSTATE_BLOB LAM0"; exit 2; }
F4=$(printf "%.4f" $D); F6=$(printf "%.6f" $D)
EX=$OUT/exits_regrid_D$F4.txt; SUM=$OUT/summary_regrid_D$F4.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79; WTM=D:/choptuik-i1025k79/solver/matter; DATA=$WT/solver/matter/data; WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_leap
SRC=l1kc71Lw1025c
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONFAULTHANDLER=1
refuse() { log "kc79 D $F4 regrid STOP: $*"; echo "kc79 D $F4 regrid STOP: $*" >> $SUM; echo "$*" > $OUT/regrid_refused_D$F4.txt; exit ${2:-1}; }
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "kc79 D $F4 regrid refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $OUT/inputs/kc71_syscheck.py 4cd86cd4 "kc71_syscheck.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $OUT/inputs/sol_${SRC}_D$F6.npy $SB "the pinned k_c 71 D $D state"
chk $OUT/inputs/${SRC}_leg3.jsonl b4f4bba7 "the pinned k_c 71 record file (leg 3's 12 records)"
chk $WT/solver/matter/ell_refine.py 631e5801 "ell_refine.py"
chk $WT/solver/matter/ell_delta.py fde699f5 "ell_delta.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "kc79 D $F4 regrid refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "kc79 D $F4 regrid refuse: solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $DATA/sol_${TAG}_D${F4}.npy $OUT/regrid_accepted_D$F4.txt $OUT/regrid_refused_D$F4.txt; do [ -e $f ] && { log "kc79 D $F4 regrid refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "kc79 D $F4 regrid pins checked (kc71 check 4cd86cd4, kc79 check 29dce7ea, source state $SB, record file b4f4bba7, ell_refine 631e5801, ell_delta fde699f5, worktree 48c36355 = solver code 505d8399)"
cd $OUT
RECS=$OUT/inputs/${SRC}_leg3.jsonl; STS=$OUT/inputs/sol_${SRC}_D$F6.npy
# ell_refine reads data/sol_SRC_D{D:.4f}.npy: the pinned state is copied there under that name (blob checked)
cp $STS $DATA/sol_${SRC}_D${F4}.npy
[ "$(git hash-object --no-filters $DATA/sol_${SRC}_D${F4}.npy)" = "$(git hash-object --no-filters $STS)" ] || refuse "the copied source state differs from its blob"
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > selftest_kc79_syscheck_D$F4.txt 2>&1; [ $? = 0 ] || refuse "kc79_syscheck_1025.py --selftest did not exit 0"
"$PY" -I inputs/kc71_syscheck.py $RECS $STS $D $WTM > source_kc71_syscheck_D$F4.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' source_kc71_syscheck_D$F4.txt >> $SUM
[ $s = 0 ] || refuse "kc71_syscheck.py does not accept the k_c 71 D $D source (exit $s)"
for m in F steps; do "$PY" -I inputs/kc71_syscheck.py $RECS $STS $D $WTM --mutate=$m > source_kc71_syscheck_D${F4}_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the source control --mutate=$m did not exit 1"; done
grep -F "\"D\": $D," $RECS | tail -n 1 > $OUT/rec_k71_D${F4}.jsonl
log "kc79 D $F4 regrid: the k_c 71 D $D source is accepted (record |F| and steps come back, both controls refused); record $(git hash-object --no-filters $OUT/rec_k71_D${F4}.jsonl | cut -c1-8)"
CMD="$PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD (8 threads, cap 21600 s)"; log "kc79 D $F4 regrid DRY run ended before the regrid"; exit 0; }
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/regrid_D$F4.log
s0=$(date +%s)
crun regrid79x_$F4 0 21600 ell_refine.py $CMD >> $OUT/regrid_D$F4.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/regrid_D$F4.log
echo "kc79 D $F4 regrid: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 21600 s")" >> $SUM; log "kc79 D $F4 regrid exit $rc wall $w s capped $CAPPED"
[ $rc = 0 ] || refuse "the regrid did not finish (exit $rc)"
[ -s $DATA/sol_${TAG}_D${F4}.npy ] && [ -s $DATA/${TAG}.jsonl ] || refuse "the regrid wrote no state or record"
cp $DATA/sol_${TAG}_D${F4}.npy $DATA/${TAG}.jsonl $OUT/
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $D $WTM > syscheck_D$F4.txt 2>&1; s=$?
grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' syscheck_D$F4.txt >> $SUM
[ $s = 0 ] || refuse "kc79_syscheck_1025.py does not accept the k_c 79 state (exit $s)"
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $D $WTM --mutate=$m > syscheck_D${F4}_mutate_$m.txt 2>&1; [ $? = 1 ] || refuse "the control --mutate=$m did not exit 1"; done
"$PY" -I inputs/kc71_syscheck.py $OUT/${TAG}.jsonl $OUT/sol_${TAG}_D${F4}.npy $D $WTM > syscheck_kc71_on_k79_result_D$F4.txt 2>&1; [ $? = 1 ] || refuse "kc71_syscheck.py did not refuse the k_c 79 result"
tail -n 1 $OUT/${TAG}.jsonl > $OUT/rec_k79_D${F4}.jsonl
# the summary line: python gets Windows paths (an MSYS path wrote an empty file once)
"$PY" -I -c "
import json
a = json.loads(open('$WOUT/rec_k71_D${F4}.jsonl').read().strip().splitlines()[-1]); b = json.loads(open('$WOUT/rec_k79_D${F4}.jsonl').read().strip().splitlines()[-1])
print('ACCEPTED: k_c 71 source D %s |F| %.4e steps %d constraint %.3e Delta %.12f | k_c 79 |F| %.4e steps %d constraint %.3e Delta %.12f (k_c 79 minus k_c 71 %.4e), regrid %s s' % (a['D'], a['F'], a['steps'], a['constraint'], a['Delta'], b['F'], b['steps'], b['constraint'], b['Delta'], b['Delta'] - a['Delta'], b.get('seconds')))
" > $OUT/regrid_accepted_D$F4.txt
[ -s $OUT/regrid_accepted_D$F4.txt ] || refuse "regrid_accepted_D$F4.txt is empty (the summary step failed)"
cat $OUT/regrid_accepted_D$F4.txt >> $SUM; log "kc79 D $F4 regrid ACCEPTED: $(cut -c1-220 $OUT/regrid_accepted_D$F4.txt)"
touch $OUT/regrid_D$F4.done
exit 0
