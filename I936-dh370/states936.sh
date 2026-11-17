#!/bin/bash
# #936: the octo-double residual and Newton step on one stored state of #841's chain (D 254.9015), with #841's own build
# (worktree choptuik-large-d-841 at 0cfff3c4 and ~/Source/venv-i800: multidouble 4.2.1, multishoot 1.2.2) and with the
# 4.8.2 build (worktree choptuik-large-d-935 and its .venv), compared bit for bit with #934's state_dump.py (state_dump936.py
# swaps its STATES). Each build runs its own worktree's hp Python. 5 threads in the dump, nice 10. Exits 0 only when the
# residual and the step are the same bits and the step control (tangents reversed) differs.
OLD=/home/nathan/Source/choptuik-large-d-841
NEW=/home/nathan/Source/choptuik-large-d-935
OLDPY=/home/nathan/Source/venv-i800/bin/python
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I936-dh370
L=$OUT/states.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
lock() { grep -A1 "name = \"$2\"" "$1/hp/Cargo.lock" | grep version | tr -d ' \n'; }
echo "# $(date -u '+%F %T') UTC, old $(git -C "$OLD" rev-parse --short HEAD) $(lock $OLD multidouble) $(lock $OLD multishoot), new $(git -C "$NEW" rev-parse --short HEAD) $(lock $NEW multidouble) $(lock $NEW multishoot), load $(cut -d' ' -f1-3 /proc/loadavg)" > "$L"
cd "$OUT" || exit 1
step() { echo "== $1 $(date -u '+%H:%M:%S')" >> "$L"; shift; nice -n 10 "$@" >> "$L" 2>&1; }
step "dump, #841's build (4.2.1)" "$OLDPY" -u state_dump936.py "$OLD/hp" "$RAW" "$OUT/states_old" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, 4.8.2" "$NEW/.venv/bin/python" -u state_dump936.py "$NEW/hp" "$RAW" "$OUT/states_new" || { echo "exit 1" >> "$L"; exit 1; }
step "dump, 4.8.2, control" "$NEW/.venv/bin/python" -u state_dump936.py "$NEW/hp" "$RAW" "$OUT/states_ctl" --control || { echo "exit 1" >> "$L"; exit 1; }
step "compare" "$NEW/.venv/bin/python" -u state_dump936.py --compare "$OUT/states_old" "$OUT/states_new" "$OUT/states_ctl"
CMP=$?
echo "# $(date -u '+%F %T') UTC, compare exit $CMP, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$L"
echo "exit $CMP" >> "$L"
exit $CMP
