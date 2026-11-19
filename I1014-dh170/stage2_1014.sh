#!/bin/bash
# #1014 on dh170: stage 2 only, from the call-4 checkpoint copied as the M 320 state (coordinator's hc 2026-11-19 19:4x UTC: stop call 5, the state is at the residual's
# evaluation floor, 1.42e-27). The commands and the 30-minute rule are run1014.sh's stage 2, unchanged.
HERE=/home/nathan/Source/choptuik-large-d-raw/I1014-dh170
RAWL=/home/nathan/Source/choptuik-large-d-raw
WT=/home/nathan/Source/choptuik-large-d-1014
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
S320=$HERE/states/lowD1014_D3.0475_M320.npz
SER=$HERE/series_D3.0475_M320_N12.npz
L=$HERE/exits_1014.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log() { echo "1014 $* $(date -u '+%F %T') UTC" >> $L; }
cd $WT/hp || exit 9
t=$(date +%s); log "stage 2 (series N 12, then the target stage) start, from the call-4 checkpoint"
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
wait $pid; log "stage 2 exit $? wall $(( $(date +%s) - t )) s"
