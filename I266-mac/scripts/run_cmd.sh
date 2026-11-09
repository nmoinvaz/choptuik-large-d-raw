#!/bin/bash
# Any other #266 step (hp/gamma_m48_gap.py analyze | qd), from the worktree root, its log in logs/TAG.log:
#   run_cmd.sh TAG analyze OUT.jsonl A.npz B.npz [options]
#   run_cmd.sh TAG qd OUTDIR STATE.npz [options]
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
TAG=$1
shift
caffeinate -i nice -n 10 $PY -u hp/gamma_m48_gap.py "$@" > $RAW/logs/$TAG.log 2>&1
echo "$TAG exit $?" >> $RAW/logs/exits.txt
