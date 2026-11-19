#!/usr/bin/env bash
# #1003 J 1500 half, step 2 (coordinator's hc of 2026-11-19 ~06:30 UTC, changed at ~06:33 UTC to a 48 h cap and at ~07:30 UTC to --procs 3 and a 72 h cap, because each worker's memory grows like k^1.7): python amp_flint_par.py 1.0 49 1500 1280 --procs 3 --fit phys --mf 6:12 --phys-prec 3840
# --out RAW/I1003-win2/sigF_w1.0000_K49_J1500_p1280.json, from solver/inner_amp of the worktree D:/choptuik-i1003 at origin/main 99363fe8 (it writes OUT.partial.json after each order; D:/choptuik-i962 stays untouched under the running pilot), venv-i962, BelowNormal (set by the launching PowerShell), 72 h cap (CAP, in seconds, 259200). Its memory is logged, alert only, by mem1003.sh (started by hand).
# Started on the coordinator's word of ~07:44 UTC while the pilot was still finishing (the pilot's cmp1003.py check is read after it ends). Glue: it chains that one command, logs start and exit in exits_1003.txt, and at the cap kills the python tree by the exact Windows pid of
# the python it started (taskkill /T). RAW is the raw-data worktree D:/choptuik-large-d-raw-743. usage: [CAP=259200] bash run1003k49.sh
PY=/c/Users/nathan/Source/venv-i962/Scripts/python.exe
X=/d/choptuik-large-d-raw-743/I1003-win2
cd /d/choptuik-i1003/solver/inner_amp || exit 9
export PYTHONFAULTHANDLER=1
log() { echo "1003k49 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1003.txt; }
cap=${CAP:-259200}
log "K 49 J 1500 start: prec 1280 --procs 3 --fit phys --mf 6:12 --phys-prec 3840, cap ${cap} s, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u amp_flint_par.py 1.0 49 1500 1280 --procs 3 --fit phys --mf 6:12 --phys-prec 3840 --out D:/choptuik-large-d-raw-743/I1003-win2/sigF_w1.0000_K49_J1500_p1280.json >> $X/sigF_w1.0000_K49_J1500_p1280.log 2>&1 &
pid=$!
wpid=$(cat /proc/$pid/winpid)
echo "$wpid" > $X/k49.winpid
capped=0
while kill -0 $pid 2>/dev/null; do
  if [ $(( $(date +%s) - t )) -ge $cap ]; then
    log "cap of ${cap} s reached, killing the tree of pid $wpid"
    MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $wpid > /dev/null 2>&1
    capped=1
    break
  fi
  sleep 15
done
wait $pid
rc=$?
log "K 49 J 1500 exit $rc wall $(( $(date +%s) - t ))s capped $capped"
