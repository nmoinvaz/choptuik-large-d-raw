#!/bin/bash
# #1025 kc79_leap on win2, step (2) (the coordinator's hc of 2026-11-23 ~12:20 UTC): "a k_c 79 leap leg from those two states, run_leap4.sh's pattern with k_c 79, tag l1kc79Lw1025d, h 0.03125, the same guard and stop rules, 12 h cap":
# ell_leap.py l1kc79Lw1025d 1 79 data/sol_l1kc79win2d205_D20.5000.npy 20.5 data/sol_l1kc79win2d2075_D20.7500.npy 20.75 21 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold, 4 BLAS threads, BelowNormal (the caller sets it),
# a cap of 43200 s (12 h) by the exact root pid. It WAITS for the acceptance of both k_c 79 regrids (regrid_accepted_D20.5000.txt and regrid_accepted_D20.7500.txt non-empty; a refusal ends it), then re-checks both seeds with
# kc79_syscheck_1025.py. The leap writes data/l1kc79Lw1025d.jsonl and sol_l1kc79Lw1025d_D*.npy in the k_c 79 worktree, copied into states/ by a copier loop. The guard (leap_guard.py with --seeds) is started beside by the launcher.
# usage: run_leap5.sh   (DRY=1: the pins and the command, without waiting)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leap5.txt
SUM=$OUT/summary_leap5.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAG=l1kc79Lw1025d
TA=l1kc79win2d205; TB=l1kc79win2d2075
DA=20.5; DB=20.75; H=0.03125
SA=sol_${TA}_D20.5000.npy; SB=sol_${TB}_D20.7500.npy
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leap5 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leap5 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leap5 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAG}.jsonl $OUT/leap5.finished $OUT/leap5.log $OUT/all5.done $OUT/leap5_STOP.txt; do [ -e $f ] && { log "leap5 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
CMD="$PY -u ell_leap.py $TAG 1 79 data/$SA $DA data/$SB $DB 21 $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
log "leap5 pins checked: ell_leap.py 1eb873e4, kc79_syscheck_1025.py 29dce7ea, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
log "leap5 waits for regrid_accepted_D20.5000.txt and regrid_accepted_D20.7500.txt"
until [ -s $OUT/regrid_accepted_D20.5000.txt ] && [ -s $OUT/regrid_accepted_D20.7500.txt ]; do
  for d in 20.5000 20.7500; do [ -e $OUT/regrid_refused_D$d.txt ] && { log "leap5: the D $d regrid was refused: no leap"; exit 3; }; done
  sleep 30
done
log "leap5: both regrids are accepted"
# the seeds in the worktree's data are the accepted states, byte for byte
for p in "$TA 20.5000" "$TB 20.7500"; do
  set -- $p; f=sol_$1_D$2.npy
  [ -s $DATA/$f ] && cmp -s $DATA/$f $OUT/$f || { log "leap5 STOP: $f in the worktree differs from or is missing in $OUT"; exit 1; }
  [ -s $OUT/rec_k79_D$2.jsonl ] || { log "leap5 STOP: no rec_k79_D$2.jsonl"; exit 1; }
done
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > leap5_syscheck_selftest.txt 2>&1 || { log "leap5 STOP: kc79_syscheck_1025.py --selftest did not exit 0"; exit 1; }
for p in "$TA 20.5 20.5000" "$TB 20.75 20.7500"; do
  set -- $p
  "$PY" -I inputs/kc79_syscheck_1025.py $OUT/$1.jsonl $OUT/sol_$1_D$3.npy $2 $WTM > leap5_syscheck_D$3.txt 2>&1 || { log "leap5 STOP: kc79_syscheck_1025.py does not accept the D $2 seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leap5_syscheck_D$3.txt >> $SUM
done
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $OUT/$TB.jsonl $OUT/sol_${TB}_D20.7500.npy 20.75 $WTM --mutate=$m > leap5_syscheck_D20.7500_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leap5 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leap5 seeds accepted by kc79_syscheck_1025.py (D 20.5 blob $(git hash-object --no-filters $OUT/$SA | cut -c1-8), D 20.75 blob $(git hash-object --no-filters $OUT/$SB | cut -c1-8); selftest 0; --mutate=F and --mutate=steps exit 1)"
mkdir -p $OUT/states
copier() {
  while [ ! -e $OUT/leap5.finished ]; do
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
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap5.log
s0=$(date +%s)
crun leap5 0 43200 ell_leap.py $CMD >> $OUT/leap5.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap5.log
echo "leap5: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap5.log | tail -n 1)" >> $SUM; log "leap5 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap5.finished
wait $cp_pid
echo "kcl leap5 done" >> $SUM
touch $OUT/all5.done
exit 0
