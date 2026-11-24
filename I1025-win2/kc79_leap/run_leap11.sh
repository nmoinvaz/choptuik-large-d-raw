#!/bin/bash
# #1025 kc79_leap on win2, CAP RESTART of the k_c 79 FAR SCOUT, queued (the coordinator's hc ~11:10 UTC 24 Nov: "a cap restart to D_end 22.5 is authorized the same way as before"; "restart it the same way as your 19:17 restart (from its
# last two states, a new tag, seeds re-checked by the syscheck, guard with --seeds, fresh 12 h cap by exact pid) ... h 0.03125, the same fold rule and watches"): WAITS for all10.done (the scout's end by its cap, 00:04:28 UTC 25 Nov), continues ONLY if
# summary_leap10.txt says it was capped ("capped at 43200 s") and its guard did not stop it (no leap10_STOP.txt); then a new ell_leap.py run from the last two records of tag l1kc79Lw1025i, tag l1kc79Lw1025j (own record file and
# states), D_end 22.5, h = the step the scout was using at its last point (the last record's h: 0.0625 unless a step had failed or the fold watch had halved it), reported in the log; seeds re-checked by kc79_syscheck_1025.py (selftest, accepts,
# --mutate=F and --mutate=steps exit 1); the guard (leap_guard.py --seeds = the two seeds' own records) and the samplers are started by launch_leap11_extras.ps1; 4 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid.
# usage: run_leap11.sh   (DRY=1: no waiting; the last two records now stand in for the seeds; checks and command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leap11.txt
SUM=$OUT/summary_leap11.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_leap
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAGS=l1kc79Lw1025i; TAGN=l1kc79Lw1025j
DEND=22.5
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leap11 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leap11 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leap11 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAGN}.jsonl $OUT/leap11.finished $OUT/leap11.log $OUT/all8.done $OUT/leap11_STOP.txt $OUT/leap11_points.txt $OUT/leap11_seedA.jsonl $OUT/leap11_seedB.jsonl; do [ -e $f ] && { log "leap11 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leap11 pins checked: ell_leap.py 1eb873e4, kc79_syscheck_1025.py 29dce7ea, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" != 1 ]; then
  log "leap11 waits for all10.done (the scout's end)"
  until [ -e $OUT/all10.done ]; do sleep 30; done
  [ -e $OUT/leap10_STOP.txt ] && { log "leap11: the scout's guard stopped it ($(head -n 1 $OUT/leap10_STOP.txt | cut -c1-200)): no restart"; exit 3; }
  grep -q 'capped at 43200 s' $OUT/summary_leap10.txt || { log "leap11: the scout did not end by its cap (see summary_leap10.txt): no restart"; exit 3; }
fi
read DA DB H <<< "$("$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k79/solver/matter/data/$TAGS.jsonl') if l.strip()]
print(repr(r[-2]['D']), repr(r[-1]['D']), repr(r[-1]['h']))" | tr -d '\r')"
[ -n "$DA" ] && [ -n "$DB" ] && [ -n "$H" ] || { log "leap11 STOP: could not read the last two records"; exit 1; }
SA=$(printf "sol_${TAGS}_D%.6f.npy" $DA); SB=$(printf "sol_${TAGS}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leap11 STOP: no $DATA/$f"; exit 1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leap11 STOP: $f differs from or is missing in states/"; exit 1; }; done
cmp -s $DATA/${TAGS}.jsonl $OUT/states/${TAGS}.jsonl || { log "leap11 STOP: the record file differs from states/"; exit 1; }
log "leap11 step h = $H (the last record h); seeds: D $DA ($SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8)) and D $DB ($SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)), record file blob $(git hash-object --no-filters $DATA/${TAGS}.jsonl | cut -c1-8) with $(grep -c . $DATA/${TAGS}.jsonl) records"
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > leap11_syscheck_selftest.txt 2>&1 || { log "leap11 STOP: kc79_syscheck_1025.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$(printf "sol_${TAGS}_D%.6f.npy" $d) $d $WTM > leap11_syscheck_D$d.txt 2>&1 || { log "leap11 STOP: kc79_syscheck_1025.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leap11_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leap11_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leap11 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leap11 seeds accepted by kc79_syscheck_1025.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAGN 1 79 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
"$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k79/solver/matter/data/$TAGS.jsonl') if l.strip()]
open('$WOUT/leap11_seedA.jsonl', 'w').write(json.dumps(r[-2]) + '\n'); open('$WOUT/leap11_seedB.jsonl', 'w').write(json.dumps(r[-1]) + '\n')"
[ -s $OUT/leap11_seedA.jsonl ] && [ -s $OUT/leap11_seedB.jsonl ] || { log "leap11 STOP: the seed record files were not written"; exit 1; }
mkdir -p $OUT/leap11 $OUT/states
powershell -NoProfile -File $WOUT/launch_leap11_extras.ps1 >> $OUT/leap11_extras.txt 2>&1
log "leap11 guard and samplers started (launch_leap11_extras.ps1)"
copier() {
  while [ ! -e $OUT/leap11.finished ]; do
    for f in $DATA/sol_${TAGN}_D*.npy $DATA/sol_${TAGN}_last.npy $DATA/sol_${TAGN}_prev.npy $DATA/${TAGN}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAGN}_D*.npy $DATA/sol_${TAGN}_last.npy $DATA/sol_${TAGN}_prev.npy $DATA/${TAGN}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap11.log
s0=$(date +%s)
crun leap11 0 43200 ell_leap.py $CMD >> $OUT/leap11.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap11.log
echo "leap11: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap11.log | tail -n 1)" >> $SUM; log "leap11 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap11.finished
wait $cp_pid
echo "kcl leap11 done" >> $SUM
touch $OUT/all8.done
exit 0
