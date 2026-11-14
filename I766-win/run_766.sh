#!/usr/bin/env bash
# #766: relayout.py at M 64 from T79's M 48 states at D 7.0 and 8.2, as T79 did at D 4, 5, 6 and 8 (T79-win/m64_D*.log:
# the same ten nodes, kc 60, ks 100, kfreeze none below D 35.35, so no freeze projector), then |Delta(64) - Delta(48)|
# against the rows' errs in hp/data/delta_all.csv (3.0e-14 at D 7.0, dM neighbours; 9.5e-21 at D 8.2, one-sided).
# Worktree C:/Users/nathan/Source/choptuik-i709 (main), venv-t151, 4 threads.
PY=/c/Users/nathan/Source/venv-t151/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754; R=$RAW/I766-win
cd /c/Users/nathan/Source/choptuik-i709/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "766 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_766.txt; }
for D in 7.0000 8.2000; do
  log "D $D start"
  "$PY" -u relayout.py $RAW/T79-win/down_D$D.npz $R/m64_D$D.npz --M 64 --kc 60 --ks 100 > $R/m64_D$D.log 2>&1
  log "D $D exit $? (must be 0)"
done
"$PY" -I $R/compare_766.py $RAW > $R/compare_766.txt 2>&1; log "compare exit $? (0 when both lie within their errs)"
log "all done"
