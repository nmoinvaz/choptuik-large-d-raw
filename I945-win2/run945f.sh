#!/usr/bin/env bash
# #945 sixth launch (coordinator's hc, 2026-11-17 ~19:30 UTC): #932's step 2 rerun exactly as run932b.sh with one change, --accept 1e-20, in the fresh
# folder I945-win2/leg/ (progress file from I343-win2/leg2.jsonl.progress.json.bak, as #932 did). Glue: it waits for the 10-thread delta_corr run's exit line
# (945e), does the setup and runs the leg's command, and logs the exit in exits_945.txt. The file's stop rules are watched by w945h.sh.
# Worktree D:/choptuik-i932 at main 808b1fac, venv-i600, 10 threads. usage: bash run945f.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2/leg
X=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945f $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt; }
mkdir -p $R/states
until grep -q '945e plan_floor exit' $X/exits_945.txt 2>/dev/null; do sleep 10; done
[ -f $R/leg.jsonl.progress.json ] || {
  cp $RAW/I343-win2/leg2.jsonl.progress.json.bak $R/leg.jsonl.progress.json
  "$PY" -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315], t_used=0.0, post=None, done=None, point_start=None, last_point_s=None, last_point_wall=None); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
  log "rerun of step 2 setup done, progress file copied from I343-win2/leg2.jsonl.progress.json.bak with targets [3.04315]"
}
log "rerun of step 2 (--accept 1e-20) start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop --accept 1e-20 >> $R/leg.log 2>&1
log "rerun of step 2 exit $? wall $(( $(date +%s) - t ))s"
