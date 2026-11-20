#!/bin/bash
# #1014 on dh170: the series at M 320 from T82-win's own stored M 320 state (coordinator's hc 2026-11-20 ~01:05 UTC), after stage 3 (M 384) ended.
# target stage was stopped by the 30-minute rule. The command is stage2_1014.sh's with the M 384 state and the M 384 outputs.
# Rules: the target stage gets 30 minutes after the series file is saved; the whole run is capped at 10 h of wall time
# (both by exact pid, logged to exits_1014.txt).
HERE=/home/nathan/Source/choptuik-large-d-raw/I1014-dh170
RAWL=/home/nathan/Source/choptuik-large-d-raw
WT=/home/nathan/Source/choptuik-large-d-1014
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
S320T=$RAWL/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz
SER=$HERE/series_D3.0475_M320t82_N12.npz
L=$HERE/exits_1014.txt
CAP=36000
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log() { echo "1014 $* $(date -u '+%F %T') UTC" >> $L; }
cd $WT/hp || exit 9
t=$(date +%s); log "stage 4 (M 320 series from T82-win's M 320 state, N 12, then the target stage; cap ${CAP} s) start, from T82-win's stored M 320 state"
nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u anm_lowd.py $RAWL $HERE/series320t82 --state $S320T --N 12 --checks "" --target 3.0474 --threads 6 --save_series $SER > $HERE/stage4.log 2>&1 &
pid=$!
saved=""
while kill -0 $pid 2>/dev/null; do
  if [ -z "$saved" ] && [ -f $SER ]; then saved=$(date +%s); log "M 320 (T82 state) series saved"; fi
  if [ -n "$saved" ] && [ $(( $(date +%s) - saved )) -gt 1800 ]; then
    py=$(ps -o pid= --ppid $pid | head -1 | tr -d ' '); [ -z "$py" ] && py=$pid
    log "target stage past 30 min after the series was saved: stopping pid $py (and $pid) by exact pid"; kill -TERM $py $pid 2>/dev/null; break
  fi
  if [ $(( $(date +%s) - t )) -gt $CAP ]; then
    py=$(ps -o pid= --ppid $pid | head -1 | tr -d ' '); [ -z "$py" ] && py=$pid
    log "10 h cap reached: stopping pid $py (and $pid) by exact pid"; kill -TERM $py $pid 2>/dev/null; break
  fi
  sleep 10
done
wait $pid; log "stage 4 exit $? wall $(( $(date +%s) - t )) s"
