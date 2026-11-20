#!/bin/bash
# #1014 on dh170, step C (coordinator approved C then B, hc 2026-11-20 about 05:31 UTC): the series from MY lifted M 320 state on the planner's converged plan (1820 steps, make_plan1820_1014.py): its base smallest pivot answers whether the 1e-11 pivot is T82-win's coarse-plan states (near 5e-5 here) or the step count, and its series is the M 320 one on a converged plan for B's rule.
# target stage was stopped by the 30-minute rule. The command is stage2_1014.sh's with the M 384 state and the M 384 outputs.
# Rules: the target stage gets 30 minutes after the series file is saved; the whole run is capped at 10 h of wall time
# (both by exact pid, logged to exits_1014.txt).
HERE=/home/nathan/Source/choptuik-large-d-raw/I1014-dh170
RAWL=/home/nathan/Source/choptuik-large-d-raw
WT=/home/nathan/Source/choptuik-large-d-1014
PY=/home/nathan/Source/choptuik-large-d-935/.venv/bin/python
S320P=$HERE/states/lowD1014_D3.0475_M320_plan1820.npz
SER=$HERE/series_D3.0475_M320p_N12.npz
L=$HERE/exits_1014.txt
CAP=36000
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1
log() { echo "1014 $* $(date -u '+%F %T') UTC" >> $L; }
cd $WT/hp || exit 9
t=$(date +%s); log "stage 5 = step C (my M 320 on the 1820-step planner plan, N 12, then the target stage; cap ${CAP} s) start, from states/lowD1014_D3.0475_M320_plan1820.npz"
nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" $PY -u anm_lowd.py $RAWL $HERE/series320p --state $S320P --N 12 --checks "" --target 3.0474 --threads 6 --save_series $SER > $HERE/stage5.log 2>&1 &
pid=$!
saved=""
while kill -0 $pid 2>/dev/null; do
  if [ -z "$saved" ] && [ -f $SER ]; then saved=$(date +%s); log "M 320 (1820-step plan) series saved"; fi
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
wait $pid; log "stage 5 exit $? wall $(( $(date +%s) - t )) s"
