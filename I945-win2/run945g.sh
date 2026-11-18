#!/usr/bin/env bash
# #945 seventh launch (coordinator's hc, 2026-11-18 ~04:30 UTC): the resume of the rerun of #932's step 2 with --accept 1e-20, after hp/lowD_highM.py was
# checked out from main 55cd5354 (find_record takes the run's --accept) into D:/choptuik-i932 (HEAD stays 808b1fac). Glue: it sets the progress file's targets to
# [3.04315] only (the copy before the edit is leg.jsonl.progress.after_945f.json), then runs the same command as run945f.sh, and logs the exit in exits_945.txt.
# The file's stop rules are watched by w945i.sh. venv-i600, 10 threads. usage: bash run945g.sh
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I945-win2/leg
X=$RAW/I945-win2
cd /d/choptuik-i932/hp || exit 9
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "945g $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_945.txt; }
[ -f $R/leg.jsonl.progress.after_945f.json ] || cp $R/leg.jsonl.progress.json $R/leg.jsonl.progress.after_945f.json
"$PY" -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315]); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
log "resume of step 2: progress file targets set to [3.04315] only (copy before: leg.jsonl.progress.after_945f.json)"
log "resume of step 2 (--accept 1e-20) start, main $(git rev-parse --short=8 HEAD) with hp/lowD_highM.py from 55cd5354"
t=$(date +%s)
"$PY" -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop --accept 1e-20 >> $R/leg.log 2>&1
log "resume of step 2 exit $? wall $(( $(date +%s) - t ))s"
