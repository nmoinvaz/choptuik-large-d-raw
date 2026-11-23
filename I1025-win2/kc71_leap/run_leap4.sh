#!/bin/bash
# #1025 kc71_leap on win2, FOURTH LEG (the coordinator's hc of 2026-11-23 ~12:00 UTC: "Start leg 4 now, beside the k_c 87 scan: from D 20.75 with h 0.03125 (the watch's), same flags and tag l1kc71Lw1025c (states as before),
# 12 h cap, headless launcher"): a new ell_leap.py run from leg 3's last two states (D 20.6875 and D 20.75), same flags (--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold), h 0.03125, to D_end 21, 4 BLAS threads, BelowNormal
# (the caller sets it), a cap of 43200 s (12 h) by the exact root pid. The tag is leg 3's: data/l1kc71Lw1025c.jsonl is appended to (leg 4's records follow leg 3's 12) and the states sol_l1kc71Lw1025c_D*.npy continue; the copier
# loop copies them into states/. Stop rules (leg4_guard.py, started beside): dDelta/dD changes sign, or sigma_reg < 1e-12. usage: run_leap4.sh DA DB H   (DRY=1: the pin checks, the seed checks and the command only)
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
EX=$OUT/exits_kcl4.txt
SUM=$OUT/summary_kcl4.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
DATA=$WT/solver/matter/data
TAG2=l1kc71Lw1025c
DA=$1; DB=$2; H=$3
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leg4 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
[ -n "$DA" ] && [ -n "$DB" ] && [ -n "$H" ] || { echo "usage: run_leap4.sh DA DB H"; exit 2; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
chk $OUT/kc71_syscheck.py 4cd86cd4 "kc71_syscheck.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leg4 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leg4 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
SA=$(printf "sol_${TAG2}_D%.6f.npy" $DA); SB=$(printf "sol_${TAG2}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leg4 refuse: no $DATA/$f"; bad=1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leg4 refuse: $f differs from or is missing in states/"; bad=1; }; done
chk $DATA/$SA cebac442 "the D 20.6875 seed"
chk $DATA/$SB fe8503cc "the D 20.75 seed"
cmp -s $DATA/${TAG2}.jsonl $OUT/states/${TAG2}.jsonl || { log "leg4 refuse: the record file differs from states/"; bad=1; }
chk $DATA/${TAG2}.jsonl b4f4bba7 "the record file (leg 3's 12 records)"
N0=$(grep -c . $DATA/${TAG2}.jsonl)
[ "$N0" = 12 ] || { log "leg4 refuse: the record file has $N0 records, not 12"; bad=1; }
tail -n 1 $DATA/${TAG2}.jsonl | grep -q "\"D\": $DB," || { log "leg4 refuse: the last record is not D $DB"; bad=1; }
for f in $OUT/leap4.finished $OUT/leap4.log $OUT/all4.done $OUT/leg4_STOP.txt; do [ -e $f ] && { log "leg4 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
log "leg4 pins checked: ell_leap.py 1eb873e4, kc71_syscheck.py 4cd86cd4, leg4_guard.py $(git hash-object --no-filters $OUT/leg4_guard.py | cut -c1-8), worktree 48c36355 with solver code = 505d8399, seeds $SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8) and $SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8), record file blob $(git hash-object --no-filters $DATA/${TAG2}.jsonl | cut -c1-8) with $N0 records"
# the seeds must come back as their records say (leg 3's own acceptance; the controls refuse planted numbers)
cd $OUT
"$PY" -I kc71_syscheck.py --selftest > leg4_syscheck_selftest.txt 2>&1 || { log "leg4 STOP: kc71_syscheck.py --selftest did not exit 0"; exit 1; }
for d in $DB $DA; do
  "$PY" -I kc71_syscheck.py $DATA/${TAG2}.jsonl $DATA/$(printf "sol_${TAG2}_D%.6f.npy" $d) $d $WTM > leg4_syscheck_D$d.txt 2>&1 || { log "leg4 STOP: kc71_syscheck.py does not accept the D $d seed"; exit 1; }
  grep -E '^(ACCEPTED|NOT ACCEPTED|controls|D )' leg4_syscheck_D$d.txt >> $SUM
done
for m in F steps; do "$PY" -I kc71_syscheck.py $DATA/${TAG2}.jsonl $DATA/$SB $DB $WTM --mutate=$m > leg4_syscheck_D${DB}_mutate_$m.txt 2>&1; [ $? = 1 ] || { log "leg4 STOP: the seed control --mutate=$m did not exit 1"; exit 1; }; done
log "leg4 seeds accepted by kc71_syscheck.py (D $DA, D $DB; selftest 0; --mutate=F and --mutate=steps exit 1)"
CMD="$PY -u ell_leap.py $TAG2 1 71 data/$SA $DA data/$SB $DB 21 $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
copier() {
  while [ ! -e $OUT/leap4.finished ]; do
    for f in $DATA/sol_${TAG2}_D*.npy $DATA/sol_${TAG2}_last.npy $DATA/sol_${TAG2}_prev.npy $DATA/${TAG2}.jsonl; do
      [ -e "$f" ] || continue
      b=$(basename $f)
      if [ $(( $(date +%s) - $(date -r "$f" +%s) )) -ge 30 ] && ! cmp -s "$f" "$OUT/states/$b"; then cp "$f" "$OUT/states/$b"; fi
    done
    sleep 120
  done
  for f in $DATA/sol_${TAG2}_D*.npy $DATA/sol_${TAG2}_last.npy $DATA/sol_${TAG2}_prev.npy $DATA/${TAG2}.jsonl; do [ -e "$f" ] && cp "$f" "$OUT/states/$(basename $f)"; done
}
copier &
cp_pid=$!
cd $WT/solver/matter || exit 1
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap4.log
s0=$(date +%s)
crun leap4 0 43200 ell_leap.py $CMD >> $OUT/leap4.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap4.log
echo "leap4: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap4.log | tail -n 1)" >> $SUM; log "leg4 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap4.finished
wait $cp_pid
echo "kcl leap4 done" >> $SUM
touch $OUT/all4.done
exit 0
