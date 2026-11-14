#!/usr/bin/env bash
# #775: relayout.py at M 64 from T79's M 48 states at the 16 other lowD-M48-unresolved rows, as #766 at D 7.0 and 8.2
# (T79's command: the same ten nodes, kc 60, ks 100, no freeze projector below D 35.35), then compare_775.py against each
# row's err in hp/data/delta_all.csv. Worktree C:/Users/nathan/Source/choptuik-i709 (main), venv-t151, 4 threads.
PY=/c/Users/nathan/Source/venv-t151/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754; R=$RAW/I775-win
cd /c/Users/nathan/Source/choptuik-i709/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "775 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_775.txt; }
for D in 4.2500 4.5000 4.7500 5.2500 5.5000 5.7500 6.2500 6.5000 6.7500 7.2500 7.5000 7.5593 7.7500 7.8779 8.0594 8.1375; do
  "$PY" -u relayout.py $RAW/T79-win/down_D$D.npz $R/m64_D$D.npz --M 64 --kc 60 --ks 100 > $R/m64_D$D.log 2>&1
  rc=$?
  log "D $D exit $rc (must be 0)"
  [ $rc = 0 ] || { log "a relayout failed, the run stops"; exit 1; }
done
"$PY" -I $R/compare_775.py $RAW /c/Users/nathan/Source/choptuik-i709/hp/data/delta_all.csv > $R/compare_775.txt 2>&1
log "compare exit $? (0 when every row's err covers its difference)"
log "all done"
