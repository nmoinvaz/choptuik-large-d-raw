#!/usr/bin/env bash
# #997 step (a), two more runs one after the other (coordinator's hc of 2026-11-19 ~02:05 UTC): (1) the third resolution at D 3.15, the first run's command with --state ..._D3.1500_M128.npz, OUT series_M128;
# (2) next to the sonic point, --state T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M256.npz --N 20 --target 3.0465, OUT series_D30475. Both with --checks "" as the first run, 9 threads, venv-i962,
# hp/ of D:/choptuik-i962 at origin/main 459180e6. Glue: it chains the two commands and logs each start and exit in exits_997.txt. RAW is the raw-data worktree D:/choptuik-large-d-raw-743.
# usage: bash run997c.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
RAW=D:/choptuik-large-d-raw-743
X=/d/choptuik-large-d-raw-743/I997-win2
cd /d/choptuik-i962/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "997c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_997.txt; }
mkdir -p $X/series_M128 $X/series_D30475
log "run 1: anm_lowd.py D 3.15 M 128 N 20 target 3.14, 9 threads, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u anm_lowd.py $RAW $RAW/I997-win2/series_M128 --state I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --N 20 --checks "" --target 3.14 --threads 9 \
    --save_series $RAW/I997-win2/series_M128/series_D3.15_M128_N20.npz >> $X/series_M128/run.log 2>&1
log "run 1 (M 128) anm_lowd.py exit $? wall $(( $(date +%s) - t ))s"
log "run 2: anm_lowd.py D 3.0475 M 256 N 20 target 3.0465, 9 threads, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u anm_lowd.py $RAW $RAW/I997-win2/series_D30475 --state T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M256.npz --N 20 --checks "" --target 3.0465 --threads 9 \
    --save_series $RAW/I997-win2/series_D30475/series_D3.0475_M256_N20.npz >> $X/series_D30475/run.log 2>&1
log "run 2 (D 3.0475, M 256) anm_lowd.py exit $? wall $(( $(date +%s) - t ))s"
