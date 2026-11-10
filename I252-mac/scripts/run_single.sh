#!/bin/bash
# #252: lighter load (Nathan via the coordinator, 22:30 UTC). The D 55 slot stops after its running circle (the first
# M 40 circle), and the D 55 M 40 circles not yet recorded run one at a time in a single process after the D 61 chain
# ends. Cached determinants are kept, so a circle stopped part-way loses nothing.
# Run: bash run_single.sh D55_BASH_PID D55_CIRCLE_PID D61_BASH_PID
PY=/Users/nathan/venv-314/bin/python
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-af41abeb756ed7275/hp
F=/Users/nathan/Source/choptuik-large-d-raw/I252-mac
ex() { echo "$1 exit $2 at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt; }
J=$F/D55/circles/modecount_circles.jsonl
n0=$(wc -l < $J)
until [ $(wc -l < $J) -gt $n0 ] || ! kill -0 $2 2>/dev/null; do sleep 15; done
kill $1 $2 2>/dev/null
echo "D55 slot stopped after its circle (load reduction) at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $F/exits.txt
while kill -0 $3 2>/dev/null; do sleep 30; done
ALL="0.477308,1.453280,0.2 0.24271,0.92524,0.2 0.09923,4.48036,0.2 0.34863,2.61221,0.2 0.36031,2.16089,0.2 0.59532,5.03932,0.2"
LEFT=$($PY -c "
import json, sys
done = {(round(r['center'][0], 6), round(r['center'][1], 6)) for r in map(json.loads, open('$J'))}
print(' '.join(s for s in '$ALL'.split() if (round(float(s.split(',')[0]), 6), round(float(s.split(',')[1]), 6)) not in done))")
echo "single process: D 55 M 40 circles left: $LEFT" >> $F/exits.txt
$PY $HP/modecount_circle.py $F/states/modecount_state_D55.0351_M64_kf23.npz $LEFT --kf=23 --n0=20 --fmax=1e-15 \
    --tag=D55.0351_M64_kf23 --data=$F/D55/circles > $F/D55/v2_circles_M40_single.log 2>&1
ex v2_circles_D55_M40_single $?
