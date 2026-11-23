#!/bin/bash
# #1025 kc79_leap on win2, RESTART of the k_c 79 leap (the coordinator's hc of 2026-11-23 ~19:20 UTC: "GO on the restart, same ruling as (b) at D 18.75: not a fold (n_null 72 -> 71 is a mode entering the regular set; tracked modes
# rose; |J+dF/dn| fell). Restart the k_c 79 leap at h 0.03125 from its D 20.84375 and D 20.875 states under new tag l1kc79Lw1025f, guard with --seeds = those two records, seeds re-checked by kc79_syscheck, old leap + guard killed by
# exact pid, fresh 12 h cap, D_end 21.5"): a new ell_leap.py run from the old leap's states at the two given D, new tag so nothing is overwritten:
#   ell_leap.py l1kc79Lw1025f 1 79 data/sol_l1kc79Lw1025d_D20.843750.npy 20.84375 data/sol_l1kc79Lw1025d_D20.875000.npy 20.875 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
# The old leap (tag l1kc79Lw1025d) and its guard are stopped BEFORE by hand (exact pids, command-line checks); this driver waits for the old driver's all5.done (states copied), refuses if the old guard had stopped the leap
# (leap5_STOP.txt), takes the two seeds from the old record file by D, re-checks them with kc79_syscheck_1025.py (selftest, accepts, --mutate=F and --mutate=steps exit 1), starts the guard (leap_guard.py --seeds, the same rule) and
# the samplers (launch_leap7_extras.ps1), then the leap: 4 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid.
# usage: run_leap7.sh DA DB   (DRY=1: no waiting; the checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leap7.txt
SUM=$OUT/summary_leap7.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_leap
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAGD=l1kc79Lw1025d; TAGF=l1kc79Lw1025f
DA=$1; DB=$2
H=0.03125; DEND=21.5
[ -n "$DA" ] && [ -n "$DB" ] || { echo "usage: run_leap7.sh DA DB"; exit 2; }
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leap7 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leap7 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leap7 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAGF}.jsonl $OUT/leap7.finished $OUT/leap7.log $OUT/all7.done $OUT/leap7_STOP.txt $OUT/leap7_points.txt $OUT/leap7_seedA.jsonl $OUT/leap7_seedB.jsonl; do [ -e $f ] && { log "leap7 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leap7 pins checked: ell_leap.py 1eb873e4, kc79_syscheck_1025.py 29dce7ea, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" != 1 ]; then
  log "leap7 waits for all5.done (the old leap's end)"
  t0=$(date +%s)
  until [ -e $OUT/all5.done ]; do [ $(( $(date +%s) - t0 )) -gt 1800 ] && { log "leap7 STOP: all5.done did not appear within 30 min (is the old leap still running?)"; exit 1; }; sleep 10; done
  [ -e $OUT/leap5_STOP.txt ] && { log "leap7: the old leap's guard stopped it ($(head -n 1 $OUT/leap5_STOP.txt | cut -c1-200)): no restart"; exit 3; }
fi
SA=$(printf "sol_${TAGD}_D%.6f.npy" $DA); SB=$(printf "sol_${TAGD}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leap7 STOP: no $DATA/$f"; exit 1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leap7 STOP: $f differs from or is missing in states/"; exit 1; }; done
cmp -s $DATA/${TAGD}.jsonl $OUT/states/${TAGD}.jsonl || { log "leap7 STOP: the record file differs from states/"; exit 1; }
log "leap7 seeds: D $DA ($SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8)) and D $DB ($SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)), record file blob $(git hash-object --no-filters $DATA/${TAGD}.jsonl | cut -c1-8) with $(grep -c . $DATA/${TAGD}.jsonl) records"
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > leap7_syscheck_selftest.txt 2>&1 || { log "leap7 STOP: kc79_syscheck_1025.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGD}.jsonl $DATA/$(printf "sol_${TAGD}_D%.6f.npy" $d) $d $WTM > leap7_syscheck_D$d.txt 2>&1 || { log "leap7 STOP: kc79_syscheck_1025.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leap7_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGD}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leap7_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leap7 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leap7 seeds accepted by kc79_syscheck_1025.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAGF 1 79 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
# the guard's previous points: the seeds' own records (they carry n_null and cos_t_reg)
"$PY" -I -c "
import json
r = {round(x['D'], 6): x for x in (json.loads(l) for l in open('D:/choptuik-i1025k79/solver/matter/data/$TAGD.jsonl') if l.strip())}
open('$WOUT/leap7_seedA.jsonl', 'w').write(json.dumps(r[round($DA, 6)]) + '\n'); open('$WOUT/leap7_seedB.jsonl', 'w').write(json.dumps(r[round($DB, 6)]) + '\n')"
[ -s $OUT/leap7_seedA.jsonl ] && [ -s $OUT/leap7_seedB.jsonl ] || { log "leap7 STOP: the seed record files were not written"; exit 1; }
mkdir -p $OUT/leap7 $OUT/states
powershell -NoProfile -File $WOUT/launch_leap7_extras.ps1 >> $OUT/leap7_extras.txt 2>&1
log "leap7 guard and samplers started (launch_leap7_extras.ps1)"
copier() {
  while [ ! -e $OUT/leap7.finished ]; do
    for f in $DATA/sol_${TAGF}_D*.npy $DATA/sol_${TAGF}_last.npy $DATA/sol_${TAGF}_prev.npy $DATA/${TAGF}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAGF}_D*.npy $DATA/sol_${TAGF}_last.npy $DATA/sol_${TAGF}_prev.npy $DATA/${TAGF}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap7.log
s0=$(date +%s)
crun leap7 0 43200 ell_leap.py $CMD >> $OUT/leap7.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap7.log
echo "leap7: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap7.log | tail -n 1)" >> $SUM; log "leap7 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap7.finished
wait $cp_pid
echo "kcl leap7 done" >> $SUM
touch $OUT/all7.done
exit 0
