#!/usr/bin/env bash
# #562: hh_planted resumed from its checkpoint (hh_planted_setup.npz, hh_planted_ckpt.npz) with the rule-2 code (wip/i562-subagent 1161f49, D:/choptuik-i562-r2),
# --h_max 0.0125, 8 threads, 6 h cap, as the coordinator's command of 2026-11-12 11:34 UTC. The output prefix stays hh_planted and the log is appended to.
R=/d/choptuik-large-d-raw/I562-win2
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
export PYTHONFAULTHANDLER=1
echo "hh_planted_resume start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_main.txt
cd /d/choptuik-i562-r2/hp || exit 9
"$PY" -u held_homotopy.py /d/choptuik-large-d-raw I562-win2/renode_0975_D242.3642.npz /d/choptuik-large-d-raw/I562-win2/hh_planted --mode planted --eps 2.5e-17 --resume 1 --h_max 0.0125 --rule 2 --threads 8 --hours 6 >> $R/hh_planted.log 2>&1
echo "hh_planted_resume exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_main.txt
