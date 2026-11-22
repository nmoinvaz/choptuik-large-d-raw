#!/bin/bash
# #1025 kc71_leap on win2, SECOND LEG (the coordinator's hc of 2026-11-22 ~06:40 UTC): when the first leg's 12 h cap ends it (run_leap.sh, 03:50:08 UTC start), start a new ell_leap.py run from the first leg's last two
# saved states whose records reproduce (leg2_pick.py), with the same flags (winb's: --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold), h as the first leg left it, to D_end 20, 4 BLAS threads, BelowNormal (the caller sets it),
# a new cap of 43200 s (12 h) by the exact root pid. usage: run_leap2.sh DA DB H   (DRY=1: the pin checks and the command only). The second leg writes data/l1kc71Lw1025b.jsonl and sol_l1kc71Lw1025b_D*.npy, copied into
# states/ by a copier loop. Driver lines go to exits_kcl2.txt and summary_kcl2.txt; the leg's output is leap2.log.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
EX=$OUT/exits_kcl2.txt
SUM=$OUT/summary_kcl2.txt
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WOUT=D:/choptuik-i935-raw/I1025-win2/kc71_leap
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
DATA=$WT/solver/matter/data
TAG1=l1kc71Lw1025
TAG2=l1kc71Lw1025b
DA=$1; DB=$2; H=$3
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "leg2 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
[ -n "$DA" ] && [ -n "$DB" ] && [ -n "$H" ] || { echo "usage: run_leap2.sh DA DB H"; exit 2; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "leg2 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "leg2 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
SA=$(printf "sol_${TAG1}_D%.6f.npy" $DA); SB=$(printf "sol_${TAG1}_D%.6f.npy" $DB)
for f in $SA $SB; do [ -s $DATA/$f ] || { log "leg2 refuse: no $DATA/$f"; bad=1; }; cmp -s $DATA/$f $OUT/states/$f || { log "leg2 refuse: $f differs from or is missing in states/"; bad=1; }; done
for f in $DATA/${TAG2}.jsonl $OUT/leap2.finished $OUT/leap2.log; do [ -e $f ] && { log "leg2 refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
CMD="$PY -u ell_leap.py $TAG2 1 71 data/$SA $DA data/$SB $DB 20 $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
log "leg2 pins checked: ell_leap.py 1eb873e4, worktree 48c36355 with solver code = 505d8399, seeds $SA blob $(git hash-object --no-filters $DATA/$SA | cut -c1-8) and $SB blob $(git hash-object --no-filters $DATA/$SB | cut -c1-8)"
if [ "$DRY" = 1 ]; then echo "DRY: cd $WTM && $CMD"; exit 0; fi
copier() {
  while [ ! -e $OUT/leap2.finished ]; do
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
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD (cwd $WTM, 4 threads)"; } > $OUT/leap2.log
s0=$(date +%s)
crun leap2 0 43200 ell_leap.py $CMD >> $OUT/leap2.log 2>&1
rc=$RC; w=$(( $(date +%s) - s0 ))
echo "exit $rc" >> $OUT/leap2.log
echo "leap2: exit $rc, $w s$([ "$CAPPED" = 1 ] && echo ", capped at 43200 s"): $(grep -E '^(reached|stop at)' $OUT/leap2.log | tail -n 1)" >> $SUM; log "leg2 exit $rc wall $w s capped $CAPPED"
touch $OUT/leap2.finished
wait $cp_pid
echo "kcl leap2 done" >> $SUM
touch $OUT/all2.done
exit 0
