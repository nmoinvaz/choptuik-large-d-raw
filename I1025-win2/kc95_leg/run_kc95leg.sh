#!/bin/bash
# #1025 kc95_leg on win2 (the coordinator's hc of 2026-11-25 ~20:05 UTC): "continue a k_c 95 leg in D from your two accepted k_c 95 states (D 22.875 and D 23.0) with ell_leap, the same command and guard as macm3's part c2 (raw I1025-macm3/kc87_leg2: run_leg2cont.sh
# and its README; ell_leap blob 5816d7b3, guard f1fe7c7c) but at k_c 95, h 0.0625, to D 23.25, --cmax 2e-2, rows above 1e-2 flagged reduced quality, 8 threads. [...] If ell_leap or the guard refuses at k_c 95, stop and report."
# The leap (macm3's command with kc 95): ell_leap.py l1kc95Lw1025m 1 95 data/<seed A> 22.875 data/<seed B> 23.0 23.25 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold, in the worktree D:/choptuik-i1025k95leg (detached at edf49057 = wip/ell1-highD, as macm3's parts b2, c and c2;
# ell_leap.py blob 5816d7b3; dss_ell, ell_ddm, ell_dd and ddnp equal 505d8399's), 8 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid. The seeds (my accepted k_c 95 states, blobs a14f0d50 and 096f1cc0, records 5381f89d and e3fff23f) are re-checked by
# kc95_syscheck_1025.py (selftest 0; accepts; --mutate=F and --mutate=steps exit 1; the k_c 87 check refuses them). The guard (leap_guard.py f1fe7c7c, --seeds = the two seeds' records) and the samplers start with the leap (launch_leg_extras.ps1).
# usage: run_kc95leg.sh   (DRY=1: the pins, the selftests, the seed checks and the command only; starts nothing)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc95_leg   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leg.txt
SUM=$OUT/summary_leg.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc95_leg
IN=$OUT/inputs; WIN=$WOUT/inputs
WT=/d/choptuik-i1025k95leg
WTM=D:/choptuik-i1025k95leg/solver/matter
DATA=$WT/solver/matter/data
TAG=l1kc95Lw1025m
SA=sol_l1kc95win2d22875_D22.8750.npy; SB=sol_l1kc95win2d23_D23.0000.npy; DA=22.875; DB=23.0; H=0.0625; DEND=23.25
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 RAYON_NUM_THREADS=8 PYTHONFAULTHANDLER=1 PYTHONDONTWRITEBYTECODE=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leg95 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 5816d7b3 "ell_leap.py"
chk $IN/leap_guard.py f1fe7c7c "leap_guard.py"
chk $KC/leap_guard.py f1fe7c7c "the launcher folder's leap_guard.py"
chk $IN/kc95_syscheck_1025.py d487e628 "kc95_syscheck_1025.py"
chk $IN/kc87_syscheck_1025.py 6df5d960 "kc87_syscheck_1025.py"
chk $IN/$SA a14f0d50 "seed A (k_c 95 D 22.875)"
chk $IN/$SB 096f1cc0 "seed B (k_c 95 D 23.0)"
chk $IN/rec_k95_D22.8750.jsonl 5381f89d "seed A's record"
chk $IN/rec_k95_D23.0000.jsonl e3fff23f "seed B's record"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = edf49057 ] || { log "leg95 refuse: the worktree is not at edf49057"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 HEAD -- solver/matter/$f.py || { log "leg95 refuse: $f.py differs from 505d8399"; bad=1; }; done
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || { log "leg95 refuse: the worktree's solver/ has changes"; bad=1; }
for f in $DATA/${TAG}.jsonl $OUT/leg.finished $OUT/leg.log $OUT/allleg.done $OUT/leg_STOP.txt $OUT/leg_points.txt $OUT/leg_seedA.jsonl $OUT/leg_seedB.jsonl; do [ -e $f ] && { log "leg95 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leg95 pins checked: ell_leap.py 5816d7b3, leap_guard.py f1fe7c7c, kc95/kc87 checks d487e628/6df5d960, seeds a14f0d50 + 096f1cc0 and their records, worktree edf49057 with solver code = 505d8399"
cd $OUT
"$PY" -I $IN/kc95_syscheck_1025.py --selftest > leg_selftest_kc95.txt 2>&1 || { log "leg95 STOP: kc95_syscheck_1025.py --selftest did not exit 0"; exit 1; }
"$PY" -I $IN/kc87_syscheck_1025.py --selftest > leg_selftest_kc87.txt 2>&1 || { log "leg95 STOP: kc87_syscheck_1025.py --selftest did not exit 0"; exit 1; }
"$PY" -I $IN/leap_guard.py --selftest > leg_selftest_guard.txt 2>&1; g0=$?
g1=0; for m in slope cos nnull; do "$PY" -I $IN/leap_guard.py --selftest --mutate=$m > leg_selftest_guard_mut_$m.txt 2>&1; [ $? = 1 ] || g1=1; done
[ $g0 = 0 ] && [ $g1 = 0 ] || { log "leg95 STOP: the guard's selftest ($g0, 0 wanted) or one of its mutations (all must exit 1: $g1) did not read as written"; exit 1; }
seedcheck() {  # D RECORD STATE TAGNAME
  "$PY" -I $IN/kc95_syscheck_1025.py $2 $3 $1 $WTM > leg_syscheck_$4.txt 2>&1 || { log "leg95 STOP: kc95_syscheck_1025.py does not accept the $4 seed (D $1)"; return 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leg_syscheck_$4.txt >> $SUM
  for m in F steps; do "$PY" -I $IN/kc95_syscheck_1025.py $2 $3 $1 $WTM --mutate=$m > leg_syscheck_$4_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leg95 STOP: the control --mutate=$m did not exit 1 on the $4 seed"; return 1; }; done
  "$PY" -I $IN/kc87_syscheck_1025.py $2 $3 $1 $WTM > leg_kc87_on_$4.txt 2>&1; [ $? = 1 ] || { log "leg95 STOP: the kc87 check did not refuse the $4 seed"; return 1; }
  return 0
}
seedcheck $DA $WIN/rec_k95_D22.8750.jsonl $WIN/$SA seedA || exit 1
seedcheck $DB $WIN/rec_k95_D23.0000.jsonl $WIN/$SB seedB || exit 1
log "leg95 seeds accepted by kc95_syscheck_1025.py (D $DA and D $DB; selftests 0; --mutate=F and --mutate=steps exit 1; the k_c 87 check refuses both); guard selftest 0 and its three mutations exit 1"
CMD="$PY -u ell_leap.py $TAG 1 95 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; log "leg95 DRY run ended: $CMD"; exit 0; fi
mkdir -p $DATA $OUT/states $OUT/leg
cp $IN/$SA $DATA/$SA; cp $IN/$SB $DATA/$SB
[ "$(git hash-object --no-filters $DATA/$SA | cut -c1-8)" = a14f0d50 ] && [ "$(git hash-object --no-filters $DATA/$SB | cut -c1-8)" = 096f1cc0 ] || { log "leg95 STOP: a copied seed state differs from its blob"; exit 1; }
cp $IN/rec_k95_D22.8750.jsonl $OUT/leg_seedA.jsonl; cp $IN/rec_k95_D23.0000.jsonl $OUT/leg_seedB.jsonl
powershell -NoProfile -File $WOUT/launch_leg_extras.ps1 >> $OUT/leg_extras.txt 2>&1
log "leg95 guard and samplers started (launch_leg_extras.ps1)"
copier() {
  while [ ! -e $OUT/leg.finished ]; do
    for f in $DATA/sol_${TAG}_D*.npy $DATA/sol_${TAG}_last.npy $DATA/sol_${TAG}_prev.npy $DATA/${TAG}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAG}_D*.npy $DATA/sol_${TAG}_last.npy $DATA/sol_${TAG}_prev.npy $DATA/${TAG}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 8 threads)"; } > $OUT/leg.log
s0=$(date +%s)
crun leg95 0 43200 ell_leap.py $CMD >> $OUT/leg.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leg.log
echo "leg95: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leg.log | tail -n 1)" >> $SUM; log "leg95 exit $rc wall $w s capped $CAPPED"
touch $OUT/leg.finished
wait $cp_pid
echo "kcl leg95 done" >> $SUM
touch $OUT/allleg.done
exit 0
