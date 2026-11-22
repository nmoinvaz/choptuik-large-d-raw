#!/bin/bash
# #1025 continuation of the k_c 63 leap after the 12 h cap of run1025leap.sh (coordinator hc 2026-11-22 ~06:35 UTC): from the last two saved
# states that reproduce their records (check_states.py), the same flags as winb's (--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold) and the h the
# run left, to D 20, 6 threads, nice 10, new 12 h cap. Mirrors the worktree's data/ files of the tag into raw every 5 minutes.
# usage: bash run1025cont.sh SOLA DA SOLB DB H      (SOLA, SOLB: state files; the command is posted on #1025 before the start)
{
SOLA=$1; DA=$2; SOLB=$3; DB=$4; H=$5
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I1025-dh370/kc63_leap_cont
WT=/home/nathan/Source/choptuik-large-d-1025
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=l1kc63dh370b
SUM=$OUT/summary_leap.txt
mkdir -p $OUT
stamp() { date -u '+%F %T'; }
log() { echo "1025 leap cont $* $(stamp) UTC" >> $OUT/exits_leap.txt; }
echo "# k_c 63 leap continuation on dh370: started $(stamp) UTC, load $(cut -d' ' -f1-3 /proc/loadavg)" > $SUM
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { log "worktree not at 48c36355: stop"; exit 1; }
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/' | head -1)" ] || { log "worktree solver/ has changes: stop"; exit 1; }
[ "$(git -C $WT hash-object $WT/solver/matter/ell_leap.py | cut -c1-8)" = 1eb873e4 ] || { log "ell_leap.py is not xfkappa's pin 1eb873e4: stop"; exit 1; }
[ -f $SOLA ] && [ -f $SOLB ] || { log "a seed state is missing: stop"; exit 1; }
cd $WT/solver/matter || exit 9
CMD="nice -n 10 timeout 43200 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 $PY -u ell_leap.py $TAG 1 63 $SOLA $DA $SOLB $DB 20 $H --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold"
echo "== $(stamp) $CMD" > $OUT/leap.log
echo "cmd: $CMD" >> $SUM
log "starting the continuation (6 threads, nice 10, cap 43200 s), load $(cut -d' ' -f1-3 /proc/loadavg)"
t0=$(date +%s)
$CMD >> $OUT/leap.log 2>&1 &
pid=$!
log "leap pid $pid"
while kill -0 $pid 2>/dev/null; do
  sleep 300
  cp -u data/*${TAG}* $OUT/ 2>/dev/null
done
wait $pid; rc=$?
cp -u data/*${TAG}* $OUT/ 2>/dev/null
echo "leap exit $rc, wall $(( $(date +%s) - t0 )) s; last lines: $(tail -2 $OUT/leap.log | cut -c1-200 | tr '\n' '|')" >> $SUM
log "leap exit $rc wall $(( $(date +%s) - t0 )) s"
exit 0
}
