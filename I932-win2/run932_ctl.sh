#!/usr/bin/env bash
# #932, the control of step 2 (I926-mac/runner_task_M320.md criterion 4): the same setup in a second fresh folder R2 (I932-win2/control)
# and the same command without --sonic_refine 4. The file says to stop it after its first Newton call: this script kills the python
# tree when the log has its first "newton 0:" line (or after 2 h). It runs before step 2 so the two never share win2's 20 threads.
# Worktree D:/choptuik-i932 at origin/main 65ec482f, venv-i600, 10 threads. usage: bash run932_ctl.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I932-win2/control
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "932c $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $RAW/I932-win2/exits_932.txt; }
mkdir -p $R/states
cp $RAW/I343-win2/leg2.jsonl.progress.json.bak $R/leg.jsonl.progress.json
"$PY" -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315], t_used=0.0, post=None, done=None, point_start=None, last_point_s=None, last_point_wall=None); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
log "control setup done, progress file copied from I343-win2/leg2.jsonl.progress.json.bak with targets [3.04315]"
log "control start (no --sonic_refine), main $(git rev-parse --short=8 HEAD)"
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_stop > $R/leg.log 2>&1 &
t0=$(date +%s)
while true; do
  grep -q 'newton 0:' $R/leg.log 2>/dev/null && { why="first Newton call ended"; break; }
  grep -q Traceback $R/leg.log 2>/dev/null && { why="TRACEBACK"; break; }
  [ $(( $(date +%s) - t0 )) -ge 7200 ] && { why="2 h cap"; break; }
  sleep 10
done
pid=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*I932-win2/control*' } | Sort-Object ProcessId | Select-Object -First 1).ProcessId")
[ -n "$pid" ] && MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $pid > /dev/null 2>&1
log "control stopped: $why (python tree of pid ${pid:-none}) after $(( $(date +%s) - t0 ))s"
