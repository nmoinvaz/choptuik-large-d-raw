#!/bin/bash
# #1025 kc71_leap on win2, LEG 6 = the continuation of leg 4 (the coordinator's hc of 2026-11-23 ~17:50 UTC): "when [leg 4] reports 'reached D 21.0', continue the same leg (k_c 71, same guard and fold rules, h 0.03125,
# a new log/tag suffix so nothing is overwritten) from its D 21 state to D_end 21.5, as the scout ahead of the k_c 79 leg; report each point as now."
# WAITS for all4.done (leg 4 ended and its states are copied), continues only if leap4.log holds "reached D 21.0" and leg 4's guard did not stop it; then the leap, from leg 4's last two states (D 20.96875 and D 21.0):
#   ell_leap.py l1kc71Lw1025e 1 71 data/sol_l1kc71Lw1025c_D20.968750.npy 20.96875 data/sol_l1kc71Lw1025c_D21.000000.npy 21.0 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
# (tag l1kc71Lw1025e: its own record file and states; the seeds are tag c's), 4 BLAS threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid. Seeds re-checked by kc71_syscheck.py (selftest, accepts, --mutate=F and
# --mutate=steps exit 1). The guard (leap_guard.py --seeds, the same rule as leg 4's) and the alert-only samplers are started by this driver outside the terminal (launch_leg6_extras.ps1).
# usage: run_leap6.sh   (DRY=1: no waiting; the last two records now stand in for the seeds; the checks and the command only, nothing started or written but the check outputs)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
EX=$OUT/exits_kcl6.txt
SUM=$OUT/summary_kcl6.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
DATA=$WT/solver/matter/data
TAGC=l1kc71Lw1025c; TAGE=l1kc71Lw1025e
H=0.03125; DEND=21.5
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leg6 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/kc71_syscheck.py 4cd86cd4 "kc71_syscheck.py"
chk $OUT/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leg6 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leg6 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAGE}.jsonl $OUT/leap6.finished $OUT/leap6.log $OUT/all6.done $OUT/leg6_STOP.txt $OUT/leg6_points.txt $OUT/leg6_seedA.jsonl $OUT/leg6_seedB.jsonl; do [ -e $f ] && { log "leg6 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leg6 pins checked: ell_leap.py 1eb873e4, kc71_syscheck.py 4cd86cd4, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" != 1 ]; then
  log "leg6 waits for all4.done (leg 4's end)"
  until [ -e $OUT/all4.done ]; do sleep 30; done
  [ -e $OUT/leg4_STOP.txt ] && { log "leg6: leg 4's guard stopped it ($(head -n 1 $OUT/leg4_STOP.txt | cut -c1-200)): no continuation"; exit 3; }
  grep -q '^reached D 21.0$' $OUT/leap4.log || { log "leg6: leap4.log does not hold 'reached D 21.0' (see summary_kcl4.txt): no continuation"; exit 3; }
fi
# the seeds: the last two records of leg 4's record file
read DA DB <<< "$("$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k71/solver/matter/data/$TAGC.jsonl') if l.strip()]
print(repr(r[-2]['D']), repr(r[-1]['D']))" | tr -d '\r')"
[ -n "$DA" ] && [ -n "$DB" ] || { log "leg6 STOP: could not read the last two records"; exit 1; }
[ "$DRY" = 1 ] || [ "$DB" = 21.0 ] || { log "leg6 STOP: the last record is D $DB, not 21.0"; exit 1; }
SA=$(printf "sol_${TAGC}_D%.6f.npy" $DA); SB=$(printf "sol_${TAGC}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leg6 STOP: no $DATA/$f"; exit 1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leg6 STOP: $f differs from or is missing in states/"; exit 1; }; done
cmp -s $DATA/${TAGC}.jsonl $OUT/states/${TAGC}.jsonl || { log "leg6 STOP: the record file differs from states/"; exit 1; }
log "leg6 seeds: D $DA ($SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8)) and D $DB ($SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)), record file blob $(git hash-object --no-filters $DATA/${TAGC}.jsonl | cut -c1-8) with $(grep -c . $DATA/${TAGC}.jsonl) records"
cd $OUT
"$PY" -I kc71_syscheck.py --selftest > leg6_syscheck_selftest.txt 2>&1 || { log "leg6 STOP: kc71_syscheck.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I kc71_syscheck.py $DATA/${TAGC}.jsonl $DATA/$(printf "sol_${TAGC}_D%.6f.npy" $d) $d $WTM > leg6_syscheck_D$d.txt 2>&1 || { log "leg6 STOP: kc71_syscheck.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leg6_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I kc71_syscheck.py $DATA/${TAGC}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leg6_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leg6 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leg6 seeds accepted by kc71_syscheck.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAGE 1 71 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
# the guard's previous points: the seeds' own records (they carry n_null and cos_t_reg)
"$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k71/solver/matter/data/$TAGC.jsonl') if l.strip()]
open('$WOUT/leg6_seedA.jsonl', 'w').write(json.dumps(r[-2]) + '\n'); open('$WOUT/leg6_seedB.jsonl', 'w').write(json.dumps(r[-1]) + '\n')"
[ -s $OUT/leg6_seedA.jsonl ] && [ -s $OUT/leg6_seedB.jsonl ] || { log "leg6 STOP: the seed record files were not written"; exit 1; }
mkdir -p $OUT/leg6
powershell -NoProfile -File $WOUT/launch_leg6_extras.ps1 >> $OUT/leg6_extras.txt 2>&1
log "leg6 guard and samplers started (launch_leg6_extras.ps1)"
copier() {
  while [ ! -e $OUT/leap6.finished ]; do
    for f in $DATA/sol_${TAGE}_D*.npy $DATA/sol_${TAGE}_last.npy $DATA/sol_${TAGE}_prev.npy $DATA/${TAGE}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAGE}_D*.npy $DATA/sol_${TAGE}_last.npy $DATA/sol_${TAGE}_prev.npy $DATA/${TAGE}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap6.log
s0=$(date +%s)
crun leap6 0 43200 ell_leap.py $CMD >> $OUT/leap6.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap6.log
echo "leap6: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap6.log | tail -n 1)" >> $SUM; log "leg6 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap6.finished
wait $cp_pid
echo "kcl leap6 done" >> $SUM
touch $OUT/all6.done
exit 0
