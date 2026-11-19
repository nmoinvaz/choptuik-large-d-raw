#!/bin/bash
# #1014 on dh170 (coordinator's hc 2026-11-19): stage 1 lift the D 3.0475 M 256 state to M 320 (lowD_dd.py), stage 2 the series at N 12 (anm_lowd.py --save_series), then the 30-minute rule on
# the target stage. Worktree ~/Source/choptuik-large-d-1014, the -935 venv's Python and hpkernel (read only, nothing built), 6 threads, nice 10, raw folder = this folder of the live raw clone.
#   run1014.sh pilot    only the start residual of the lifted state (lowD_dd.py --start_residual_only), a minute or two
#   run1014.sh run      stages 1 and 2 and the watch
HERE=/home/nathan/Source/choptuik-large-d-raw/I1014-dh170
RAWL=/home/nathan/Source/choptuik-large-d-raw
WT=/home/nathan/Source/choptuik-large-d-1014
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
S256=/home/nathan/scratch1014/raw/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M256.npz
NODES=0.000157,0.000313,0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.975
S320=$HERE/states/lowD1014_D3.0475_M320.npz
SER=$HERE/series_D3.0475_M320_N12.npz
L=$HERE/exits_1014.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log() { echo "1014 $* $(date -u '+%F %T') UTC" >> $L; }
cd $WT/hp || exit 9
case $1 in
  pilot)
    log "pilot start"
    nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u lowD_dd.py $HERE/m320_pilot.jsonl --start $S256 --Ms 320 --nodes $NODES --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 6 --tag lowD1014 --start_residual_only > $HERE/pilot.log 2>&1
    log "pilot exit $?" ;;
  run)
    t=$(date +%s); log "stage 1 (lift to M 320) start"
    nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u lowD_dd.py $HERE/m320.jsonl --start $S256 --Ms 320 --nodes $NODES --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 6 --tag lowD1014 > $HERE/stage1.log 2>&1
    rc=$?; log "stage 1 exit $rc wall $(( $(date +%s) - t )) s"
    f=$WT/hp/data/lowD_states/lowD1014_D3.0475_M320.npz
    [ $rc -eq 0 ] && [ -f $f ] || { log "no converged M 320 state ($f), stopping"; exit 3; }
    cp -p $f $S320; cmp $f $S320 && log "state copied to states/"
    t=$(date +%s); log "stage 2 (series N 12, then the target stage) start"
    nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u anm_lowd.py $RAWL $HERE/series --state $S320 --N 12 --checks "" --target 3.0474 --threads 6 --save_series $SER > $HERE/stage2.log 2>&1 &
    pid=$!
    # the 30-minute rule: from the moment the series file is saved, the target stage gets 30 minutes
    saved=""
    while kill -0 $pid 2>/dev/null; do
      if [ -z "$saved" ] && [ -f $SER ]; then saved=$(date +%s); log "series saved"; fi
      if [ -n "$saved" ] && [ $(( $(date +%s) - saved )) -gt 1800 ]; then
        py=$(ps -o pid= --ppid $pid | head -1 | tr -d ' '); [ -z "$py" ] && py=$pid
        log "target stage past 30 min after the series was saved: stopping pid $py (and $pid) by exact pid"; kill -TERM $py $pid 2>/dev/null; break
      fi
      sleep 10
    done
    wait $pid; log "stage 2 exit $? wall $(( $(date +%s) - t )) s" ;;
  *) echo "usage: run1014.sh pilot|run"; exit 2 ;;
esac
