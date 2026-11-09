#!/bin/bash
# #252: the D 61 M 64 kf 23 count (criterion 3 of ../README.md), fixed left column, #242's rule. Runs only if the D 61
# determinant check passed. Run: caffeinate -i nice -n 10 bash run_count_D61.sh
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
$PY -c "import json,sys; sys.exit(0 if json.load(open('$F/checks/det_check_D61_M64.json'))['passed'] else 1)" \
    || { ex skip_count_D61_det_check_not_passed 1; exit 1; }
$PY $HP/modecount_wind.py $F/states/modecount_state_D61.0264_M64_kf23.npz --kf=23 --h0=0.6 --lam=2.043532530673195 \
    --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=D61.0264_M64_kf23 --data=$F/D61/data > $F/D61/count.log 2>&1
ex count_D61 $?
