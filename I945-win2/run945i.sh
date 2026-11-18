#!/usr/bin/env bash
# #945 eighth launch (coordinator's hc and #945 comment 6984938523, 2026-11-18 ~16:38 UTC): the last resume (run945g.sh) unchanged plus --prefer_start predictor, with the worktree
# D:/choptuik-i932 fast-forwarded to origin/main 0fc2fab0 (hp/lowD_highM.py gains --prefer_start; Python only, the venv's hpkernel is kept). Glue: it restores the progress file
# to run945g's start state (leg.jsonl.progress.after_945f.json with targets [3.04315] only; the file as it was after the M 384 failure is leg.jsonl.progress.after_945i.json),
# then runs the command of run945g.sh with the one added flag and logs the exit in exits_945.txt. The file's stop rules are watched by w945i.sh. venv-i600, 10 threads.
# usage: bash run945i.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2/leg
X=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945i $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt; }
[ -f $R/leg.jsonl.progress.after_945i.json ] || cp $R/leg.jsonl.progress.json $R/leg.jsonl.progress.after_945i.json
cp $R/leg.jsonl.progress.after_945f.json $R/leg.jsonl.progress.json
"$PY" -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315]); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
log "resume of step 2: progress file restored from leg.jsonl.progress.after_945f.json with targets [3.04315] only (the state after the M 384 failure is leg.jsonl.progress.after_945i.json)"
log "resume of step 2 (--accept 1e-20 --prefer_start predictor) start, main $(git rev-parse --short=8 HEAD)"
t=$(date +%s)
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop --accept 1e-20 --prefer_start predictor >> $R/leg.log 2>&1
log "resume of step 2 exit $? wall $(( $(date +%s) - t ))s"
