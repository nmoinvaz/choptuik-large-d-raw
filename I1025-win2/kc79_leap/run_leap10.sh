#!/bin/bash
# #1025 kc79_leap on win2, the k_c 79 FAR SCOUT (the coordinator's hc of 2026-11-24 ~11:10 UTC): "let leg 9 end where it stops (D 21.484375 by its retry), no raised bar, no restart. With its freed threads (4), start a k_c 79 FAR SCOUT
# ahead of the tag g leap: tag l1kc79Lw1025i, seeds the tag g records D 21.1875 and D 21.21875 (re-checked by kc79_syscheck, controls exit 1), ell_leap.py l1kc79Lw1025i 1 79 <D 21.1875 state> 21.1875 <D 21.21875 state> 21.21875 22.5
# 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold (h 0.0625; the leap halves to 0.03125 if a step fails), the guard with --seeds, the same fold rule, tracked-mode and branch-watch reporting, 12 h cap by exact pid; a cap restart
# to D_end 22.5 is authorized the same way as before. Report each point with your columns, and say the seconds per point at h 0.0625 against 0.03125. The tag g leap continues to D 21.5 unchanged."
# WAITS for all9.done (leg 9's end, whatever its reason: its 4 threads are the scout's), then: seeds = the tag g records at D 21.1875 and D 21.21875 (states in the k_c 79 worktree, byte-compared with the raw copies; the two seed
# RECORDS compared between the worktree's record file and the raw copy, since the tag g leap keeps appending), kc79_syscheck_1025.py (selftest, accepts, --mutate=F and --mutate=steps exit 1), the guard (leap_guard.py --seeds =
# the two seed records, which carry n_null and cos_t_reg) and the samplers (launch_leap10_extras.ps1), then the leap: 4 threads, BelowNormal (the caller sets it), cap 43200 s by the exact root pid.
# usage: run_leap10.sh   (DRY=1: no waiting; the pins, the seed checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
KC=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $KC/lib_kcl.sh
OUT=/d/choptuik-i935-raw/I1025-win2/kc79_leap   # lib_kcl.sh sets OUT to the leap folder
EX=$OUT/exits_leap10.txt
SUM=$OUT/summary_leap10.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc79_leap
WT=/d/choptuik-i1025k79
WTM=D:/choptuik-i1025k79/solver/matter
DATA=$WT/solver/matter/data
TAGS=l1kc79Lw1025g; TAGN=l1kc79Lw1025i
DA=21.1875; DB=21.21875; H=0.0625; DEND=22.5
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leap10 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/inputs/kc79_syscheck_1025.py 29dce7ea "kc79_syscheck_1025.py"
chk $KC/leap_guard.py f1fe7c7c "leap_guard.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leap10 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leap10 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $DATA/${TAGN}.jsonl $OUT/leap10.finished $OUT/leap10.log $OUT/all10.done $OUT/leap10_STOP.txt $OUT/leap10_points.txt $OUT/leap10_seedA.jsonl $OUT/leap10_seedB.jsonl; do [ -e $f ] && { log "leap10 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leap10 pins checked: ell_leap.py 1eb873e4, kc79_syscheck_1025.py 29dce7ea, leap_guard.py f1fe7c7c, worktree 48c36355 with solver code = 505d8399"
if [ "$DRY" != 1 ]; then
  log "leap10 waits for all9.done (leg 9's end)"
  until [ -e $KC/all9.done ]; do sleep 30; done
  log "leap10: leg 9 has ended ($(grep -E '^(stop at|reached)' $KC/leap9.log | tail -n 1 | cut -c1-160))"
fi
SA=$(printf "sol_${TAGS}_D%.6f.npy" $DA); SB=$(printf "sol_${TAGS}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leap10 STOP: no $DATA/$f"; exit 1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leap10 STOP: $f differs from or is missing in states/"; exit 1; }; done
# the seed records, by D, equal in the worktree's record file and the raw copy; written for the guard
"$PY" -I -c "
import json, sys
def rec(path, D):
    r = [json.loads(l) for l in open(path) if l.strip()]
    m = [x for x in r if abs(x['D'] - D) < 1e-9]
    assert len(m) == 1, (path, D, len(m))
    return m[0]
w = 'D:/choptuik-i1025k79/solver/matter/data/$TAGS.jsonl'; c = '$WOUT/states/$TAGS.jsonl'
a, b = rec(w, $DA), rec(w, $DB)
assert a == rec(c, $DA) and b == rec(c, $DB), 'the seed records differ between the worktree and the raw copy'
if '$DRY' != '1':
    open('$WOUT/leap10_seedA.jsonl', 'w').write(json.dumps(a) + '\n'); open('$WOUT/leap10_seedB.jsonl', 'w').write(json.dumps(b) + '\n')
print('seed records equal: D', a['D'], 'F', a['F'], 'steps', a['steps'], '| D', b['D'], 'F', b['F'], 'steps', b['steps'])" > $OUT/leap10_seedcheck.txt 2>&1 || { log "leap10 STOP: the seed records differ or are missing: $(tail -n 1 $OUT/leap10_seedcheck.txt | cut -c1-200)"; exit 1; }
log "leap10 seeds: D $DA ($SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8)) and D $DB ($SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)); $(cat $OUT/leap10_seedcheck.txt | cut -c1-200)"
cd $OUT
"$PY" -I inputs/kc79_syscheck_1025.py --selftest > leap10_syscheck_selftest.txt 2>&1 || { log "leap10 STOP: kc79_syscheck_1025.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$(printf "sol_${TAGS}_D%.6f.npy" $d) $d $WTM > leap10_syscheck_D$d.txt 2>&1 || { log "leap10 STOP: kc79_syscheck_1025.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leap10_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I inputs/kc79_syscheck_1025.py $DATA/${TAGS}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leap10_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leap10 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leap10 seeds accepted by kc79_syscheck_1025.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAGN 1 79 data/$SA $DA data/$SB $DB $DEND $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
[ -s $OUT/leap10_seedA.jsonl ] && [ -s $OUT/leap10_seedB.jsonl ] || { log "leap10 STOP: the seed record files were not written"; exit 1; }
mkdir -p $OUT/leap10 $OUT/states
powershell -NoProfile -File $WOUT/launch_leap10_extras.ps1 >> $OUT/leap10_extras.txt 2>&1
log "leap10 guard and samplers started (launch_leap10_extras.ps1)"
copier() {
  while [ ! -e $OUT/leap10.finished ]; do
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
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap10.log
s0=$(date +%s)
crun leap10 0 43200 ell_leap.py $CMD >> $OUT/leap10.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap10.log
echo "leap10: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap10.log | tail -n 1)" >> $SUM; log "leap10 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap10.finished
wait $cp_pid
echo "kcl leap10 done" >> $SUM
touch $OUT/all10.done
exit 0
