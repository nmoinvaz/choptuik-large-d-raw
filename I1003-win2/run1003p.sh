#!/usr/bin/env bash
# #1003 J 1500 half, step 1 (coordinator's hc of 2026-11-19 ~06:30 UTC): the pilot, python amp_flint_par.py 1.0 25 1500 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840 --out RAW/I1003-win2/pilot_K25_J1500.json,
# from solver/inner_amp of D:/choptuik-i962 at origin/main, venv-i962, BelowNormal (set by the launching PowerShell on this script's bash, which its children inherit), 1 h cap.
# Glue: it chains that one command, logs the start and exit in exits_1003.txt, and at the cap kills the python tree by the exact Windows pid of the python it started (taskkill /T,
# the spawn workers die with it). RAW is the raw-data worktree D:/choptuik-large-d-raw-743. usage: [CAP=3600] bash run1003p.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
X=/d/choptuik-large-d-raw-743/I1003-win2
cd /d/choptuik-i962/solver/inner_amp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "1003p $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1003.txt; }
cap=${CAP:-3600}
log "pilot start: K 25 J 1500 prec 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840, cap ${cap} s, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u amp_flint_par.py 1.0 25 1500 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840 --out D:/choptuik-large-d-raw-743/I1003-win2/pilot_K25_J1500.json >> $X/pilot_K25_J1500.log 2>&1 &
pid=$!
wpid=$(cat /proc/$pid/winpid)
echo "$wpid" > $X/pilot.winpid
capped=0
while kill -0 $pid 2>/dev/null; do
  if [ $(( $(date +%s) - t )) -ge $cap ]; then
    log "pilot cap of ${cap} s reached, killing the tree of pid $wpid"
    MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1
    capped=1
    break
  fi
  sleep 10
done
wait $pid
rc=$?
log "pilot exit $rc wall $(( $(date +%s) - t ))s capped $capped"
