#!/usr/bin/env bash
# #932 step 2 (I926-mac/runner_task_M320.md, main in place of wip/sa-926, folder I932-win2, history I343-win2/leg2.jsonl.progress.json.bak):
# the setup and the leg's command with --sonic_refine 4 --sonic_stop, as given. It only runs them and logs the exit; the file's stops
# (traceback, a pass at 8 Newton calls without convergence, 30 h) are watched by a separate script.
# Worktree D:/choptuik-i932 at origin/main 65ec482f, venv-i600, 10 threads. usage: bash run932b.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I932-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "932b $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_932.txt; }
mkdir -p $R/states
[ -f $R/leg.jsonl.progress.json ] || {
  cp $RAW/I343-win2/leg2.jsonl.progress.json.bak $R/leg.jsonl.progress.json
  "$PY" -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315], t_used=0.0, post=None, done=None, point_start=None, last_point_s=None, last_point_wall=None); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
  log "step 2 setup done, progress file copied from I343-win2/leg2.jsonl.progress.json.bak with targets [3.04315]"
}
log "step 2 start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop >> $R/leg.log 2>&1
log "step 2 exit $? wall $(( $(date +%s) - t ))s"
