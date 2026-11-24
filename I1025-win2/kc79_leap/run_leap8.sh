#!/bin/bash
# #1025 kc79_leap on win2, SECOND RESTART of the k_c 79 leap, queued (the coordinator's hc ~04:40 UTC 24 Nov: "when each ends by its cap, restart it the same way as your 19:17 restart (from its last two states, a new tag, seeds
# re-checked by the syscheck, guard with --seeds, fresh 12 h cap by exact pid): k_c 79 to D_end 21.5 ... h 0.03125, the same fold rule and watches. Record each restart in the README."):
# WAITS for all7.done (the restarted leap's end by its cap, 07:17:20 UTC), continues ONLY if its summary says it was capped (summary_leap7.txt: "capped at 43200 s") and its guard did not stop it (no leap7_STOP.txt); then a new ell_leap.py
# run from the last two records of tag l1kc79Lw1025f, tag l1kc79Lw1025g (own record file and states, nothing overwritten):
#   ell_leap.py l1kc79Lw1025g 1 79 data/sol_l1kc79Lw1025f_D<A>.npy A data/sol_l1kc79Lw1025f_D<B>.npy B 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
# The seeds are re-checked by kc79_syscheck_1025.py (selftest, accepts, --mutate=F and --mutate=steps exit 1); the guard (leap_guard.py --seeds = the two seeds' own records) and the samplers are started by launch_leap8_extras.ps1;
# 4 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid. usage: run_leap8.sh   (DRY=1: no waiting; the last two records now stand in for the seeds; checks and command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leap8.txt
SUM=$OUT/summary_leap8.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_leap
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAGS=l1kc79Lw1025f; TAGN=l1kc79Lw1025g
H=0.03125; DEND=21.5
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leap8 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leap8 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leap8 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAGN}.jsonl $OUT/leap8.finished $OUT/leap8.log $OUT/all8.done $OUT/leap8_STOP.txt $OUT/leap8_points.txt $OUT/leap8_seedA.jsonl $OUT/leap8_seedB.jsonl; do [ -e $f ] && { log "leap8 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leap8 pins checked: ell_leap.py 1eb873e4, kc79_syscheck_1025.py 29dce7ea, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" != 1 ]; then
  log "leap8 waits for all7.done (the restarted leap's end)"
  until [ -e $OUT/all7.done ]; do sleep 30; done
  [ -e $OUT/leap7_STOP.txt ] && { log "leap8: the leap's guard stopped it ($(head -n 1 $OUT/leap7_STOP.txt | cut -c1-200)): no restart"; exit 3; }
  grep -q 'capped at 43200 s' $OUT/summary_leap7.txt || { log "leap8: the restarted leap did not end by its cap (see summary_leap7.txt): no restart"; exit 3; }
fi
read DA DB <<< "$("$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k79/solver/matter/data/$TAGS.jsonl') if l.strip()]
print(repr(r[-2]['D']), repr(r[-1]['D']))" | tr -d '\r')"
[ -n "$DA" ] && [ -n "$DB" ] || { log "leap8 STOP: could not read the last two records"; exit 1; }
SA=$(printf "sol_${TAGS}_D%.6f.npy" $DA); SB=$(printf "sol_${TAGS}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leap8 STOP: no $DATA/$f"; exit 1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leap8 STOP: $f differs from or is missing in states/"; exit 1; }; done
cmp -s $DATA/${TAGS}.jsonl $OUT/states/${TAGS}.jsonl || { log "leap8 STOP: the record file differs from states/"; exit 1; }
log "leap8 seeds: D $DA ($SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8)) and D $DB ($SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)), record file blob $(git hash-object --no-filters $DATA/${TAGS}.jsonl | cut -c1-8) with $(grep -c . $DATA/${TAGS}.jsonl) records"
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > leap8_syscheck_selftest.txt 2>&1 || { log "leap8 STOP: kc79_syscheck_1025.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$(printf "sol_${TAGS}_D%.6f.npy" $d) $d $WTM > leap8_syscheck_D$d.txt 2>&1 || { log "leap8 STOP: kc79_syscheck_1025.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leap8_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leap8_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leap8 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leap8 seeds accepted by kc79_syscheck_1025.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAGN 1 79 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
"$PY" -I -c "
import json
r = [json.loads(l) for l in open('D:/choptuik-i1025k79/solver/matter/data/$TAGS.jsonl') if l.strip()]
open('$WOUT/leap8_seedA.jsonl', 'w').write(json.dumps(r[-2]) + '\n'); open('$WOUT/leap8_seedB.jsonl', 'w').write(json.dumps(r[-1]) + '\n')"
[ -s $OUT/leap8_seedA.jsonl ] && [ -s $OUT/leap8_seedB.jsonl ] || { log "leap8 STOP: the seed record files were not written"; exit 1; }
mkdir -p $OUT/leap8 $OUT/states
powershell -NoProfile -File $WOUT/launch_leap8_extras.ps1 >> $OUT/leap8_extras.txt 2>&1
log "leap8 guard and samplers started (launch_leap8_extras.ps1)"
copier() {
  while [ ! -e $OUT/leap8.finished ]; do
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
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap8.log
s0=$(date +%s)
crun leap8 0 43200 ell_leap.py $CMD >> $OUT/leap8.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap8.log
echo "leap8: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap8.log | tail -n 1)" >> $SUM; log "leap8 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap8.finished
wait $cp_pid
echo "kcl leap8 done" >> $SUM
touch $OUT/all8.done
exit 0
