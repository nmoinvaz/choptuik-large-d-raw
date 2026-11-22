#!/bin/bash
# #1025 kc71_leap, RESTART 1 of the leap (the coordinator's ruling (b) of 2026-11-22 ~09:00 UTC on the D 18.75 fold watch, a near-null singular value crossing the 1e-12 cutoff): from the D 18.6875 and D 18.75 states at
# h 0.0625 with the same flags (winb's: --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold), same tag l1kc71Lw1025 (records and states continue in the same files; D 19, 19.5 and 20 stay on the grid 18.5 + 0.0625 k). Started outside the
# terminal by cim_start.ps1. No cap here: leg1_guard2.sh owns the cap (15:50:08 UTC, exact pid) and the copier. Writes the root pid (the python launcher stub, whose command line holds ell_leap.py) to leap_root_r1.pid.
# usage: leap_r1.sh [DRY=1: pins and seed checks only]
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
OUT=/d/choptuik-i935-raw/I1025-win2/kc71_leap
. $OUT/lib_kcl.sh
PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe
WT=/d/choptuik-i1025k71
WTM=D:/choptuik-i1025k71/solver/matter
DATA=$WT/solver/matter/data
TAG=l1kc71Lw1025
SA=sol_${TAG}_D18.687500.npy; SB=sol_${TAG}_D18.750000.npy
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 PYTHONFAULTHANDLER=1
bad=0
chk() { local h; h=$(git hash-object --no-filters "$1"); case "$h" in $2*) ;; *) log "restart1 refuse: $3 is blob $h, not $2"; bad=1;; esac; }
chk $WT/solver/matter/ell_leap.py 1eb873e4 "ell_leap.py"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 48c36355 ] || { log "restart1 refuse: the worktree is not at 48c36355"; bad=1; }
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py solver/matter/ddnp.py || { log "restart1 refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $SA $SB; do [ -s $DATA/$f ] || { log "restart1 refuse: no $f"; bad=1; }; cmp -s $DATA/$f $OUT/states/$f || { log "restart1 refuse: $f differs from states/"; bad=1; }; done
[ -e $OUT/leap_root_r1.pid ] && { log "restart1 refuse: leap_root_r1.pid exists"; bad=1; }
[ $bad = 0 ] || exit 2
for pr in "$SA 18.6875" "$SB 18.75"; do set -- $pr
  "$PY" -I $OUT/kc71_syscheck.py $WTM/data/${TAG}.jsonl $WTM/data/$1 $2 $WTM > $OUT/syscheck_r1_$2.txt 2>&1 || { log "restart1 refuse: the state of D $2 is not accepted by kc71_syscheck.py"; exit 2; }
done
log "restart1 pins checked: ell_leap.py 1eb873e4, worktree 48c36355, solver code 505d8399, seeds $SA $(git hash-object --no-filters $DATA/$SA | cut -c1-8) and $SB $(git hash-object --no-filters $DATA/$SB | cut -c1-8) accepted by kc71_syscheck.py"
CMD="$PY -u ell_leap.py $TAG 1 71 data/$SA 18.6875 data/$SB 18.75 20 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
[ "$DRY" = 1 ] && { echo "DRY: cd $WTM && $CMD"; exit 0; }
cd $WT/solver/matter || exit 1
echo "# $(date -u '+%F %T') UTC RESTART 1 cmd: $CMD (cwd $WTM, 4 threads)" >> $OUT/leap.log
$CMD >> $OUT/leap.log 2>&1 &
pid=$!; wpid=$(cat /proc/$pid/winpid)
echo $wpid > $OUT/leap_root_r1.pid
log "restart1 leap root pid $wpid (guard owns the cap)"
wait $pid; rc=$?
log "restart1 leap exit $rc"
echo "leap restart 1: exit $rc" >> $SUM
echo $rc > $OUT/leap_r1.exit
exit 0
