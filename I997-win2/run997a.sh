#!/usr/bin/env bash
# #997 step (a) first run (coordinator's hc of 2026-11-19 ~01:30 UTC and #997 comment 6996854170): anm_lowd.py at D 3.15, M 160, --N 20, target 3.14, 9 threads, from hp/ in D:/choptuik-i962 fast-forwarded to
# origin/main 459180e6 (done by hand after ks_chain2 stopped). Glue: it chains the one command and logs its start and exit in exits_997.txt. RAW is the raw-data worktree D:/choptuik-large-d-raw-743
# (it has I927-mac/inputs/, the live clone D:/choptuik-large-d-raw has not). usage: bash run997a.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
RAW=D:/choptuik-large-d-raw-743
X=/d/choptuik-large-d-raw-743/I997-win2
cd /d/choptuik-i962/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "997a $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_997.txt; }
mkdir -p $X/series
log "anm_lowd.py D 3.15 M 160 N 20 target 3.14, 9 threads, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u anm_lowd.py $RAW $RAW/I997-win2/series --state I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz --N 20 --checks "" --target 3.14 --threads 9 \
    --save_series $RAW/I997-win2/series/series_D3.15_M160_N20.npz >> $X/series/run.log 2>&1
log "anm_lowd.py exit $? wall $(( $(date +%s) - t ))s"
