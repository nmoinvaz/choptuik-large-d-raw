#!/bin/bash
# #936 on dh170: the octo-double residual_o and newton_o on the stored order-150 state D 230 (#903's chain_k150), with
# the chain's own build (main checkout 7f88c5bb and its .venv, multidouble 4.7.0) and the 4.8.2 build (#935's worktree
# and venv), compared bit for bit (state_dump.py), then the control (new build, tangents reversed, mutate=25) against
# the old. Old and new run at the same time, 4 threads each (8 threads, nice 10); the control runs alone at 8.
# Exits 0 only when the residual and step bits are equal and the control differs.
OLDWT=$HOME/Source/choptuik-large-d
NEWWT=$HOME/Source/choptuik-large-d-935
RAW=$HOME/Source/choptuik-large-d-raw
ROOT=$HOME/Source/choptuik-large-d-raw-push   # a worktree of origin/main: the committed state files
OUT=$RAW/I936-dh170
L=$OUT/states.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$OUT" || exit 1
echo "# $(date -u '+%F %T') UTC, old $(git -C "$OLDWT" rev-parse --short HEAD), new $(git -C "$NEWWT" rev-parse --short HEAD), raw $(git -C "$ROOT" rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L"
echo "== dump, old and new at the same time, 4 threads each $(date -u '+%H:%M:%S')" >> "$L"
STATE_DUMP_THREADS=4 nice -n 10 "$OLDWT/.venv/bin/python" -u state_dump.py "$OLDWT/hp" "$ROOT" "$OUT/states_old" > dump_old.log 2>&1 &
PO=$!
STATE_DUMP_THREADS=4 nice -n 10 "$NEWWT/.venv/bin/python" -u state_dump.py "$NEWWT/hp" "$ROOT" "$OUT/states_new" > dump_new.log 2>&1 &
PN=$!
wait $PO; RO=$?; echo "old exit $RO $(date -u '+%H:%M:%S')" >> "$L"
wait $PN; RN=$?; echo "new exit $RN $(date -u '+%H:%M:%S')" >> "$L"
[ $RO = 0 ] && [ $RN = 0 ] || { echo "exit 1 (a dump failed)" >> "$L"; exit 1; }
echo "== dump, new, control, 8 threads $(date -u '+%H:%M:%S')" >> "$L"
STATE_DUMP_THREADS=8 nice -n 10 "$NEWWT/.venv/bin/python" -u state_dump.py "$NEWWT/hp" "$ROOT" "$OUT/states_ctl" --control > dump_ctl.log 2>&1
RC=$?; echo "control exit $RC $(date -u '+%H:%M:%S')" >> "$L"
[ $RC = 0 ] || { echo "exit 1 (the control dump failed)" >> "$L"; exit 1; }
echo "== compare $(date -u '+%H:%M:%S')" >> "$L"
"$NEWWT/.venv/bin/python" -u state_dump.py --compare "$OUT/states_old" "$OUT/states_new" "$OUT/states_ctl" >> "$L" 2>&1
CMP=$?
echo "# $(date -u '+%F %T') UTC, compare exit $CMP" >> "$L"
echo "exit $CMP" >> "$L"
exit $CMP
